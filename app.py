import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import gradio as gr


api_key = os.environ["GOOGLE_API_KEY"]

if not api_key:
  raise ValueError ("Chưa cấu hình GOOGLE_API_KEY!")

os.environ["GOOGLE_API_KEY"] = api_key

vectorstore_path = "vectorstore"

embeddings = HuggingFaceEmbeddings(
    model_name = "bkai-foundation-models/vietnamese-bi-encoder",
    model_kwargs = {"device" : "cpu"}
)

db = FAISS.load_local(
    vectorstore_path,
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = db.as_retriever(search_kwargs = {"k":4})


llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite",temperature = 0.1)

template = """
Bạn là một trợ lý luật sư AI chuyên nghiệp về Bảo mật, Dữ liệu và An ninh mạng. 
Hãy sử dụng ngữ cảnh pháp lý dưới đây để trả lời câu hỏi của người dùng một cách chính xác nhất.
Ngữ cảnh pháp lý:
{context}
Câu hỏi: {question}
Yêu cầu trả lời:
1. Nếu thông tin không có trong văn bản, hãy nói "Mình xin lỗi, thông tin này không nằm trong cơ sở dữ liệu của mình".
2. Trích dẫn cụ thể Điều/Khoản nếu có trong văn bản.
3. Trình bày rõ ràng, dễ hiểu.
Trả lời:
"""

prompts = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context" : retriever | format_docs, "question" : RunnablePassthrough()}
    |prompts
    |llm
    |StrOutputParser()
)

def predict(message,history):
    return rag_chain.invoke(message)


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