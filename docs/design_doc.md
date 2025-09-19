# 本地开源方案：Linux + vLLM API（韩文 PDF 幻灯片 → 英文并保留版式）

> 目标：在**Linux 环境**下，利用**本地大模型（通过 vLLM 提供 OpenAI API 接口）**，实现韩文 PDF 幻灯片文本自动翻译为英文，**仅替换文字**，其余（图片、字体、排版、颜色、图表）保持不变。全程本地离线，禁止联网。

---

## 1. 核心要求

* **输入**：韩文 PDF 幻灯片（几十页）。
* **输出**：英文 PDF（排版、图表、图片、字体尽量保持不变）。
* **限制条件**：

  * 环境为 Linux。
  * 翻译模型通过 vLLM 暴露 OpenAI API 接口（兼容 `ChatCompletion` / `Completion` 格式）。
  * 禁止调用任何联网 API（如 Google、DeepL、外部 HuggingFace Hub 等）。
  * 仅替换韩文文字 → 英文；所有非文本元素保持原样。

---

## 2. 总体设计

### 流水线步骤

1. **OCR & 文本解析**

   * 使用 `ocrmypdf`（kor+eng 语言包）确保 PDF 内所有韩文文字都可被提取。
   * 使用 `PyMuPDF (fitz)` 或 `pdfminer.six` 提取每个文字块：内容、坐标、字体、字号、对齐方式。

2. **翻译调用（本地模型 via vLLM）**

   * 批量收集韩文文本段落。
   * 调用本地 vLLM API（OpenAI 接口格式）进行翻译：`source=ko → target=en`。
   * 使用缓存（hash → translation）避免重复翻译。

3. **文本替换 & 排版保持**

   * 两种策略：

     * **方案 A（推荐）**：将 PDF 转换为 PPTX/DOCX → 使用 `python-pptx` / `python-docx` 替换文字 → 导出 PDF。
     * **方案 B（高保真覆盖层）**：保持原 PDF 不变 → 新建透明图层，将英文翻译文本绘制在原文字 bbox 上 → 合并生成新 PDF。

4. **导出 PDF**

   * A 方案：用 LibreOffice (`soffice --headless`) 从 PPTX/DOCX 导出 PDF。
   * B 方案：用 `reportlab` / `pikepdf` 合成覆盖层与原始 PDF。

---

## 3. 模块与工具

* **解析**：`ocrmypdf`, `PyMuPDF`, `pdfminer.six`
* **转换**：`pdf2docx`, `LibreOffice`
* **编辑**：`python-docx`, `python-pptx`
* **翻译**：vLLM (本地 API, OpenAI 格式)
* **输出**：`LibreOffice`, `reportlab`, `pikepdf`

---

## 4. 翻译 API 调用示例（vLLM 本地）

```python
import openai

openai.api_base = "http://localhost:8000/v1"  # vLLM 部署地址
openai.api_key = "EMPTY"  # 本地无需鉴权

resp = openai.ChatCompletion.create(
    model="qwen2.5-7b-instruct",  # 已在 vLLM 中加载
    messages=[
        {"role": "system", "content": "You are a translator. Translate Korean into English. Preserve formatting."},
        {"role": "user", "content": "한글 텍스트 예시"}
    ],
    temperature=0,
)
print(resp["choices"][0]["message"]["content"])
```

* **批量处理**：

  * 将文本块分组，每组长度 ≤ 1024 tokens。
  * 使用翻译缓存：同样文本不重复请求。

---

## 5. Pipeline A（可编辑文件替换）

1. `ocrmypdf input.pdf ocr.pdf --language kor+eng`
2. `soffice --headless --convert-to pptx ocr.pdf`
3. 遍历 PPTX 内所有 `shape.text_frame.paragraphs.runs`，用翻译替换 run.text。
4. `soffice --headless --convert-to pdf slides_translated.pptx`

**优点**：保持幻灯片结构；适合演示文稿。
**风险**：复杂排版可能有少量跑版。

---

## 6. Pipeline B（覆盖层叠加）

1. 用 `PyMuPDF` 提取所有文字块的坐标 bbox。
2. 翻译后，使用 `reportlab` 在同位置绘制英文文本。
3. 用 `pikepdf` 将覆盖层 PDF 合并到原 PDF。

**优点**：原版式、图表、字体完全保留。
**风险**：换行/字距需要手工控制，复杂度高。

---

## 7. 字体与版式保持

* 使用 Noto Sans / Noto Serif 英文字体，保证跨平台一致性。
* 如果 B 方案，需测量英文文本宽度，确保不会溢出 bbox。
* 保持字号比例（必要时缩小 ≤10%）。

---

## 8. 目录结构建议

```
project/
  configs/
    config.yaml
  data/
    input.pdf
    working/
      slides.pptx
  outputs/
    translated.pdf
  scripts/
    pipeline_a.py
    pipeline_b.py
    translate_api.py
  cache/
    translations.json
  glossary/
    terms.csv
```

---

## 9. 配置文件样例

```yaml
pipeline: A            # A=可编辑文件替换; B=覆盖层
input_pdf: data/input.pdf
output_pdf: outputs/translated.pdf

ocr:
  enabled: true
  lang: kor+eng

translate:
  api_base: http://localhost:8000/v1
  model: qwen2.5-7b-instruct
  batch_size: 10
  cache: cache/translations.json

layout:
  overflow_shrink_pct: 10
  font: Noto Sans
```

---

