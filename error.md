337.1       building 'fitz._fitz' extension
337.1       swigging fitz/fitz.i to fitz/fitz_wrap.c
337.1       swig -python -o fitz/fitz_wrap.c fitz/fitz.i
337.1       error: command 'swig' failed: No such file or directory
337.1       [end of output]
337.1   
337.1   note: This error originates from a subprocess, and is likely not a problem with pip.
337.1   ERROR: Failed building wheel for PyMuPDF
337.1   Running setup.py clean for PyMuPDF
337.3 Successfully built pdf-translate img2pdf
337.3 Failed to build PyMuPDF
337.4 error: failed-wheel-build-for-install
337.4 
337.4 × Failed to build installable wheels for some pyproject.toml based projects
337.4 ╰─> PyMuPDF
------
Dockerfile:32
--------------------
  30 |     COPY scripts ./scripts
  31 |     
  32 | >>> RUN pip install --upgrade pip && pip install -e .
  33 |     
  34 |     ENTRYPOINT ["pdf-translate"]
--------------------
ERROR: failed to solve: process "/bin/sh -c pip install --upgrade pip && pip install -e ." did not complete successfully: exit code: 1