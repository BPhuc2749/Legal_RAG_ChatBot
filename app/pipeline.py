import os
import time
import unicodedata
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.prompt import TEMPLATE
from app.config import VECTORSTORE_PATH, EMBED_MODEL, TOP_K, LLM_MODEL, TEMPERATURE


class LegalRAGPipeline:
    def __init__(self):
        load_dotenv()

        self.debug_retrieval_enabled = os.getenv("DEBUG_RETRIEVAL", "0") == "1"

        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Chưa cấu hình GOOGLE_API_KEY!")
        os.environ["GOOGLE_API_KEY"] = api_key

        # 1) Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBED_MODEL,
            model_kwargs={"device": "cuda"},
        )

        # 2) Vectorstore
        self.db = FAISS.load_local(
            VECTORSTORE_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

        # 3) Retriever 
        self.retriever = self.db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": TOP_K, "fetch_k": 20, "lambda_mult": 0.8},
        )
        
        

        # 4) LLM
        self.llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=TEMPERATURE)

        # 5) Prompt + chain
        self.prompts = ChatPromptTemplate.from_template(TEMPLATE)
        self.rag_chain = self.prompts | self.llm | StrOutputParser()

    def normalize_text(self, text: str) -> str:
        return unicodedata.normalize("NFC", text).lower()

    def classify_source(self, filename: str) -> str:
        name = self.normalize_text(filename)
        if "luật" in name:
            return "LUAT"
        if "chính sách" in name:
            return "CHINHSACH"
        return "QUYDINH"

    def format_docs(self, docs) -> str:
        out = []
        for d in docs:
            meta = d.metadata or {}
            src = meta.get("source", "unknown")
            page = meta.get("page", "")
            src_type = self.classify_source(src)
            out.append(
                f"[SOURCE_TYPE: {src_type} | SOURCE: {src} | PAGE: {page}]\n{d.page_content}"
            )
        return "\n\n---\n\n".join(out)

    def debug_retrieval(self, question: str, preview_chars: int = 400):
        docs = self.retriever.invoke(question)
        print("\n" + "=" * 80)
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
        print("\n" + "=" * 80)
        return docs

    
    def retrieve(self, question: str):
        if self.debug_retrieval_enabled:
            return self.debug_retrieval(question)
        return self.retriever.invoke(question)

    def run(self, question: str, top_k: int | None = None) -> Dict[str, Any]:
        """
        Main pipeline:
        - retrieve docs
        - build context with citations header
        - call LLM
        - return answer + unique citations + latency
        """
        start = time.time()

        # optional override k 
        if top_k is not None:
            self.retriever.search_kwargs["k"] = int(top_k)

        # 1) Retrieve
        docs = self.retrieve(question)

        # 2) Build context for prompt (inline citations nằm trong context)
        context = self.format_docs(docs)

        # 3) Generate answer
        answer = self.rag_chain.invoke({"context": context, "question": question})

        latency = time.time() - start

        # 4) Build "sources tổng kết" (unique theo source+page, giữ thứ tự xuất hiện)
        contexts: List[Dict[str, Any]] = []
        seen = set()
        for d in docs:
            meta = d.metadata or {}
            src = meta.get("source", "unknown")
            page = meta.get("page", "")
            key = (src, page)
            if key in seen:
                continue
            seen.add(key)

            contexts.append(
                {
                    "source": src,
                    "page": page,
                    "source_type": self.classify_source(src),
                }
            )

        return {
            "question": question,
            "answer": answer,
            "contexts": contexts,  
            "latency": latency,
        }

