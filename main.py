from src.vectorstore import VectorStoreManager
from src.graph import debug_run

# Descarga e indexa el libro desde la URL global (BOOK_URL en vectorstore.py)
vector_manager = VectorStoreManager()
vector_manager.add_book_from_url()  # Esto descarga, procesa e indexa el libro

# Realiza una consulta al sistema RAG
respuesta = debug_run("¿Quién es el personaje principal?")
print("\nRespuesta generada:")
print(respuesta.get("answer", "No se encontró respuesta.")) 