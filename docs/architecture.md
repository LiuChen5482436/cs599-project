# 系统架构说明

## 总体架构

```mermaid
flowchart LR
    User[用户] --> Web[React 前端]
    Web --> API[FastAPI API 层]
    API --> Orchestrator[Orchestrator 总控 Agent]
    Orchestrator --> Safety[SafetyGate 安全门]
    Orchestrator --> Followup[FollowupAgent 追问]
    Orchestrator --> RAG[RAGAgent 检索]
    Orchestrator --> Risk[RiskClassifier 风险分级]
    Orchestrator --> Advice[AdviceGenerator 建议生成]
    Orchestrator --> Summary[SummaryWriter 摘要]
    RAG --> Chroma[(Chroma 向量库)]
    RAG --> Docs[医学知识库]
    Advice --> LLM[DashScope/Qwen]
    Followup --> LLM
    Summary --> LLM
    API --> DB[(SQLite)]
    API --> Logs[日志]
```

## Agent 交互流程

```mermaid
sequenceDiagram
    participant U as User
    participant F as React Frontend
    participant A as FastAPI
    participant O as Orchestrator
    participant S as SafetyGate
    participant Q as FollowupAgent
    participant R as RAGAgent
    participant C as RiskClassifier
    participant G as AdviceGenerator
    participant D as SQLite

    U->>F: 输入症状
    F->>A: POST /chat
    A->>D: 保存用户消息
    A->>O: process_message()
    O->>S: detect_red_flags()
    alt 红旗症状
        S-->>O: emergency response
        O-->>A: 急救建议
    else 信息不足
        O->>Q: identify_missing_fields()
        Q-->>O: 追问问题
        O-->>A: needs_followup=true
    else 信息充足
        O->>R: retrieve()
        R-->>O: 医学知识片段
        O->>C: generate_risk_report()
        C-->>O: 风险等级与因素
        O->>G: generate_advice()
        G-->>O: 健康建议
        O-->>A: 完整答复
    end
    A->>D: 保存助手回复与风险结果
    A-->>F: ChatResponse
    F-->>U: 展示结果
```

## 数据流设计

```mermaid
flowchart TD
    Message[用户自然语言症状] --> Validation[Pydantic 校验]
    Validation --> Session[会话与用户信息合并]
    Session --> EmergencyCheck[红旗症状检测]
    EmergencyCheck -->|命中| EmergencyAdvice[急救建议]
    EmergencyCheck -->|未命中| Completeness[信息完整性检查]
    Completeness -->|缺失| FollowupQuestion[追问问题]
    Completeness -->|完整| Retrieval[医学知识检索]
    Retrieval --> RiskScore[风险分级打分]
    RiskScore --> LLMAdvice[LLM 建议生成]
    LLMAdvice --> Persistence[SQLite 持久化]
    EmergencyAdvice --> Persistence
    FollowupQuestion --> Persistence
```

## 风险等级策略

| 等级 | 名称 | 触发条件 | 输出策略 |
| --- | --- | --- | --- |
| A | 急诊 | 分数 >= 70 或红旗症状 | 立即拨打 120 或急诊 |
| B | 尽快就医 | 分数 >= 50 | 24 小时内就医 |
| C | 门诊 | 分数 >= 30 | 1-3 天内门诊 |
| D | 居家观察 | 分数 < 30 | 居家观察，症状加重就医 |

## 工程边界

系统定位为“健康咨询与就医分诊辅助”，不是诊断系统。所有生成建议必须包含“不能替代医生诊断”的边界声明；红旗症状命中时不继续生成普通建议，而是优先返回急救建议。
