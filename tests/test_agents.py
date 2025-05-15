import pytest
from src.agents import planner_agent, rewriter_agent, retriever_agent, synthesizer_agent, critic_agent

def test_planner_agent():
    state = {"query": "What is RAG?"}
    result = planner_agent(state)
    assert isinstance(result, dict)

def test_rewriter_agent():
    state = {"query": "What is RAG?"}
    result = rewriter_agent(state)
    assert isinstance(result, dict)

def test_retriever_agent():
    state = {"query": "What is RAG?"}
    result = retriever_agent(state)
    assert isinstance(result, dict)

def test_synthesizer_agent():
    state = {"query": "What is RAG?"}
    result = synthesizer_agent(state)
    assert isinstance(result, dict)

def test_critic_agent():
    state = {"query": "What is RAG?"}
    result = critic_agent(state)
    assert isinstance(result, dict) 