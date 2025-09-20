"""Pipeline A: convert PDF to PPTX via pdf2pptx, replace text, export results."""
from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pptx import Presentation  # type: ignore
from pdf2pptx import Converter  # type: ignore

from .config import AppConfig
from .ocr import ensure_searchable_pdf
from .translation import TranslationClient
from .utils import ensure_parent, clean_directory

logger = logging.getLogger(__name__)


@dataclass
class ParagraphHandle:
    paragraph: "Paragraph"
    text: str


def _has_hangul(text: str) -> bool:
    return any("\uac00" <= ch <= "\ud7a3" for ch in text)


def _sample_preview(texts: List[str], limit: int = 40, max_items: int = 3) -> str:
    sample = []
    for text in texts[:max_items]:
        collapsed = " ".join(text.split())
        if len(collapsed) > limit:
            collapsed = f"{collapsed[:limit]}…"
        sample.append(collapsed)
    return ", ".join(sample)


class PipelineA:
    def __init__(self, config: AppConfig, translator: TranslationClient, work_dir: Path | None = None) -> None:
        self.config = config
        self.translator = translator
        self.work_dir = work_dir or config.working_dir
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> Path:
        source_pdf = self.config.input_pdf
        if self.config.ocr.enabled:
            source_pdf = ensure_searchable_pdf(source_pdf, self.config.ocr.lang, self.work_dir)

        pptx_path = self._convert_pdf_to_pptx(source_pdf)
        translated_pptx = self._translate_pptx(pptx_path)
        self._persist_pptx(translated_pptx)

        output_path = self.config.output_pdf
        if output_path.suffix.lower() == ".pdf":
            logger.info("Generating final PDF using overlay pipeline (no LibreOffice)")
            from .pipeline_b import PipelineB

            overlay_pipeline = PipelineB(self.config, self.translator, work_dir=self.work_dir)
            output_path = overlay_pipeline.run()

        if self.config.cleanup_working:
            logger.debug("Cleaning working directory %s", self.work_dir)
            clean_directory(self.work_dir)

        return output_path

    def _convert_pdf_to_pptx(self, pdf_path: Path) -> Path:
        logger.info("Converting %s to PPTX via pdf2pptx", pdf_path)
        if pdf_path.suffix.lower() == ".pptx":
            target = self.work_dir / pdf_path.name
            shutil.copy2(pdf_path, target)
            return target

        pptx_path = self.work_dir / f"{pdf_path.stem}.pptx"
        ensure_parent(pptx_path)
        if pptx_path.exists() and pptx_path.stat().st_mtime >= pdf_path.stat().st_mtime:
            logger.info("Using cached PPTX at %s", pptx_path)
            return pptx_path

        converter = Converter(str(pdf_path))
        try:
            converter.convert(str(pptx_path))
        finally:
            converter.close()

        if not pptx_path.exists():
            raise FileNotFoundError(f"pdf2pptx did not create PPTX at {pptx_path}")

        logger.debug("Created PPTX at %s", pptx_path)
        return pptx_path

    def _translate_pptx(self, pptx_path: Path) -> Path:
        logger.info("Translating text content within %s", pptx_path)
        presentation = Presentation(str(pptx_path))
        handles = self._collect_paragraphs(presentation)
        texts = [handle.text for handle in handles]
        logger.info("Identified %d paragraphs containing Hangul", len(texts))
        if texts:
            logger.debug("Sample source paragraphs: %s", _sample_preview(texts))
        translations = self.translator.translate_batch(texts)
        if translations:
            logger.debug("Sample translated paragraphs: %s", _sample_preview(translations))
        for handle, translation in zip(handles, translations):
            self._apply_translation(handle, translation)
        translated_path = self.work_dir / f"{pptx_path.stem}_translated.pptx"
        presentation.save(str(translated_path))
        return translated_path

    def _persist_pptx(self, translated_pptx: Path) -> Path:
        target = self.config.output_pdf
        if target.suffix.lower() == ".pdf":
            pptx_target = target.with_suffix(".pptx")
        else:
            pptx_target = target
        ensure_parent(pptx_target)
        shutil.copy2(translated_pptx, pptx_target)
        logger.info("Translated PPTX saved to %s", pptx_target)
        return pptx_target

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
