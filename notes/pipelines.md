# LEGAL CHATBOT

## Inputs
- PDFs location: data/data_file (7 PDF luật)
- Vectorstore location: vectorstore/faiss (index.faiss + index.pkl)
- User question: câu hỏi tiếng Việt từ user

## Steps
1) Load PDF: chạy khi build index (PyPDFLoader, DirectoryLoader)
2) Chunking: RecursiveCharacterTextSplitter (chunk_size=1200, overlap=250,separators = ["\n",'.',';','',' '])
3) Embedding: bkai-foundation-models/vietnamese-bi-encoder (GPU local khi encode kết hợp hf_token)
4) Vectorstore: FAISS save_local/load_local ở vectorstore/faiss
5) Retrieval: as_retriever(top-k=3)
6) Prompt: nhét {context} + {question}, yêu cầu trả theo điều/khoản và không bịa
7) LLM: Gemini (gemini-2.5-flash-lite), temperature=0.1, max-tokens = None, max_retries = 2, timeout = None
8) Output: plain text (chưa show citations)

## Debug checklist
- In ra top-k retrieved chunks để xem có đúng luật không
- Nếu đúng chunk mà trả sai → sửa prompt
- Nếu sai chunk → sửa chunking/k hoặc rebuild index