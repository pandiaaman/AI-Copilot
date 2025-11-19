# uvicorn app-improved:app --reload
import os
import json
import time
import hashlib
import warnings
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# FastAPI imports
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# LangChain imports
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

# Reranking imports
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# Query classification imports
from sentence_transformers import SentenceTransformer

# Caching imports
import redis
import logging
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")
load_dotenv()

app = FastAPI(title="Enhanced MediaCentral CTMS Chatbot API", version="2.0.0")

# CORS configuration
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

# Global variables
chat_history: List[tuple] = []

# Initializing Redis cache (optional - will work without Redis)
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    CACHE_ENABLED = True
    logger.info("✅ Redis cache connected")
except:
    CACHE_ENABLED = False
    logger.warning("⚠️ Redis not available - caching disabled")

class QueryClassifier:
    """Advanced query classification system"""
    
    def __init__(self):
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Define query types with examples
            self.query_types = {
                "specific_api": [
                    "How to use createFolder API",
                    "What parameters does search take",
                    "How to call the asset endpoint",
                    "API documentation for folders",
                    "POST request parameters",
                    "How to update asset categories",
                    "API request example",
                    "JSON request format",
                    "How to make API call",
                    "Endpoint for creating folder",
                    "Request body structure",
                    "API response format"
                ],
                "conceptual": [
                    "What is CTMS",
                    "How does asset management work",
                    "Explain the folder structure",
                    "What are categories in CTMS",
                    "How does authentication work",
                    "Understanding MediaCentral",
                    "CTMS concepts"
                ],
                "troubleshooting": [
                    "Error when creating folder",
                    "Why is search not working",
                    "Getting 404 error",
                    "Authentication failed",
                    "Cannot access API",
                    "API call failing",
                    "Request timeout",
                    "Invalid response"
                ],
                "broad_overview": [
                    "Tell me about all features",
                    "Complete guide to CTMS",
                    "Overview of all APIs",
                    "Everything about MediaCentral",
                    "Full documentation",
                    "All API endpoints",
                    "Complete API reference"
                ]
            }
            
            # Pre-compute embeddings for each type
            self.type_embeddings = {}
            for qtype, examples in self.query_types.items():
                embeddings = [self.model.encode(example) for example in examples]
                self.type_embeddings[qtype] = np.mean(embeddings, axis=0)
            
            logger.info("✅ Query classifier initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize query classifier: {e}")
            self.model = None
            self.type_embeddings = {}
    
    def classify_query(self, question: str) -> Tuple[str, float]:
        """Classify query and return type with confidence"""
        if not self.model or not self.type_embeddings:
            return "general", 0.5
        
        try:
            question_embedding = self.model.encode(question)
            
            similarities = {}
            for qtype, type_embedding in self.type_embeddings.items():
                similarity = np.dot(question_embedding, type_embedding) / (
                    np.linalg.norm(question_embedding) * np.linalg.norm(type_embedding)
                )
                similarities[qtype] = float(similarity)  # Ensure Python float
            
            best_type = max(similarities, key=similarities.get)
            confidence = similarities[best_type]
            
            return best_type, float(confidence)  # Ensure Python float
            
        except Exception as e:
            logger.error(f"Error in query classification: {e}")
            return "general", 0.5

