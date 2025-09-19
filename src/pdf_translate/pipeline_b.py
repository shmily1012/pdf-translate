"""Pipeline B: overlay translated text on top of original PDF."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz  # PyMuPDF
from pikepdf import Pdf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from .config import AppConfig
from .ocr import ensure_searchable_pdf
from .translation import TranslationClient
from .utils import ensure_parent

logger = logging.getLogger(__name__)


@dataclass
class TextBlock:
    page: int
    text: str
    bbox: tuple[float, float, float, float]


class PipelineB:
    def __init__(self, config: AppConfig, translator: TranslationClient, work_dir: Path | None = None) -> None:
        self.config = config
        self.translator = translator
        self.work_dir = work_dir or Path("data/working")
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> Path:
        source_pdf = self.config.input_pdf
        if self.config.ocr.enabled:
            source_pdf = ensure_searchable_pdf(source_pdf, self.config.ocr.lang, self.work_dir)

        doc = fitz.open(str(source_pdf))
        blocks = self._extract_blocks(doc)
        translations = self.translator.translate_batch([block.text for block in blocks])
        overlay_pdf = self._create_overlay(doc, blocks, translations)
        output = self._merge_overlay(source_pdf, overlay_pdf)
        return output

    def _extract_blocks(self, doc: fitz.Document) -> List[TextBlock]:
        blocks: List[TextBlock] = []
        for page_index, page in enumerate(doc):
            for block in page.get_text("blocks"):
                x0, y0, x1, y1, text, block_no, block_type = block
                if not text.strip():
                    continue
                if block_type != 0:
                    continue
                if not self._has_hangul(text):
                    continue
                blocks.append(TextBlock(page=page_index, text=text.strip(), bbox=(x0, y0, x1, y1)))
        logger.info("Collected %d text blocks for translation", len(blocks))
        return blocks

    def _create_overlay(self, doc: fitz.Document, blocks: List[TextBlock], translations: List[str]) -> Path:
        overlay_path = self.work_dir / "overlay.pdf"
        ensure_parent(overlay_path)
        canvas_obj = canvas.Canvas(str(overlay_path))
        font_name = self._resolve_font(self.config.layout.font)

        grouped: dict[int, List[tuple[TextBlock, str]]] = {}
        for block, translated in zip(blocks, translations):
            grouped.setdefault(block.page, []).append((block, translated))

        for page_index, page in enumerate(doc):
            width, height = page.rect.width, page.rect.height
            canvas_obj.setPageSize((width, height))
            for block, translated in grouped.get(page_index, []):
                self._draw_block(canvas_obj, block, translated, font_name, height)
            canvas_obj.showPage()

        canvas_obj.save()
        return overlay_path

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
        lines = translated.splitlines() or [translated]
        line_count = max(1, len(lines))
        base_font_size = block_height / line_count
        shrink_factor = 1.0 - (self.config.layout.overflow_shrink_pct / 100.0)
        font_size = max(6, base_font_size * shrink_factor)
        line_height = font_size * 1.1

        y_start = page_height - y0 - font_size
        text_obj = canvas_obj.beginText()
        text_obj.setTextOrigin(x0, y_start)
        text_obj.setFont(font_name, font_size)
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
        ensure_parent(self.config.output_pdf)
        base = Pdf.open(str(base_pdf))
        overlay = Pdf.open(str(overlay_pdf))
        for page, layer in zip(base.pages, overlay.pages):
            page.add_overlay(layer)
        base.save(str(self.config.output_pdf))
        return self.config.output_pdf

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
