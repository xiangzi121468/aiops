# AIOps 运维模板（字段 + 示例）

以下模板面向 K8s / DevOps / 监控告警场景，包含字段定义与示例，适合用于上下文压缩、检索与分析。

## 模板字段（建议结构）

### 1) 基础元信息
```yaml
元信息:
  事件编号: "<INCIDENT_ID>"
  发生时间: "<ISO-8601>"
  级别: "P0|P1|P2|P3"
  来源: "prometheus|loki|apm|manual"
  环境: "prod|staging|dev"
  平台版本: "<VERSION>"
```

### 2) 系统与资源上下文
```yaml
上下文:
  集群:
    名称: "<CLUSTER_NAME>"
    版本: "<K8S_VERSION>"
    区域: "<REGION>"
  命名空间: "<NAMESPACE>"
  工作负载:
    类型: "Deployment|StatefulSet|DaemonSet|Job"
    名称: "<WORKLOAD_NAME>"
    Pod: "<POD_NAME>"
    节点: "<NODE_NAME>"
```

### 3) 监控指标
```yaml
指标:
  CPU:
    使用率: <NUMBER>
    限制率: <NUMBER>
  内存:
    使用量MB: <NUMBER>
    限制MB: <NUMBER>
    使用率: <NUMBER>
  磁盘:
    IO等待ms: <NUMBER>
  网络:
    下行MBps: <NUMBER>
    上行MBps: <NUMBER>
  QPS: <NUMBER>
  错误率: <NUMBER>
```

### 4) 日志信息
```yaml
日志:
  - "<关键日志片段_1>"
  - "<关键日志片段_2>"
```

### 5) 事件与告警
```yaml
事件告警:
  - 名称: "<ALERT_NAME>"
    级别: "P0|P1|P2|P3"
    触发条件: "<RULE_OR_THRESHOLD>"
    持续秒: <NUMBER>
```

### 6) 变更与发布
```yaml
变更发布:
  部署版本: "<VERSION>"
  配置变更: "<SUMMARY>"
  执行人: "<USER_OR_SYSTEM>"
  时间: "<ISO-8601>"
```

### 7) 拓扑与依赖
```yaml
拓扑依赖:
  上游: ["<SERVICE_A>", "<SERVICE_B>"]
  下游: ["<SERVICE_C>"]
  依赖项: ["<DB>", "<CACHE>", "<MQ>"]
  链路ID: ["<TRACE_ID_1>"]
```

### 8) 异常分析结果
```yaml
AI分析:
  根因假设: "<ROOT_CAUSE_HYPOTHESIS>"
  证据: ["<EVIDENCE_1>", "<EVIDENCE_2>"]
  置信度: 0.0
```

### 9) 处置建议与自动化动作
```yaml
处置动作:
  建议步骤: ["<STEP_1>", "<STEP_2>"]
  自动化: ["<SCRIPT_1>", "<RUNBOOK_1>"]
  回滚方案: "<ROLLBACK_PLAN>"
```

### 10) 结果回溯与学习
```yaml
结果反馈:
  结果: "<RESOLVED|MITIGATED|FAILED>"
  验证指标: ["<METRIC_1>", "<METRIC_2>"]
  经验沉淀: "<SUMMARY>"
```

### 11) 趋势预测
```yaml
趋势预测:
  指标: "<METRIC_NAME>"
  趋势: "up|down|flat"
  预测窗口分钟: <NUMBER>
  风险等级: "low|medium|high"
```

### 12) 阈值动态学习
```yaml
阈值学习:
  指标: "<METRIC_NAME>"
  基线窗口: "7d|30d"
  新阈值: <NUMBER>
  依据: "<WHY>"
```

### 13) 根因分析
```yaml
根因分析:
  根因: "<ROOT_CAUSE>"
  影响因素: ["<FACTOR_1>", "<FACTOR_2>"]
  修复措施: "<FIX_SUMMARY>"
```

---

## 示例

```yaml
元信息:
  事件编号: "INC-20260120-001"
  发生时间: "2026-01-20T10:21:33+08:00"
  级别: "P1"
  来源: "prometheus"
  环境: "prod"
  平台版本: "v1.0"

上下文:
  集群:
    名称: "prod-k8s-cluster"
    版本: "v1.19.16"
    区域: "cn-hangzhou"
  命名空间: "prod-env"
  工作负载:
    类型: "Deployment"
    名称: "pay-center"
    Pod: "pay-center-86d8546d4-zqprn"
    节点: "node-172.16.171.209"

指标:
  CPU:
    使用率: 92.4
    限制率: 100
  内存:
    使用量MB: 1830
    限制MB: 2048
    使用率: 89.4
  磁盘:
    IO等待ms: 35
  网络:
    下行MBps: 12.4
    上行MBps: 8.9
  QPS: 2150
  错误率: 3.2

日志:
  - "ERROR payment timeout: upstream=bank-gateway"
  - "WARN retry exceeded: order_id=823749"

事件告警:
  - 名称: "HighErrorRate"
    级别: "P1"
    触发条件: "error_rate_pct > 2% for 5m"
    持续秒: 420

变更发布:
  部署版本: "pay-center:v2.3.7"
  配置变更: "timeout=2s -> 1s"
  执行人: "ci-cd"
  时间: "2026-01-20T09:55:10+08:00"

拓扑依赖:
  上游: ["api-gateway"]
  下游: ["bank-gateway", "order-service"]
  依赖项: ["mysql-pay", "redis-session"]
  链路ID: ["trace-7f3a8c9d"]

AI分析:
  根因假设: "bank-gateway latency spike + timeout too aggressive"
  证据: ["bank-gateway p95 latency 2.8s", "timeout set to 1s"]
  置信度: 0.72

处置动作:
  建议步骤: ["increase timeout to 3s", "add circuit breaker"]
  自动化: ["runbook/pay-center/rollback_timeout"]
  回滚方案: "rollback to pay-center:v2.3.6"

结果反馈:
  结果: "MITIGATED"
  验证指标: ["error_rate_pct back to 0.4%", "p95 latency < 1.2s"]
  经验沉淀: "timeout change must be validated against upstream SLA"

趋势预测:
  指标: "error_rate_pct"
  趋势: "down"
  预测窗口分钟: 30
  风险等级: "low"

阈值学习:
  指标: "error_rate_pct"
  基线窗口: "30d"
  新阈值: 1.5
  依据: "post-optimization baseline stabilized"

根因分析:
  根因: "Timeout misconfiguration under upstream latency spike"
  影响因素: ["latency surge", "no circuit breaker"]
  修复措施: "timeout raised; circuit breaker enabled"
```