class ResponseOptimizer:
    """Optimize responses based on query characteristics"""
    
    @staticmethod
    def get_response_config(query_type: str, confidence: float) -> Dict[str, Any]:
        """Determine optimal response configuration"""
        
        base_configs = {
            "specific_api": {
                "max_tokens": 600,  # Increased for more detailed examples
                "temperature": 0.1,  # Lower for more precise technical responses
                "detail_level": "detailed_with_examples",
                "k_docs": 12  # More documents to find comprehensive examples
            },
            "conceptual": {
                "max_tokens": 400,
                "temperature": 0.2,
                "detail_level": "educational",
                "k_docs": 8
            },
            "troubleshooting": {
                "max_tokens": 450,  # Increased for code examples
                "temperature": 0.1,  # Lower for precise solutions
                "detail_level": "solution_focused_with_examples",
                "k_docs": 10  # More docs to find solution examples
            },
            "broad_overview": {
                "max_tokens": 700,  # Increased for comprehensive examples
                "temperature": 0.2,
                "detail_level": "comprehensive_with_examples",
                "k_docs": 15
            },
            "general": {
                "max_tokens": 400,
                "temperature": 0.2,
                "detail_level": "balanced_with_examples",
                "k_docs": 10
            }
        }
        
        config = base_configs.get(query_type, base_configs["general"])
        
        # Adjust based on confidence
        if confidence < 0.4:
            config["k_docs"] = min(config["k_docs"] + 3, 15)  # Get more docs if uncertain
        
        return config

