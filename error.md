[+] Building 83.2s (14/15)                                                                                                                      docker:default
 => => transferring context: 198B                                                                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                       0.7s
 => [internal] load build context                                                                                                                         0.0s
 => => transferring context: 3.91kB                                                                                                                       0.0s
 => CACHED [1/9] FROM docker.io/library/python:3.11-slim@sha256:a0939570b38cddeb861b8e75d20b1c8218b21562b18f301171904b544e8cf228                          0.0s
 => [2/9] RUN apt-get update &&     apt-get install -y --no-install-recommends         build-essential         ocrmypdf         poppler-utils         t  36.5s
 => [3/9] RUN swig -version                                                                                                                               0.2s
 => [4/9] WORKDIR /app                                                                                                                                    0.0s
 => [5/9] COPY pyproject.toml README.md requirements.txt ./                                                                                               0.0s
 => [6/9] COPY src ./src                                                                                                                                  0.0s
 => [7/9] COPY configs ./configs                                                                                                                          0.0s
 => [8/9] COPY scripts ./scripts                                                                                                                          0.0s 
 => [9/9] RUN pip install --upgrade pip && pip install -e .                                                                                              44.8s 
 => => #   Stored in directory: /tmp/pip-ephem-wheel-cache-amb0knuq/wheels/21/0a/64/6a8143672bcea0d35b8cf705ba12b11bb191367cfde88d4f35                         
 => => #   DEPRECATION: Building 'PyMuPDF' using the legacy setup.py bdist_wheel mechanism, which will be removed in a future version. pip 25.3 will enforce t 
 => => # his behaviour change. A possible replacement is to use the standardized build interface by setting the `--use-pep517` option, (possibly combined with 
 => => #  `--no-build-isolation`), or adding a `pyproject.toml` file to the source tree of 'PyMuPDF'. Discussion can be found at https://github.com/pypa/pip/i 
 => => # ssues/6334                                                                                                                                           
 => => #   Building wheel for PyMuPDF (setup.py): started  