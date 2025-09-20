332.8       error: command 'swig' failed: No such file or directory
332.8       [end of output]
332.8   
332.8   note: This error originates from a subprocess, and is likely not a problem with pip.
332.8   ERROR: Failed building wheel for PyMuPDF
332.8   Running setup.py clean for PyMuPDF
333.0 Successfully built pdf-translate img2pdf
333.0 Failed to build PyMuPDF
333.1 error: failed-wheel-build-for-install
333.1 
333.1 × Failed to build installable wheels for some pyproject.toml based projects
333.1 ╰─> PyMuPDF
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
(pdf-translate) [root@pae-llm-host pdf-translate]# 