# Wiki → HTML 教學簡報對照與檢查
這份對照表用以說明簡報不是無來源生成。正式來源 ID 以 SOURCE_INDEX.md 為準。

| 教學主題／投影片（教學順序） | Wiki 概念 | 文獻依據 |
|---|---|---|
| AI 引用為什麼需要查核 | citation quality | P02 ALCE |
| RAG 與來源檢索 | retrieval | P01 RAG、P05 Self-RAG |
| 論文題名、作者、年份、DOI | metadata | P02–P04 正式 DOI 與出版資訊 |
| 引用能否支持敘述 | claim-evidence | P02 ALCE |
| 拆解複合主張 | atomic facts | P03 FActScore |
| 分階段驗證 | verification loop | P04 CoVe、P05 Self-RAG |
| 預先檢查、失敗退回 | workflow | 由本作業實驗設計，非論文原有的完整系統 |
| DOI 選擇互動題 | metadata | P02 正式 DOI |
| 99% 泛化主張的查核題 | claim-evidence | 本作業自編負向測試，不是論文實驗結果 |

## 真實執行紀錄與侷限
- 第一版以 P*.json 匹配來源，檔名不符，發現 0/5 篇匯入。
- 改為匹配 *.json 後正常讀入 5/5 篇。
- 在 ingest 前加入 Metadata Gate，拒絕人工注入的錯誤 DOI 10.9999/fictional-alce。
- 此前實作紀錄：21/21 項瀏覽器互動測試通過；測試的是互動與響應式版面，不等於五篇全文逐段核對。
- 限制：全文 PDF 尚未 ingest；網站是否完成公開部署需另行確認。
