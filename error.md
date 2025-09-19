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
  File "/app/src/pdf_translate/pipeline_a.py", line 62, in _convert_pdf_to_pptx
    raise FileNotFoundError(f"Expected converted PPTX at {pptx_path}")
FileNotFoundError: Expected converted PPTX at data/working/PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2_ocr.pptx15234