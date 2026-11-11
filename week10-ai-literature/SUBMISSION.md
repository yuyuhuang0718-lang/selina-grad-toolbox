# 第十週作業｜AI 輔助學術文獻查核
**繳交標題：北科大 114378003 工管碩二 黃芊瑜 AI 輔助學術文獻查核**

## 1. LLM Wiki 主題
本次主題為「AI 輔助學術文獻查核」，教學題目是「AI 給的論文引用，真的查得到嗎？」參考 Karpathy 的 LLM Wiki 知識維護模式，先規劃 AGENTS.md、Wiki 架構與來源規則，再以 ingest / query / lint 迭代。重點是判斷 AI 引用是否真實、DOI 與書目是否吻合、以及論文是否支持引用的主張。

## 2. LLM Wiki 成果
- 原始專案： https://github.com/yuyuhuang0718-lang/selina-grad-toolbox/tree/main/week10-ai-literature
- HTML Wiki 原始檔： https://yuyuhuang0718-lang.github.io/selina-grad-toolbox/week10-ai-literature/wiki.html
- GitHub Pages 建置／部署成功（2026-11-11），網址如下；請以瀏覽器開啟確認。

已整理五篇正式文獻：Lewis et al. (2020) RAG、Gao et al. (2023) ALCE、Min et al. (2023) FActScore、Dhuliawala et al. (2024) CoVe、Asai et al. (2024) Self-RAG。來源涵蓋正式書目、摘要與方法筆記，延伸為六張核心概念頁。Crossref 官方資料用於 DOI 規則參考。尚未匯入完整 PDF，未宣稱完成逐頁全文核對。

## 3. 教學 HTML 簡報
- HTML 簡報原始檔： https://yuyuhuang0718-lang.github.io/selina-grad-toolbox/week10-ai-literature/slides.html
- GitHub Pages 建置／部署成功（2026-11-11），網址如下；請以瀏覽器開啟確認。

共 15 張 HTML 教學投影片，按照「問題 → DOI 與書目 → 引用主張與原文證據 → Wiki 流程 → 互動查核 → 結論」由淺入深設計。內含 DOI 和 Claim-Evidence 互動題，並以投影片與 Wiki 主題對照說明可追溯性。

## 4. Loop / Graph
官方來源 → Pre-ingest Metadata Gate → Ingest → Wiki → Query → Claim-Evidence Lint → HTML 簡報 → Browser Test。

檢查不合格時，metadata/來源數量返回原始來源；主張缺乏足夠證據就重新 Query 或標示 Pending；HTML 互動與版面異常則返回簡報程式修正。越早攔截錯誤，越能避免錯誤在後續內容擴散。

## 5. 實際執行與測試
第一版 Ingest 使用 P*.json 搜尋，實際檔名不符合，造成 0/5 篇未讀入。改成 *.json 並檢查輸入數量，重新匯入 5/5 篇。另設計錯誤 DOI 10.9999/fictional-alce 作負向測試，成功被 Metadata Gate 拒絕，與 ALCE DOI 10.18653/v1/2023.emnlp-main.398 不一致。此前執行紀錄指出 21/21 項瀏覽器測試通過，包括搜尋、篩選、鍵盤翻頁、互動題與手機顯示。

## 6. 反思
最容易出問題的節點是 Ingest 前的來源掃描與書目資料。原本只在後段 Lint 查錯，後來新增 Pre-ingest Metadata Gate，提前檢查輸入筆數、檔名、ID、題名、年份、DOI。若失敗就停止，不讓錯誤來源進入 Wiki。這讓 Graph 從單向「輸入→輸出」變為具有可追溯、可重試回路的知識管理流程。

**補充：** 目前 PDF 全文未完成 ingest。GitHub Pages 工作流程已回報成功，未能從本執行環境直接以 HTTP 檢查頁面，正式繳交前請自行開啟以上兩個網址確認畫面。
