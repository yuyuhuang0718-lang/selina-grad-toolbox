# 小魚的 AI 學術文獻查核 Wiki × 教學 HTML 簡報

**第十週 1110 作業｜主題：AI 輔助學術文獻查核**

教學標題：「**AI 給的論文引用，真的查得到嗎？**」

依 Andrej Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念建立 Markdown 知識庫（raw → wiki → schema），由五篇學術研究論文資料做來源，產生 15 張可操作 HTML 教學簡報。設計重點是 **Ingest → Query → Lint** 的可追溯 loop / graph，以及把 metadata 驗證提前到 Wiki 生成之前。

## 開啟成果

- `site/index.html`：教學入口首頁。
- `site/wiki.html`：互聯式 LLM Wiki，含五篇來源和六個概念。
- `site/slides.html`：15 張 HTML 簡報，含兩個互動題、鍵盤／按鈕翻頁及來源對照。

三份 HTML 都不需要 API key、Node modules 或網路服務；可直接以瀏覽器開啟。若有 Python，可在專案根目錄執行 `python -m http.server 8000 --directory site`，再開 `http://localhost:8000`。

## 工作流

```bash
python scripts/test_workflow.py    # 包含空來源和錯誤 DOI 的負向測試
python scripts/ingest.py           # preflight → Wiki Markdown 索引及概念頁
python scripts/lint.py             # 五篇來源、metadata、內部連結查核
python scripts/build.py            # 讀 Wiki 綜合內容 → HTML 網站和投影片
python scripts/browser_test.py     # Chromium UI 互動測試（如已安裝 playwright）
```

`browser_test.py` 需要 Python `playwright` 套件與 Chromium，其餘三個主要腳本使用 Python 標準函式庫即可。

## 專案檔案

```text
AGENTS.md                          Wiki 維護與作業規則
raw/sources/*.json                 五篇正式論文的 metadata 和可靠摘要筆記
raw/sources/CrossrefDocs-REST.md   輔助官方文件（非五篇之一）
raw/papers/README.md               PDF 下載狀態及規則
wiki/index.md                      知識導覽
wiki/log.md                        Ingest / Query / Lint 的可讀紀錄
wiki/papers/*.md                   五篇論文 Wiki 知識頁
wiki/concepts/*.md                 六張互聯概念頁
wiki/queries/slide-knowledge.md    從 Wiki 問答整理而成的教學大綱
site/*.html                        首頁、Wiki、HTML 投影片
scripts/metadata_rules.py          Pre-ingest Gate
scripts/ingest.py                  持續整合知識頁
scripts/lint.py                    驗證
scripts/build.py                   HTML 生成功能
scripts/browser_test.py            UI 實際測試
scripts/download_pdfs.py          在可連線環境補 PDF 的工具
docs/WORKFLOW.md                   Graph、loop 與重跑條件
docs/TRACEABILITY.md               Slide-to-Wiki 來源表
docs/BROWSER_TEST.md               真實 browser 結果
docs/REFLECTION.md                 真實錯誤與調整反思
docs/SUBMISSION.md                 作業區貼文
```

## 重要限制（請如實交代）

目前已由官方出版頁／會議頁查到五篇正式 metadata 與摘要重點，並存入 raw/sources，成功產生 5 張論文 Wiki 頁與 6 張概念頁；**網路隔離的執行環境無法下載 5 篇全文 PDF**，所以不宣稱已全文 ingest。若老師必須看到原始 PDF，請在可連線的電腦執行 `python scripts/download_pdfs.py` 補下載並逐篇閱讀。正確 DOI 的測試採官方頁已核對資料之**離線快照比對**，不是即時 Crossref API 調用。

## 發布成網頁

建議建立**獨立 GitHub Repository**，將此專案上傳；在 GitHub → Settings → Pages 啟用 GitHub Actions 或主分支 `/site` 發布方案（GitHub Pages 的目錄選項通常是 `/ (root)` 或 `/docs`，因此也可把 `site/` 內容複製到 `docs/` 再選 `/docs`）。發佈後需實際開啟公開網址確認，再填入 `docs/SUBMISSION.md`。**目前尚未部署，沒有可供任意公開訪客使用的實際網址。**