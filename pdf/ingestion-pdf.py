import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

if __name__ == "__main__":
    print("ingesting data...")
    
    # load pdf document
    loader = PyPDFLoader("./pdfdata/ctms-postman-collections-documentation-all.pdf")
    document = loader.load()
    
    # split entire documents into chunks  
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", ".", " ", ""])
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    # load pinecone
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    # create vector embeddings and save it in pinecone database
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.environ["OPENAI_API_KEY"])
    PineconeVectorStore.from_documents(texts, embeddings, index_name=os.environ["INDEX_NAME_PDF"])