class AdvancedRetriever:
    """Enhanced retrieval with confidence scoring and filtering"""
    
    def __init__(self, vectorstore, embeddings):
        self.vectorstore = vectorstore
        self.embeddings = embeddings
    
    def extract_code_examples(self, documents: List[Document]) -> Dict[str, List[str]]:
        """Extract and categorize code examples from documents"""
        code_examples = {
            "json_requests": [],
            "json_responses": [],
            "postman_steps": [],
            "general_code": []
        }
        
        for doc in documents:
            content = doc.page_content
            
            # Find JSON code blocks
            import re
            json_blocks = re.findall(r'```[json]*\s*\n(.*?)\n\s*```', content, re.DOTALL)
            for block in json_blocks:
                if '"request"' in block.lower() or block.strip().startswith('{'):
                    if 'response' in doc.page_content.lower():
                        code_examples["json_responses"].append(block.strip())
                    else:
                        code_examples["json_requests"].append(block.strip())
                
            # Find general code blocks
            general_blocks = re.findall(r'```\s*\n(.*?)\n\s*```', content, re.DOTALL)
            for block in general_blocks:
                if block not in json_blocks:
                    code_examples["general_code"].append(block.strip())
            
            # Extract Postman-related examples
            if 'postman' in content.lower():
                postman_sections = re.findall(r'postman.*?api.*?calls.*?$', content, re.MULTILINE | re.IGNORECASE)
                code_examples["postman_steps"].extend(postman_sections)
        
        return code_examples
    
    def enhance_context_with_examples(self, documents: List[Document], query: str) -> str:
        """Create enhanced context that prioritizes code examples"""
        if not documents:
            return ""
        
        # Extract code examples
        code_examples = self.extract_code_examples(documents)
        
        # Build context with emphasis on examples
        context_parts = []
        
        # Add documents with code examples first
        docs_with_code = [doc for doc in documents if '```' in doc.page_content or 'example' in doc.page_content.lower()]
        docs_without_code = [doc for doc in documents if doc not in docs_with_code]
        
        # Prioritize documents with code
        prioritized_docs = docs_with_code + docs_without_code
        
        for i, doc in enumerate(prioritized_docs[:10]):  # Limit to top 10 docs
            source = doc.metadata.get("source", f"Document {i+1}")
            content = doc.page_content
            
            # Add emphasis for code-containing documents
            if doc in docs_with_code:
                context_parts.append(f"📋 **{source}** (Contains Code Examples):\n{content}")
            else:
                context_parts.append(f"📄 **{source}**:\n{content}")
        
        # Add extracted examples summary if any
        if any(code_examples.values()):
            context_parts.append("\n🔧 **Extracted Code Examples Summary:**")
            if code_examples["json_requests"]:
                context_parts.append("📥 **Request Examples Found:** " + str(len(code_examples["json_requests"])))
            if code_examples["json_responses"]:
                context_parts.append("📤 **Response Examples Found:** " + str(len(code_examples["json_responses"])))
            if code_examples["postman_steps"]:
                context_parts.append("🚀 **Postman Examples Found:** " + str(len(code_examples["postman_steps"])))
        
        return "\n\n".join(context_parts)
    
    def enhance_answer_with_examples(self, answer: str, documents: List[Document], query: str, query_type: str) -> str:
        """Enhance answer with missing code examples from documents"""
        
        # Check if answer already has good code examples
        has_json_examples = '```json' in answer or '```' in answer
        has_examples = 'example' in answer.lower() and ('{' in answer or 'post' in answer.lower())
        
        # For API queries, we definitely want code examples
        if query_type == "specific_api" and not (has_json_examples or has_examples):
            code_examples = self.extract_code_examples(documents)
            
            # Add the most relevant code examples
            example_additions = []
            
            if code_examples["json_requests"]:
                example_additions.append("\n\n## 📝 Request Example:\n```json\n" + code_examples["json_requests"][0] + "\n```")
            
            if code_examples["json_responses"]:
                example_additions.append("\n\n## 📤 Response Example:\n```json\n" + code_examples["json_responses"][0] + "\n```")
            
            if code_examples["postman_steps"]:
                example_additions.append("\n\n## 🚀 Postman Usage:\n" + code_examples["postman_steps"][0])
            
            # Find JSON blocks in any document for this query
            if not example_additions:
                for doc in documents[:3]:  # Check top 3 docs
                    content = doc.page_content
                    if '```' in content:
                        import re
                        json_blocks = re.findall(r'```[json]*\s*\n(.*?)\n\s*```', content, re.DOTALL)
                        if json_blocks:
                            example_additions.append(f"\n\n## 💡 Code Example from {doc.metadata.get('source', 'Documentation')}:\n```json\n{json_blocks[0].strip()}\n```")
                            break
            
            if example_additions:
                enhanced_answer = answer + "".join(example_additions[:2])  # Add max 2 examples
                logger.info(f"✨ Enhanced answer with {len(example_additions)} code examples")
                return enhanced_answer
        
        # For troubleshooting, add examples if helpful
        elif query_type == "troubleshooting" and not has_examples:
            for doc in documents[:2]:
                content = doc.page_content
                if 'example' in content.lower() and ('correct' in content.lower() or 'proper' in content.lower()):
                    import re
                    example_blocks = re.findall(r'```[json]*\s*\n(.*?)\n\s*```', content, re.DOTALL)
                    if example_blocks:
                        enhanced_answer = answer + f"\n\n## ✅ Correct Usage Example:\n```json\n{example_blocks[0].strip()}\n```"
                        logger.info("✨ Enhanced troubleshooting answer with correct usage example")
                        return enhanced_answer
                    break
        
        return answer
    
    def filter_relevant_chunks(self, query: str, documents: List[Document], threshold: float = 0.3) -> List[Document]:
        """Filter documents based on relevance score with bonus for code examples"""
        if not documents:
            return documents
        
        try:
            query_embedding = self.embeddings.embed_query(query)
            
            scored_docs = []
            for doc in documents:
                # Use first 500 chars for similarity calculation (efficiency)
                doc_embedding = self.embeddings.embed_query(doc.page_content[:500])
                similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
                
                # Bonus scoring for documents with code examples
                code_bonus = 0.0
                content = doc.page_content.lower()
                
                # Detect various types of code examples
                if '```json' in content or '```' in content:
                    code_bonus += 0.15  # Strong bonus for JSON code blocks
                elif 'request body' in content or 'response' in content:
                    code_bonus += 0.10  # Bonus for API documentation
                elif 'example:' in content or 'example response' in content:
                    code_bonus += 0.08  # Bonus for examples
                elif 'postman' in content:
                    code_bonus += 0.12  # Bonus for Postman examples
                
                # Additional bonus for specific API-related content
                if any(term in content for term in ['post', 'get', 'put', 'delete', 'endpoint']):
                    code_bonus += 0.05
                
                # Check metadata for code examples (from ingestion)
                if doc.metadata.get("has_code_examples", False):
                    code_bonus += 0.10
                if doc.metadata.get("has_api_endpoint", False):
                    code_bonus += 0.08
                
                # Apply bonus and ensure we don't exceed 1.0
                final_score = min(similarity + code_bonus, 1.0)
                
                if final_score > threshold:
                    doc.metadata["relevance_score"] = float(final_score)
                    doc.metadata["code_bonus"] = float(code_bonus)
                    scored_docs.append((doc, final_score))
            
            # Sort by relevance and return top documents
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            return [doc for doc, score in scored_docs]
            
        except Exception as e:
            logger.error(f"Error in document filtering: {e}")
            return documents
    
    def calculate_response_confidence(self, query: str, retrieved_docs: List[Document]) -> float:
        """Calculate confidence score for the response"""
        if not retrieved_docs:
            return 0.1
        
        try:
            # Factor 1: Average similarity between query and docs
            relevance_scores = [
                doc.metadata.get("relevance_score", 0.5) 
                for doc in retrieved_docs
            ]
            avg_relevance = float(np.mean(relevance_scores)) if relevance_scores else 0.5
            
            # Factor 2: Number of relevant documents found (normalized)
            doc_count_factor = min(len(retrieved_docs) / 5, 1.0)
            
            # Factor 3: Consistency of document types
            doc_types = [doc.metadata.get("document_type", "unknown") for doc in retrieved_docs]
            type_consistency = len(set(doc_types)) / len(doc_types) if doc_types else 1.0
            
            # Combine factors
            confidence = (avg_relevance * 0.5) + (doc_count_factor * 0.3) + (type_consistency * 0.2)
            
            return float(min(confidence, 1.0))  # Ensure Python float type
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5

