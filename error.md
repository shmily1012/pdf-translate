(pdf-translate) [root@pae-llm-host pdf-translate]#    docker run --rm      -v "$(pwd)/configs:/app/configs"      -v "$(pwd)/data:/app/data"      -v "$(pwd)/outputs:/app/outputs"      -v "$(pwd)/cache:/app/cache"      pdf-translate --config configs/config.yaml
INFO:pdf_translate.ocr:Skipping OCR; cached file data/working/PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2_ocr.pdf is up to date
INFO:pdf_translate.pipeline_a:Converting data/working/PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2_ocr.pdf to PPTX via LibreOffice
Traceback (most recent call last):
  File "/usr/local/bin/pdf-translate", line 7, in <module>
    sys.exit(main())
             ^^^^^^
  File "/app/src/pdf_translate/cli.py", line 50, in main
    pipeline.run()
  File "/app/src/pdf_translate/pipeline_a.py", line 41, in run
    pptx_path = self._convert_pdf_to_pptx(source_pdf)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/pdf_translate/pipeline_a.py", line 61, in _convert_pdf_to_pptx
    pptx_path = self._select_output_file(
                ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/pdf_translate/pipeline_a.py", line 141, in _select_output_file
    raise FileNotFoundError(
FileNotFoundError: LibreOffice did not create an output file matching '.pptx' for PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2_ocr: Warning: failed to launch javaldx - java may not function correctly
Error: no export filter for /app/data/working/PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2_ocr.pptx found, aborting.
Error: no export filter