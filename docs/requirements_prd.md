# Product Requirements Document (PRD): Evolutionary AI Platform
# 产品需求文档：进化型 AI 平台

## 1. Executive Summary (项目概述)
This project aims to build a dual-phase AI platform: starting as a **Personal Knowledge Assistant (Phase 1)** and evolving into an autonomous **AIOps Engineering Agent (Phase 2)**.
本项目旨在构建一个双阶段 AI 平台：初期作为**个人知识与技术助手（第一阶段）**，随后演进为具备自主能力的**AIOps 运维工程师 Agent（第二阶段）**。

## 2. Phase 1: The Intelligent Brain (核心：智慧大脑)
**Goal**: Solve the "Information Silo" and "Context Loss" problems for developers.
**目标**：解决开发者的“信息孤岛”与“上下文丢失”问题。

| ID | Feature (功能) | Description (描述) | Impact (价值) |
| :--- | :--- | :--- | :--- |
| **1.1** | **Multi-Source RAG** | Ingest Code (AST-aware), Markdown (Obsidian links), and Web URLs. | "Second Brain" recall. |
| **1.2** | **Hybrid Memory** | **Semantic**: SQL-based User Profile (e.g., "User prefers Python").<br>**Episodic**: Vector-based recall of past conversations. | Personalized, context-aware answers. |
| **1.3** | **Knowledge Gardener** | Background worker that dedupes, merges, and updates stale notes. | Keeps knowledge base significantly healthier. |
| **1.4** | **Architecture Auditor** | Validates new code/designs against *past failures* (Post-Mortems). | Proactive risk prevention. |

## 3. Phase 2: The Nervous System (演进：AIOps 神经系统)
**Goal**: Close the loop between "Monitoring" and "Fixing".
**目标**：打通“监控发现”到“故障修复”的闭环。

| ID | Module (模块) | Integrations (集成) | Workflow (工作流) |
| :--- | :--- | :--- | :--- |
| **2.1** | **Sensors (Eyes)** | **Prometheus**: AlertManager Webhook.<br>**Logs**: ELK / Loki API. | "Alert detected -> Query Logs -> AI Diagnosis" |
| **2.2** | **Effectors (Hands)** | **Kubernetes/EKS**: Pod/Deployment control.<br>**SSH/Shell**: Safe command execution. | "Diagnosis -> Recommend Fix (Restart/Scale) -> Human Approve -> Execute" |
| **2.3** | **Infrastructure (IaC)** | **Terraform**: Alibaba Cloud / AWS Providers. | "Requirement -> Gen TF Code -> **Auditor Check** -> Apply" |

## 4. The Self-Learning Loop (核心差异化：自学习闭环)
**Concept**: The system gets smarter with every incident.
1.  **Incident Resolution**: User marks an operational issue as "Fixed".
2.  **Auto-PostMortem**: Agent allows logs, chat history, and actions into a markdown case study.
3.  **Write-Back**: The case study is indexed into the Knowledge Base.
4.  **Future Impact**: Next time, the **Architecture Auditor** uses this case to warn about similar patterns.

## 5. User Interface (交互界面)
*   **Chat Mode**: Standard conversational UI for queries and coding assistance.
*   **War Room (作战室)**: A split-screen Mode for incidents.
    *   *Left*: Real-time Log Stream & Metric Charts.
    *   *Right*: AI Copilot actively analyzing the stream.

## 6. Non-Functional Requirements (非功能需求)
*   **Security**: Strict "Human-in-the-Loop" for any state-changing Ops (Write/Delete/Resrtart).
*   **Stack**: FastAPI (Backend), React (Frontend), LangGraph (Agent State), ChromaDB (Vector), SQLite (Relational).

---
*This document serves as the single source of truth for the project scope.*
*本文档作为项目范围的唯一事实来源。*
