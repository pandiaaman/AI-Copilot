# uvicorn app:app --reload
import os
import warnings
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# 🔹 New imports for reranking
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from sentence_transformers import CrossEncoder

from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
import asyncio

warnings.filterwarnings("ignore")
load_dotenv()

app = FastAPI(title="MediaCentral CTMS Chatbot API")

# Allow your frontend to access the API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stateful chat history
chat_history: List[tuple] = []

# Prompt template
prompt_template = """
You are an expert assistant for MediaCentral CTMS Registry documentation.
You are trusted by users and developers to provide **accurate, complete, and empathetic explanations**.

Always answer with:
- Clear step-by-step instructions.
- Complete details for API endpoints or features.
- Examples and precautions whenever applicable.
- Emotional touch to make the user feel guided and confident.

For a **feature-related question**, structure your answer in depth for the user to understand everything properly. Keep it step by step process and details in each step with examples.

If you don’t know the answer, admit it honestly.
If you don't find the asked question information in the document, just tell "I don't know" and don't answer further.

Question: {question}
Context (from most relevant documents only): {summaries}

Answer with clarity, completeness, and a friendly guiding tone:
"""

prompt = PromptTemplate(input_variables=["summaries", "question"], template=prompt_template)

# Embeddings + VectorStore
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

# Normal retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

# Conversational retrieval chain (normal)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=chat,
    retriever=retriever,
    return_source_documents=True,
    chain_type="map_reduce",
    combine_docs_chain_kwargs={"combine_prompt": prompt}
)

# 🔹 Reranked retriever
cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=5)
reranked_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=retriever
)

qa_chain_reranked = ConversationalRetrievalChain.from_llm(
    llm=chat,
    retriever=reranked_retriever,
    return_source_documents=True,
    chain_type="map_reduce",
    combine_docs_chain_kwargs={"combine_prompt": prompt}
)

# Request model
class QueryRequest(BaseModel):
    question: str
    max_history: Optional[int] = 10

# Response model
class QueryResponse(BaseModel):
    answer: str
    sources: List[str] = []

# ----------------------
# Normal Query Endpoint
# ----------------------
@app.post("/query", response_model=QueryResponse)
def query_bot(req: QueryRequest):
    global chat_history
    res = qa_chain({"question": req.question, "chat_history": chat_history})
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]

    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)

# ----------------------
# Reranked Query Endpoint
# ----------------------
@app.post("/query-reranked", response_model=QueryResponse)
def query_bot_reranked(req: QueryRequest):
    global chat_history
    res = qa_chain_reranked({"question": req.question, "chat_history": chat_history})
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]

    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)


# ----------------------
# Utility: Detect broad vs narrow queries
# ----------------------
def is_broad_question(question: str) -> bool:
    broad_keywords = [
        "all", "overview", "every",
        "features", "complete guide", "everything"
    ]
    q_lower = question.lower()
    return any(keyword in q_lower for keyword in broad_keywords)


# ----------------------
# Dynamic Query Endpoint (chooses reranked or not)
# Auto detects broad and narrow queries
# ----------------------
@app.post("/query-dynamic", response_model=QueryResponse)
def query_bot_dynamic(req: QueryRequest):
    global chat_history
    
    # Decide which chain to use
    if is_broad_question(req.question):
        print("🔎 Broad query detected → Using NORMAL retriever (no rerank)")
        res = qa_chain({"question": req.question, "chat_history": chat_history})
    else:
        print("🎯 Narrow query detected → Using RERANKED retriever")
        res = qa_chain_reranked({"question": req.question, "chat_history": chat_history})
    
    # Extract answer + sources
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]

    # Update chat history
    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)