class CacheManager:
    """Manage response caching"""
    
    @staticmethod
    def get_cache_key(query: str) -> str:
        """Generate cache key for query"""
        return f"response:{hashlib.md5(query.lower().strip().encode()).hexdigest()}"
    
    @staticmethod
    def get_cached_response(query: str) -> Optional[Dict]:
        """Retrieve cached response"""
        if not CACHE_ENABLED:
            return None
        
        try:
            cache_key = CacheManager.get_cache_key(query)
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.error(f"Cache retrieval error: {e}")
        
        return None
    
    @staticmethod
    def cache_response(query: str, response: Dict, ttl: int = 3600):
        """Cache response"""
        if not CACHE_ENABLED:
            return
        
        try:
            cache_key = CacheManager.get_cache_key(query)
            redis_client.setex(cache_key, ttl, json.dumps(response))
        except Exception as e:
            logger.error(f"Cache storage error: {e}")

# Dynamic prompt templates with emphasis on code examples
PROMPT_TEMPLATES = {
    "specific_api": """You are an API documentation expert for MediaCentral CTMS Registry.

CRITICAL INSTRUCTIONS:
- ALWAYS include complete JSON request and response examples when available in the documentation
- Show exact API endpoints, HTTP methods, and parameter structures
- Include Postman collection examples if mentioned
- Provide step-by-step API call sequences

For API-related questions, structure your answer as:
1. **Overview**: Brief explanation of the API functionality
2. **HTTP Method & Endpoint**: Exact API call details
3. **Request Format**: Complete JSON request example with all parameters
4. **Response Format**: Complete JSON response example
5. **Step-by-step Process**: Detailed implementation steps
6. **Error Handling**: Common issues and solutions
7. **Postman Examples**: If collection steps are available  

Question: {question}
Context: {summaries}

Provide a complete, actionable answer with extensive code examples:""",
    
    "troubleshooting": """You are a technical support specialist for MediaCentral CTMS.

CRITICAL INSTRUCTIONS:
- Include relevant code examples that demonstrate the correct usage
- Show both incorrect and correct API call examples when applicable
- Provide complete JSON structures for troubleshooting

For troubleshooting questions:
1. **Problem Identification**: What's likely causing the issue
2. **Correct API Usage**: Show proper request/response examples
3. **Step-by-step Solution**: Detailed fix instructions with code
4. **Verification**: How to test the solution with examples
5. **Prevention**: Best practices with code examples

Question: {question}
Context: {summaries}

Provide a clear troubleshooting guide with code examples:""",
    
    "conceptual": """You are a MediaCentral CTMS educator.

CRITICAL INSTRUCTIONS:
- Include practical code examples to illustrate concepts
- Show JSON structures and API patterns when explaining features
- Provide real-world usage examples from the documentation

For conceptual questions:
1. **Clear Definition**: What the concept means
2. **Practical Examples**: Real JSON requests/responses showing the concept
3. **Implementation Details**: How to use it with code examples
4. **Related Features**: Connected concepts with examples
5. **Best Practices**: Recommended patterns with code

Question: {question}
Context: {summaries}

Provide an educational explanation with practical code examples:""",
    
    "broad_overview": """You are an expert MediaCentral CTMS consultant.

CRITICAL INSTRUCTIONS:
- Include key API examples for each major feature discussed
- Show representative JSON structures and endpoint patterns
- Provide a variety of request/response examples

For comprehensive questions:
1. **Structured Overview**: Organize by major features/capabilities
2. **API Examples**: Include key endpoints and JSON examples for each area
3. **Implementation Patterns**: Common usage patterns with code
4. **Integration Examples**: How different APIs work together
5. **Next Steps**: Recommended learning path with example priorities

Question: {question}
Context: {summaries}

Provide a comprehensive guide with extensive code examples:""",
    
    "general": """You are an expert assistant for MediaCentral CTMS Registry documentation.

CRITICAL INSTRUCTIONS FOR CODE EXAMPLES:
- ALWAYS prioritize and include JSON request/response examples when they exist in the documentation
- Show complete API call structures with all parameters
- Include Postman collection steps if mentioned in the documentation
- Provide exact HTTP methods, endpoints, and headers
- Show both request body and expected response formats

Response Structure:
- Clear step-by-step instructions
- Complete API endpoint details with HTTP methods
- Full JSON request examples with parameter explanations
- Complete JSON response examples with field descriptions
- Postman usage examples when available
- Error scenarios with example error responses
- Practical implementation guidance

IMPORTANT: If the documentation contains code blocks with ```json or ``` examples, 
you MUST include them in your response. These are crucial for developers.

If you don't know the answer, admit it honestly.
If the question is about anything else other than the documentation, say "I am specialized in MediaCentral CTMS documentation and cannot assist with that."
If you don't find the asked question information in the document, just tell "I don't know" and don't answer further.

Question: {question}
Context (from most relevant documents - pay special attention to code examples): {summaries}

Answer with clarity, completeness, and extensive code examples:"""
}

