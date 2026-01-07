# Implementation Plan: Evolutionary AI Platform

## Phase 1: The Brain (Current Focus)
**Goal**: Build the intelligent core that can understand code, user preferences, and manual queries.

### Core Architecture ("The Kernel")
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React + Tailwind (Split View: Chat + Artifacts)
- **Agent Runtime**: LangGraph (Stateful execution)
- **Memory Store**:
    - `Vector` (ChromaDB): Docs, Code, Past Conversations.
    - `SQL` (SQLite): User Profile (Passive Extraction), Action Logs.

### Feature Checklist

#### 1. Core System & Auth
- [ ] **Project Init**: Setup Monorepo (FastAPI + React). <!-- id: 1 -->
- [ ] **Authentication**: JWT-based Auth (Login/Register) to protect Knowledge Base. <!-- id: 2 -->
- [ ] **User Profile DB**: Schema for storing `user_preferences` (e.g., preferred_language, cloud_provider). <!-- id: 3 -->

#### 2. The Chat Interface (Frontend)
- [ ] **Split Layout**: Left=Chat, Right=Context/Preview. <!-- id: 4 -->
- [ ] **Action Cards UI**: Specialized UI components for "Approval Requests" (e.g., [Approve] [Deny]). <!-- id: 5 -->
- [ ] **Artifact Viewer**: Markdown/Code viewer for RAG results. <!-- id: 6 -->

#### 3. Knowledge Ingestion (The Senses)
- [ ] **File Upload API**: Support for `.zip`, `.md`, `.py` uploads. <!-- id: 7 -->
- [ ] **Git Sync Service**: Background worker to `clone/pull` specified Git repos. <!-- id: 8 -->
- [ ] **Ingestion Pipeline**: Text Splitter -> Embedding -> ChromaDB. <!-- id: 9 -->

#### 4. The Agent (The Brain)
- [ ] **Tool Registry**: Implement base tools (`search_knowledge`, `read_file`). <!-- id: 10 -->
- [ ] **Passive Profiler**: Background analysis of chat history to extract User Facts. <!-- id: 11 -->
- [ ] **Permission Layer**: Middleware that intercepts "Side-Effect Tools" and enforces User Approval. <!-- id: 12 -->

---

## Phase 2: The Nervous System (Future AIOps)
**Goal**: Connect "The Brain" to real-time sensors and effectors.

- [ ] **Webhook Receiver**: Prometheus AlertManager endpoint.
- [ ] **Log Streamer**: Connection to ELK/Loki.
- [ ] **K8s Controller**: `kubectl` wrapper tools.
- [ ] **Terraform Manager**: IaC generation and plan review.
