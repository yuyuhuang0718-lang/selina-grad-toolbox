# Wiki 來源索引（五篇正式研究論文）
> 本次 ingest 的是正式書目、摘要與方法筆記；目前並未匯入完整 PDF。每條資料保留正式來源與需注意的查核點。

## P01 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- Lewis et al., NeurIPS 2020
- https://arxiv.org/abs/2005.11401
- 正式論文：https://papers.nips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf
- 重點：參數化語言模型結合外部檢索的非參數化記憶；用於說明先查資料再生成。
- DOI：未在本作業資料中提供，不能捏造。

## P02 — Enabling Large Language Models to Generate Text with Citations
- Gao et al., EMNLP 2023
- https://aclanthology.org/2023.emnlp-main.398/
- DOI：https://doi.org/10.18653/v1/2023.emnlp-main.398
- 重點：引用品質不能只看是否有連結；必須檢查是否支持主張。

## P03 — FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation
- Min et al., EMNLP 2023
- https://aclanthology.org/2023.emnlp-main.741/
- DOI：https://doi.org/10.18653/v1/2023.emnlp-main.741
- 重點：把長篇敘述拆分成可查核的原子事實。

## P04 — Chain-of-Verification Reduces Hallucination in Large Language Models
- Dhuliawala et al., Findings of ACL 2024
- https://aclanthology.org/2024.findings-acl.212/
- DOI：https://doi.org/10.18653/v1/2024.findings-acl.212
- 重點：草稿 → 規劃驗證問題 → 獨立查核 → 產生修訂版。
- 注意：arXiv 首發為 2023 年；正式會議發表年份是 2024 年。

## P05 — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- Asai et al., ICLR 2024
- https://proceedings.iclr.cc/paper_files/paper/2024/hash/25f7be9694d7b32d5cc670927b8091e1-Abstract-Conference.html
- 重點：檢索、生成與自我評估之間的回饋。
- DOI：未在本作業資料中提供，不自行推測。

## 額外查核規則來源
- Crossref REST API 官方文件：https://www.crossref.org/documentation/retrieve-metadata/rest-api/
