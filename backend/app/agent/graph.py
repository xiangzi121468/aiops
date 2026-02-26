from typing import Any, Dict, List, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from app.agent.llm import get_llm
from app.memory.service import recall_episodic, recall_semantic
from app.retrieval.hybrid import hybrid_search


class AgentState(TypedDict):
    query: str
    top_k: int
    retrieved: List[Dict[str, Any]]
    semantic_memories: List[Dict[str, Any]]
    episodic_memories: List[Dict[str, Any]]
    answer: str


def _serialize_semantic(rows) -> List[Dict[str, Any]]:
    return [
        {
            "key": row.key,
            "value": row.value,
            "confidence": row.confidence,
            "source": row.source,
        }
        for row in rows
    ]


def _serialize_episodic(rows) -> List[Dict[str, Any]]:
    return [{"content": row.content, "metadata_json": row.metadata_json} for row in rows]


def build_graph(db: Session):
    def retrieve_node(state: AgentState) -> AgentState:
        retrieved = hybrid_search(db=db, query=state["query"], top_k=state["top_k"])
        state["retrieved"] = retrieved
        return state

    def memory_node(state: AgentState) -> AgentState:
        semantic_rows = recall_semantic(db=db, query=None, limit=5)
        episodic_rows = recall_episodic(db=db, limit=5)
        state["semantic_memories"] = _serialize_semantic(semantic_rows)
        state["episodic_memories"] = _serialize_episodic(episodic_rows)
        return state

    def answer_node(state: AgentState) -> AgentState:
        llm = get_llm()
        if not llm:
            state["answer"] = (
                "LLM not configured. Retrieved "
                f"{len(state['retrieved'])} docs, "
                f"{len(state['semantic_memories'])} semantic memories, "
                f"{len(state['episodic_memories'])} episodic memories."
            )
            return state

        context_lines = []
        for idx, doc in enumerate(state["retrieved"][:5]):
            context_lines.append(f"[Doc {idx + 1}] {doc['content']}")
        for idx, mem in enumerate(state["semantic_memories"][:5]):
            context_lines.append(f"[Semantic {idx + 1}] {mem['key']}: {mem['value']}")
        for idx, mem in enumerate(state["episodic_memories"][:3]):
            context_lines.append(f"[Episodic {idx + 1}] {mem['content']}")

        system_prompt = (
            "You are an AIOps assistant. Answer concisely and cite relevant context."
        )
        human_prompt = (
            f"Query: {state['query']}\n\nContext:\n" + "\n".join(context_lines)
        )
        response = llm.invoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
        )
        state["answer"] = response.content
        return state

    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("memory", memory_node)
    graph.add_node("answer", answer_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "memory")
    graph.add_edge("memory", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
