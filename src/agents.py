import os
from typing import Dict

# Variables de entorno globales para el modelo LLM
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

# Simulate a simple keyword-based planner
RETRIEVAL_KEYWORDS = ["find", "search", "retrieve", "context", "information", "explain", "details"]


def planner_agent(state: Dict) -> Dict:
    query = state.get("query", "")
    if any(keyword in query.lower() for keyword in RETRIEVAL_KEYWORDS):
        state["planner_decision"] = "retrieve"
        return {**state, "_next": "retrieve"}
    else:
        state["planner_decision"] = "direct"
        return {**state, "_next": "direct"}


def rewriter_agent(state: Dict) -> Dict:
    query = state.get("query", "")
    reformulated_query = f"[REFORMULATED] {query}"
    state["rewritten_query"] = reformulated_query
    return {**state, "query": reformulated_query}


def retriever_agent(state: Dict) -> Dict:
    # Simulate retrieval (replace with real vectorstore in production)
    query = state.get("query", "")
    retrieved_docs = [f"Relevant doc for: {query}"]
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
    if llm:
        prompt = f"Pregunta: {query}\nContexto: {context[0] if context else ''}\nRespuesta:"
        answer = llm.invoke(prompt)
        state["answer"] = answer
    else:
        if context:
            answer = f"Synthesized answer for '{query}' with context: {context[0]}"
        else:
            answer = f"Direct answer for '{query}'"
        state["answer"] = answer
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