# ----------------------
# Dynamic Query Endpoint With Confidence Score(chooses reranked or not)
# Auto detects broad and narrow queries
# ----------------------
@app.post("/query-dynamic-conf", response_model=QueryResponse)
def query_bot_dynamic(req: QueryRequest):
    global chat_history
    
    # Decide which chain to use
    if is_broad_question(req.question):
        print("🔎 Broad query detected → Using NORMAL retriever (no rerank)")
        res = qa_chain({"question": req.question, "chat_history": chat_history})
    else:
        print("🎯 Narrow query detected → Using RERANKED retriever")
        res = qa_chain_reranked({"question": req.question, "chat_history": chat_history})
        
        # Log reranker confidence scores
        print("\n📊 Reranker Scores:")
        for doc in res.get("source_documents", []):
            score = doc.metadata.get("relevance_score", None)
            src = doc.metadata.get("source", "Unknown")
            if score is not None:
                print(f" - {src}: {score:.4f}")
            else:
                print(f" - {src}: [no score returned]")

    # Extract answer + sources
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]

    # Update chat history
    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)


# ----------------------
# Dynamic Query Endpoint With Streaming answers
# Auto detects broad and narrow queries
# ----------------------
@app.post("/query-dynamic-streaming")
async def query_bot_dynamic_stream(req: QueryRequest, request: Request):
    global chat_history

    # Decide chain type (broad vs narrow)
    if is_broad_question(req.question):
        print("🔎 Broad query detected → Using NORMAL retriever (no rerank)")
        retriever_chain = qa_chain
    else:
        print("🎯 Narrow query detected → Using RERANKED retriever")
        retriever_chain = qa_chain_reranked

    # Create a callback handler to stream tokens
    callback = AsyncIteratorCallbackHandler()
    stream_chat = ChatOpenAI(
        verbose=True,
        temperature=0.4,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"],
        streaming=True,
        callbacks=[callback]
    )

    # Recreate chain with streaming LLM
    stream_chain = ConversationalRetrievalChain.from_llm(
        llm=stream_chat,
        retriever=retriever_chain.retriever,
        return_source_documents=True,
        chain_type="map_reduce",
        combine_docs_chain_kwargs={"combine_prompt": prompt}
    )

    async def token_streamer():
        """Generator that streams tokens as they are produced"""
        chat_history = []

        task = asyncio.create_task(
            stream_chain.acall({"question": req.question, "chat_history": chat_history})
        )
        async for token in callback.aiter():
            # Stop streaming if client disconnects
            if await request.is_disconnected():
                task.cancel()
                break
            yield token
        res = await task
        # Final metadata (sources) at end of stream
        sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]
        yield f"\n\nSources: {', '.join(sources)}"

        # Update chat history
        answer = res["answer"]
        chat_history.append((req.question, answer))
        if len(chat_history) > req.max_history:
            chat_history = chat_history[-req.max_history:]

    return StreamingResponse(token_streamer(), media_type="text/plain")


# TODO: Check if this is right later
# @app.post("/query-stream")
# def query_stream(req: QueryRequest):
#     """
#     Streaming response endpoint for frontend to get incremental answers.
#     """
#     global chat_history

#     def event_generator():
#         # Generator to yield chunks
#         # Here we set streaming=True in ChatOpenAI
#         chat_stream = ChatOpenAI(
#             verbose=True,
#             temperature=0.4,
#             model_name="gpt-3.5-turbo",
#             openai_api_key=os.environ["OPENAI_API_KEY"],
#             streaming=True
#         )

#         # Initialize a streaming chain for this request
#         streaming_chain = ConversationalRetrievalChain.from_llm(
#             llm=chat_stream,
#             retriever=retriever,
#             return_source_documents=True,
#             chain_type="map_reduce",
#             combine_docs_chain_kwargs={"combine_prompt": prompt}
#         )

#         # Streaming response dictionary
#         buffer = ""
#         for token in streaming_chain.stream({"question": req.question, "chat_history": chat_history}):
#             buffer += token
#             # Send incremental token to frontend
#             yield f"data:{json.dumps({'answer': buffer})}\n\n"

#         # After streaming ends, update chat history
#         chat_history.append((req.question, buffer))
#         if len(chat_history) > req.max_history:
#             chat_history = chat_history[-req.max_history:]

#         # Signal that streaming is done
#         yield "data:[DONE]\n\n"

#     return StreamingResponse(event_generator(), media_type="text/event-stream")