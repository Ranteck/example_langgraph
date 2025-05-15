import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document
from typing import List, Dict, Any, TypedDict
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()

embedding_model = os.environ.get("EMBEDDING_MODEL")
book_url = os.environ.get("BOOK_URL")

class VectorStoreManager:
    def __init__(self, persist_path: str = "faiss_index"):
        self.persist_path = persist_path
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectorstore = None

    def load_documents(self, docs_path: str) -> List[Document]:
        if docs_path is None:
            raise ValueError("docs_path cannot be None. Please provide a valid file path.")
        if docs_path.lower().endswith('.pdf'):
            loader = PyPDFLoader(docs_path)
        else:
            loader = TextLoader(docs_path)
        return loader.load()

    def build_vectorstore(self, documents: List[Document]):
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        self.vectorstore.save_local(self.persist_path)

    def load_vectorstore(self):
        self.vectorstore = FAISS.load_local(self.persist_path, self.embeddings)

    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        if not self.vectorstore:
            self.load_vectorstore()
        return self.vectorstore.similarity_search(query, k=k)

    def add_book_from_url(self, url: str = None, local_path: str = None):
        """
        Descarga un libro desde una URL (PDF o TXT), lo guarda localmente, lo carga y lo indexa.
        Si no se pasa url, usa BOOK_URL global.
        """
        if url is None and not book_url:
            raise ValueError("No URL provided and book_url is not set.")
        if url is None:
            url = book_url
        if not local_path:
            if url is None:
                raise ValueError("URL cannot be None when determining file extension.")
            ext = url.split('.')[-1].split('?')[0].lower()
            local_path = f"downloaded_book.{ext}"
        # Sanitize local_path to prevent path traversal
        local_path = os.path.basename(local_path)

        # Detect if url is a remote URL or a local file
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https"):
            response = requests.get(url)
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                f.write(response.content)
        else:
            # Local file: just use the path directly
            local_path = url

        documents = self.load_documents(local_path)
        self.build_vectorstore(documents)
        return local_path