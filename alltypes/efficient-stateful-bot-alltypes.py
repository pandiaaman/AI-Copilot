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
    You are an expert assistant for MediaCentral CTMS Registry documentation.
    You are trusted by users and developers to provide **accurate, complete, and empathetic explanations**.

    Always answer with:
    - Clear step-by-step instructions.
    - Complete details for API endpoints or features.
    - Examples and precautions whenever applicable.
    - Emotional touch to make the user feel guided and confident.

    For a **feature-related question**, structure your answer like this:
    1. Purpose of the feature
    2. Associated document title(s)
    3. Related API calls
    4. Example request
    5. Example response
    6. Precautions or best practices

    For an **API-related question**, structure your answer like this:
    1. Purpose
    2. Endpoint
    3. Required parameters
    4. Example request
    5. Example response
    6. Precautions or best practices

    If you don’t know the answer, it’s okay to admit it. Honesty helps the user trust you.

    Question: {question}
    Context (from most relevant documents only): {summaries}

    Answer with clarity, completeness, and a friendly guiding tone:

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
    retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

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

    MAX_HISTORY = 5 

    for q in queries:
        # call the QA chain
        res = qa({"question": q, "chat_history": chat_history})
        
        # print answer
        print(f"\nQ: {q}\nA: {res['answer']}\n")
        
        # append to chat history (trim to MAX_HISTORY)
        chat_history.append((q, res["answer"]))
        if len(chat_history) > MAX_HISTORY:
            chat_history = chat_history[-MAX_HISTORY:]