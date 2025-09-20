"""Configuration loading for the PDF translation pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


@dataclass
class OCRConfig:
    enabled: bool = True
    lang: str = "kor+eng"


@dataclass
class TranslateConfig:
    api_base: str = "http://localhost:8000/v1"
    model: str = "qwen2.5-7b-instruct"
    batch_size: int = 10
    cache: str = "cache/translations.json"
    api_key: Optional[str] = None


@dataclass
class LayoutConfig:
    overflow_shrink_pct: int = 10
    font: str = "Noto Sans"
    background_color: Optional[str] = None


@dataclass
class AppConfig:
    input_path: Path
    output_path: Path
    ocr: OCRConfig
    translate: TranslateConfig
    layout: LayoutConfig
    working_dir: Path
    cleanup_working: bool

    @property
    def translate_cache_path(self) -> Path:
        return Path(self.translate.cache)


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp) or {}


def _build_ocr_config(data: Dict[str, Any]) -> OCRConfig:
    return OCRConfig(
        enabled=bool(data.get("enabled", True)),
        lang=str(data.get("lang", "kor+eng")),
    )


def _build_translate_config(data: Dict[str, Any]) -> TranslateConfig:
    return TranslateConfig(
        api_base=str(data.get("api_base", "http://localhost:8000/v1")),
        model=str(data.get("model", "qwen2.5-7b-instruct")),
        batch_size=int(data.get("batch_size", 10)),
        cache=str(data.get("cache", "cache/translations.json")),
        api_key=data.get("api_key"),
    )


def _build_layout_config(data: Dict[str, Any]) -> LayoutConfig:
    return LayoutConfig(
        overflow_shrink_pct=int(data.get("overflow_shrink_pct", 10)),
        font=str(data.get("font", "Noto Sans")),
        background_color=data.get("background_color"),
    )


def load_config(path: Path) -> AppConfig:
    data = _load_yaml(path)

    input_path_value = data.get("input_path") or data.get("input_pdf")
    output_path_value = data.get("output_path") or data.get("output_pdf")
    if not input_path_value or not output_path_value:
        raise ValueError("config must specify input_path/output_path")

    ocr = _build_ocr_config(data.get("ocr", {}))
    translate = _build_translate_config(data.get("translate", {}))
    layout = _build_layout_config(data.get("layout", {}))

    working = Path(data.get("working_dir", "data/working"))
    cleanup = bool(data.get("cleanup_working", False))

    return AppConfig(
        input_path=Path(input_path_value),
        output_path=Path(output_path_value),
        ocr=ocr,
        translate=translate,
        layout=layout,
        working_dir=working,
        cleanup_working=cleanup,
    )


def load_config_from_file(path: str | Path) -> AppConfig:
    return load_config(Path(path))
