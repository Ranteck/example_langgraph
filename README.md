# Multi-Agent RAG System (LangGraph)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system using collaborative agents and LangGraph. The system interprets user queries, retrieves relevant information, synthesizes answers, and iterates for clarity.

## Architecture

- **PlannerAgent**: Decides if the query is direct or requires retrieval.
- **RewriterAgent**: Reformulates the query for better retrieval.
- **RetrieverAgent**: Searches for relevant information in a vector store (FAISS).
- **SynthesizerAgent**: Generates answers using context and the query.
- **CriticAgent**: Evaluates if the answer is sufficient; can trigger further retrieval if needed.

## Workflow

1. User query enters the system.
2. PlannerAgent decides the flow.
3. If retrieval is needed, RewriterAgent and RetrieverAgent are invoked.
4. SynthesizerAgent generates a response.
5. CriticAgent evaluates the response and may loop back for more context.

## Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your documents:**
   - Place your text documents in a directory or specify their path.
   - Use the `VectorStoreManager` in `src/vectorstore.py` to load and index your documents with FAISS.

3. **Run the RAG workflow:**
   - Use the `build_rag_graph()` and `debug_run(query)` functions in `src/graph.py` to process queries and inspect the agent state transitions.
   - Example:

     ```python
     from src.graph import debug_run
     debug_run("Find information about LangGraph architecture")
     ```

4. **Visualize the agent graph:**
   - Generate a PNG of the workflow graph:

     ```python
     from src.graph import draw_graph_png
     draw_graph_png()
     # This will create 'multi_agent_rag.png' in your working directory.
     ```

## Agent Responsibilities

- **PlannerAgent:** Analyzes the query and decides if it can be answered directly or requires retrieval.
- **RewriterAgent:** Reformulates ambiguous or complex queries to optimize retrieval.
- **RetrieverAgent:** Retrieves relevant documents from the FAISS vector store.
- **SynthesizerAgent:** Synthesizes a response using the query and retrieved context.
- **CriticAgent:** Evaluates the response; if insufficient, triggers another retrieval/synthesis loop.

## Notes

- Edge cases (ambiguous or incomplete queries) are handled in the agent logic.
- No unit tests are included by user request.
- All project rules and guidelines are in the `cursor_project_rules` folder.
