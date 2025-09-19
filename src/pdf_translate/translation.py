"""Translation client that talks to a local vLLM OpenAI-compatible endpoint."""
from __future__ import annotations

import logging
from typing import Iterable, List, Sequence

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

        if remaining:
            logger.info("Translating %d text chunks", len(remaining))
            for start in range(0, len(remaining), self.batch_size):
                batch = remaining[start : start + self.batch_size]
                translations = [self._translate_single(text) for text in batch]
                for text, translation in zip(batch, translations):
                    if self.cache:
                        self.cache.set(text, translation)
                for rel_idx, translation in enumerate(translations):
                    absolute_idx = missing_indices[start + rel_idx]
                    results[absolute_idx] = translation

        if self.cache:
            self.cache.save()

        return results

    def _translate_single(self, text: str) -> str:
        if self._mode == "new":
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text},
                ],
                temperature=0,
            )
            return response.choices[0].message.content.strip()

        response = self._client.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        return response["choices"][0]["message"]["content"].strip()
