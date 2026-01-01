import os
import unicodedata
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import gradio as gr
from dotenv import load_dotenv
from app.prompt import TEMPLATE
from app.config import VECTORSTORE_PATH, EMBED_MODEL, TOP_K, LLM_MODEL, TEMPERATURE


load_dotenv()

DEBUG_RETRIEVAL = os.getenv("DEBUG_RETRIEVAL", "0") == "1"

api_key = os.environ["GOOGLE_API_KEY"]

if not api_key:
  raise ValueError ("Chưa cấu hình GOOGLE_API_KEY!")

os.environ["GOOGLE_API_KEY"] = api_key

embeddings = HuggingFaceEmbeddings(
    model_name = EMBED_MODEL,
    model_kwargs = {"device" : "cuda"}
)

db = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# retriever = db.as_retriever(search_kwargs = {"k":TOP_K})
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": TOP_K, "fetch_k": 20, "lambda_mult": 0.5},
)


llm = ChatGoogleGenerativeAI(model = LLM_MODEL,temperature = TEMPERATURE)


prompts = ChatPromptTemplate.from_template(TEMPLATE)

# Hàm normalize_text để chuyển chữ tiếng việt in hoa thành chữ thường, đúng chuẩn tiếng việt

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text).lower()


# phân loại và gắn nhãn cho các nguồn (luật, chính sách, quy định)

def classify_source(filename: str) -> str:
    name = normalize_text(filename)
    if "luật" in name:
        return "LUAT"
    if "chính sách" in name:
        return "CHINHSACH"
    return "QUYDINH"


# Format lại các chunk theo  source type (LUAT,CHINHSACH,QUYDINH) | source | page /n page_content

def format_docs(docs):
    out = []
    for d in docs :
        meta = d.metadata or {}
        src = meta.get("source","unknown")
        page = meta.get("page","")
        src_type = classify_source(src)
        out.append(f"[SOURCE_TYPE: {src_type} | SOURCE: {src} | PAGE: {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(out)

# Để debug_retrieval xem các chunk được lấy làm ngữ cảnh 
def debug_retrieval(question: str, k: int = 3, preview_chars: int = 400):
    docs = retriever.invoke(question)
    print("\n" + "="*80)
    print(f"[RETRIEVAL DEBUG] Question: {question}")
    print(f"Top-{len(docs)} docs:")
    for i, d in enumerate(docs, 1):
        meta = getattr(d, "metadata", {}) or {}
        src = meta.get("source") or meta.get("file_path") or meta.get("filename") or "unknown"
        src = os.path.basename(src)
        page = meta.get("page", meta.get("page_number", ""))
        snippet = d.page_content[:preview_chars].replace("\n", " ")
        print(f"\n--- Doc #{i} | source={src} | page={page} ---")
        print(snippet)
    print("\n" + "="*80)
    return docs


rag_chain_manual = prompts | llm | StrOutputParser()

def predict(message, history):
    if DEBUG_RETRIEVAL:
        docs = debug_retrieval(message)
    else:
        docs = retriever.invoke(message)
    context = format_docs(docs)
    return rag_chain_manual.invoke({"context": context, "question": message})

demo = gr.ChatInterface(
    fn=predict,
    title = "Chatbot tư vấn Luật Công nghệ",
    description = "Hệ thống RAG tra cứu Luật an ninh mạng, Luật an toàn thông tin mạng, Bảo vệ dữ liệu cá nhân, Giao dịch điện tử, Quản lí thiết bị CNTT, Bảo mật dữ liệu",
    examples=[
        "Dữ liệu cá nhân nhạy cảm là gì?",
        "Dữ liệu cá nhân gồm những gì ?",
        "Quyền của chủ thể dữ liệu?"
    ]
)


if __name__ == "__main__":
    demo.launch()