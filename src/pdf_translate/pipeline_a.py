"""Pipeline A: convert PDF to PPTX, replace text, export back to PDF."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pptx import Presentation  # type: ignore

from .config import AppConfig
from .ocr import ensure_searchable_pdf
from .translation import TranslationClient
from .utils import ensure_parent, run_command

logger = logging.getLogger(__name__)


@dataclass
class ParagraphHandle:
    paragraph: "Paragraph"
    text: str


def _has_hangul(text: str) -> bool:
    return any("\uac00" <= ch <= "\ud7a3" for ch in text)


class PipelineA:
    def __init__(self, config: AppConfig, translator: TranslationClient, work_dir: Path | None = None) -> None:
        self.config = config
        self.translator = translator
        self.work_dir = work_dir or Path("data/working")
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> Path:
        source_pdf = self.config.input_pdf
        if self.config.ocr.enabled:
            source_pdf = ensure_searchable_pdf(source_pdf, self.config.ocr.lang, self.work_dir)

        pptx_path = self._convert_pdf_to_pptx(source_pdf)
        translated_pptx = self._translate_pptx(pptx_path)
        output_pdf = self._export_pdf(translated_pptx)
        return output_pdf

    def _convert_pdf_to_pptx(self, pdf_path: Path) -> Path:
        logger.info("Converting %s to PPTX via LibreOffice", pdf_path)
        ensure_parent(self.work_dir / "dummy")
        run_command(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pptx",
                str(pdf_path),
                "--outdir",
                str(self.work_dir),
            ]
        )
        pptx_path = self.work_dir / f"{pdf_path.stem}.pptx"
        if not pptx_path.exists():
            raise FileNotFoundError(f"Expected converted PPTX at {pptx_path}")
        return pptx_path

    def _translate_pptx(self, pptx_path: Path) -> Path:
        logger.info("Translating text content within %s", pptx_path)
        presentation = Presentation(str(pptx_path))
        handles = self._collect_paragraphs(presentation)
        texts = [handle.text for handle in handles]
        translations = self.translator.translate_batch(texts)
        for handle, translation in zip(handles, translations):
            self._apply_translation(handle, translation)
        translated_path = self.work_dir / f"{pptx_path.stem}_translated.pptx"
        presentation.save(str(translated_path))
        return translated_path

    def _export_pdf(self, pptx_path: Path) -> Path:
        ensure_parent(self.config.output_pdf)
        logger.info("Exporting translated PPTX %s to PDF", pptx_path)
        run_command(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                str(pptx_path),
                "--outdir",
                str(self.config.output_pdf.parent),
            ]
        )
        output_pdf = self.config.output_pdf.parent / f"{pptx_path.stem}.pdf"
        if output_pdf != self.config.output_pdf:
            if self.config.output_pdf.exists():
                self.config.output_pdf.unlink()
            output_pdf.replace(self.config.output_pdf)
        return self.config.output_pdf

    def _collect_paragraphs(self, presentation: Presentation) -> List[ParagraphHandle]:
        handles: List[ParagraphHandle] = []
        for slide in presentation.slides:
            for shape in slide.shapes:
                if not getattr(shape, "has_text_frame", False):
                    continue
                text_frame = shape.text_frame
                for paragraph in text_frame.paragraphs:
                    text = paragraph.text.strip()
                    if not text:
                        continue
                    if not _has_hangul(text):
                        continue
                    handles.append(ParagraphHandle(paragraph=paragraph, text=text))
        return handles

    def _apply_translation(self, handle: ParagraphHandle, translation: str) -> None:
        paragraph = handle.paragraph
        if paragraph.runs:
            paragraph.runs[0].text = translation
            for run in paragraph.runs[1:]:
                run.text = ""
        else:
            run = paragraph.add_run()
            run.text = translation
