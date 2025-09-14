import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Use same embedding model as ingestion
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Load Pinecone vector store
vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME_PDF"], embedding=embeddings
)

# Chat model
chat = ChatOpenAI(verbose=True, temperature=0, model_name="gpt-3.5-turbo")

qa = RetrievalQA.from_chain_type(
    llm=chat, chain_type="stuff", retriever=vectorstore.as_retriever()
)    

# Stateless queries
queries = [
    "What are the various API endpoints provided by MediaCentral CTMS Registry?",
    "How can I get started with these postman collections?",
    "How to set a thumbnail for my asset in CloudUX? What API should I hit, what are the different precautions I need to take?",
    "What should be the expected response for the above request?"
]

for q in queries:
    res = qa.invoke(q)
    print(f"\nQ: {q}\nA: {res['result']}\n")