# Initialize components
logger.info("🚀 Initializing enhanced CTMS chatbot components...")

# Initialize query classifier
query_classifier = QueryClassifier()

# Setup embeddings (using the new large model)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    dimensions=1024
)

# Setup vector store
vectorstore = PineconeVectorStore(
    index_name=os.environ["INDEX_NAME_LARGE"],
    embedding=embeddings
)

# Initialize advanced retriever
advanced_retriever = AdvancedRetriever(vectorstore, embeddings)

# Base retriever
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

# Reranked retriever
cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=8)
reranked_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)

logger.info("✅ All components initialized successfully")

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    max_history: Optional[int] = 10
    use_cache: Optional[bool] = True

class QueryResponse(BaseModel):
    answer: str
    sources: List[str] = []
    confidence: Optional[float] = None
    query_type: Optional[str] = None
    response_time: Optional[float] = None
    cached: Optional[bool] = False

# Utility functions
def is_broad_question(question: str) -> bool:
    """Legacy broad question detection"""
    broad_keywords = [
        "all", "overview", "every", "everything",
        "features", "complete guide", "full documentation"
    ]
    q_lower = question.lower()
    return any(keyword in q_lower for keyword in broad_keywords)

def create_dynamic_prompt(query_type: str) -> PromptTemplate:
    """Create dynamic prompt based on query type"""
    template = PROMPT_TEMPLATES.get(query_type, PROMPT_TEMPLATES["general"])
    return PromptTemplate(input_variables=["summaries", "question"], template=template)

