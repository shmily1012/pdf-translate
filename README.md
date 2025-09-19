# PDF Translate

Translate Korean PDF slide decks into English on an air-gapped Linux machine while keeping the slides readable. The tool wraps the end-to-end workflow described in the design doc and offers two interchangeable pipelines:

* **Pipeline A (default)** – Convert PDF → PPTX, replace Korean text with English in-place, and export back to PDF. Best when you want an editable slide deck.
* **Pipeline B** – Keep the original PDF intact and draw translated text on a transparent overlay. Best when layout fidelity matters more than editability.

---

## Key Features
- Calls a **local vLLM server** through the OpenAI-compatible API; no external network traffic.
- Optional **OCR pre-processing** with `ocrmypdf` to ensure text extraction works even on scanned slides.
- Built-in **translation cache** so repeated runs do not resend identical text to the model.
- Configurable **font fallback, shrink percentage, and batching** so you can tune the results for different decks.

---

## Prerequisites
Install these system tools before using the project:

- Linux environment with Python 3.10+
- [LibreOffice](https://www.libreoffice.org/) (provides the `soffice` CLI used for PDF⇄PPTX conversions)
- [ocrmypdf](https://ocrmypdf.readthedocs.io/) with the `kor+eng` language pack (available via `apt`, `brew`, or `pip`)
- [vLLM](https://vllm.ai/) running locally and exposing an OpenAI-compatible HTTP endpoint (for example `http://localhost:8000/v1`)
- Optional but recommended: Noto Sans / Noto Serif fonts for cleaner English overlay output (Pipeline B)

---

## Installation
1. Clone the repository and create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   ```
2. Install the project in editable mode (installs Python dependencies from `pyproject.toml`):
   ```bash
   pip install -e .
   ```
3. Verify that the required CLI tools resolve:
   ```bash
   soffice --version
   ocrmypdf --version
   ```
4. Start your vLLM server and confirm it answers OpenAI-style requests (see `scripts/translate_api.py` for a quick test script).

---

## Project Layout
```
configs/
  config.yaml        # Main configuration file
src/pdf_translate/
  cli.py             # CLI entry point
  config.py          # YAML config loader
  translation.py     # vLLM client with caching
  pipeline_a.py      # PPTX round-trip pipeline
  pipeline_b.py      # Overlay pipeline
  ...
scripts/
  translate_api.py   # Simple translation smoke test
cache/
  translations.json  # Created automatically on first run
```

---

## Configure the Pipeline
Edit `configs/config.yaml` to point to your files and environment. Important keys:

- `pipeline`: choose `A` for PPTX editing or `B` for overlay rendering.
- `input_pdf` / `output_pdf`: source PDF to translate and destination path for the final result.
- `ocr.enabled`: set to `true` if the PDF may contain scans; disable to skip the OCR step.
- `translate.api_base` / `model` / `batch_size`: connection details for the local vLLM server.
- `translate.cache`: location for the translation cache JSON file.
- `layout.overflow_shrink_pct`: how aggressively to shrink font size when overlays would overflow their bounding boxes (Pipeline B).
- `layout.font`: ReportLab font name or a path to a TTF file used for overlay rendering.

---

## Run a Translation
Activate your virtual environment and call the CLI:

```bash
python -m pdf_translate.cli --config configs/config.yaml
```

If you installed the package, you can use the entry point instead:

```bash
pdf-translate --config configs/config.yaml
```

Logs show each stage (OCR, conversion, translation, export). When the command finishes, the translated PDF is written to `output_pdf` from the config.

### Pipeline A tips
- The round trip relies on LibreOffice, so very complex layouts may shift slightly—inspect the PPTX in `data/working` if you need to adjust text boxes manually.
- Intermediate `.pptx` files remain in `data/working`; you can open them with PowerPoint/LibreOffice to verify changes.

### Pipeline B tips
- Choose a font that fits your corporate template. You can provide an absolute path to a `.ttf` file in `layout.font` if the font is not pre-registered with ReportLab.
- If English text wraps poorly, tweak `overflow_shrink_pct` or add manual line breaks in the translation cache.

---

## Re-running & Caching
- Translations are cached in `cache/translations.json` keyed by the original Korean string. Delete the file to force fresh translations.
- OCR output and converted PPTX files are reused when the source PDF timestamp has not changed, speeding up subsequent runs.

---

## Troubleshooting
- **`Command ... not found`** – Ensure `soffice` and `ocrmypdf` are installed and visible in `$PATH`.
- **`Font ... not registered` warnings** – ReportLab could not find the font; install it system-wide or point `layout.font` to a `.ttf` file.
- **Overlay text overlapping** – Increase `layout.overflow_shrink_pct` or edit the cached translation to add manual line breaks.
- **Model request failures** – Confirm the vLLM server is running at `translate.api_base` and that it supports chat-completion requests.

---

## Quick Smoke Test
Use the helper script to confirm your translation endpoint works before processing a full deck:

```bash
python scripts/translate_api.py
```

The script reads your config, makes a single translation request with sample Hangul text, and prints the English result.

---

## Next Steps
- Populate `data/input.pdf` with your slide deck and update `config.yaml` paths.
- Build a terminology file in `glossary/terms.csv` (future enhancement) if you need consistent domain terms.
- Integrate additional QA checks (visual diffing, PDF font checks) as needed for your workflow.
