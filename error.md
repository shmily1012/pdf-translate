docker run --rm -it \
  -v "$(pwd)/data:/app/data" \
  pdf-translate /bin/bash
soffice --headless \
  --convert-to "pptx:Impress MS PowerPoint 2007 XML" \
  /app/data/working/PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2_ocr.pdf \
  --outdir /app/data/working
