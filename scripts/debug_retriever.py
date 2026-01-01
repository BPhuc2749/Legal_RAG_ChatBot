from app.pipeline import LegalRAGPipeline

q = "Khi nào được xử lý dữ liệu cá nhân mà không cần sự đồng ý?"

rag = LegalRAGPipeline()

docs = rag.retriever.invoke(q)

print(f"Question: {q}")
print(f"Retrieved: {len(docs)} chunks\n")

for i, d in enumerate(docs, 1):
    meta = d.metadata or {}
    src = meta.get("source", "unknown")
    page = meta.get("page", "")
    text = d.page_content[:600].replace("\n", " ")
    print(f"--- #{i} | {src} | page {page} ---")
    print(text)
    print()

# python -m scripts.debug_retriever