## 10. 验收标准

* 所有韩文文本均有英文替代。
* 图片、图表、颜色、字体样式保持不变。
* 页数与对象数一致。
* 无漏译、乱码、跑版严重情况。

---

## 11. 推荐实践

* 先跑 **Pipeline A**，快速生成译稿。
* 对跑版严重的页，切换 **Pipeline B** 单独处理。
* 翻译时启用 **术语保护**（占位符 → 回填）。
* 输出时生成 **双份文件**：纯英文版 + 中英对照版（可审校）。


# 设计文档·补遗（面向编码实现 | 简洁版）

## A. OpenAI-like API 对接约定

* 运行时通过 **配置/环境变量**注入，不在代码硬编码：

  * `translate.api_base`（例：`http://127.0.0.1:8000/v1`）
  * `translate.api_key`（例：`ENV OPENAI_API_KEY`；本地可用任意占位）
  * `translate.model`（例：`qwen2.5-7b-instruct`）
* 统一走 `chat.completions`；`temperature=0.0`；`max_tokens` 动态估算（与输入长度成比例）；
* 失败重试 2 次，指数退避；启用**去重缓存**（文本 SHA1 → 译文）。

**最小调用（示意）**

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url=os.environ["OPENAI_API_BASE"],     # 由你提供
    api_key=os.environ.get("OPENAI_API_KEY","EMPTY")
)

def translate_batch(batch: list[str], model: str) -> list[str]:
    SEP = "\n<<<SEG>>>\n"
    msg = [
        {"role":"system","content":"You are a professional translator (Korean → English). Keep meaning, numbers, units, figure/table refs. Output English only."},
        {"role":"user","content": SEP.join(batch)}
    ]
    r = client.chat.completions.create(model=model, messages=msg, temperature=0.0)
    text = r.choices[0].message.content
    parts = [p.strip() for p in text.split(SEP)]
    # 兜底对齐：如返回段数不匹配，按行数/标点再切
    if len(parts) != len(batch):
        parts = text.splitlines()[:len(batch)]
    return parts
```

## B. “仅翻译韩文”的判定与替换

* **检测规则**：字符串中包含任意 **Hangul** 字符即视为韩文（Unicode 正则 `[\p{Hangul}]`）。
* **遍历粒度**：

  * **Pipeline A（默认）**：PPTX/DOCX 中按 `shape → paragraph → run` 级遍历；只对 `has_korean(run.text)` 的 run 做**原位替换**；保留字体、字号、颜色、对齐等样式属性。
  * **Pipeline B（单页降级）**：PDF 文本 span + bbox；仅对含韩文的 span 生成英文覆盖层（ReportLab），坐标/字号/对齐匹配，合并到原 PDF（pikepdf）。
* **保留不变**：图片、图表、矢量、背景、色板、页眉页脚、布局网格；不移动对象、不改尺寸。

## C. 分段、缓存、术语

* **分段策略**：句号/换行/项目符号边界；控制每批 tokens（避免超长）；
* **缓存**：对**去样式纯文本**做 SHA1，命中直接返回译文；
* **术语保护**：翻译前用占位符保护专名/术语（CSV：`src,tgt,regex,case_sensitive`），翻译后回填；保持大小写与单复数一致。

## D. 排版与溢出控制

* **A 方案**：替换后若 run 溢出文本框：

  * 微缩字号 ≤ `overflow_shrink_pct`（默认 10%）；
  * 或按空白优先断行；**禁止**改变图片/图表尺寸与位置。
* **B 方案**：渲染前测量字符串宽度；必要时同样微缩字号或软换行；默认**不遮挡原文**，若重影明显，仅在文字 bbox 内画极薄白底（不盖住图片/图表）。

## E. 配置片段（给 Codex）

```yaml
pipeline: A                      # A=可编辑替换；B=覆盖层；auto=失败页切换B
input_pdf: data/input.pdf
output_pdf: outputs/translated.pdf

ocr:
  enabled: true                  # 扫描件先 ocrmypdf kor+eng
  lang: kor+eng
  dpi: 300

translate:
  api_base: ${OPENAI_API_BASE}
  api_key: ${OPENAI_API_KEY}
  model: ${OPENAI_API_MODEL}
  batch_size: 8
  sep: "<<<SEG>>>"
  cache: cache/translations.json
  timeout_sec: 120
  retries: 2

layout:
  overflow_shrink_pct: 10
  font_fallbacks: ["Noto Sans CJK KR", "Noto Sans"]

terms:
  glossary: glossary/terms.csv
  protect_proper_nouns: true
```

## F. 编码清单（Checklist）

* [ ] 仅遍历/替换**含韩文**的 run/span；无韩文不动。
* [ ] 分批 + 分隔符对齐；启用缓存；失败重试。
* [ ] 术语占位保护→翻译→回填；数字/单位/图表编号原样保留。
* [ ] A 方案默认；对跑版页切 B（单页）。
* [ ] 导出：英文版 `translated.pdf`；（可选）`bilingual.pdf` 供审校。
* [ ] QA：页数/对象计数一致；随机 10% 页人工抽检无重叠/漏译；术语一致率 ≥ 98%。

## G. 误差/降级处理

* 翻译 API 失败 → 重试→缓存→记录“待人工”占位（不破坏版式）；
* A 方案严重跑版 → 页面级切 B；
* OCR 质量差 → 提升 DPI/去噪/矫正后重跑；必要页人工圈选补 OCR。

