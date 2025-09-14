import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredFileLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
    UnstructuredCSVLoader,
)
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

def load_documents_from_folder(folder_path: str):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(file_path)
            elif ext == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            elif ext == ".docx":
                loader = UnstructuredWordDocumentLoader(file_path)
            elif ext in [".xls", ".xlsx"]:
                loader = UnstructuredExcelLoader(file_path)
            elif ext in [".ppt", ".pptx"]:
                loader = UnstructuredPowerPointLoader(file_path)
            elif ext == ".html":
                loader = UnstructuredHTMLLoader(file_path)
            elif ext == ".csv":
                loader = UnstructuredCSVLoader(file_path)
            else:
                # Fallback generic loader
                loader = UnstructuredFileLoader(file_path)

            docs = loader.load()
            documents.extend(docs)
            print(f"Loaded {len(docs)} docs from {filename}")
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")

    return documents


if __name__ == "__main__":
    print("Ingesting data from folder-data/...")

    # 1. Load documents from folder
    documents = load_documents_from_folder("./folder-data")
    print(f"Loaded {len(documents)} documents")

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    texts = text_splitter.split_documents(documents)
    print(f"Created {len(texts)} chunks")

    # 3. Setup Pinecone
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    # 4. Embeddings + Push to Pinecone
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME_ALL_TYPES"]
    )

    print("✅ Ingestion complete!")