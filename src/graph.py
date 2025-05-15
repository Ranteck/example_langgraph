from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, List
from typing_extensions import TypedDict
from src.agents import synthesizer_agent

# Estado global para chat multi-turno
class ChatState(TypedDict):
    messages: Annotated[List, add_messages]

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

def debug_run():
    graph = build_chat_graph().compile()
    state = {"messages": []}
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Adiós!")
            break
        state["messages"].append(user_input)
        result = graph.invoke(state)
        # La respuesta del bot es el último mensaje
        bot_response = result["messages"][-1]
        print("Bot:", bot_response)
        state = result 