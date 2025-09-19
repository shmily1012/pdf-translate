"""Translation client that talks to a local vLLM OpenAI-compatible endpoint."""
from __future__ import annotations

import logging
from typing import List, Sequence

from .cache import TranslationCache

logger = logging.getLogger(__name__)


class TranslationClient:
    def __init__(
        self,
        api_base: str,
        model: str,
        batch_size: int = 10,
        cache: TranslationCache | None = None,
        api_key: str | None = None,
        system_prompt: str | None = None,
    ) -> None:
        self.api_base = api_base
        self.model = model
        self.batch_size = max(1, batch_size)
        self.cache = cache
        self.system_prompt = (
            system_prompt
            or "You are a professional translator. Translate Korean text to natural English while preserving formatting cues."
        )

        try:
            # New-style client (openai>=1.0)
            from openai import OpenAI

            self._client = OpenAI(base_url=api_base, api_key=api_key or "EMPTY")
            self._mode = "new"
        except ImportError:
            import openai

            openai.api_base = api_base
            openai.api_key = api_key or "EMPTY"
            self._client = openai
            self._mode = "legacy"

    def translate_batch(self, texts: Sequence[str]) -> List[str]:
        total = len(texts)
        if not total:
            logger.debug("translate_batch called with empty input")
            return []

        results: List[str] = []
        remaining: List[str] = []
        missing_indices: List[int] = []

        for idx, text in enumerate(texts):
            cached = self.cache.get(text) if self.cache else None
            if cached is not None:
                results.append(cached)
            else:
                results.append("")
                remaining.append(text)
                missing_indices.append(idx)

        cache_hits = total - len(remaining)
        if cache_hits:
            logger.debug("Cache hit for %d/%d chunks", cache_hits, total)

        if remaining:
            logger.info(
                "Translating %d/%d text chunks (batch size=%d)",
                len(remaining),
                total,
                self.batch_size,
            )
            for start in range(0, len(remaining), self.batch_size):
                batch = remaining[start : start + self.batch_size]
                logger.debug(
                    "Sending batch %d containing %d chunks: %s",
                    (start // self.batch_size) + 1,
                    len(batch),
                    ", ".join(_preview(text) for text in batch),
                )
                translations = [self._translate_single(text) for text in batch]
                for text, translation in zip(batch, translations):
                    if self.cache:
                        self.cache.set(text, translation)
                for rel_idx, translation in enumerate(translations):
                    absolute_idx = missing_indices[start + rel_idx]
                    results[absolute_idx] = translation
        else:
            logger.info("All %d chunks served from cache", total)

        if self.cache:
            self.cache.save()
            logger.debug("Translation cache persisted to %s", self.cache.path)

        return results

    def _translate_single(self, text: str) -> str:
        logger.debug("Requesting translation for: %s", _preview(text, limit=120))
        if self._mode == "new":

            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text},
                ],
                temperature=0,
            )
            translation = response.choices[0].message.content.strip()
        else:
            response = self._client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text},
                ],
                temperature=0,
            )
            translation = response["choices"][0]["message"]["content"].strip()

        logger.debug("Received translation: %s", _preview(translation, limit=120))
        return translation


def _preview(text: str, limit: int = 60) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit]}…"
