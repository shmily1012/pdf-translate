(pdf-translate) [root@pae-llm-host pdf-translate]#    docker run --rm      -v "$(pwd)/configs:/app/configs"      -v "$(pwd)/data:/app/data"      -v "$(pwd)/oputs:/app/outputs"      -v "$(pwd)/cache:/app/cache"      pdf-translate --config configs/config.yaml
INFO:pdf_translate.ocr:Running ocrmypdf on data/PS1101_245TB_AtomosP_E3_L_PDFSS_250715_R2.pdf
INFO:pdf_translate.pipeline_b:Collected 563 text blocks for translation
INFO:pdf_translate.pipeline_b:Identified 563 text blocks containing Hangul
INFO:pdf_translate.translation:Translating 563/563 text chunks (batch size=10)
INFO:openai._base_client:Retrying request to /chat/completions in 0.397468 seconds
INFO:openai._base_client:Retrying request to /chat/completions in 0.788605 seconds
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
    yield
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 250, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 256, in handle_request
    raise exc from None
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 236, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 101, in handle_request
    raise exc
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 78, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 124, in _connect
    stream = self._network_backend.connect_tcp(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 207, in connect_tcp
    with map_exceptions(exc_map):
  File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/usr/local/lib/python3.11/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ConnectError: [Errno 111] Connection refused

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/openai/_base_client.py", line 982, in request
    response = self._client.send(
               ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 914, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1014, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 249, in handle_request
    with map_httpcore_exceptions():
  File "/usr/local/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [Errno 111] Connection refused

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/bin/pdf-translate", line 7, in <module>
    sys.exit(main())
             ^^^^^^
  File "/app/src/pdf_translate/cli.py", line 50, in main
    pipeline.run()
  File "/app/src/pdf_translate/pipeline_b.py", line 56, in run
    translations = self.translator.translate_batch([block.text for block in blocks])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/pdf_translate/translation.py", line 83, in translate_batch
    translations = [self._translate_single(text) for text in batch]
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/pdf_translate/translation.py", line 83, in <listcomp>
    translations = [self._translate_single(text) for text in batch]
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/src/pdf_translate/translation.py", line 102, in _translate_single
    response = self._client.chat.completions.create(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_utils/_utils.py", line 286, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/resources/chat/completions/completions.py", line 1147, in create
    return self._post(
           ^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_base_client.py", line 1259, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/openai/_base_client.py", line 1014, in request
    raise APIConnectionError(request=request) from err
openai.APIConnectionError: Connection error.
(pdf-translate) [root@pae-llm-host pdf-translate]# 