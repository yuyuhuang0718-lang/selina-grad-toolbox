# AGENTS.md｜小魚的研究生工具小教室

這份文件是本專案的開發與內容規則。修改前先閱讀本檔、README.md 及目前的內容檔；以使用者當次要求為優先。一般新增課程可直接依本流程完成，不必每一步都再詢問。

## 1. 專案目的與讀者

為研究生與大學生製作繁體中文的工具入門教學，涵蓋 Word 文件整理、Excel 資料處理及 PowerPoint 簡報表達。每個單元都應幫讀者完成一件具體的小事。避免空泛的勵志文、廣告、未經核實的捷徑與虛構使用成果。

網站名稱固定為「小魚的研究生工具小教室」，英文輔助名稱為 SELINA’S STUDY LAB。語氣親切、清楚，先說目的，再解釋步驟；使用全形中文標點。

## 2. 技術與指令

- 靜態多頁網站：Python 標準函式庫產生 HTML，原生 CSS 與 JavaScript 提供互動。
- 不需要 npm 安裝、不使用 API key、後端或付費服務。
- Python 3.10+；JavaScript 驗證使用 Node.js 18+。
- 建置：`python3 scripts/build.py`。
- 驗證：`python3 scripts/check.py`，其中包含資料契約、內部連結、互動核心與新增第 N+1 課的測試。
- 本機閱讀：在一般開發環境執行 `python3 -m http.server 8000 --directory dist`，再開啟 `http://localhost:8000/`。
- 若在具專用預覽服務的環境，使用該服務，沿用其指定的網址與連接埠。

## 3. 目錄與單一內容來源

```text
AGENTS.md                     本文件
README.md                     執行、部署與專案說明
SUBMISSION.md                 作業繳交文字
content/
  site.json                   網站名稱、說明與實際連結
  lesson-template.json        新課程範本；不會被當成正式課程
  lessons/<slug>.json         每課唯一的正式內容來源
templates/page.html           全站 HTML 骨架
assets/site.css               共用視覺樣式
assets/site.js                搜尋、進度、測驗與工具的畫面行為
assets/tools.mjs              工具的純函式
assets/favicon.svg            原創圖示
scripts/build.py              驗證內容並產生靜態頁面
scripts/check.py              自動驗證
scripts/test-tools.mjs         互動核心的邊界測試
docs/EXTENDING.md              擴充範例與驗證方式
docs/VERIFICATION.md           實際檢查結果，不能預先宣稱通過
dist/                         產物；由建置自動產生
.github/workflows/pages.yml   GitHub Pages 建置與部署流程
```

課程的文字一律改 `content/lessons/*.json`；不要只改 `dist/`。建置會重新產生 `dist/`。新增課程不能要求人工同步首頁清單。

## 4. 命名與資料契約

檔名採英文小寫及連字號，例如 `word-table-of-contents.json`。檔名去掉副檔名後必須等於 `slug`。網址為 `lessons/<slug>/index.html`。

每個課程 JSON 必須具備下列欄位；禁止插入原始 HTML、script 或內嵌樣式：

| 欄位 | 格式與要求 |
| --- | --- |
| `slug` | 不重複；正則 `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` |
| `order` | 正整數、不可重複；決定首頁及前後課程順序 |
| `title` | 有實際任務的繁體中文標題 |
| `subtitle` | 一到兩句，交代學完能完成什麼 |
| `category` | `word`、`excel`、`slides` 或 `general` |
| `minutes` | 1–60 的整數；標示為預估學習時間 |
| `updated` | `YYYY-MM-DD`；內容最後查核日，不可填未來日期 |
| `goals` | 至少 2 個非空字串，使用可觀察的動作 |
| `intro` | 短段落，說明使用情境 |
| `concepts` | 至少 2 筆；每筆有 `term`、`explanation` |
| `steps` | 至少 3 筆；每筆有 `title`、`description` |
| `demo` | `type`、`title`、`description`；type 為 `outline`、`cleaner`、`storyboard`、`none` |
| `mistakes` | 至少 2 筆；每筆有 `wrong` 與 `better` |
| `practice` | `task`、`solution`；解答以可展開區塊呈現 |
| `quiz` | 至少 2 題；每題有 `question`、`choices`（2–4 個不重複選項）、`answer`（從 0 開始的正確選項索引）、`explanation` |
| `checklist` | 至少 3 個自我檢核項目 |
| `sources` | 至少 1 筆；每筆有 `title`、`url`（HTTPS）、`accessed`（YYYY-MM-DD） |

一般新課程用 `demo.type: "none"`，仍會有操作練習及測驗，不需要改 JavaScript。只有在新互動確實必要時才新增 type，並同步更新本文件、建置驗證、工具函式及畫面行為。

## 5. 每堂課固定章節

1. 課程標題、分類、預估時間、內容查核日。
2. 學習目標與使用情境。
3. 核心觀念。
4. 操作步驟。
5. 動手試試（有互動時顯示）及自己練習。
6. 常見誤解與修正方式。
7. 小測驗：作答後顯示對錯及理由，允許重新作答。
8. 自我檢核、學習完成按鈕及參考來源。

