from src.vectorstore import VectorStoreManager
from src.graph import debug_run
import os

# Descarga e indexa el libro desde la URL global (BOOK_URL en vectorstore.py)
book_url = os.environ.get("BOOK_URL")
if not book_url or book_url.strip() == "":
    book_url = input("Por favor, ingresa la URL o ruta local del libro a indexar: ").strip()
    os.environ["BOOK_URL"] = book_url

vector_manager = VectorStoreManager()
vector_manager.add_book_from_url(url=book_url)  # Descarga, procesa e indexa el libro para el pipeline multi-agente

# Inicia el chat multi-turno con memoria y recuperación real
debug_run() 