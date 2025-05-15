import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document
from typing import List, Dict, Any, TypedDict
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
import ipaddress
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
        def is_safe_url(url):
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                return False  # Not a remote URL
            hostname = parsed.hostname
            try:
                ip = ipaddress.ip_address(hostname)
                if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                    return False
            except ValueError:
                if hostname in ("localhost", "127.0.0.1", "::1"):
                    return False
            return True

        if url is None and not book_url:
            raise ValueError("No URL provided and book_url is not set.")
        if url is None:
            url = book_url

        parsed = urlparse(url)
        if parsed.scheme in ("http", "https"):
            if not is_safe_url(url):
                raise ValueError("Unsafe URL: points to a local/private address.")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if not local_path:
                ext = url.split('.')[-1].split('?')[0].lower()
                local_path = f"downloaded_book.{ext}"
            local_path = os.path.basename(local_path)
            with open(local_path, 'wb') as f:
                f.write(response.content)
        elif os.path.isfile(url):
            local_path = url
        else:
            raise ValueError("Invalid file path or URL.")

        documents = self.load_documents(local_path)
        self.build_vectorstore(documents)
        return local_path