def log_query_analytics(query: str, response_time: float, token_count: int, confidence: float, query_type: str):
    """Log query analytics for optimization"""
    analytics = {
        "timestamp": datetime.now().isoformat(),
        "query_length": len(query.split()),
        "response_time": response_time,
        "estimated_tokens": token_count,
        "confidence_score": confidence,
        "query_type": query_type
    }
    logger.info(f"Query Analytics: {json.dumps(analytics)}")

# ----------------------
# ENHANCED ENDPOINTS
# ----------------------

@app.post("/query-enhanced", response_model=QueryResponse)
def query_bot_enhanced(req: QueryRequest):
    """Enhanced query endpoint with all optimizations"""
    global chat_history
    start_time = time.time()
    
    # Check cache first
    if req.use_cache:
        cached_response = CacheManager.get_cached_response(req.question)
        if cached_response:
            cached_response["cached"] = True
            cached_response["response_time"] = time.time() - start_time
            return QueryResponse(**cached_response)
    
    try:
        # Classify query
        query_type, classification_confidence = query_classifier.classify_query(req.question)
        logger.info(f"🎯 Query classified as: {query_type} (confidence: {classification_confidence:.3f})")
        
        # Get response configuration
        response_config = ResponseOptimizer.get_response_config(query_type, classification_confidence)
        
        # Choose retrieval strategy and create retriever with appropriate k value
        k_docs = response_config["k_docs"]
        
        if query_type == "broad_overview" or is_broad_question(req.question):
            logger.info("📚 Using normal retriever for broad query")
            # Create a new base retriever with the specific k value
            retriever = vectorstore.as_retriever(search_kwargs={"k": k_docs})
        else:
            logger.info("🎯 Using reranked retriever for focused query")
            # Create a new base retriever for reranking with higher k, then rerank to fewer
            base_retriever_temp = vectorstore.as_retriever(search_kwargs={"k": min(k_docs * 2, 20)})
            reranker_temp = CrossEncoderReranker(model=cross_encoder_model, top_n=k_docs)
            retriever = ContextualCompressionRetriever(
                base_compressor=reranker_temp,
                base_retriever=base_retriever_temp
            )
        
        # Create dynamic prompt
        prompt = create_dynamic_prompt(query_type)
        
        # Create optimized chat model
        chat = ChatOpenAI(
            verbose=False,
            temperature=response_config["temperature"],
            max_tokens=response_config["max_tokens"],
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"]
        )
        
        # Create chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=retriever,
            return_source_documents=True,
            chain_type="map_reduce",
            combine_docs_chain_kwargs={"combine_prompt": prompt}
        )
        
        # Execute query
        res = qa_chain({"question": req.question, "chat_history": chat_history})
        answer = res["answer"]
        retrieved_docs = res.get("source_documents", [])
        
        # Filter and enhance documents
        filtered_docs = advanced_retriever.filter_relevant_chunks(
            req.question, retrieved_docs, threshold=0.25
        )
        
        # Enhance answer with code examples if missing
        answer = advanced_retriever.enhance_answer_with_examples(answer, filtered_docs, req.question, query_type)
        
        # Calculate confidence
        confidence = advanced_retriever.calculate_response_confidence(req.question, filtered_docs)
        
        # Prepare sources
        sources = [doc.metadata.get("source", "Unknown") for doc in filtered_docs[:10]]
        
        # Response time
        response_time = time.time() - start_time
        
        # Estimate token count (rough approximation)
        estimated_tokens = len(answer.split()) * 1.3
        
        # Log analytics
        log_query_analytics(req.question, response_time, estimated_tokens, confidence, query_type)
        
        # Update chat history
        chat_history.append((req.question, answer))
        if len(chat_history) > req.max_history:
            chat_history = chat_history[-req.max_history:]
        
        # Prepare response (ensure all numeric values are JSON serializable)
        response_data = {
            "answer": answer,
            "sources": sources,
            "confidence": float(confidence),
            "query_type": query_type,
            "response_time": float(response_time),
            "cached": False
        }
        
        # Cache response if confidence is high
        if confidence > 0.6 and req.use_cache:
            CacheManager.cache_response(req.question, response_data)
        
        return QueryResponse(**response_data)
        
    except Exception as e:
        logger.error(f"❌ Error in enhanced query: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.post("/query-streaming-enhanced")
async def query_bot_streaming_enhanced(req: QueryRequest, request: Request):
    """Enhanced streaming endpoint"""
    global chat_history
    
    try:
        # Classify query for optimal retrieval
        query_type, confidence = query_classifier.classify_query(req.question)
        response_config = ResponseOptimizer.get_response_config(query_type, confidence)
        
        # Choose retrieval strategy and create retriever with appropriate k value
        k_docs = response_config["k_docs"]
        
        if query_type == "broad_overview" or is_broad_question(req.question):
            # Create a new base retriever with the specific k value
            retriever = vectorstore.as_retriever(search_kwargs={"k": k_docs})
        else:
            # Create a new base retriever for reranking with higher k, then rerank to fewer
            base_retriever_temp = vectorstore.as_retriever(search_kwargs={"k": min(k_docs * 2, 20)})
            reranker_temp = CrossEncoderReranker(model=cross_encoder_model, top_n=k_docs)
            retriever = ContextualCompressionRetriever(
                base_compressor=reranker_temp,
                base_retriever=base_retriever_temp
            )
        
        # Create streaming callback
        callback = AsyncIteratorCallbackHandler()
        
        # Create streaming chat model
        stream_chat = ChatOpenAI(
            verbose=False,
            temperature=response_config["temperature"],
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            streaming=True,
            callbacks=[callback]
        )
        
        # Create dynamic prompt
        prompt = create_dynamic_prompt(query_type)
         
        # Create streaming chain
        stream_chain = ConversationalRetrievalChain.from_llm(
            llm=stream_chat,
            retriever=retriever,
            return_source_documents=True,
            chain_type="map_reduce",
            combine_docs_chain_kwargs={"combine_prompt": prompt}
        )
        
        # Copy current chat history to use in the async function
        current_chat_history = chat_history.copy()
        
        async def enhanced_token_streamer():
            """Enhanced token streaming with metadata"""
            
            # Send initial metadata (ensure JSON serializable types)
            yield f"data: {json.dumps({'type': 'metadata', 'query_type': query_type, 'confidence': float(confidence)})}\n\n"
            
            task = asyncio.create_task(
                stream_chain.acall({"question": req.question, "chat_history": current_chat_history})
            )
            
            # Stream tokens
            async for token in callback.aiter():
                if await request.is_disconnected():
                    task.cancel()
                    break
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
            
            # Get final result
            res = await task
            
            # Process and send final metadata
            retrieved_docs = res.get("source_documents", [])
            filtered_docs = advanced_retriever.filter_relevant_chunks(
                req.question, retrieved_docs, threshold=0.25
            )
            
            final_confidence = advanced_retriever.calculate_response_confidence(req.question, filtered_docs)
            sources = [doc.metadata.get("source", "Unknown") for doc in filtered_docs[:10]]
            
            yield f"data: {json.dumps({'type': 'final', 'sources': sources, 'confidence': float(final_confidence)})}\n\n"
            yield "data: [DONE]\n\n"
            
            # Update global chat history after streaming completes
            answer = res.get("answer", "")
            global chat_history
            chat_history.append((req.question, answer))
            if len(chat_history) > req.max_history:
                chat_history = chat_history[-req.max_history:]
        
        # Return the streaming response directly
        return StreamingResponse(enhanced_token_streamer(), media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"❌ Error in streaming query: {e}")
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")

# ----------------------
# LEGACY ENDPOINTS (maintained for backwards compatibility)
# ----------------------

@app.post("/query", response_model=QueryResponse)
def query_bot(req: QueryRequest):
    """Legacy normal query endpoint"""
    global chat_history
    
    chat = ChatOpenAI(
        verbose=True,
        temperature=0.4,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    
    prompt = PromptTemplate(
        input_variables=["summaries", "question"], 
        template=PROMPT_TEMPLATES["general"]
    )
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=base_retriever,
        return_source_documents=True,
        chain_type="map_reduce",
        combine_docs_chain_kwargs={"combine_prompt": prompt}
    )
    
    res = qa_chain({"question": req.question, "chat_history": chat_history})
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]
    
    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)

