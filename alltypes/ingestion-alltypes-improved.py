import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any
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
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from pinecone import Pinecone
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class DocumentProcessor:
    """Enhanced document processor with metadata enrichment and smart chunking"""
    
    def __init__(self):
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"), 
                ("###", "Header 3"),
                ("####", "Header 4"),
            ]
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Reduced for better precision with large embeddings
            chunk_overlap=150,  # Increased overlap for better context
            separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""]
        )
    
    def enhance_document_metadata(self, doc: Document, filename: str, file_path: str) -> Document:
        """Add rich metadata to documents for better retrieval"""
        
        content = doc.page_content
        
        # Basic file information
        file_stats = os.stat(file_path)
        
        # Determine document type
        doc_type = self._classify_document_type(filename, content)
        
        # Extract section information
        section = self._extract_section(content)
        
        # Analyze content characteristics
        has_code_examples = "```" in content or "`" in content
        has_api_endpoint = any(method in content.lower() for method in ["get ", "post ", "put ", "delete ", "patch "])
        has_table = "|" in content and "---" in content
        
        # Count various elements
        word_count = len(content.split())
        line_count = len(content.split('\n'))
        
        # Generate content hash for deduplication
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Update metadata
        doc.metadata.update({
            "source": filename,
            "file_path": file_path,
            "document_type": doc_type,
            "section": section,
            "word_count": word_count,
            "line_count": line_count,
            "has_code_examples": has_code_examples,
            "has_api_endpoint": has_api_endpoint,
            "has_table": has_table,
            "content_hash": content_hash,
            "file_size": file_stats.st_size,
            "last_modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            "ingestion_timestamp": datetime.now().isoformat(),
            "chunk_id": None,  # Will be set during chunking
        })
        
        return doc
    
    def _classify_document_type(self, filename: str, content: str) -> str:
        """Classify document type based on filename and content"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        if "api" in filename_lower or "endpoint" in content_lower:
            return "api_reference"
        elif "tutorial" in filename_lower or "how to" in content_lower:
            return "tutorial"
        elif "troubleshoot" in filename_lower or "error" in content_lower:
            return "troubleshooting"
        elif "example" in filename_lower or "sample" in content_lower:
            return "example"
        elif "overview" in filename_lower or "introduction" in content_lower:
            return "overview"
        else:
            return "documentation"
    
    def _extract_section(self, content: str) -> str:
        """Extract main section from content"""
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line.replace("# ", "").strip()
            elif line.startswith("## "):
                return line.replace("## ", "").strip()
        return "general"
    
    def smart_chunk_document(self, doc: Document) -> List[Document]:
        """Apply smart chunking strategy based on document type"""
        
        # First, try markdown-aware splitting for .md files
        if doc.metadata.get("source", "").endswith(".md"):
            try:
                md_chunks = self.markdown_splitter.split_text(doc.page_content)
                if len(md_chunks) > 1:
                    # If markdown splitting worked, apply recursive splitting to each chunk
                    all_chunks = []
                    for i, chunk in enumerate(md_chunks):
                        sub_docs = self.text_splitter.create_documents([chunk])
                        for j, sub_doc in enumerate(sub_docs):
                            # Inherit metadata from parent document
                            sub_doc.metadata = doc.metadata.copy()
                            sub_doc.metadata["chunk_id"] = f"{doc.metadata.get('content_hash', '')}_{i}_{j}"
                            sub_doc.metadata["parent_chunk"] = i
                            sub_doc.metadata["sub_chunk"] = j
                            all_chunks.append(sub_doc)
                    return all_chunks
            except Exception as e:
                logger.warning(f"Markdown splitting failed for {doc.metadata.get('source')}: {e}")
        
        # Fallback to recursive splitting
        chunks = self.text_splitter.split_documents([doc])
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"{doc.metadata.get('content_hash', '')}_{i}"
            chunk.metadata["chunk_index"] = i
        
        return chunks

def load_documents_from_folder(folder_path: str, processor: DocumentProcessor) -> List[Document]:
    """Load and process documents from folder with enhanced metadata"""
    documents = []
    failed_files = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()

        try:
            # Load document based on file type
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
            
            # Enhance each document with metadata
            enhanced_docs = []
            for doc in docs:
                enhanced_doc = processor.enhance_document_metadata(doc, filename, file_path)
                enhanced_docs.append(enhanced_doc)
            
            documents.extend(enhanced_docs)
            logger.info(f"✅ Loaded {len(docs)} docs from {filename}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load {filename}: {e}")
            failed_files.append((filename, str(e)))

    if failed_files:
        logger.warning(f"Failed to load {len(failed_files)} files:")
        for filename, error in failed_files:
            logger.warning(f"  - {filename}: {error}")

    return documents

def chunk_documents(documents: List[Document], processor: DocumentProcessor) -> List[Document]:
    """Apply smart chunking to all documents"""
    all_chunks = []
    
    for doc in documents:
        try:
            chunks = processor.smart_chunk_document(doc)
            all_chunks.extend(chunks)
            logger.info(f"Created {len(chunks)} chunks from {doc.metadata.get('source', 'unknown')}")
        except Exception as e:
            logger.error(f"Failed to chunk document {doc.metadata.get('source', 'unknown')}: {e}")
            # Fallback: add original document
            all_chunks.append(doc)
    
    return all_chunks

def deduplicate_chunks(chunks: List[Document]) -> List[Document]:
    """Remove duplicate chunks based on content hash"""
    seen_hashes = set()
    unique_chunks = []
    
    for chunk in chunks:
        # Create hash of chunk content
        chunk_hash = hashlib.md5(chunk.page_content.encode()).hexdigest()
        
        if chunk_hash not in seen_hashes:
            seen_hashes.add(chunk_hash)
            chunk.metadata["chunk_content_hash"] = chunk_hash
            unique_chunks.append(chunk)
    
    removed_count = len(chunks) - len(unique_chunks)
    if removed_count > 0:
        logger.info(f"Removed {removed_count} duplicate chunks")
    
    return unique_chunks

def validate_chunks(chunks: List[Document]) -> List[Document]:
    """Validate and filter chunks"""
    valid_chunks = []
    
    for chunk in chunks:
        # Skip empty or very short chunks
        if len(chunk.page_content.strip()) < 50:
            continue
            
        # Skip chunks that are just headers or metadata
        if len(chunk.page_content.split()) < 10:
            continue
        
        valid_chunks.append(chunk)
    
    removed_count = len(chunks) - len(valid_chunks)
    if removed_count > 0:
        logger.info(f"Filtered out {removed_count} invalid chunks")
    
    return valid_chunks

def get_ingestion_stats(chunks: List[Document]) -> Dict[str, Any]:
    """Generate ingestion statistics"""
    stats = {
        "total_chunks": len(chunks),
        "total_words": sum(len(chunk.page_content.split()) for chunk in chunks),
        "total_chars": sum(len(chunk.page_content) for chunk in chunks),
        "document_types": {},
        "sources": set(),
        "avg_chunk_size": 0,
        "chunks_with_code": 0,
        "chunks_with_api": 0,
        "chunks_with_tables": 0
    }
    
    for chunk in chunks:
        # Document type distribution
        doc_type = chunk.metadata.get("document_type", "unknown")
        stats["document_types"][doc_type] = stats["document_types"].get(doc_type, 0) + 1
        
        # Source files
        stats["sources"].add(chunk.metadata.get("source", "unknown"))
        
        # Feature counts
        if chunk.metadata.get("has_code_examples"):
            stats["chunks_with_code"] += 1
        if chunk.metadata.get("has_api_endpoint"):
            stats["chunks_with_api"] += 1
        if chunk.metadata.get("has_table"):
            stats["chunks_with_tables"] += 1
    
    if stats["total_chunks"] > 0:
        stats["avg_chunk_size"] = stats["total_words"] / stats["total_chunks"]
    
    stats["sources"] = list(stats["sources"])
    
    return stats

if __name__ == "__main__":
    logger.info("🚀 Starting enhanced data ingestion from folder-data/...")
    
    # Initialize document processor
    processor = DocumentProcessor()
    
    # 1. Load documents from folder
    logger.info("📁 Loading documents from folder...")
    documents = load_documents_from_folder("./folder-data", processor)
    logger.info(f"✅ Loaded {len(documents)} documents")

    # 2. Apply smart chunking
    logger.info("✂️ Applying smart chunking strategy...")
    chunks = chunk_documents(documents, processor)
    logger.info(f"✅ Created {len(chunks)} initial chunks")
    
    # 3. Deduplicate chunks
    logger.info("🔍 Deduplicating chunks...")
    chunks = deduplicate_chunks(chunks)
    logger.info(f"✅ {len(chunks)} unique chunks after deduplication")
    
    # 4. Validate chunks
    logger.info("✔️ Validating chunks...")
    chunks = validate_chunks(chunks)
    logger.info(f"✅ {len(chunks)} valid chunks after filtering")

    # 5. Generate statistics
    stats = get_ingestion_stats(chunks)
    logger.info("📊 Ingestion Statistics:")
    logger.info(f"  - Total chunks: {stats['total_chunks']}")
    logger.info(f"  - Total words: {stats['total_words']:,}")
    logger.info(f"  - Average chunk size: {stats['avg_chunk_size']:.1f} words")
    logger.info(f"  - Source files: {len(stats['sources'])}")
    logger.info(f"  - Chunks with code: {stats['chunks_with_code']}")
    logger.info(f"  - Chunks with API endpoints: {stats['chunks_with_api']}")
    logger.info(f"  - Chunks with tables: {stats['chunks_with_tables']}")
    logger.info(f"  - Document types: {stats['document_types']}")

    # 6. Setup Pinecone
    logger.info("🔗 Setting up Pinecone connection...")
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    # 7. Setup embeddings (using the new large model)
    logger.info("🧠 Initializing text-embedding-3-large model...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=os.environ["OPENAI_API_KEY"],
        dimensions=1024  # Optimized dimension for better performance
    )

    # 8. Push to Pinecone with enhanced metadata
    logger.info("⬆️ Uploading to Pinecone vector database...")
    try:
        vectorstore = PineconeVectorStore.from_documents(
            chunks, 
            embeddings, 
            index_name=os.environ["INDEX_NAME_LARGE"]
        )
        logger.info("✅ Successfully uploaded to Pinecone!")
        
        # Log final success message with key metrics
        logger.info("🎉 Enhanced ingestion completed successfully!")
        logger.info(f"📈 Uploaded {len(chunks)} enhanced chunks to {os.environ['INDEX_NAME_LARGE']}")
        logger.info(f"💾 Using text-embedding-3-large model with 1024 dimensions")
        logger.info(f"📚 Processed {len(stats['sources'])} source files")
        
    except Exception as e:
        logger.error(f"❌ Failed to upload to Pinecone: {e}")
        raise