課程頁需保留回首頁、章節導覽與上一課／下一課。自我檢核全數勾選後，才可標示完成；讀者可取消完成。

## 6. 視覺規則

- 整體為奶油白與鼠尾草綠的閱讀筆記風，搭配少量陶土橘與柔和藍色。
- 核心色票：背景 `#f7f6f0`、紙白 `#fffefb`、文字 `#253d35`、綠色 `#476651`、次要文字 `#607168`、邊框 `#dce2d7`。
- Word 使用淡藍、Excel 使用淡綠、簡報使用淡橘；分類名稱需同時用文字表示。
- 共用字體優先系統繁體中文無襯線字型，不依賴外部字型服務。
- 桌面內容最大寬度 1160px；課程正文適合長文閱讀。手機 680px 以下使用單欄，表格可在容器內橫向捲動。
- 正文至少 16px，行高至少 1.7；按鈕可清楚聚焦，觸控高度至少 44px。
- 使用語意化標題、明確的表單標籤、跳到主要內容連結、可見的鍵盤焦點；尊重減少動態效果設定。
- 圖示使用自行繪製的 SVG／CSS。不要使用課堂品牌、吉祥物、他人照片或未授權素材。

## 7. 內容正確性與引用

- 工具功能與選單名稱需查官方文件，優先 Microsoft Support；標示介面可能因版本、平台或語言不同。
- 以自己的話整理。每課列出確實讀過的官方來源及查閱日期，不能只列搜尋首頁。
- 自編資料要明示是教學範例。不要放學號、面試經歷、真實研究資料或公司資料。
- Word 要說清楚：標題樣式、目錄與手動更新的關係。字體放大不等於套用標題樣式。
- Excel 要說清楚：保留原始資料、空值不等於 0、去重前先定義欄位。TRIM 以 ASCII 空格為對象，不能宣稱可去除所有 Unicode 空白。
- 簡報的「一頁一個主訊息」為本教室的編輯建議，不能宣稱為 Microsoft 的強制規則。可讀性、標題及輔助工具依官方來源說明。

## 8. 互動與資料規則

- 所有工具均在瀏覽器內操作，不上傳輸入資料；不加入分析追蹤、登入或廣告。
- 用 `textContent` 或建立 DOM 節點呈現使用者輸入，不把輸入直接放入 `innerHTML`。
- 顯示搜尋結果數、找不到結果時的提示與清除按鈕；分類與搜尋要能同時生效。
- 學習進度存在帶版本前綴的 localStorage。儲存不可用時改用記憶體，清楚說明無法跨頁保留；網站其他功能仍可用。
- 只保存完成課程的 slug；不保存工具輸入。重設進度必須有使用者的明確按鈕操作。
- 資料整理示範僅接受三欄 TSV（ID、名稱、分數），最多 100 筆。先清理 ASCII 空格，再以三欄完全相同判斷重複；同 ID 不同資料要保留並提示，空值維持空值。
- 大綱示範僅展示標題層級如何形成目錄，不模擬 Word 排版或真實頁碼。
- 簡報工具為自編三段表達練習，不做自動評分或虛構成效承諾。

## 9. 新增課程的標準流程

1. 讀本文件與相近課程；確認本課要解決的任務。
2. 查閱官方來源，先完成內容稿。
3. 複製 `content/lesson-template.json` 到 `content/lessons/<slug>.json`。
4. 填完所有欄位；選取未使用的 order；預設 demo.type 為 none。
5. 執行建置及驗證。新課程、首頁卡片、篩選數量與前後課程應自動更新。
6. 如有新互動，測試正常輸入、空白輸入、邊界、鍵盤操作及手機閱讀。
7. 更新 docs/VERIFICATION.md，記錄實際做過的檢查，不可寫尚未執行的成功結果。
8. 更新 README 的課程清單及相關說明；已授權的部署與上傳可依任務要求完成。

## 10. 交付與部署

- GitHub 根目錄必須能看到 AGENTS.md、README.md 及完整來源，不能只放 ZIP。
- `.github/workflows/pages.yml` 在推送 main 時建置並驗證；GitHub Pages 為選用發布方式。先在 Settings → Pages 選 GitHub Actions，再手動執行流程並勾選 deploy_pages，才部署 dist。網址必須以實際部署結果為準。
- 全站使用相對路徑，支援 GitHub Pages 的專案子路徑。
- 公開部署前確認使用者要求的網站存取範圍；公開教學只放範例資料。
- 不提交密碼、token、.git、暫存截圖或個人帳號快取。
- SUBMISSION.md 要誠實區分完成與未完成，不得把預測 GitHub 網址寫成已上傳。

## 11. 完成標準

- 首頁、所有課程頁及專案規則頁皆可閱讀，內部連結正確。
- 搜尋、分類、測驗、練習及完成狀態能操作；localStorage 失效不讓頁面崩潰。
- 只新增一份課程 JSON，即可產生第 N+1 課、首頁卡片及前後導覽；測試用課程只在暫存副本，不留在正式站。
- 通過 `python3 scripts/check.py`。實際瀏覽器驗證與未驗證項目應分開記錄。
- 如受登入或服務限制，完成可完成的檔案、網站與驗證，清楚指出剩下哪一步。
