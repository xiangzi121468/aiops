# 架构与设计规范：进化型 AIOps 智能体

## 1. 项目愿景
构建一个 **双阶段智能平台**：
1.  **第一阶段（大脑）**：个人知识库与技术助手。它能从用户的代码库和偏好中学习，成为一个“懂你”的副驾驶。
2.  **第二阶段（双手）**：自主化 AIOps Agent。具备实时监控、故障诊断和运维修复能力，并拥有“自我学习闭环”。

## 2. 核心需求

### 2.1 功能性需求
*   **多源 RAG (检索增强)**：支持摄入并检索 本地代码、Markdown 笔记 以及 网页链接。
*   **混合记忆 (Hybrid Memory)**：
    *   *情景记忆 (Episodic)*：基于向量 (Vector) 检索过去的对话历史和类似案例。
    *   *语义记忆 (Semantic)*：基于结构化 SQL 存储用户画像（User Profile），例如“显式偏好：使用 Python 3.10”。
*   **基础设施即代码 (IaC Capabilities)**：
    *   集成 **Terraform**：支持 Alibaba Cloud 及多云 Provider 的声明式管理。
    *   Agent 具备生成 `.tf` 代码、执行 `terraform plan` 并进行安全审计的能力。
*   **主动工具调用 (Active Tool Use)**：Agent 必须通过“工具 (Tools)”与外部交互（搜索、读文件，以及未来的系统操作），严禁在 Prompt 中硬编码逻辑。
*   **自我学习闭环 (Self-Learning Loop)**：当一个运维问题被标记为“已解决”时，系统必须自动总结案例并写回知识库。
*   **高阶业务模块**:
    *   **架构审计员 (The Auditor)**：基于历史故障库，对新代码/设计进行事前风控。
    *   **知识园丁 (The Gardener)**：后台定期去重、优化、更新知识库内容。
    *   **作战室 (War Room)**：实时日志监控与 AI 诊断并行的仪表盘视图。

### 2.2 安全与 AIOps 特性
*   **人机回环 (Human-in-the-Loop)**：高风险操作（如 `restart_service`）必须经过 UI 弹窗确认。
*   **白名单机制 (Allowlist)**：严格控制可执行的系统命令范围。

## 3. 系统架构

### 3.1 逻辑架构图 (Mermaid)

```mermaid
graph TD
    subgraph "感知层 (Sensors)"
        U[用户对话] --> Router
        W[Webhook / 报警] --> Router
    end

    subgraph "核心层 (Agent Runtime)"
        Router{路由分发}
        Router -- "查询" --> Agent[LangGraph 智能体]
        
        Agent <-->|读/写| MEM_ST[短时记忆]
        Agent <-->|检索| MEM_EP[情景记忆 (Vector)]
        Agent <-->|画像| MEM_SEM[语义记忆 (SQL)]
    end

    subgraph "执行层 (Tools Layer)"
        Agent -- "调用" --> T_RAG[RAG 搜索工具]
        Agent -- "调用" --> T_SYS[K8s/EKS 控制器]
        Agent -- "调用" --> T_LOG[日志查询器]
        Agent -- "调用" --> T_IAC[Terraform 管理器]
        Agent -- "调用" --> T_LEARN[知识回写工具]
    end

    subgraph "外部世界"
        T_RAG --> KB[(知识库)]
        T_SYS --> K8S[EKS/Kubernetes]
        T_LOG --> LOGS[ELK/Loki]
        T_IAC --> CLOUD[阿里云/AWS]
        T_LEARN --> KB
    end

    subgraph "反馈闭环"
        INFRA -.->|日志/状态| W
        Agent -.->|复盘总结| T_LEARN
    end
```

### 3.2 关键组件
1.  **编排器 (LangGraph)**：
    *   管理对话和诊断的状态机。
    *   决策循环：`检索` -> `规划` -> `执行工具` -> `验证` -> `输出结果`。
2.  **存储层**:
    *   **ChromaDB (向量)**：存储代码块、笔记片段，以及*历史解决案例*。
    *   **SQLite (关系型)**：存储用户画像、会话日志和审计记录。

## 4. 工作流

### 4.1 自我学习闭环 (The Self-Learning Loop)
1.  **触发**：用户标记某个问题为“已解决”。
2.  **动作**：Agent 触发 `CaseSummarizer` 工具。
3.  **处理**：
    *   聚合对话历史。
    *   提取：`故障现象`, `根本原因`, `解决方案`, `执行的命令`。
    *   生成：标准化的 Markdown 复盘文档 (Post-Mortem)。
4.  **存储**：将文档 Embed 到向量库，并将原文件存入 `knowledge/cases/` 目录。
5.  **收益**：下次遇到类似问题，RAG 会优先检索到这个案例。

### 4.2 AIOps 执行流程 (未来规划)
1.  **报警**：Prometheus 发送 JSON 到 `/webhook/alert`。
2.  **查询**：Agent 在向量库中搜索“服务 X 高延迟”。
3.  **规划**：找到运维手册 (Runbook) -> “检查数据库连接”。
4.  **行动**：调用 `check_db_status()` 工具。
5.  **报告**：将诊断结果推送到用户聊天界面，等待修复授权。

## 5. 技术栈
*   **语言**: Python 3.11+
*   **Web 框架**: FastAPI
*   **前端**: React + TailwindCSS (Vite)
*   **LLM 编排**: LangChain / LangGraph
*   **向量数据库**: ChromaDB (本地持久化)
*   **应用数据库**: SQLite
