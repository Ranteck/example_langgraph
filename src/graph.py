from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, List, Any, Optional
from typing_extensions import TypedDict
from src.agents import planner_agent, rewriter_agent, retriever_agent, synthesizer_agent, critic_agent

# Estado global para chat multi-turno
class ChatState(TypedDict):
    messages: Annotated[List, add_messages]

# Estado global para RAG multi-agente con memoria conversacional
class RAGState(TypedDict, total=False):
    query: str
    planner_decision: str
    rewritten_query: str
    retrieved_docs: List[str]
    answer: str
    critic_decision: str
    _next: str
    messages: List[str]

# Nodo de chat que procesa el historial de mensajes
# Usa el synthesizer_agent para generar la respuesta

def chatbot(state: ChatState):
    # El último mensaje del usuario está en state["messages"][-1]
    # El agente debe generar una respuesta y agregarla a la lista
    response_state = synthesizer_agent({"query": state["messages"][-1]})
    answer = response_state.get("answer", "No se encontró respuesta.")
    return {"messages": state["messages"] + [answer]}

def build_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("chatbot", chatbot)
    graph.add_edge(START, "chatbot")
    graph.add_conditional_edges("chatbot", lambda state: END)
    return graph

# Función de condición para el planificador
def planner_condition(state: RAGState):
    if state.get("planner_decision") == "retrieve":
        return "RewriterAgent"
    return "SynthesizerAgent"

# Función de condición para el crítico
def critic_condition(state: RAGState):
    if state.get("critic_decision") == "refine":
        return "RetrieverAgent"
    return END

# Construcción del grafo multi-agente RAG
def build_rag_graph():
    graph = StateGraph(RAGState)
    graph.add_node("PlannerAgent", planner_agent)
    graph.add_node("RewriterAgent", rewriter_agent)
    graph.add_node("RetrieverAgent", retriever_agent)
    graph.add_node("SynthesizerAgent", synthesizer_agent)
    graph.add_node("CriticAgent", critic_agent)
    graph.add_conditional_edges("PlannerAgent", planner_condition)
    graph.add_edge("RewriterAgent", "RetrieverAgent")
    graph.add_edge("RetrieverAgent", "SynthesizerAgent")
    graph.add_edge("SynthesizerAgent", "CriticAgent")
    graph.add_conditional_edges("CriticAgent", critic_condition)
    graph.add_edge(START, "PlannerAgent")
    return graph

# Ciclo de chat multi-turno usando el pipeline multi-agente y memoria conversacional
def debug_run():
    graph = build_rag_graph().compile()
    state = {"messages": []}
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Adiós!")
            break
        state["query"] = user_input
        state["messages"].append(f"Usuario: {user_input}")
        result = graph.invoke(state)
        answer = result.get("answer", "No se encontró respuesta.")
        print("Bot:", answer)
        state = result
        state["messages"].append(f"Bot: {answer}") 