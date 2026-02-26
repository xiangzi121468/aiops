# AIOps 进化平台

> **从个人知识助手到自主运维工程师**

这是一个进化型的 AI 平台，旨在从“第二大脑”（个人知识库）起步，最终进化为能够自动诊断和修复基础设施问题的“AIOps 智能体”。

## 🚀 愿景 (Vision)

本项目遵循双阶段演进路线：

1.  **第一阶段：大脑 (Phase 1: The Brain) —— 当前重心**
    *   **目标**：解决开发者的“上下文切换”成本和“信息孤岛”问题。
    *   **核心**：基于 RAG（检索增强生成）的助手，能够深度理解你的代码、文档和偏好。
    *   **关键特性**：**被动画像 (Passive Profiling)** —— AI 会从日常对话中自动提取并记住你的技术栈和习惯（如“偏好 Python 3.11”）。

2.  **第二阶段：神经系统 (Phase 2: The Nervous System) —— 未来规划**
    *   **目标**：实现自主化运维 (Autonomous Operations)。
    *   **核心**：集成 Prometheus、Kubernetes 和 Cloud API。
    *   **关键特性**：**自学习闭环 (Self-Learning Loop)** —— 已解决的故障会被自动总结为“复盘报告 (Post-Mortem)”，并回写到大脑中，指导未来的故障处理。

## ✨ 核心特性

*   **双栏交互界面 (Split-View Interface)**：左侧对话，右侧展示上下文/制品（代码预览、文档原文）。
*   **主动工具调用 (Active Tool Use)**：智能体不仅仅是聊天，它能通过调用工具（Tools）实际执行任务。
*   **混合记忆体系 (Hybrid Memory)**：
    *   *情景记忆 (Episodic)*：基于向量库，记住过去的对话和案例。
    *   *语义记忆 (Semantic)*：基于 SQL 结构化存储用户画像。
*   **长记忆治理**：写入触发、召回优先级、生命周期与审批机制。
*   **Git 知识同步 (Git-Sync)**：直接连接 GitHub/GitLab 仓库，保持知识库与代码库实时同步。
*   **人机回环 (Human-in-the-Loop)**：采用“激进”的自主模式，但在执行敏感操作（如重启服务）前，必须弹窗请求用户“批准/拒绝”。

## 🛠 技术栈

*   **后端**: Python 3.11+, FastAPI, LangGraph (Agent 编排)
*   **前端**: React, TailwindCSS, Vite
*   **数据存储**: ChromaDB (向量), SQLite (关系型)
*   **部署**: Docker / K8s (服务端架构)

## 📂 项目结构

```bash
.
├── backend/        # FastAPI 应用与 Agent 逻辑
├── frontend/       # React 单页应用
├── docs/           # 架构设计与规划文档
└── data/           # 数据持久化目录 (Gitignored)
```

## 🚦 快速开始

### 前置要求
*   Docker & Docker Compose
*   Python 3.11+ (本地开发)
*   Node.js 18+ (本地开发)

### 本地运行 (Local)

*(即将推出)*

## ✅ 测试流程（MVP）

1) 启动后端：`uvicorn app.main:app --reload`  
2) 文本入库（知识采集）：
```
curl -X POST http://localhost:8000/api/v1/ingest/text ^
  -H "Content-Type: application/json" ^
  -d "{\"source\":\"docs/demo.md\",\"content\":\"AIOps is about monitoring and automation.\"}"
```
3) 混合检索：
```
curl -X POST http://localhost:8000/api/v1/retrieve/hybrid ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"monitoring automation\",\"top_k\":5}"
```
4) 记忆写入/召回：
```
curl -X POST http://localhost:8000/api/v1/memory/record ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"semantic\",\"key\":\"preferred_language\",\"value\":\"Python\"}"

curl -X POST http://localhost:8000/api/v1/memory/recall ^
  -H "Content-Type: application/json" ^
  -d "{\"type\":\"semantic\",\"query\":\"preferred\",\"limit\":5}"
```
5) 检索评估：
```
curl -X POST http://localhost:8000/api/v1/evaluate/retrieval ^
  -H "Content-Type: application/json" ^
  -d "{\"items\":[{\"query\":\"monitoring\",\"expected\":\"automation\"}],\"top_k\":5}"
```
6) LangGraph Agent 运行：
```
curl -X POST http://localhost:8000/api/v1/agent/run ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"AIOps 的核心是什么\",\"top_k\":5}"
```

## 🧪 UI 接入（本地测试页）

```
cd frontend
python -m http.server 5173
```
浏览器打开 `http://localhost:5173`，即可进行知识采集/检索/记忆与评估的基础操作。

## 📄 文档索引

*   [实施计划 (Implementation Plan)](./docs/实施计划.md)
*   [架构设计 (Architecture Design)](./docs/架构设计.md)
*   [产品需求 (PRD)](./docs/产品需求.md)
*   [上下文记忆工程](./docs/形成上下文记忆工程.md)
*   [AIOps 运维模板](./docs/AIOps运维模板.md)

## 🗺️ 路线图

### M1：基础闭环（2 周）
- 完成：知识采集流水线、基础检索、会话编减、基本权限与审计
- 交付：可用的检索问答 + 最小合规模块（脱敏/审计）
- 验收：检索命中率与处理时长可观测；审计可追溯

### M2：运维上下文与自动化雏形（2-3 周）
- 完成：运维模板字段采集、告警/日志/拓扑聚合、动作建议
- 交付：运维问题的结构化上下文与处置建议
- 验收：运维模板字段完整、动作建议可追踪

### M3：隔离与可靠性增强（2 周）
- 完成：多租户隔离、降级策略、审批机制
- 交付：权限与审批闭环、故障回退路径
- 验收：跨租户不可见、审批超时回退生效

### M4：性能与可观测性（持续）
- 完成：索引优化、缓存、压测、容量规划
- 交付：性能基线与成本统计
- 验收：检索延迟目标满足；Embedding 调用成本可统计

## 🤝 贡献指南

1.  Fork 本仓库
2.  创建特性分支 (`git checkout -b feature/amazing-feature`)
3.  提交更改 (`git commit -m 'Add some amazing feature'`)
4.  推送到分支 (`git push origin feature/amazing-feature`)
5.  发起 Pull Request

## 📜 许可证

[MIT](LICENSE)

