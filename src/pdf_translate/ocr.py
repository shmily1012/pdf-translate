"""OCR helper that wraps ocrmypdf when needed."""
from __future__ import annotations

import logging
from pathlib import Path

from .utils import run_command, ensure_parent

logger = logging.getLogger(__name__)


def ensure_searchable_pdf(input_pdf: Path, lang: str, work_dir: Path) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = work_dir / f"{input_pdf.stem}_ocr.pdf"
    if output_pdf.exists() and output_pdf.stat().st_mtime >= input_pdf.stat().st_mtime:
        logger.info("Skipping OCR; cached file %s is up to date", output_pdf)
        return output_pdf

    logger.info("Running ocrmypdf on %s", input_pdf)
    ensure_parent(output_pdf)
    run_command(
        [
            "ocrmypdf",
            "--force-ocr",
            f"--language={lang}",
            str(input_pdf),
            str(output_pdf),
        ]
    )
    return output_pdf
