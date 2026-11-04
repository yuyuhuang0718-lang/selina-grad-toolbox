# 新增一堂小課

## 可直接交給 AI 的任務

> 請先閱讀 AGENTS.md，再新增一堂「Excel 樞紐分析表入門」。查閱 Microsoft 官方來源，以自己的話完成所有固定章節。使用尚未用過的 order，分類選 excel，demo.type 選 none；沿用原有視覺與模板，不修改既有課程的內容。完成後執行 python3 scripts/check.py，確認新頁面、首頁卡片、分類與前後課導覽皆會自動更新，並更新驗證紀錄。

## 檔案與操作

1. 複製 `content/lesson-template.json` 為 `content/lessons/excel-pivot-table.json`。
2. 將 slug 改成 `excel-pivot-table`；檔名必須與 slug 相同。
3. 讀官方教學並完成文字稿；替換範本中所有提示文字、測驗與示例來源。確認來源真正支持本課內容。
4. 保留必備欄位，填入查閱日期與內容查核日期；必要時把 order 改成新的未使用正整數。
5. 執行 `python3 scripts/build.py`，再執行 `python3 scripts/check.py`。
6. 瀏覽新課程並實際操作測驗；將確認結果寫入 `docs/VERIFICATION.md`。

不必手動加首頁卡片、改分類數量或編輯上一課與下一課。這些都由內容檔自動產生。

`none` 表示不加入專用工具；操作練習、解答、測驗與自我檢核仍會顯示。如果新課程確實需要新互動，才修改 JavaScript、驗證與 AGENTS.md。

## 本專案如何證明可以延伸

`scripts/check.py` 在暫存副本中新增一份 `extension-demo.json`，使用現有模板產生第 N+1 課，檢查新頁面、首頁卡片及雙向課程導覽。驗證後自動移除暫存副本；正式站保留真正撰寫的課程。

課堂「呆一布講義」為資訊架構參考；本專案自行設計課程資料契約、共用建置器、品牌與互動，不使用課堂吉祥物或圖像。
