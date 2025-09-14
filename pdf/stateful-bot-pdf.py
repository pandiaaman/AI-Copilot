import os
import warnings
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate

warnings.filterwarnings("ignore")

load_dotenv()

chat_history = []

if __name__ == "__main__":

    prompt_template = """
    You are an expert assistant for MediaCentral CTMS Registry documentation. 
    Always provide complete, detailed, step-by-step explanations in your answers. 
    If the question is about API endpoints, list all endpoints with their details. 
    If the question is about how to use an API, provide examples and precautions.

    Explain the API in detail with the following structure:
    1. Purpose
    2. Endpoint
    3. Required Parameters
    4. Example Request
    5. Example Response
    6. Precautions or best practices

    Question: {question}
    Context: {summaries}

    Answer in detail:
    """

    prompt = PromptTemplate(
        input_variables=["summaries", "question"],
        template=prompt_template,
    )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.environ["OPENAI_API_KEY"])
    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME_PDF"], embedding=embeddings
    )

    chat = ChatOpenAI(verbose=True, temperature=0.4, model_name="gpt-3.5-turbo", openai_api_key=os.environ["OPENAI_API_KEY"])

    retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, 
        chain_type="map_reduce", 
        retriever=retriever, 
        return_source_documents=True, 
        combine_docs_chain_kwargs={
            "combine_prompt": prompt
        }
    )  

    queries = [
    "What are the various API endpoints provided by MediaCentral CTMS Registry?",
    "How can I get started with these postman collections?",
    "How to set a thumbnail for my asset in CloudUX? What API should I hit, what are the different precautions I need to take?",
    "What should be the expected response for the above request?"
]

for q in queries:
    res = qa({"question": q, "chat_history": chat_history})
    print(f"\nQ: {q}\nA: {res['answer']}\n")
    chat_history.append((q, res["answer"]))