"""Translation cache stored on disk."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional


class TranslationCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._data: Dict[str, str] = {}
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as fp:
                    self._data = json.load(fp)
            except json.JSONDecodeError:
                self._data = {}

    def get(self, text: str) -> Optional[str]:
        return self._data.get(text)

    def set(self, text: str, translation: str) -> None:
        self._data[text] = translation

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump(self._data, fp, ensure_ascii=False, indent=2)
