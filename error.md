      creating build/temp.linux-x86_64-cpython-311/fitz
      gcc -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -fPIC -Imupdf-1.20.0-source/include -Imupdf-1.20.0-source/include/mupdf -Imupdf-1.20.0-source/thirdparty/freetype/include -I/usr/include/freetype2 -I/usr/local/include/python3.11 -c fitz/fitz_wrap.c -o build/temp.linux-x86_64-cpython-311/fitz/fitz_wrap.o
      fitz/fitz_wrap.c: In function ‘JM_get_page_labels’:
      fitz/fitz_wrap.c:4871:37: error: passing argument 3 of ‘fz_buffer_storage’ from incompatible pointer type [-Wincompatible-pointer-types]
       4871 |         fz_buffer_storage(ctx, res, &c);
            |                                     ^~
            |                                     |
            |                                     char **
      In file included from mupdf-1.20.0-source/include/mupdf/fitz/output.h:28,
                       from mupdf-1.20.0-source/include/mupdf/fitz.h:34,
                       from fitz/fitz_wrap.c:3288:
      mupdf-1.20.0-source/include/mupdf/fitz/buffer.h:72:75: note: expected ‘unsigned char **’ but argument is of type ‘char **’
         72 | size_t fz_buffer_storage(fz_context *ctx, fz_buffer *buf, unsigned char **datap);
            |                                                           ~~~~~~~~~~~~~~~~^~~~~
      fitz/fitz_wrap.c: In function ‘JM_get_fontbuffer’:
      fitz/fitz_wrap.c:5463:11: warning: variable ‘ext’ set but not used [-Wunused-but-set-variable]
       5463 |     char *ext = NULL;
            |           ^~~
      fitz/fitz_wrap.c: In function ‘JM_invert_pixmap_rect’:
      fitz/fitz_wrap.c:6025:19: warning: operation on ‘s’ may be undefined [-Wsequence-point]
       6025 |                 *s++ = 255 - *s;
            |                  ~^~
      fitz/fitz_wrap.c:6026:30: warning: value computed is not used [-Wunused-value]
       6026 |             if (dest->alpha) *s++;
            |                              ^~~~
      fitz/fitz_wrap.c: In function ‘JM_image_profile’:
      fitz/fitz_wrap.c:6065:11: warning: pointer targets in assignment from ‘char *’ to ‘unsigned char *’ differ in signedness [-Wpointer-sign]
       6065 |         c = PyBytes_AS_STRING(imagedata);
            |           ^
      fitz/fitz_wrap.c:6068:11: warning: pointer targets in assignment from ‘char *’ to ‘unsigned char *’ differ in signedness [-Wpointer-sign]
       6068 |         c = PyByteArray_AS_STRING(imagedata);
            |           ^
      fitz/fitz_wrap.c: In function ‘JM_color_count’:
      fitz/fitz_wrap.c:6309:55: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
       6309 |                     pixel = PyBytes_FromStringAndSize(oldpix, n);
            |                                                       ^~~~~~
            |                                                       |
            |                                                       unsigned char *
      In file included from /usr/local/include/python3.11/Python.h:50,
                       from fitz/fitz_wrap.c:203:
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c:6322:43: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
       6322 |         pixel = PyBytes_FromStringAndSize(oldpix, n);
            |                                           ^~~~~~
            |                                           |
            |                                           unsigned char *
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘JM_new_javascript’:
      fitz/fitz_wrap.c:6848:47: warning: pointer targets in passing argument 2 of ‘fz_new_buffer_from_copied_data’ differ in signedness [-Wpointer-sign]
       6848 |     res = fz_new_buffer_from_copied_data(ctx, data, strlen(data));
            |                                               ^~~~
            |                                               |
            |                                               char *
      mupdf-1.20.0-source/include/mupdf/fitz/buffer.h:105:81: note: expected ‘const unsigned char *’ but argument is of type ‘char *’
        105 | fz_buffer *fz_new_buffer_from_copied_data(fz_context *ctx, const unsigned char *data, size_t size);
            |                                                            ~~~~~~~~~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c: In function ‘JM_choice_options’:
      fitz/fitz_wrap.c:7180:19: warning: unused variable ‘pdf’ [-Wunused-variable]
       7180 |     pdf_document *pdf = pdf_get_bound_document(ctx, annot_obj);
            |                   ^~~
      fitz/fitz_wrap.c: In function ‘JM_get_widget_properties’:
      fitz/fitz_wrap.c:7251:16: warning: unused variable ‘res’ [-Wunused-variable]
       7251 |     fz_buffer *res = NULL;
            |                ^~~
      fitz/fitz_wrap.c:7250:39: warning: unused variable ‘o’ [-Wunused-variable]
       7250 |     pdf_obj *obj = NULL, *js = NULL, *o = NULL;
            |                                       ^
      fitz/fitz_wrap.c:7250:27: warning: unused variable ‘js’ [-Wunused-variable]
       7250 |     pdf_obj *obj = NULL, *js = NULL, *o = NULL;
            |                           ^~
      fitz/fitz_wrap.c: In function ‘JM_set_widget_properties’:
      fitz/fitz_wrap.c:7386:9: warning: variable ‘result’ set but not used [-Wunused-but-set-variable]
       7386 |     int result = 0;
            |         ^~~~~~
      fitz/fitz_wrap.c: In function ‘JM_embed_file’:
      fitz/fitz_wrap.c:7666:64: warning: pointer targets in passing argument 2 of ‘fz_new_buffer_from_copied_data’ differ in signedness [-Wpointer-sign]
       7666 |                            fz_new_buffer_from_copied_data(ctx, "  ", 1),
            |                                                                ^~~~
            |                                                                |
            |                                                                char *
      mupdf-1.20.0-source/include/mupdf/fitz/buffer.h:105:81: note: expected ‘const unsigned char *’ but argument is of type ‘char *’
        105 | fz_buffer *fz_new_buffer_from_copied_data(fz_context *ctx, const unsigned char *data, size_t size);
            |                                                            ~~~~~~~~~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c: In function ‘JM_append_rune’:
      fitz/fitz_wrap.c:8153:18: warning: suggest parentheses around ‘&&’ within ‘||’ [-Wparentheses]
       8153 |     if (ch >= 32 && ch <= 255 || ch == 10) {
            |         ~~~~~~~~~^~~~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘JM_set_ocg_arrays’:
      fitz/fitz_wrap.c:9521:40: warning: unused variable ‘indobj’ [-Wunused-variable]
       9521 |     pdf_obj *arr = NULL, *obj = NULL, *indobj = NULL;
            |                                        ^~~~~~
      fitz/fitz_wrap.c: In function ‘jm_append_merge’:
      fitz/fitz_wrap.c:10441:40: warning: suggest parentheses around ‘&&’ within ‘||’ [-Wparentheses]
      10441 |         if (strcmp(prevtype, "f") != 0 && strcmp(prevtype, "s") != 0
            |             ~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘JM_new_tracedraw_device’:
      fitz/fitz_wrap.c:10724:30: error: assignment to ‘void (*)(fz_context *, fz_device *, const fz_text *, fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10724 |         dev->super.fill_text = jm_increase_seqno;
            |                              ^
      fitz/fitz_wrap.c:10725:32: error: assignment to ‘void (*)(fz_context *, fz_device *, const fz_text *, const fz_stroke_state *, fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10725 |         dev->super.stroke_text = jm_increase_seqno;
            |                                ^
      fitz/fitz_wrap.c:10728:32: error: assignment to ‘void (*)(fz_context *, fz_device *, const fz_text *, fz_matrix)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10728 |         dev->super.ignore_text = jm_increase_seqno;
            |                                ^
      fitz/fitz_wrap.c:10730:31: error: assignment to ‘void (*)(fz_context *, fz_device *, fz_shade *, fz_matrix,  float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10730 |         dev->super.fill_shade = jm_increase_seqno;
            |                               ^
      fitz/fitz_wrap.c:10731:31: error: assignment to ‘void (*)(fz_context *, fz_device *, fz_image *, fz_matrix,  float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10731 |         dev->super.fill_image = jm_increase_seqno;
            |                               ^
      fitz/fitz_wrap.c:10732:36: error: assignment to ‘void (*)(fz_context *, fz_device *, fz_image *, fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10732 |         dev->super.fill_image_mask = jm_increase_seqno;
            |                                    ^
      fitz/fitz_wrap.c: In function ‘JM_new_tracetext_device’:
      fitz/fitz_wrap.c:10760:30: error: assignment to ‘void (*)(fz_context *, fz_device *, const fz_path *, int,  fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10760 |         dev->super.fill_path = jm_increase_seqno;
            |                              ^
      fitz/fitz_wrap.c:10771:31: error: assignment to ‘void (*)(fz_context *, fz_device *, fz_shade *, fz_matrix,  float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10771 |         dev->super.fill_shade = jm_increase_seqno;
            |                               ^
      fitz/fitz_wrap.c:10772:31: error: assignment to ‘void (*)(fz_context *, fz_device *, fz_image *, fz_matrix,  float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10772 |         dev->super.fill_image = jm_increase_seqno;
            |                               ^
      fitz/fitz_wrap.c:10773:36: error: assignment to ‘void (*)(fz_context *, fz_device *, fz_image *, fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, ...)’ [-Wincompatible-pointer-types]
      10773 |         dev->super.fill_image_mask = jm_increase_seqno;
            |                                    ^
      fitz/fitz_wrap.c: In function ‘JM_new_bbox_device’:
      fitz/fitz_wrap.c:10870:30: error: assignment to ‘void (*)(fz_context *, fz_device *, const fz_text *, fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, const fz_text *, fz_matrix, ...)’ [-Wincompatible-pointer-types]
      10870 |         dev->super.fill_text = jm_bbox_fill_text;
            |                              ^
      fitz/fitz_wrap.c:10871:32: error: assignment to ‘void (*)(fz_context *, fz_device *, const fz_text *, const fz_stroke_state *, fz_matrix,  fz_colorspace *, const float *, float,  fz_color_params)’ from incompatible pointer type ‘void (*)(fz_context *, fz_device *, const fz_text *, const fz_stroke_state *, fz_matrix, ...)’ [-Wincompatible-pointer-types]
      10871 |         dev->super.stroke_text = jm_bbox_stroke_text;
            |                                ^
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:10905:40: warning: ‘struct Document’ declared inside parameter list will not be visible outside of this definition or declaration
      10905 | SWIGINTERN void delete_Document(struct Document *self){
            |                                        ^~~~~~~~
      fitz/fitz_wrap.c: In function ‘Document_load_page’:
      fitz/fitz_wrap.c:11035:23: warning: unused variable ‘val’ [-Wunused-variable]
      11035 |             PyObject *val = NULL;
            |                       ^~~
      fitz/fitz_wrap.c: In function ‘Document__embfile_add’:
      fitz/fitz_wrap.c:11567:20: warning: variable ‘size’ set but not used [-Wunused-but-set-variable]
      11567 |             size_t size = 0;
            |                    ^~~~
      fitz/fitz_wrap.c:11566:17: warning: unused variable ‘entry’ [-Wunused-variable]
      11566 |             int entry = 0;
            |                 ^~~~~
      fitz/fitz_wrap.c: In function ‘Document_next_location’:
      fitz/fitz_wrap.c:11719:17: warning: unused variable ‘page_n’ [-Wunused-variable]
      11719 |             int page_n = -1;
            |                 ^~~~~~
      fitz/fitz_wrap.c: In function ‘Document__getPDFfileid’:
      fitz/fitz_wrap.c:11983:68: warning: pointer targets in passing argument 1 of ‘JM_UnicodeFromStr’ differ in signedness [-Wpointer-sign]
      11983 |                         LIST_APPEND_DROP(idlist, JM_UnicodeFromStr(hex));
            |                                                                    ^~~
            |                                                                    |
            |                                                                    unsigned char *
      fitz/fitz_wrap.c:4903:41: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
       4903 | PyObject *JM_UnicodeFromStr(const char *c)
            |                             ~~~~~~~~~~~~^
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:12090:194: warning: ‘struct Graftmap’ declared inside parameter list will not be visible outside of this definition or declaration
      12090 | SWIGINTERN PyObject *Document_insert_pdf(struct Document *self,struct Document *docsrc,int from_page,int to_page,int start_at,int rotate,int links,int annots,int show_progress,int final,struct Graftmap *_gmap){
            |                                                                                                                                                                                                  ^~~~~~~~
      fitz/fitz_wrap.c: In function ‘Document__get_char_widths’:
      fitz/fitz_wrap.c:12380:36: warning: unused variable ‘fb_font’ [-Wunused-variable]
      12380 |             fz_font *font = NULL, *fb_font= NULL;
            |                                    ^~~~~~~
      fitz/fitz_wrap.c:12377:17: warning: unused variable ‘lang’ [-Wunused-variable]
      12377 |             int lang = 0;
            |                 ^~~~
      fitz/fitz_wrap.c:12376:17: warning: unused variable ‘cwlen’ [-Wunused-variable]
      12376 |             int cwlen = 0;
            |                 ^~~~~
      fitz/fitz_wrap.c: In function ‘Document_extract_font’:
      fitz/fitz_wrap.c:12532:24: warning: unused variable ‘len’ [-Wunused-variable]
      12532 |             Py_ssize_t len = 0;
            |                        ^~~
      fitz/fitz_wrap.c: In function ‘Document_fullcopy_page’:
      fitz/fitz_wrap.c:13195:69: warning: pointer targets in passing argument 2 of ‘fz_new_buffer_from_copied_data’ differ in signedness [-Wpointer-sign]
      13195 |                                fz_new_buffer_from_copied_data(gctx, "  ", 1), NULL, 0);
            |                                                                     ^~~~
            |                                                                     |
            |                                                                     char *
      mupdf-1.20.0-source/include/mupdf/fitz/buffer.h:105:81: note: expected ‘const unsigned char *’ but argument is of type ‘char *’
        105 | fz_buffer *fz_new_buffer_from_copied_data(fz_context *ctx, const unsigned char *data, size_t size);
            |                                                            ~~~~~~~~~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c:13153:22: warning: unused variable ‘page2’ [-Wunused-variable]
      13153 |             pdf_obj *page2 = NULL;
            |                      ^~~~~
      fitz/fitz_wrap.c: In function ‘Document__move_copy_page’:
      fitz/fitz_wrap.c:13231:26: warning: unused variable ‘page2’ [-Wunused-variable]
      13231 |                 pdf_obj *page2 = pdf_lookup_page_loc(gctx, pdf, nb, &parent2, &i2);
            |                          ^~~~~
      fitz/fitz_wrap.c: In function ‘Document__get_page_labels’:
      fitz/fitz_wrap.c:13367:24: warning: unused variable ‘res’ [-Wunused-variable]
      13367 |             fz_buffer *res = NULL;
            |                        ^~~
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:13804:68: warning: ‘struct TextPage’ declared inside parameter list will not be visible outside of this definition or declaration
      13804 | SWIGINTERN PyObject *Page_extend_textpage(struct Page *self,struct TextPage *tpage,int flags,PyObject *matrix){
            |                                                                    ^~~~~~~~
      fitz/fitz_wrap.c: In function ‘Page_get_svg_image’:
      fitz/fitz_wrap.c:13882:29: warning: unused variable ‘seps’ [-Wunused-variable]
      13882 |             fz_separations *seps = NULL;
            |                             ^~~~
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:14470:104: warning: ‘struct Colorspace’ declared inside parameter list will not be visible outside of this definition or declaration
      14470 | SWIGINTERN struct Pixmap *Page__makePixmap(struct Page *self,struct Document *doc,PyObject *ctm,struct Colorspace *cs,int alpha,int annots,PyObject *clip){
            |                                                                                                        ^~~~~~~~~~
      fitz/fitz_wrap.c:14703:151: warning: ‘struct Graftmap’ declared inside parameter list will not be visible outside of this definition or declaration
      14703 | SWIGINTERN PyObject *Page__show_pdf_page(struct Page *self,struct Page *fz_srcpage,int overlay,PyObject *matrix,int xref,int oc,PyObject *clip,struct Graftmap *graftmap,char *_imgname){
            |                                                                                                                                                       ^~~~~~~~
      fitz/fitz_wrap.c: In function ‘Page__insert_image’:
      fitz/fitz_wrap.c:14813:52: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
      14813 |                 md5_py = PyBytes_FromStringAndSize(digest, 16);
            |                                                    ^~~~~~
            |                                                    |
            |                                                    unsigned char *
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c:14842:52: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
      14842 |                 md5_py = PyBytes_FromStringAndSize(digest, 16);
            |                                                    ^~~~~~
            |                                                    |
            |                                                    unsigned char *
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c:14862:13: warning: label ‘have_imask’ defined but not used [-Wunused-label]
      14862 |             have_imask:;
            |             ^~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘Page_get_contents’:
      fitz/fitz_wrap.c:14989:35: warning: comparison of integer expressions of different signedness: ‘int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
      14989 |                     for (i = 0; i < n; i++) {
            |                                   ^
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:15015:53: warning: ‘struct Colorspace’ declared inside parameter list will not be visible outside of this definition or declaration
      15015 | SWIGINTERN struct Pixmap *new_Pixmap__SWIG_0(struct Colorspace *cs,PyObject *bbox,int alpha){
            |                                                     ^~~~~~~~~~
      fitz/fitz_wrap.c:15025:53: warning: ‘struct Colorspace’ declared inside parameter list will not be visible outside of this definition or declaration
      15025 | SWIGINTERN struct Pixmap *new_Pixmap__SWIG_1(struct Colorspace *cs,struct Pixmap *spix){
            |                                                     ^~~~~~~~~~
      fitz/fitz_wrap.c:15130:53: warning: ‘struct Colorspace’ declared inside parameter list will not be visible outside of this definition or declaration
      15130 | SWIGINTERN struct Pixmap *new_Pixmap__SWIG_5(struct Colorspace *cs,int w,int h,PyObject *samples,int alpha){
            |                                                     ^~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘new_Pixmap__SWIG_5’:
      fitz/fitz_wrap.c:15144:32: warning: comparison of integer expressions of different signedness: ‘int’ and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
      15144 |                 if (stride * h != size) {
            |                                ^~
      fitz/fitz_wrap.c: In function ‘Pixmap_set_alpha’:
      fitz/fitz_wrap.c:15310:83: warning: comparison of integer expressions of different signedness: ‘Py_ssize_t’ {aka ‘long int’} and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
      15310 |                 if (opaque && PySequence_Check(opaque) && PySequence_Size(opaque) == n) {
            |                                                                                   ^~
      fitz/fitz_wrap.c:15318:80: warning: comparison of integer expressions of different signedness: ‘Py_ssize_t’ {aka ‘long int’} and ‘size_t’ {aka ‘long unsigned int’} [-Wsign-compare]
      15318 |                 if (matte && PySequence_Check(matte) && PySequence_Size(matte) == n) {
            |                                                                                ^~
      fitz/fitz_wrap.c: In function ‘Pixmap_digest’:
      fitz/fitz_wrap.c:15619:46: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
      15619 |             return PyBytes_FromStringAndSize(digest, 16);
            |                                              ^~~~~~
            |                                              |
            |                                              unsigned char *
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘Annot__update_appearance’:
      fitz/fitz_wrap.c:16330:21: warning: suggest parentheses around ‘&&’ within ‘||’ [-Wparentheses]
      16330 |                     && type != PDF_ANNOT_POLYGON
            |                     ^
      fitz/fitz_wrap.c: In function ‘Annot_update_file’:
      fitz/fitz_wrap.c:16607:21: warning: unused variable ‘size’ [-Wunused-variable]
      16607 |             int64_t size = 0;
            |                     ^~~~
      fitz/fitz_wrap.c:16604:19: warning: unused variable ‘data’ [-Wunused-variable]
      16604 |             char *data = NULL;              // for new file content
            |                   ^~~~
      fitz/fitz_wrap.c: In function ‘TextPage_extractIMGINFO’:
      fitz/fitz_wrap.c:17053:63: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
      17053 |                                     PyBytes_FromStringAndSize(digest, 16));
            |                                                               ^~~~~~
            |                                                               |
            |                                                               unsigned char *
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘TextPage_extractBLOCKS’:
      fitz/fitz_wrap.c:17088:31: warning: unused variable ‘last_y0’ [-Wunused-variable]
      17088 |                         float last_y0 = 0.0;
            |                               ^~~~~~~
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:17288:40: warning: ‘struct Graftmap’ declared inside parameter list will not be visible outside of this definition or declaration
      17288 | SWIGINTERN void delete_Graftmap(struct Graftmap *self){
            |                                        ^~~~~~~~
      fitz/fitz_wrap.c: In function ‘new_Graftmap’:
      fitz/fitz_wrap.c:17304:20: error: returning ‘pdf_graft_map *’ from a function with incompatible return type ‘struct Graftmap *’ [-Wincompatible-pointer-types]
      17304 |             return map;
            |                    ^~~
      fitz/fitz_wrap.c: At top level:
      fitz/fitz_wrap.c:17306:42: warning: ‘struct TextWriter’ declared inside parameter list will not be visible outside of this definition or declaration
      17306 | SWIGINTERN void delete_TextWriter(struct TextWriter *self){
            |                                          ^~~~~~~~~~
      fitz/fitz_wrap.c:17322:96: warning: ‘struct Font’ declared inside parameter list will not be visible outside of this definition or declaration
      17322 | SWIGINTERN PyObject *TextWriter_append(struct TextWriter *self,PyObject *pos,char *text,struct Font *font,float fontsize,char *language,int right_to_left,int small_caps){
            |                                                                                                ^~~~
      fitz/fitz_wrap.c:17392:36: warning: ‘struct Font’ declared inside parameter list will not be visible outside of this definition or declaration
      17392 | SWIGINTERN void delete_Font(struct Font *self){
            |                                    ^~~~
      fitz/fitz_wrap.c: In function ‘Font_buffer’:
      fitz/fitz_wrap.c:17578:39: warning: pointer targets in passing argument 1 of ‘PyBytes_FromStringAndSize’ differ in signedness [-Wpointer-sign]
      17578 |             return JM_BinFromCharSize(data, len);
            |                                       ^~~~
            |                                       |
            |                                       unsigned char *
      fitz/fitz_wrap.c:3286:60: note: in definition of macro ‘JM_BinFromCharSize’
       3286 | #define JM_BinFromCharSize(x, y) PyBytes_FromStringAndSize(x, (Py_ssize_t) y)
            |                                                            ^
      /usr/local/include/python3.11/bytesobject.h:34:50: note: expected ‘const char *’ but argument is of type ‘unsigned char *’
         34 | PyAPI_FUNC(PyObject *) PyBytes_FromStringAndSize(const char *, Py_ssize_t);
            |                                                  ^~~~~~~~~~~~
      fitz/fitz_wrap.c: In function ‘_wrap_delete_Document’:
      fitz/fitz_wrap.c:18206:19: error: passing argument 1 of ‘delete_Document’ from incompatible pointer type [-Wincompatible-pointer-types]
      18206 |   delete_Document(arg1);
            |                   ^~~~
            |                   |
            |                   struct Document *
      fitz/fitz_wrap.c:10905:50: note: expected ‘struct Document *’ but argument is of type ‘struct Document *’
      10905 | SWIGINTERN void delete_Document(struct Document *self){
            |                                 ~~~~~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c: In function ‘_wrap_Document_insert_pdf’:
      fitz/fitz_wrap.c:20210:97: error: passing argument 11 of ‘Document_insert_pdf’ from incompatible pointer type [-Wincompatible-pointer-types]
      20210 |     result = (PyObject *)Document_insert_pdf(arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11);
            |                                                                                                 ^~~~~
            |                                                                                                 |
            |                                                                                                 struct Graftmap *
      fitz/fitz_wrap.c:12090:204: note: expected ‘struct Graftmap *’ but argument is of type ‘struct Graftmap *’
      12090 | SWIGINTERN PyObject *Document_insert_pdf(struct Document *self,struct Document *docsrc,int from_page,int to_page,int start_at,int rotate,int links,int annots,int show_progress,int final,struct Graftmap *_gmap){
            |                                                                                                                                                                                           ~~~~~~~~~~~~~~~~~^~~~~
      fitz/fitz_wrap.c: In function ‘_wrap_Page_extend_textpage’:
      fitz/fitz_wrap.c:22593:52: error: passing argument 2 of ‘Page_extend_textpage’ from incompatible pointer type [-Wincompatible-pointer-types]
      22593 |     result = (PyObject *)Page_extend_textpage(arg1,arg2,arg3,arg4);
            |                                                    ^~~~
            |                                                    |
            |                                                    struct TextPage *
      fitz/fitz_wrap.c:13804:78: note: expected ‘struct TextPage *’ but argument is of type ‘struct TextPage *’
      13804 | SWIGINTERN PyObject *Page_extend_textpage(struct Page *self,struct TextPage *tpage,int flags,PyObject *matrix){
            |                                                             ~~~~~~~~~~~~~~~~~^~~~~
      fitz/fitz_wrap.c: In function ‘_wrap_Page__makePixmap’:
      fitz/fitz_wrap.c:23841:63: error: passing argument 4 of ‘Page__makePixmap’ from incompatible pointer type [-Wincompatible-pointer-types]
      23841 |     result = (struct Pixmap *)Page__makePixmap(arg1,arg2,arg3,arg4,arg5,arg6,arg7);
            |                                                               ^~~~
            |                                                               |
            |                                                               struct Colorspace *
      fitz/fitz_wrap.c:14470:116: note: expected ‘struct Colorspace *’ but argument is of type ‘struct Colorspace *’
      14470 | SWIGINTERN struct Pixmap *Page__makePixmap(struct Page *self,struct Document *doc,PyObject *ctm,struct Colorspace *cs,int alpha,int annots,PyObject *clip){
            |                                                                                                 ~~~~~~~~~~~~~~~~~~~^~
      fitz/fitz_wrap.c: In function ‘_wrap_Page__show_pdf_page’:
      fitz/fitz_wrap.c:24303:81: error: passing argument 8 of ‘Page__show_pdf_page’ from incompatible pointer type [-Wincompatible-pointer-types]
      24303 |     result = (PyObject *)Page__show_pdf_page(arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9);
            |                                                                                 ^~~~
            |                                                                                 |
            |                                                                                 struct Graftmap *
      fitz/fitz_wrap.c:14703:161: note: expected ‘struct Graftmap *’ but argument is of type ‘struct Graftmap *’
      14703 | SWIGINTERN PyObject *Page__show_pdf_page(struct Page *self,struct Page *fz_srcpage,int overlay,PyObject *matrix,int xref,int oc,PyObject *clip,struct Graftmap *graftmap,char *_imgname){
            |                                                                                                                                                ~~~~~~~~~~~~~~~~~^~~~~~~~
      fitz/fitz_wrap.c: In function ‘_wrap_new_Pixmap__SWIG_0’:
      fitz/fitz_wrap.c:24698:50: error: passing argument 1 of ‘new_Pixmap__SWIG_0’ from incompatible pointer type [-Wincompatible-pointer-types]
      24698 |     result = (struct Pixmap *)new_Pixmap__SWIG_0(arg1,arg2,arg3);
            |                                                  ^~~~
            |                                                  |
            |                                                  struct Colorspace *
      fitz/fitz_wrap.c:15015:65: note: expected ‘struct Colorspace *’ but argument is of type ‘struct Colorspace *’
      15015 | SWIGINTERN struct Pixmap *new_Pixmap__SWIG_0(struct Colorspace *cs,PyObject *bbox,int alpha){
            |                                              ~~~~~~~~~~~~~~~~~~~^~
      fitz/fitz_wrap.c: In function ‘_wrap_new_Pixmap__SWIG_1’:
      fitz/fitz_wrap.c:24733:50: error: passing argument 1 of ‘new_Pixmap__SWIG_1’ from incompatible pointer type [-Wincompatible-pointer-types]
      24733 |     result = (struct Pixmap *)new_Pixmap__SWIG_1(arg1,arg2);
            |                                                  ^~~~
            |                                                  |
            |                                                  struct Colorspace *
      fitz/fitz_wrap.c:15025:65: note: expected ‘struct Colorspace *’ but argument is of type ‘struct Colorspace *’
      15025 | SWIGINTERN struct Pixmap *new_Pixmap__SWIG_1(struct Colorspace *cs,struct Pixmap *spix){
            |                                              ~~~~~~~~~~~~~~~~~~~^~
      fitz/fitz_wrap.c: In function ‘_wrap_new_Pixmap__SWIG_5’:
      fitz/fitz_wrap.c:24907:50: error: passing argument 1 of ‘new_Pixmap__SWIG_5’ from incompatible pointer type [-Wincompatible-pointer-types]
      24907 |     result = (struct Pixmap *)new_Pixmap__SWIG_5(arg1,arg2,arg3,arg4,arg5);
            |                                                  ^~~~
            |                                                  |
            |                                                  struct Colorspace *
      fitz/fitz_wrap.c:15130:65: note: expected ‘struct Colorspace *’ but argument is of type ‘struct Colorspace *’
      15130 | SWIGINTERN struct Pixmap *new_Pixmap__SWIG_5(struct Colorspace *cs,int w,int h,PyObject *samples,int alpha){
            |                                              ~~~~~~~~~~~~~~~~~~~^~
      fitz/fitz_wrap.c: In function ‘_wrap_delete_Graftmap’:
      fitz/fitz_wrap.c:29434:19: error: passing argument 1 of ‘delete_Graftmap’ from incompatible pointer type [-Wincompatible-pointer-types]
      29434 |   delete_Graftmap(arg1);
            |                   ^~~~
            |                   |
            |                   struct Graftmap *
      fitz/fitz_wrap.c:17288:50: note: expected ‘struct Graftmap *’ but argument is of type ‘struct Graftmap *’
      17288 | SWIGINTERN void delete_Graftmap(struct Graftmap *self){
            |                                 ~~~~~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c: In function ‘_wrap_delete_TextWriter’:
      fitz/fitz_wrap.c:29497:21: error: passing argument 1 of ‘delete_TextWriter’ from incompatible pointer type [-Wincompatible-pointer-types]
      29497 |   delete_TextWriter(arg1);
            |                     ^~~~
            |                     |
            |                     struct TextWriter *
      fitz/fitz_wrap.c:17306:54: note: expected ‘struct TextWriter *’ but argument is of type ‘struct TextWriter *’
      17306 | SWIGINTERN void delete_TextWriter(struct TextWriter *self){
            |                                   ~~~~~~~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c: In function ‘_wrap_TextWriter_append’:
      fitz/fitz_wrap.c:29619:59: error: passing argument 4 of ‘TextWriter_append’ from incompatible pointer type [-Wincompatible-pointer-types]
      29619 |     result = (PyObject *)TextWriter_append(arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8);
            |                                                           ^~~~
            |                                                           |
            |                                                           struct Font *
      fitz/fitz_wrap.c:17322:102: note: expected ‘struct Font *’ but argument is of type ‘struct Font *’
      17322 | SWIGINTERN PyObject *TextWriter_append(struct TextWriter *self,PyObject *pos,char *text,struct Font *font,float fontsize,char *language,int right_to_left,int small_caps){
            |                                                                                         ~~~~~~~~~~~~~^~~~
      fitz/fitz_wrap.c: In function ‘_wrap_delete_Font’:
      fitz/fitz_wrap.c:29773:15: error: passing argument 1 of ‘delete_Font’ from incompatible pointer type [-Wincompatible-pointer-types]
      29773 |   delete_Font(arg1);
            |               ^~~~
            |               |
            |               struct Font *
      fitz/fitz_wrap.c:17392:42: note: expected ‘struct Font *’ but argument is of type ‘struct Font *’
      17392 | SWIGINTERN void delete_Font(struct Font *self){
            |                             ~~~~~~~~~~~~~^~~~
      error: command '/usr/bin/gcc' failed with exit code 1
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for PyMuPDF
  Running setup.py clean for PyMuPDF
Failed to build PyMuPDF
error: failed-wheel-build-for-install

× Failed to build installable wheels for some pyproject.toml based projects
╰─> PyMuPDF
root@955b42d34407:/app# PyMuPDF