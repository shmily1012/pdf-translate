"""CLI entry point for the PDF translation pipelines."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .cache import TranslationCache
from .config import load_config_from_file
from .pipeline_a import PipelineA
from .pipeline_b import PipelineB
from .translation import TranslationClient


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate Korean PDFs to English while preserving layout.")
    parser.add_argument(
        "--config",
        default="configs/config.yaml",
        help="Path to YAML configuration file.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    config = load_config_from_file(args.config)
    cache = TranslationCache(config.translate_cache_path)
    translator = TranslationClient(
        api_base=config.translate.api_base,
        model=config.translate.model,
        batch_size=config.translate.batch_size,
        cache=cache,
        api_key=config.translate.api_key,
    )

    if config.pipeline == "A":
        pipeline = PipelineA(config, translator)
    else:
        pipeline = PipelineB(config, translator)

    pipeline.run()
    logging.info("Translation finished. Output written to %s", config.output_pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
