"""Example script showing how to call the local vLLM OpenAI-compatible endpoint."""
from __future__ import annotations

from pdf_translate.config import load_config_from_file
from pdf_translate.translation import TranslationClient
from pdf_translate.cache import TranslationCache


def main() -> None:
    config = load_config_from_file("configs/config.yaml")
    cache = TranslationCache(config.translate_cache_path)
    translator = TranslationClient(
        api_base=config.translate.api_base,
        model=config.translate.model,
        batch_size=1,
        cache=cache,
    )
    sample = "한글 텍스트 예시"
    translated = translator.translate_batch([sample])[0]
    print(translated)


if __name__ == "__main__":
    main()
