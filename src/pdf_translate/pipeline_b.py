"""Pipeline B: overlay translated text on top of original PDF."""
from __future__ import annotations

import logging
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pdfplumber
from pikepdf import Pdf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .config import AppConfig
from .ocr import ensure_searchable_pdf
from .translation import TranslationClient
from .utils import ensure_parent, clean_directory

logger = logging.getLogger(__name__)


@dataclass
class TextBlock:
    page: int
    text: str
    bbox: tuple[float, float, float, float]
    font_size: float
    font_name: str | None = None


def _sample_preview(texts: List[str], limit: int = 40, max_items: int = 3) -> str:
    sample = []
    for text in texts[:max_items]:
        collapsed = " ".join(text.split())
        if len(collapsed) > limit:
            collapsed = f"{collapsed[:limit]}…"
        sample.append(collapsed)
    return ", ".join(sample)


class PipelineB:
    def __init__(self, config: AppConfig, translator: TranslationClient, work_dir: Path | None = None) -> None:
        self.config = config
        self.translator = translator
        self.work_dir = work_dir or config.working_dir
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self._background_color = self._prepare_background_color(config.layout.background_color)

    def run(self) -> Path:
        source_pdf = self.config.input_path
        if self.config.ocr.enabled:
            source_pdf = ensure_searchable_pdf(source_pdf, self.config.ocr.lang, self.work_dir)

        blocks = self._extract_blocks(source_pdf)
        logger.info("Identified %d text blocks containing Hangul", len(blocks))
        if blocks:
            logger.debug("Sample source blocks: %s", _sample_preview([block.text for block in blocks]))
        translations = self.translator.translate_batch([block.text for block in blocks], progress=True)
        if translations:
            logger.debug("Sample translated blocks: %s", _sample_preview(translations))
        overlay_pdf = self._create_overlay(blocks, translations)
        output = self._merge_overlay(source_pdf, overlay_pdf)
        if self.config.cleanup_working:
            logger.debug("Cleaning working directory %s", self.work_dir)
            clean_directory(self.work_dir)
        return output

    def _extract_blocks(self, pdf_path: Path) -> List[TextBlock]:
        blocks: List[TextBlock] = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page_index, page in enumerate(pdf.pages):
                chars = page.chars
                if not chars:
                    continue
                lines = self._group_chars_into_lines(chars)
                for line_chars in lines:
                    text = self._compose_text(line_chars)
                    if not text.strip():
                        continue
                    if not self._has_hangul(text):
                        continue
                    x0 = min(float(ch["x0"]) for ch in line_chars)
                    y0 = min(float(ch["top"]) for ch in line_chars)
                    x1 = max(float(ch["x1"]) for ch in line_chars)
                    y1 = max(float(ch["bottom"]) for ch in line_chars)
                    avg_size = sum(float(ch.get("size", 0)) for ch in line_chars) / len(line_chars)
                    font_name = self._dominant_font(line_chars)
                    blocks.append(
                        TextBlock(
                            page=page_index,
                            text=text.strip(),
                            bbox=(x0, y0, x1, y1),
                            font_size=avg_size,
                            font_name=font_name,
                        )
                    )
        logger.info("Collected %d text blocks for translation", len(blocks))
        return blocks

    def _create_overlay(self, blocks: List[TextBlock], translations: List[str]) -> Path:
        overlay_path = self.work_dir / "overlay.pdf"
        ensure_parent(overlay_path)
        canvas_obj = canvas.Canvas(str(overlay_path))
        font_name = self._resolve_font(self.config.layout.font)

        grouped: Dict[int, List[tuple[TextBlock, str]]] = defaultdict(list)
        for block, translated in zip(blocks, translations):
            grouped.setdefault(block.page, []).append((block, translated))

        # Determine page sizes via pdfplumber to ensure alignment
        with pdfplumber.open(str(self.config.input_path)) as pdf:
            page_sizes = [ (page.width, page.height) for page in pdf.pages ]

        for page_index, (width, height) in enumerate(page_sizes):
            canvas_obj.setPageSize((width, height))
            for block, translated in grouped.get(page_index, []):
                self._draw_block(canvas_obj, block, translated, font_name, height)
            canvas_obj.showPage()

        canvas_obj.save()
        return overlay_path

    @staticmethod
    def _group_words_by_line(words: List[dict]) -> List[dict]:
        grouped: List[dict] = []
        if not words:
            return grouped

        current_line = {
            "text": words[0]["text"],
            "x0": words[0]["x0"],
            "x1": words[0]["x1"],
            "top": words[0]["top"],
            "bottom": words[0]["bottom"],
        }
        current_y = words[0]["top"]

        for word in words[1:]:
            if abs(word["top"] - current_y) <= 2:
                current_line["text"] += " " + word["text"]
                current_line["x1"] = word["x1"]
                current_line["top"] = min(current_line["top"], word["top"])
                current_line["bottom"] = max(current_line["bottom"], word["bottom"])
            else:
                grouped.append(current_line)
                current_line = {
                    "text": word["text"],
                    "x0": word["x0"],
                    "x1": word["x1"],
                    "top": word["top"],
                    "bottom": word["bottom"],
                }
                current_y = word["top"]

        grouped.append(current_line)
        return grouped

    def _draw_block(
        self,
        canvas_obj: canvas.Canvas,
        block: TextBlock,
        translated: str,
        font_name: str,
        page_height: float,
    ) -> None:
        x0, y0, x1, y1 = block.bbox
        block_width = x1 - x0
        block_height = y1 - y0
        if self._background_color and translated.strip():
            canvas_obj.saveState()
            canvas_obj.setFillColor(self._background_color)
            canvas_obj.rect(x0, page_height - y1, block_width, block_height, fill=1, stroke=0)
            canvas_obj.restoreState()
        lines = translated.splitlines() or [translated]
        line_count = max(1, len(lines))
        base_font_size = block.font_size if block.font_size else block_height / line_count
        shrink_factor = 1.0 - (self.config.layout.overflow_shrink_pct / 100.0)
        font_size = max(6, base_font_size * shrink_factor)
        line_height = font_size * 1.1

        y_start = page_height - y0 - font_size
        text_obj = canvas_obj.beginText()
        text_obj.setTextOrigin(x0, y_start)
        text_obj.setFont(font_name, font_size)
        text_obj.setFillColor(colors.black)
        text_obj.setLeading(line_height)

        for line in lines:
            adjusted = self._fit_line(line, font_name, font_size, block_width)
            for segment in adjusted.split("\n"):
                text_obj.textLine(segment)
        canvas_obj.drawText(text_obj)

    def _fit_line(self, text: str, font_name: str, font_size: float, max_width: float) -> str:
        width = pdfmetrics.stringWidth(text, font_name, font_size)
        if width <= max_width:
            return text
        words = text.split()
        if not words:
            return text
        result: List[str] = []
        current: List[str] = []
        for word in words:
            tentative = " ".join(current + [word]) if current else word
            if pdfmetrics.stringWidth(tentative, font_name, font_size) <= max_width:
                current.append(word)
            else:
                if current:
                    result.append(" ".join(current))
                current = [word]
        if current:
            result.append(" ".join(current))
        return "\n".join(result)

    def _merge_overlay(self, base_pdf: Path, overlay_pdf: Path) -> Path:
        ensure_parent(self.config.output_path)
        base = Pdf.open(str(base_pdf))
        overlay = Pdf.open(str(overlay_pdf))
        for page, layer in zip(base.pages, overlay.pages):
            page.add_overlay(layer)
        base.save(str(self.config.output_path))
        return self.config.output_path

    def _resolve_font(self, preferred_name: str) -> str:
        if preferred_name in pdfmetrics.getRegisteredFontNames():
            return preferred_name
        font_path = Path(preferred_name)
        if font_path.exists():
            from reportlab.pdfbase.ttfonts import TTFont

            font_name = font_path.stem
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            return font_name
        logger.warning("Font %s not registered; using Helvetica", preferred_name)
        return "Helvetica"

    @staticmethod
    def _has_hangul(text: str) -> bool:
        return any("\uac00" <= ch <= "\ud7a3" for ch in text)

    @staticmethod
    def _prepare_background_color(value: str | None):
        if not value:
            return None
        try:
            return colors.toColor(value)
        except Exception:
            logger.warning("Invalid background color %s; ignoring", value)
            return None

    @staticmethod
    def _group_chars_into_lines(chars: List[dict], tolerance: float = 2.0) -> List[List[dict]]:
        if not chars:
            return []
        sorted_chars = sorted(chars, key=lambda ch: (ch["top"], ch["x0"]))
        lines: List[List[dict]] = []
        current: List[dict] = []
        current_top = None
        for ch in sorted_chars:
            top = ch["top"]
            if current and abs(top - current_top) > tolerance:
                lines.append(current)
                current = []
            if not current:
                current_top = top
            current.append(ch)
        if current:
            lines.append(current)
        return lines

    @staticmethod
    def _compose_text(line_chars: List[dict], gap_ratio: float = 0.15) -> str:
        if not line_chars:
            return ""
        line_chars = sorted(line_chars, key=lambda ch: ch["x0"])
        pieces: List[str] = []
        last_x1 = None
        avg_width = sum((ch["x1"] - ch["x0"]) for ch in line_chars) / max(len(line_chars), 1)
        for ch in line_chars:
            if last_x1 is not None and (ch["x0"] - last_x1) > avg_width * gap_ratio:
                pieces.append(" ")
            pieces.append(ch.get("text", ""))
            last_x1 = ch["x1"]
        return "".join(pieces)

    @staticmethod
    def _dominant_font(line_chars: List[dict]) -> str | None:
        fonts = [ch.get("fontname") for ch in line_chars if ch.get("fontname")]
        if not fonts:
            return None
        most_common, _ = Counter(fonts).most_common(1)[0]
        return most_common
