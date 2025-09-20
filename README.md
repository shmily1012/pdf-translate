# PDF Translate

Translate Korean PDF slide decks into English on an air-gapped Linux machine while keeping the slides readable. The tool wraps the end-to-end workflow described in the design doc and offers two interchangeable pipelines:

* **Pipeline A (default)** – Convert PDF → PPTX with `pdf2pptx`, replace Korean text with English in-place, save a translated PPTX, and optionally generate the final PDF through the overlay flow. Best when you want an editable slide deck alongside the PDF output.
* **Pipeline B** – Keep the original PDF intact and draw translated text on a transparent overlay (now powered by `pdfplumber` for extraction). Best when layout fidelity matters more than editability.

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
- [ocrmypdf](https://ocrmypdf.readthedocs.io/) with the `kor+eng` language pack (available via `apt`, `brew`, or `pip`)
- `poppler-utils` (provides the rendering backend used by `pdf2pptx` and `pdfplumber`)
- [pdf2pptx](https://pypi.org/project/pdf2pptx/) and [pdfplumber](https://github.com/jsvine/pdfplumber) Python dependencies (installed via pip; both require Poppler)
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
3. Verify that required CLI tools resolve:
   ```bash
   ocrmypdf --version
   tesseract --version
   ```
4. Start your vLLM server and confirm it answers OpenAI-style requests (see `scripts/translate_api.py` for a quick test script).

---

## Docker Option
Prefer a containerized setup? A `Dockerfile` is provided that bundles ocrmypdf, Tesseract (with Korean data), Poppler, fonts, and the Python project.

1. Build the image from the project root:
   ```bash
   docker build -t pdf-translate .
   ```
2. Run the pipeline, mounting your working directories so results persist:
   ```bash
   docker run --rm \
     -v "$(pwd)/configs:/app/configs" \
     -v "$(pwd)/data:/app/data" \
     -v "$(pwd)/outputs:/app/outputs" \
     -v "$(pwd)/cache:/app/cache" \
     pdf-translate --config configs/config.yaml
   ```
3. If your vLLM server is on the host machine, make sure the container can reach it. On Linux you can add `--network host`; otherwise point `translate.api_base` to an address accessible from inside the container (for example `http://host.docker.internal:8000/v1`).

The default entrypoint already runs `pdf-translate --config configs/config.yaml`, so you can omit the command override if the mount paths align with the config.

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
- `working_dir`: scratch space used for OCR output, PPTX conversions, overlays.
- `cleanup_working`: set to `true` to remove temporary files in `working_dir` after a successful run.
- `ocr.enabled`: set to `true` if the PDF may contain scans; disable to skip the OCR step.
- `translate.api_base` / `model` / `batch_size`: connection details for the local vLLM server.
- `translate.api_key`: optional API token if your endpoint requires one (omit or leave blank for unsecured local instances).
- `translate.cache`: location for the translation cache JSON file.
- `layout.overflow_shrink_pct`: how aggressively to shrink font size when overlays would overflow their bounding boxes (Pipeline B).
- `layout.font`: ReportLab font name or a path to a TTF file used for overlay rendering.
- `layout.background_color`: optional hex/name color used to paint a rectangle behind translated text in Pipeline B (helps mask the original text when overlays should fully replace Hangul).

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
- The conversion uses `pdf2pptx`, which may flatten complex effects; inspect the generated PPTX (saved alongside your PDF) and adjust text boxes if needed.
- Intermediate `.pptx` files remain in `data/working`; you can open them with PowerPoint/Keynote/etc. to verify changes before delivery.

### Pipeline B tips
- Choose a font that fits your corporate template. You can provide an absolute path to a `.ttf` file in `layout.font` if the font is not pre-registered with ReportLab.
- If English text wraps poorly, tweak `overflow_shrink_pct` or add manual line breaks in the translation cache.
- Set `layout.background_color` (for example `"#FFFFFF"`) if you want the translated text to fully cover the original Hangul instead of overlaying transparently.

---

## Re-running & Caching
- Translations are cached in `cache/translations.json` keyed by the original Korean string. Delete the file to force fresh translations.
- OCR output and converted PPTX files are reused when the source PDF timestamp has not changed, speeding up subsequent runs.

---

## Troubleshooting
- **`Command ... not found`** – Ensure `ocrmypdf`, `tesseract`, and other required CLIs are installed and visible in `$PATH`.
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
