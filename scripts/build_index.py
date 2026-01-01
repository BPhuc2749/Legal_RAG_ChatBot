import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBED_MODEL, VECTORSTORE_PATH

DATA_DIR = Path("data/data_file")  

def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Không thấy folder: {DATA_DIR.resolve()}")

    print(f"Loading PDFs from: {DATA_DIR.resolve()}")
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    docs = loader.load()
    print(f"Loaded docs: {len(docs)}")

    print("Splitting...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1250,
        chunk_overlap=500,
        separators=["\n\n", "\n", ".", ";", " ", ""]
    )
    
    chunks = splitter.split_documents(docs)
    print(f"Chunks: {len(chunks)}")

    # Chuẩn hóa metadata source -> chỉ giữ tên file
    for d in chunks:
        src = d.metadata.get("source", "unknown")
        d.metadata["source"] = os.path.basename(src)

    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cuda"},
    )

    
    db = FAISS.from_documents(chunks, embeddings)

    out_dir = Path(VECTORSTORE_PATH)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving index to: {out_dir.resolve()}")
    db.save_local(str(out_dir))
    

if __name__ == "__main__":
    main()