@app.post("/query-reranked", response_model=QueryResponse)
def query_bot_reranked(req: QueryRequest):
    """Legacy reranked query endpoint"""
    global chat_history
    
    chat = ChatOpenAI(
        verbose=True,
        temperature=0.4,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    
    prompt = PromptTemplate(
        input_variables=["summaries", "question"], 
        template=PROMPT_TEMPLATES["general"]
    )
    
    qa_chain_reranked = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=reranked_retriever,
        return_source_documents=True,
        chain_type="map_reduce",
        combine_docs_chain_kwargs={"combine_prompt": prompt}
    )
    
    res = qa_chain_reranked({"question": req.question, "chat_history": chat_history})
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]
    
    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)

@app.post("/query-dynamic", response_model=QueryResponse)
def query_bot_dynamic(req: QueryRequest):
    """Legacy dynamic query endpoint"""
    global chat_history
    
    chat = ChatOpenAI(
        verbose=True,
        temperature=0.4,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    
    prompt = PromptTemplate(
        input_variables=["summaries", "question"], 
        template=PROMPT_TEMPLATES["general"]
    )
    
    # Legacy broad question detection
    if is_broad_question(req.question):
        print("🔎 Broad query detected → Using NORMAL retriever (no rerank)")
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=base_retriever,
            return_source_documents=True,
            chain_type="map_reduce",
            combine_docs_chain_kwargs={"combine_prompt": prompt}
        )
        res = qa_chain({"question": req.question, "chat_history": chat_history})
    else:
        print("🎯 Narrow query detected → Using RERANKED retriever")
        qa_chain_reranked = ConversationalRetrievalChain.from_llm(
            llm=chat,
            retriever=reranked_retriever,
            return_source_documents=True,
            chain_type="map_reduce",
            combine_docs_chain_kwargs={"combine_prompt": prompt}
        )
        res = qa_chain_reranked({"question": req.question, "chat_history": chat_history})
    
    answer = res["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])]
    
    chat_history.append((req.question, answer))
    if len(chat_history) > req.max_history:
        chat_history = chat_history[-req.max_history:]
    
    return QueryResponse(answer=answer, sources=sources)

# ----------------------
# UTILITY ENDPOINTS
# ----------------------

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "features": {
            "query_classification": bool(query_classifier.model),
            "caching": CACHE_ENABLED,
            "enhanced_retrieval": True,
            "streaming": True
        }
    }

@app.get("/stats")
def get_stats():
    """Get system statistics"""
    return {
        "chat_history_length": len(chat_history),
        "index_name": os.environ.get("INDEX_NAME_LARGE", "unknown"),
        "embedding_model": "text-embedding-3-large",
        "cache_enabled": CACHE_ENABLED,
        "query_classifier_status": "active" if query_classifier.model else "disabled",
        "enhancements": {
            "code_example_prioritization": True,
            "enhanced_prompts": True,
            "bonus_scoring_for_examples": True,
            "answer_enhancement": True
        }
    }

@app.post("/clear-history")
def clear_chat_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return {"message": "Chat history cleared", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Enhanced MediaCentral CTMS Chatbot API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
