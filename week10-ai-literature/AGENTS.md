# AGENTS.md｜小魚的 AI 學術文獻查核 LLM Wiki

> 依 Andrej Karpathy 的 [LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 設計。目標是**可累積的知識庫**，不只是「上傳 PDF → 即時摘要」。進行任何改動前請閱讀此文件。

## 1. 專案主題與讀者

- 主題：「AI 輔助學術文獻查核——AI 給的論文引用，真的查得到嗎？」
- 對象：大學生與研究生，無須程式或 AI 研究背景。
- 使用繁體中文（臺灣用語）撰寫，技術名詞、模型名稱、指標與論文標題保留英文，如 RAG、Atomic Facts、FActScore、Citation Quality。
- 學習目標：查書目、查原文支持、標示待查核、重現資料驗證與修正流程。

## 2. 分層規則（不可混淆）

1. `raw/sources/`：原始來源的「可稽核摘錄與 metadata snapshot」，儘量不修改既有紀錄。來源新版本應留新檔。
2. `raw/papers/`：正式 PDF，來源必須是官方或作者公開的 PDF；尚未成功下載時不能寫成已下載。
3. `wiki/papers/`：每篇論文一頁，從原始資料整理出摘要、證據位置、限制、概念連結。
4. `wiki/concepts/`：跨論文的概念綜合頁，保留互聯關係。
5. `wiki/index.md`：知識導覽；`wiki/log.md`：append-only 操作紀錄。
6. `wiki/queries/`：從 Wiki 問題產出的可重用回答；HTML 簡報只能根據已存在的 Wiki 和有證據的 Query 產生。
7. `site/`：可直接瀏覽的靜態教學網站／Wiki／HTML 簡報。

**重要：** 本專案目前已 ingest 官方頁面 metadata 與摘要／方法證據筆記共五篇，**未成功下載或分析五篇全文 PDF**。PDF status 在 `raw/papers/README.md` 明示。不得宣稱已做全文查核。

## 3. 命名與內容契約

- 論文：`AuthorYYYY-ShortName.md`，例如 `Gao2023-ALCE.md`、`Dhuliawala2024-CoVe.md`。
- 名稱以**正式出版年份**優先；如預印本年份不同，另於 arXiv ID 和備註標示。不可把預印本年份和會議發表年份任意互換。
- 概念：英文小寫 kebab-case，例如 `claim-evidence.md`。
- 論文頁必填：題名、完整作者清單、正式發表年份、venue、DOI（若有）、arXiv（若有）、官方來源、證據章節、核心結論、使用限制、相互連結。
- 重要數學推導、Loss Function 或偽程式碼請以標準 LaTeX `$...$` 或 `$$...$$` 保留；不可自行補寫不存在的公式。FActScore 的教學簡化比例不得偽稱為論文完整公式。

## 4. Ingest 操作（每次新增資料重複）

1. 決定來源與教學用途，優先官方出版社、會議、學會、Crossref。
2. 擷取正式 title、authors、year、venue、DOI／arXiv 與摘要、方法證據位置。
3. **Pre-ingest Metadata Gate**：先檢查來源數量、命名、書目欄位、來源 ID 和最基本 evidence；不過關不得寫入 Wiki。
4. 將新來源筆記放 `raw/sources/`；若為 PDF，應放 `raw/papers/`，在網路允許時使用 `python scripts/download_pdfs.py`。
5. 執行 `python scripts/ingest.py` 建立／更新論文頁、概念頁與 index.md，並在 log.md 記錄。
6. 與原始來源對照，避免過度推論；新資料與舊資料矛盾時明確記錄並保留兩方。
7. 執行 `python scripts/lint.py`。

## 5. Query 操作

1. **先閱讀 `wiki/index.md`**，再讀該問題相關的論文頁、概念頁與已存查詢。
2. 將回答拆成 Atomic Facts，各自對應 Source ID／Section／Status。
3. 僅對 Supported 項目產出肯定句；Pending 項目要標「待查證」；Unsupported 項目不得輸出成既定事實。
4. 新的有價值比較或教學整理要寫入 `wiki/queries/`，並加回 index。
5. 教學簡報中的每個重點應能對到 Wiki 頁面，留下 Slide-to-Wiki Traceability。

## 6. Lint 與錯誤回饋 loop

檢查來源 ID、檔案漏讀、題名／作者／年份／DOI 混淆、跨頁矛盾、頁面孤兒、無證據數值與 Wiki 相對連結。錯誤退回：

- Metadata 未過：回到來源／Pre-ingest Gate，修正後再 Ingest。
- Claim 未有來源：回 Wiki Query 和原始證據，必要時標 Pending，不可強行生成。
- HTML 功能／可讀性有問題：回到 `scripts/build.py` 和 HTML 測試。

不可把「檢查測試刻意注入錯誤」寫成「AI 真實發生幻覺的統計」。

## 7. HTML 簡報規則

- 初學者教學順序：問題情境 → 學習目標 → 5 篇來源角色 → 3 層 Wiki 架構 → 查核步驟 → 互動練習 → graph/loop → 實際測試 → 反思與參考。
- 奶油白、鼠尾草綠，少量陶土橘；繁體中文，手機版可閱讀，按鈕可使用鍵盤。
- HTML 所引用的正式學術事實均能在 Wiki 來源找到，不可杜撰論文成果、數值或擴大研究結論。
- 可在不需後端或 API key 的靜態網站打開。互動題為本教室自編示例，非連線版即時 DOI 查詢。

## 8. 作業驗證與部署

```bash
python scripts/test_workflow.py
python scripts/ingest.py
python scripts/lint.py
python scripts/build.py
python scripts/browser_test.py
```

`site/index.html` 為入口，`site/wiki.html` 與 `site/slides.html` 為兩個交付成果。可上傳 GitHub Pages，但**部署成功與公開網址必須由實際驗證結果確認**。不要宣稱已部署，除非真有可開啟網址。