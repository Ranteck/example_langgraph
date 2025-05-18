import os
from typing import Dict
from src.vectorstore import VectorStoreManager

# Variables de entorno globales para el modelo LLM
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

# Simulate a simple keyword-based planner
RETRIEVAL_KEYWORDS = ["find", "search", "retrieve", "context", "information", "explain", "details"]

# Inicializa el vector_manager globalmente para uso en los agentes
vector_manager = VectorStoreManager()
try:
    vector_manager.load_vectorstore()
except Exception:
    pass


def planner_agent(state: Dict) -> Dict:
    # Siempre forzar recuperación para cualquier pregunta
    state["planner_decision"] = "retrieve"
    return {**state, "_next": "retrieve"}


def rewriter_agent(state: Dict) -> Dict:
    query = state.get("query", "")
    reformulated_query = f"[REFORMULATED] {query}"
    state["rewritten_query"] = reformulated_query
    return {**state, "query": reformulated_query}


def retriever_agent(state: Dict) -> Dict:
    query = state.get("query", "")
    if "rewritten_query" in state:
        query = state["rewritten_query"]
    retrieved_docs = [doc.page_content for doc in vector_manager.retrieve(query)]
    state["retrieved_docs"] = retrieved_docs
    return state


# --- LLM Integration for Synthesizer Agent ---
try:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
except ImportError:
    llm = None

def synthesizer_agent(state: Dict) -> Dict:
    query = state.get("query", "")
    context = state.get("retrieved_docs", [])
    if context:
        joined_context = "\n\n".join(context)
        prompt = (
            f"Responde la siguiente pregunta SOLO usando la información del contexto proporcionado.\n"
            f"Pregunta: {query}\n"
            f"Contexto:\n{joined_context}\n"
            f"Respuesta:"
        )
    else:
        prompt = (
            f"No se encontró información relevante en el documento para la pregunta: {query}"
        )
    if llm and context:
        answer = llm.invoke(prompt)
        # Si la respuesta es un objeto con 'content', extraer solo el texto
        if hasattr(answer, 'content'):
            state["answer"] = answer.content
        else:
            state["answer"] = str(answer)
    else:
        state["answer"] = prompt
    return state


def critic_agent(state: Dict) -> Dict:
    answer = state.get("answer", "")
    # Simulate critic: if answer contains 'context', require refinement
    if "context" in answer and "enough" not in answer:
        state["critic_decision"] = "refine"
        return {**state, "_next": "refine"}
    else:
        state["critic_decision"] = "satisfactory"
        return {**state, "_next": "satisfactory"} 