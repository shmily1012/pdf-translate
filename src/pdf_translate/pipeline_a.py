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
        before = {path.name for path in self.work_dir.iterdir() if path.suffix.lower().startswith(".ppt")}
        proc = run_command(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pptx:Impress MS PowerPoint 2007 XML",
                str(pdf_path),
                "--outdir",
                str(self.work_dir),
            ]
        )
        pptx_path = self._select_output_file(
            suffix_hint=".pptx",
            stem=pdf_path.stem,
            before=before,
            process_stdout=proc.stdout,
            process_stderr=proc.stderr,
        )
        logger.debug("Selected PPTX output %s", pptx_path)
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

    def _export_pdf(self, pptx_path: Path) -> Path:
        ensure_parent(self.config.output_pdf)
        logger.info("Exporting translated PPTX %s to PDF", pptx_path)
        ensure_parent(self.config.output_pdf)
        output_dir = self.config.output_pdf.parent
        before = {path.name for path in output_dir.iterdir() if path.suffix.lower().startswith(".pdf")}
        proc = run_command(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf:writer_pdf_Export",
                str(pptx_path),
                "--outdir",
                str(output_dir),
            ]
        )
        output_pdf = self._select_output_file(
            suffix_hint=".pdf",
            stem=pptx_path.stem,
            before=before,
            directory=output_dir,
            process_stdout=proc.stdout,
            process_stderr=proc.stderr,
        )
        if output_pdf != self.config.output_pdf:
            if self.config.output_pdf.exists():
                self.config.output_pdf.unlink()
            output_pdf.replace(self.config.output_pdf)
        return self.config.output_pdf

    def _select_output_file(
        self,
        suffix_hint: str,
        stem: str,
        before: set[str],
        process_stdout: str,
        process_stderr: str,
        directory: Path | None = None,
    ) -> Path:
        directory = directory or self.work_dir
        suffix_hint_lower = suffix_hint.lower()
        candidates = []
        for path in directory.iterdir():
            if path.name in before:
                continue
            name_lower = path.name.lower()
            if stem.lower() in name_lower and suffix_hint_lower in name_lower:
                candidates.append(path)
        if not candidates:
            for path in directory.iterdir():
                if path.name in before:
                    continue
                if suffix_hint_lower in path.name.lower():
                    candidates.append(path)

        if not candidates:
            detail = process_stderr.strip() or process_stdout.strip() or "no output captured"
            raise FileNotFoundError(
                f"LibreOffice did not create an output file matching '{suffix_hint}' for {stem}: {detail}"
            )

        candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return candidates[0]

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
