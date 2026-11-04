# 小魚的研究生工具小教室

把研究生活的小卡關，整理成一堂能動手做的小課。

本專案是第九週 1103 作業：建立自己的 `AGENTS.md`，讓 AI 理解網站的內容格式、視覺、檔案結構與擴充流程。以研究生常用的 Word、Excel 與簡報技巧為主題，提供 3 堂教學與 3 個互動示範。

## 網站

[開啟小魚的研究生工具小教室](https://selina-grad-toolbox-1103.shadyridge7.chatgpt.site/)

[GitHub 完整專案](https://github.com/yuyuhuang0718-lang/selina-grad-toolbox)

`content/site.json` 保存網站與 Repository 連結，作業說明見 SUBMISSION.md。

## 目前單元

| 單元 | 學習任務 | 練習工具 |
| --- | --- | --- |
| 讓 Word 幫你整理目錄 | 標題樣式、自動目錄與更新 | 標題層級與目錄預覽 |
| 把 Excel 資料整理乾淨 | 表格結構、空格、重複與缺漏 | 三欄 TSV 資料整理練習 |
| 讓簡報一眼看懂重點 | 主訊息、內容取捨與可讀性 | 一頁簡報內容預覽 |

共通功能包含搜尋與分類、可展開解答、選擇題與理由、自我檢核、瀏覽器學習進度、官方來源、前後課導覽與規則下載。

## 本機執行

需要 Python 3.10+，驗證另外需要 Node.js 18+。不需要安裝第三方套件。

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

在瀏覽器開啟 `http://localhost:8000/`。不要只以 `file://` 開啟 HTML，JavaScript 模組需要 HTTP 環境。

## 如何繼續新增內容

先讀 [AGENTS.md](AGENTS.md)，再依 [EXTENDING.md](docs/EXTENDING.md) 複製課程範本。只新增 `content/lessons/<slug>.json`，首頁卡片、課程頁、分類數量與前後導覽會一併產生。文字修改應從內容 JSON 開始，不直接改 dist。

```text
content/lessons/   正式課程
content/lesson-template.json   新課程範本
templates/        共用 HTML 骨架
assets/           共用樣式與互動
scripts/          建置及驗證
docs/             擴充方式及驗證結果
dist/             可部署的靜態網站
```

## GitHub 與 GitHub Pages

完整專案放在上方公開 Repository，根目錄可見 AGENTS.md、README.md、內容來源與可部署的 dist。

專案已包含 `.github/workflows/pages.yml`。推送到 main 時先驗證專案；目前公開網站沿用上方網址。若日後要啟用 GitHub Pages，先在 Settings → Pages 將來源選為 GitHub Actions，再於 Actions 手動執行工作流程並勾選 deploy_pages，流程才會部署 dist。未勾選時只執行檢查。

網站使用相對路徑，支援 GitHub Pages 的專案子路徑。部署狀態與網址必須由實際成功結果確認。

## 資料與內容

工具在瀏覽器本機執行；不會上傳或保存工具輸入。完成狀態存放 localStorage；停用儲存時降級為本頁記憶體狀態並提示限制。

資料整理示範以三欄完全相同判定重複，空值保留為空值，同 ID 的不同紀錄不會自動刪除。ASCII 空格處理對應 TRIM 的基本行為，不宣稱能移除所有 Unicode 空白。

工具操作依 Microsoft Support 官方說明整理；每課附來源及查閱日期。簡報的三段表達框架與情境為本教室自編教學。所有程式圖示為本專案自行繪製。課堂範例 [呆一布講義](https://diveai-lab.github.io/diveai-lessons/) 用作資訊架構參考。

## AI 協作與驗證

使用 AI 協助規劃、內容初稿、程式實作及驗證；繳交前請親自閱讀並試用，確認能說明 AGENTS.md 如何支持新增內容。實際檢查及限制見 [VERIFICATION.md](docs/VERIFICATION.md)。
