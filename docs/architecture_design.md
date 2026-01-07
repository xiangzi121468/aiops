# Architecture & Design Specification: Evolutionary AIOps Agent

## 1. Project Vision
To build a **Dual-Phase Intelligence Platform**:
1.  **Phase 1 (The Brain)**: A Personal Knowledge Base & Technical Assistant that learns from user preferences and codebases.
2.  **Phase 2 (The Hands)**: An Autonomous AIOps Agent capable of real-time monitoring, diagnosis, and operational remediation with a self-learning loop.

## 2. Core Requirements

### 2.1 Functional Requirements
*   **Multi-Source RAG**: Ingest and retrieve from Local Code, Markdown Notes, and Web URLs.
*   **Hybrid Memory**:
    *   *Episodic*: Vector-based recall of past conversations/problems.
    *   *Semantic*: Structured User Profile (SQL) for storing explicit preferences (e.g., "Use Python 3.10").
*   **Active Tool Use**: The Agent must use specific "Tools" for all external interactions (Search, Read File, and later System Ops).
*   **Self-Learning Loop**: Successfully resolved operational cases must be automatically summarized and written back to the Knowledge Base.

### 2.2 Security & Safety (AIOps)
*   **Human-in-the-Loop**: High-risk actions (e.g., `restart_service`) require comprehensive UI confirmation.
*   **Tool Allowlist**: Strict control over which system commands can be executed.

## 3. System Architecture

### 3.1 Logical Architecture (Mermaid)

```mermaid
graph TD
    subgraph "Sensors (Inputs)"
        U[User Chat] --> Router
        W[Webhook / Alert] --> Router
    end

    subgraph "The Core (Agent Runtime)"
        Router{Router}
        Router -- "Query" --> Agent[LangGraph Agent]
        
        Agent <-->|Read/Write| MEM_ST[Short Term Mem]
        Agent <-->|Retrieval| MEM_EP[Episodic Mem (Vector)]
        Agent <-->|Profile| MEM_SEM[User Profile (SQL)]
    end

    subgraph "Effectors (Tools Layer)"
        Agent -- "Call" --> T_RAG[RAG Search Tool]
        Agent -- "Call" --> T_SYS[System Ops Tool]
        Agent -- "Call" --> T_LEARN[Knowledge Writer]
    end

    subgraph "The World"
        T_RAG --> KB[(Knowledge Base)]
        T_SYS --> INFRA[Server / Cloud]
        T_LEARN --> KB
    end

    subgraph "Feedback Loop"
        INFRA -.->|Logs/Status| W
        Agent -.->|Post-Mortem| T_LEARN
    end
```

### 3.2 Key Components
1.  **Orchestrator (LangGraph)**:
    *   Manages the state of the conversation/diagnosis.
    *   Decides loop steps: `Retrieve` -> `Plan` -> `Execute Tool` -> `Verify` -> `Result`.
2.  **Memory Store**:
    *   **ChromaDB (Vector)**: Stores code chunks, note segments, and *past resolved cases*.
    *   **SQLite (Relational)**: Stores User Profiles, Session Logs, and Audit Trails.

## 4. Workflows

### 4.1 The Self-Learning Loop
1.  **Trigger**: User marks an issue as "Resolved".
2.  **Action**: Agent triggers `CaseSummarizer` utility.
3.  **Process**:
    *   Aggregates conversation history.
    *   Extracts: `Issue`, `Root Cause`, `Resolution`, `Command Used`.
    *   Generates: A standard Markdown Post-Mortem.
4.  **Storage**: Metadata -> VectorDB. File -> `knowledge/cases/`.
5.  **Benefit**: Future queries hit this exact case first.

### 4.2 AIOps Execution (Future)
1.  **Alert**: Prometheus sends JSON to `/webhook/alert`.
2.  **Lookup**: Agent queries VectorDB for "High latency on Service X".
3.  **Plan**: Finds Runbook -> "Check DB Connection".
4.  **Action**: Calls `check_db_status()` tool.
5.  **Report**: Pushes finding to User Chat awaiting approval for fix.

## 5. Technology Stack
*   **Language**: Python 3.11+
*   **API Framework**: FastAPI
*   **Frontend**: React + TailwindCSS (Vite)
*   **LLM Orchestration**: LangChain / LangGraph
*   **Vector DB**: ChromaDB (Local persistence)
*   **Relational DB**: SQLite
