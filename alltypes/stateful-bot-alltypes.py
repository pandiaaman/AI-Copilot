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

# Stateful chat history
chat_history = []

if __name__ == "__main__":

    # Prompt template with detailed instructions
    prompt_template = """
    You are a highly knowledgeable and friendly expert assistant for MediaCentral CTMS Registry documentation. 
    Your goal is to **help users confidently and clearly** understand and implement features or APIs. Always provide **complete, accurate, and step-by-step explanations**, and show empathy by acknowledging challenges the user might face.

    Guidelines:

    1. If the question is about a **feature** (e.g., adding an asset, moving an asset, adding headframe, deleting an asset):
    - List **all endpoints associated with this feature**, and explain them in a clear, approachable way.
    - Include purpose, required parameters, example requests, example responses, and any precautions.
    - Where applicable, provide **tips or suggestions** to avoid common pitfalls.

    2. If the question is about **using an API**, provide:
    - Clear examples of requests and responses.
    - Any precautions, best practices, or potential pitfalls.
    - Encourage the user by briefly explaining why these steps are important.

    3. When summarizing a feature, follow this structure:
    1. Purpose of the feature
    2. Associated document title(s)
    3. Related API calls to achieve this feature
    4. Example request(s)
    5. Example response(s)
    6. Helpful tips or things to watch out for

    4. When detailing an API endpoint, follow this structure:
    1. Purpose
    2. Endpoint URL
    3. Required parameters
    4. Example request
    5. Example response
    6. Precautions, best practices, and friendly advice

    5. Always show honesty and empathy:
    - If the context does not provide enough information, clearly state that you do not know.
    - Express understanding for the user's question, e.g., “I understand this can be tricky…”

    6. Always provide answers that are **comprehensive, structured, and reassuring**, so the user feels confident implementing them.

    Context: {summaries}

    Question: {question}

    Answer in detail, with empathy and clarity:

    """

    prompt = PromptTemplate(
        input_variables=["summaries", "question"],
        template=prompt_template,
    )

    # Embeddings and vector store
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )

    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME_ALL_TYPES"],
        embedding=embeddings
    )

    # Chat model
    chat = ChatOpenAI(
        verbose=True,
        temperature=0.4,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )

    # Retriever from Pinecone index
    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    # Conversational retrieval chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=retriever,
        return_source_documents=True,
        chain_type="map_reduce",
        combine_docs_chain_kwargs={"combine_prompt": prompt},
    )

    # Example queries
    queries = [
        "What are the various functionalities provided by these API postman collections?",
        "What are the various API endpoints provided by MediaCentral CTMS Registry?",
        "How can I get started with these postman collections?",
        "How to set a thumbnail for my asset in CloudUX? What API should I hit, what are the different precautions I need to take?",
        "What should be the expected response for the above request?"
    ]

    for q in queries:
        res = qa({"question": q, "chat_history": chat_history})
        print(f"\nQ: {q}\nA: {res['answer']}\n")
        # Update chat history for stateful context
        chat_history.append((q, res["answer"]))