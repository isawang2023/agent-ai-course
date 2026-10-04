---
title: Agent / AI 产品学习路线（深度版·带自测）
tags:
  - 学习/AgentAI
  - 学习/进阶
状态: 未开始
更新日期: 2026-09-30
预计投入: 每周 5-8h
---

> [!note] 这份文件是什么
> [[Agent AI 加速学习计划（4-6周版）|加速版]] 的进阶版本。
> 同样去掉论文和学术课程，只保留**能看懂的资料 + 动手项目 + 自测验收**。
> 配色语义：**青=目标 · 蓝=资料 · 紫=动手 · 灰=术语/清单 · 黄=题目 · 绿=答案 · 橙=常见坑**

## 目录

- [[#和加速版的关系]]
- [[#目标反推 · 这条路线是否合适你]]
- [[#模块 1 · AI / LLM 基础认知]]
- [[#模块 2 · Agent 核心原理]]
- [[#模块 3 · MCP / RAG / Memory 工程体系]]
- [[#模块 4 · 体验搭建 + 产品设计视角]]
- [[#模块 5 · Agent 评测（Eval）]]
- [[#模块 6 · 结合工作实战]]
- [[#术语速查表]]
- [[#官方免费课程资源库]]
- [[#学习进度追踪]]
- [[#补丁包 · 补齐这份路线没覆盖的能力]]
- [[#不需要学的内容（省时间）]]

---

## 和加速版的关系

> [!quote] 两版对比
> | | 加速版（4-6周） | 深度版（本文） |
> | --- | --- | --- |
> | 定位 | 快速建立认知框架 | 深入理解 + 动手验证 |
> | 每周投入 | 3-4 小时 | 5-8 小时 |
> | 自测 | 1 题/周，快速验收 | 3 题/模块，必须全对 |
> | 动手 | 体验为主，跑通即可 | 至少完成 2 个实操项目 |
> | 适合 | 先从这里开始 | 加速版完成后，或想直接深入 |

---

## 目标反推 · 这条路线是否合适你

**最终目标**：能参与 Agent 技术和架构评审讨论，和研发对话不掉线，能从产品角度提出有依据的设计判断。

**当前基础**：强产品 / UX 背景，熟悉用户体验设计，了解业务，但没有亲手搭过 Agent。

> [!quote] 反推验证
> | 目标能力 | 对应模块 | 够用了吗？ |
> | --- | --- | --- |
> | 理解 LLM 的能力边界 | 模块 1 | 够，不需要数学 |
> | 区分 Workflow / Agent，知道什么时候用哪个 | 模块 2 | 够，这是产品判断核心 |
> | 听懂 MCP / RAG / Memory 的技术讨论 | 模块 3 | 够，理解原理即可 |
> | 能自己跑通一个 Agent，建立真实体感 | 模块 4 | 必须做，不能跳过 |
> | 能判断一个 Agent 功能好不好 | 模块 5 | 够，Eval 思维比代码更重要 |
> | 能把 Agent 能力落进实际科研场景 | 模块 6 | 这是最终考试 |

> [!success] 难度曲线判断
> 模块 1-3 偏认知，节奏快；模块 4 需要动手，是坡度最大的一段；模块 5-6 回到产品思维，你的已有经验可以直接用上。
> **整体路线对强产品背景的人是合适的。**

---

## 模块 1 · AI / LLM 基础认知

> [!tip] 学什么
> 这个模块不是学技术，是建立语言基础。你需要能听懂研发说"这个模型 128K context，成本高"时，脑子里有清晰的画面。
> - AI、LLM、Multimodal、Embedding 的关系
> - Token、Context Window、Temperature 这些基本概念
> - 当前主流模型生态（GPT、Claude、DeepSeek 等）的定位差异
> - 模型能力、成本、速度的权衡——这是产品选型的核心

### 先用起来

> [!example] 不看视频不看文章，先用 · 约 1h
> 拿你工作中的真实任务去试：
> - [ ] 把一份会议纪要丢给 ChatGPT 或 Claude，让它提炼 3 个行动项
> - [ ] 让 AI 帮你写一段需求描述或邮件（先写提示词，改到满意为止）
> - [ ] 让 AI 做一件它不擅长的事（比如问最近的新闻），观察它会不会编造

### 对比实验

> [!example] 约 30min
> - [ ] 同一个问题，分别问 **ChatGPT / Claude / DeepSeek**，写下三者的差异（速度、质量、风格）
> - [ ] 把一篇 5000 字以上的文章塞给 AI，看它是否会遗漏前面的内容
> - [ ] 试试模糊指令 vs 清晰指令的差别（"帮我写个方案" vs "你是科研产品经理，请为'AI 论文总结'功能写需求文档，包含用户场景、核心功能、验收标准"）

### 从使用中发现概念

> [!quote] 做完上面的练习，你已经接触了这些概念
> | 你刚做的事 | 对应的概念 | 为什么产品经理要懂 |
> | --- | --- | --- |
> | 把会议纪要丢给 AI 处理 | Prompt / Inference | 每次调用都消耗 token 和算力，影响成本和响应速度 |
> | 观察 AI 编造不存在的新闻 | Hallucination（幻觉） | 模型不知道自己在编，产品必须设计兜底机制 |
> | 对比三个模型的回答差异 | 模型选型 | 不同模型在成本/质量/速度上各有取舍，是产品决策 |
> | 发现长文章后半段被忽略 | Context Window | 超出范围就"忘记"，需要设计文档截断或分块方案 |
> | 清晰指令比模糊指令效果好很多 | Prompt Engineering | 输入质量决定输出质量，产品需要预设好的提示词 |
>
> 带着这些直觉，再去看下面的课程，你会发现"哦原来这就是那个东西"。

### 学习资料

> [!info] 官方课程（选 1-2 个即可）· 约 2-6h
> - [ ] **AI for Everyone**（DeepLearning.AI / Coursera，~6h，免费旁听）— Andrew Ng 专为非技术人设计，78 万人学过，AI 入门的黄金标准
>   - [打开课程](https://www.coursera.org/learn/ai-for-everyone)
> - [ ] **Claude 101**（Anthropic Academy，~2h，完全免费，有证书）— 从零学会用 Claude，含项目、工具连接、深度研究等模块
>   - [打开课程](https://anthropic.skilljar.com/claude-101)
> - [ ] **AI Foundations**（OpenAI Academy，~1h，完全免费）— OpenAI 官方入门，含练习和测评，学完可拿徽章
>   - [打开课程](https://academy.openai.com/pages/courses)
> - [ ] **Karpathy — How I use LLMs**（YouTube，~1h）— 不讲原理，讲一个 AI 专家日常怎么高效使用 AI 工具
>   - 搜索 "Andrej Karpathy How I use LLMs"

> [!abstract]- 进阶阅读 · 偏技术，选看
> - [ ] **3Blue1Brown — But what is a GPT?**（~1h）— 可视化讲 Transformer 机制，零数学门槛但需要技术兴趣
>   - [打开视频](https://www.youtube.com/watch?v=wjZofJX0v4M)
> - [ ] **Karpathy — Intro to LLMs**（~1h）— 最经典的 LLM 入门，偏技术但讲得极其清楚
>   - [打开视频](https://www.youtube.com/watch?v=zjkBMFhNj_g)
> - [ ] **Generative AI for Everyone**（DeepLearning.AI / Coursera，~6h，免费旁听）— 比 AI for Everyone 更新，聚焦生成式 AI 的能力和局限
>   - [打开课程](https://www.coursera.org/learn/generative-ai-for-everyone)

### 提示词基础

> [!example] 产品经理最实用的 AI 技能 · 约 30min
> - [ ] 试试给 AI 一个**角色**："你是一个有 10 年经验的产品总监"
> - [ ] 试试给 AI **示例**：先给一个好的输出范例，再让它照着格式生成
> - [ ] 试试**分步骤拆解**复杂任务："先列出要点，然后逐条展开"
>
> 想系统学提示词？推荐：
> - **AI Prompting for Everyone**（DeepLearning.AI，~6h，视频免费）— Andrew Ng 2026 新课，零代码
> - **提示词工程**（OpenAI Academy，免费）— OpenAI 官方提示词课

### 自测题

> [!warning] 必须 3 题全对才算通过

**问题 1 · 概念辨析**

> [!question] 题目
> - Token 是什么？一个中文字大约等于几个 token？1 万汉字大概消耗多少 token？
> - Context Window 是什么？超出了会怎样？对产品设计有什么影响？
> - Embedding 用来做什么？和普通文字有什么不同？

> [!success]- 参考答案 · 点击展开
> - **Token**：模型读写的最小单位，1 个中文字 ≈ 1-2 token，1 万汉字约 1-2 万 token
> - **Context Window**：模型一次能看到的最大范围，超出就"忘记"前面的内容——对产品设计的影响是：长对话需要压缩/摘要，长文档需要分块处理
> - **Embedding**：把文字转成数字向量，用来做搜索和相似度计算（如 RAG）。普通文字是给人看的，Embedding 是给模型做数学运算的

**问题 2 · 产品选型判断**

> [!question] 题目
> 你在评审一个功能需求：用户上传 5 万字学术报告，让 AI 帮忙提炼核心观点。研发说要用 GPT-3.5（4K context）。
> **你怎么判断这个方案是否可行？**

> [!success]- 参考答案 · 点击展开
> **方案不可行。** 5 万字 ≈ 5-10 万 token，远超 GPT-3.5 的 4K 上限。
>
> 可行方案有两个：
> 1. **换模型**：用 GPT-4o（128K）或 Claude（200K），context 够大，直接塞进去
> 2. **改架构**：用 RAG，先把报告切片 + 向量化，用户提问时检索相关段落，不需要一次性喂入全文
>
> **产品视角：** 你应该追问研发"用哪个模型、context 多大"，而不是等他们做完才发现截断问题。

**问题 3 · Temperature 应用**

> [!question] 题目
> 你要给科研用户设计一个"论文摘要生成"功能，另一个是"研究头脑风暴"功能。
> **两个功能的 Temperature 分别应该怎么设置，为什么？**

> [!success]- 参考答案 · 点击展开
> - **论文摘要**：Temperature 接近 0。摘要要准确、确定性强，不需要创意，需要忠实原文
> - **研究头脑风暴**：Temperature 0.7-1.0。需要发散、多样性，用户期望看到意外的角度
>
> **产品含义：** 这两个功能的 prompt 和模型参数配置应该不同，不能用同一个配置。

> [!warning] 常见坑
> 题目里的 GPT-3.5 / 4K 是 2023-24 的语境，2026 年主流模型 context 已普遍 128K+。别背数字，记思路：**先估算 token 量级，再谈模型选型和架构。**

> [!note] 导航
> - 加速版对照：[[Agent AI 加速学习计划（4-6周版）#第1周 · AI / LLM 是什么]]
> - 下一模块：[[#模块 2 · Agent 核心原理]]

---

## 模块 2 · Agent 核心原理

> [!tip] 学什么
> 这是整条路线最重要的模块。你需要能清楚区分三种东西的边界：Prompt（一次性指令）、Workflow（固定流程）、Agent（动态决策）。这个判断是产品架构选型的核心。
> - Agent 与 Chat、Workflow、Copilot 的本质区别
> - Agent Loop：思考 → 行动 → 观察 → 再思考，为什么是循环而不是直线
> - ReAct、Planning、Reflection 这些模式分别解决什么问题
> - 什么时候该用 Workflow（确定性强），什么时候该用 Agent（不确定性高）
> - Multi-Agent：多个 Agent 协作，什么场景真的需要

### 学习资料

> [!info] 课程 + 必读博客 · 约 3-4h
> - [ ] **Agentic AI**（DeepLearning.AI / Coursera，~10h 完整版，免费旁听）— 专讲 Agent 的四种模式：Reflection / Tool Use / Planning / Multi-Agent
>   - [打开课程](https://www.deeplearning.ai/courses/agentic-ai/)
>   - 注意：这门课有部分 Python 代码，**只看视频讲解部分即可**，跳过代码实操
> - [ ] **Anthropic — Building Effective Agents**（必读博客，~30min）
>   - [打开文章](https://www.anthropic.com/engineering/building-effective-agents)
>   - 最重要的一篇。讲清楚 5 种架构模式（Prompt Chaining / Routing / Parallelization / Orchestrator / Multi-Agent）和适用场景，读完能参与 80% 的架构讨论
> - [ ] **Agents and Workflows**（OpenAI Academy，~1-2h，完全免费）— 练习搭建一个 Agent 辅助的工作流
>   - [打开课程](https://academy.openai.com/pages/courses)

> [!abstract]- 进阶阅读 · 偏技术，选看
> - [ ] **Lilian Weng — LLM Powered Autonomous Agents**（2023，经典）
>   - [打开文章](https://lilianweng.github.io/posts/2023-06-23-agent/)
>   - 配图非常多，系统讲 Agent = Planning + Memory + Tool Use 三要素，偏技术但图解清晰
> - [ ] **Anthropic 工程博客**（持续更新）— 关注 multi-agent 和 agent 工程实践
>   - [打开博客](https://www.anthropic.com/engineering)

### 动手实践

> [!example] 2 个观察练习
> - [ ] 用 Claude 开启 tool use，给它一个任务（如"帮我搜索最近的 AI 新闻并总结"），观察它怎么"决定调工具 → 拿到结果 → 继续推理"，数一数它循环了几轮
> - [ ] 用 ChatGPT Code Interpreter 跑一个数据分析（上传一个 CSV），观察它如何多步骤执行：读文件 → 生成代码 → 运行 → 看错误 → 修改代码

### 自测题

> [!warning] 必须 3 题全对才算通过

**问题 1 · 架构选型**

> [!question] 题目
> 以下场景分别应该用 Prompt / Workflow / Agent？说明理由。
> 1. 把一段英文摘要翻译成中文
> 2. 用户输入论文题目 → 自动搜索相关文献 → 提取摘要 → 生成综述草稿（流程固定）
> 3. 用户说"帮我分析这份用户调研数据"，但你不知道数据什么格式、需要分析什么维度

> [!success]- 参考答案 · 点击展开
> 1. **Prompt**：单次任务，一个 prompt 完成，不需要多步
> 2. **Workflow**：多步骤但流程固定，每步的输入输出是明确的，提前设计好就行
> 3. **Agent**：不确定需要几步，每步做什么依赖上一步的结果，需要模型自己决策
>
> **判断原则：流程能不能提前写死？能写死用 Workflow，不能写死才用 Agent。**

**问题 2 · Agent Loop 拆解**

> [!question] 题目
> 画出（或文字描述）Agent 处理"帮我找最近一周关于大模型 Eval 的论文，筛选出有实验数据的"的完整流程。
> 至少 3 轮 Loop，写出每轮的"思考 / 行动 / 观察"。

> [!success]- 参考答案示例 · 点击展开
> ```
> 第 1 轮：
>   思考：需要搜索最近论文，关键词"LLM evaluation"
>   行动：调用 search_papers("LLM evaluation", date_range="last_7_days")
>   观察：返回 12 篇论文列表，含标题和摘要
>
> 第 2 轮：
>   思考：需要判断哪些有实验数据，逐一看摘要
>   行动：调用 get_abstract(paper_id) × 12 次（或批量）
>   观察：拿到所有摘要，其中 5 篇明确提到 benchmark / experiment
>
> 第 3 轮：
>   思考：已有足够信息，整理结果
>   行动：生成结构化输出（论文名 + 实验亮点）
>   观察：任务完成，输出给用户
> ```
> **关键：** 每轮的"观察"决定下一轮的"思考"——这就是为什么叫 Loop 而不是线性流程。

**问题 3 · Multi-Agent 判断**

> [!question] 题目
> 以下两个场景，哪个真的需要 Multi-Agent？哪个用单 Agent 就够了？
> 1. 用户上传 PDF，Agent 要读取、分析、总结，然后生成 PPT
> 2. 系统要同时处理 100 个用户提交的论文审核请求，每个审核需要 5 分钟

> [!success]- 参考答案 · 点击展开
> 1. **单 Agent 就够**：任务是串行的，一步接一步，不需要并发，一个 Agent 依次完成即可
> 2. **需要 Multi-Agent**：100 个任务相互独立，可以并行处理。用 Multi-Agent（或并发 Agent）能把总时间从 500 分钟压缩到接近 5 分钟
>
> **Multi-Agent 的核心价值是：并行（处理独立任务）和专业化（每个 Agent 只做好一件事）。不是为了复杂而复杂。**

> [!note] 导航
> - 加速版对照：[[Agent AI 加速学习计划（4-6周版）#第2周 · Agent 到底在干什么]]
> - 上一模块：[[#模块 1 · AI / LLM 基础认知]] · 下一模块：[[#模块 3 · MCP / RAG / Memory 工程体系]]

---

## 模块 3 · MCP / RAG / Memory 工程体系

> [!tip] 学什么
> 这个模块解决的问题是：Agent 怎么获取它需要的信息？这是产品设计中"Agent 能不能做到"的核心判断依据。
> - Tool / Function Calling 的实际工作方式——模型是如何"决定"调哪个工具的
> - MCP（Model Context Protocol）：Agent 连接外部工具/数据的标准协议，为什么需要标准化
> - RAG（检索增强生成）：先搜索再回答，减少幻觉，适合知识库场景
> - Memory：短期（当前对话上下文）vs 长期（跨对话持久化），两种的架构完全不同
> - Context Engineering：给 Agent 什么信息、什么时候给、以什么格式给

### 学习资料

> [!info] 核心材料 · 约 1.5-3h
> - [ ] **MCP 官网 Overview**（只看概览页，5 分钟）
>   - [打开网页](https://modelcontextprotocol.io)
>   - 看完你能解释"为什么需要 MCP 而不是直接写 API"
> - [ ] **RAG 概念讲解**（YouTube，搜 "RAG explained"，~10min）
>   - 核心流程：Retrieval（向量搜索找相关段落）→ Augmented（塞进 context）→ Generation（模型基于检索内容回答）
>   - 这是模块自测第 2 题的核心知识，务必理解
> - [ ] **Anthropic — Context Engineering for Agents**
>   - [打开博客](https://www.anthropic.com/engineering)
>   - 核心：给 Agent 什么信息、什么时候给、以什么格式给
> - [ ] **Applied AI Foundations**（OpenAI Academy，~1.5h，完全免费）— 讲如何把 AI 嵌入实际工作流，重点看工具调用和数据接入部分
>   - [打开课程](https://academy.openai.com/pages/courses)
> - [ ] **AI Fluency: Framework & Foundations**（Anthropic Academy，~3h，完全免费）— 重点看"与 AI 交互的最佳实践"部分，和 Context Engineering 相关
>   - [打开课程](https://anthropic.skilljar.com/ai-fluency-framework-foundations)

> [!abstract]- 进阶阅读 · 偏技术，选看
> - [ ] **OpenAI — Building retrieval pipelines**（开发者向）
>   - [打开文档](https://platform.openai.com/docs/guides/retrieval)
>   - 如果想深入理解 RAG 的工程实现：切片策略、Embedding 模型选择、检索排序
> - [ ] **Anthropic 工程博客 — Memory 相关文章**（持续更新）
>   - [打开博客](https://www.anthropic.com/engineering)
>   - 关注 Agent 的长短期记忆设计和实现

### 动手实践

> [!example] 至少完成 1 个
> - [ ] 用 **Dify** 搭一个 RAG 知识库问答（上传 2-3 份文档 → 对话 → 观察它的检索过程）
> - [ ] 用 **Coze** 搭一个带工具调用的 Bot（让它能搜索 + 回答）
> - [ ] 用 **Claude Code** 体验 MCP 的实际工作方式（就是你现在用的这个工具）

### 自测题

> [!warning] 必须 3 题全对才算通过

**问题 1 · 三个概念的区别**

> [!question] 题目
> 用一句话分别解释：Tool Calling 是什么、MCP 解决什么、RAG 的核心流程是什么？

> [!success]- 参考答案 · 点击展开
> - **Tool Calling**：模型决定"我需要调某个函数"，由应用去执行，把结果还给模型——模型是决策者，应用是执行者
> - **MCP**：标准化 Agent 连接外部工具/数据的协议，避免每个 Agent 都要单独适配不同工具接口——相当于给 Agent 和工具之间定了一套"插头标准"
> - **RAG 核心流程**：Retrieval（向量检索相关内容）→ Augmented（把检索结果塞进 prompt）→ Generation（模型基于检索内容回答，而不是凭空编造）

**问题 2 · RAG 失败排查**

> [!question] 题目
> 你们搭了一个科研知识库问答系统（RAG），但用户反馈"明明文档里写了这个结论，但 AI 说没找到"。
> **你会从哪几个环节排查？**

> [!success]- 参考答案 · 点击展开
> 按失败可能性从高到低排查：
>
> 1. **切片问题**：关键信息被切断到两个片段中间，检索只拿到一半——调整切片大小和重叠量
> 2. **检索失败**：向量相似度没算对，导致相关内容排名靠后没进 Top-K——检查 Embedding 模型，或换用混合检索（向量 + 关键词）
> 3. **Rerank 问题**：检索到了但排序靠后，被截掉——加一层 Rerank 模型
> 4. **Context 截断**：检索到了但 prompt 太长超出 context window——压缩 prompt 或换大 context 模型
> 5. **模型幻觉**：检索到了但模型没用上，自己编了答案——加强 prompt 中"必须基于检索内容回答"的指令，或做 Grounding 验证
>
> **产品含义：** RAG 失败不是一个地方的问题，是流水线里任何一段都可能断。

**问题 3 · Memory 设计**

> [!question] 题目
> 你在设计一个科研 Agent，用户可能会在不同天多次回来对话。
> **哪些内容应该存短期 Memory，哪些应该存长期 Memory？**

> [!success]- 参考答案 · 点击展开
> - **短期 Memory（当前对话）**：用户在这次对话里问过什么、提到的论文名、正在讨论的研究方向——对话结束后可以丢弃
> - **长期 Memory（跨对话持久化）**：用户的研究领域、偏好的引用格式、之前标注过的重要论文、历史项目——下次打开还需要用到
>
> **设计要点：** 长期 Memory 需要主动管理（太多反而变噪声），要给用户"删除 / 编辑我的记忆"的控制权。

> [!note] 导航
> - 加速版对照：[[Agent AI 加速学习计划（4-6周版）#第3周 · MCP / RAG / Memory 这些工程概念]]
> - 上一模块：[[#模块 2 · Agent 核心原理]] · 下一模块：[[#模块 4 · 体验搭建 + 产品设计视角]]

---

## 模块 4 · 体验搭建 + 产品设计视角

> [!tip] 学什么
> 这个模块有两个目标：一是通过动手建立真实体感（不是为了变成工程师，而是为了理解工程的约束和可能性），二是开始用产品视角审视 Agent 体验。
> - 用零代码工具跑通一个最小 Agent，看到数据怎么在节点之间流转
> - 体验 2-3 个现有 AI 产品，带着产品问题去拆解它们的设计
> - 建立对 AI 产品 UX 核心模式的认知：透明度、控制感、可信度、错误恢复

### 动手搭建

> [!example] 零代码（推荐，约 1h）
> - [ ] 用 **Dify** 或 **Coze** 搭一个多步骤 Workflow：用户提问 → 搜索 → 整理 → 回答
> - [ ] 打开每个节点，看输入和输出，理解数据在节点之间怎么流转
> - [ ] 故意给一个边界 case（空输入、超长文本），观察出错时的表现

> [!example] 少量代码（选修，适合想更深入的人）
> - [ ] **OpenAI Agents SDK Quickstart**
>   - [打开教程](https://platform.openai.com/docs/guides/agents-sdk)
>   - 官方教程，5 个文件搭一个能调工具的 Agent
> - [ ] **Hugging Face Agents Course Unit 1**
>   - [打开课程](https://huggingface.co/learn/agents-course)
>   - 有代码但不难，有中文版

### 体验和拆解现有 AI 产品

> [!info] 选 2 个产品，每个至少用 15 分钟完成一个真实任务
> - [ ] **Perplexity** — 搜索过程展示、引用设计、追问引导
> - [ ] **Cursor / Claude Code** — 多步任务处理、出错恢复、用户干预
> - [ ] **Google Gemini Deep Research** — 研究过程透明度、报告生成、信息层级

> [!tip] 带着这 4 个问题去体验
> - 用户能看到 Agent 在做什么吗？（透明度）
> - 出错了怎么告诉用户？用户能干预吗？（控制感）
> - 等待过程是什么体验？有进度反馈吗？（等待设计）
> - 结果怎么呈现？有引用来源吗？（可信度）

### AI 产品 UX 核心模式

> [!quote] 五个设计模式
> | 设计模式 | 解决什么问题 | 好的做法 |
> | --- | --- | --- |
> | 过程透明 | 用户不知道 Agent 在干什么 | 展示步骤（"正在搜索 → 正在阅读 → 正在整理"） |
> | 渐进式结果 | 等待时间长，用户焦虑 | 流式输出，边生成边展示 |
> | 来源引用 | 用户不知道结果能不能信 | 每条结论标注来自哪篇文献/哪个段落 |
> | 用户控制 | Agent 跑偏了用户没法干预 | 关键节点让用户确认，允许中途调整 |
> | 错误恢复 | 出错了用户不知道怎么办 | 区分错误类型，给具体的下一步建议 |

### 自测题

> [!warning] 必须 3 题全对才算通过

**问题 1 · 产品体验拆解**

> [!question] 题目
> 你体验了 Perplexity 和 ChatGPT，发现 Perplexity 搜索后会展示"正在阅读 5 个来源"并逐条显示引用，而 ChatGPT 直接给出最终答案。
> **从产品角度分析：这两种设计分别适合什么场景？各有什么风险？**

> [!success]- 参考答案 · 点击展开
> **Perplexity（过程透明 + 引用模式）**
> - 适合场景：用户需要**可验证的信息**（研究、决策、事实查询），信任是关键
> - 风险：如果过程太长或来源质量差，透明反而暴露了弱点；信息密度大，用户认知负担重
>
> **ChatGPT（直接回答模式）**
> - 适合场景：用户需要**快速答案**（日常问答、创意、代码），效率是关键
> - 风险：用户无法验证答案来源，一旦出现幻觉用户可能直接信了；用户不知道答案基于什么信息
>
> **产品判断：** 不是哪种更好，而是取决于用户的**信任需求**——需要验证的场景用透明模式，需要效率的场景用直接模式。科研场景偏向 Perplexity 模式。

**问题 2 · Agent 调错工具**

> [!question] 题目
> 你搭了一个 Agent，工具库里有 `search_web`、`search_papers`、`get_weather`。但 Agent 被问"帮我找关于 RAG 的论文"时，调用了 `search_web` 而不是 `search_papers`。
> **从产品角度，这说明什么？怎么修？**

> [!success]- 参考答案 · 点击展开
> **说明什么：** Tool 的描述（给模型看的"说明书"）没写清楚，模型无法区分两个搜索工具的适用场景。
> 这本质上是产品定义问题——**Tool 描述也是产品文案的一部分，只不过读者是模型而非用户。**
>
> **修法：** 把 `search_papers` 描述从模糊的"搜索内容"改成"专门搜索学术论文，适用于用户提到论文、研究、综述、arXiv 等场景"，区分度就够了。
>
> **产品含义：** Tool 描述的质量直接影响 Agent 的行为准确性。作为产品经理，你需要参与定义每个 Tool 的描述文案——这和写用户界面文案一样重要。

**问题 3 · UX 设计判断**

> [!question] 题目
> 你们要上线一个"AI 文献综述"功能，Agent 会搜索论文 → 阅读摘要 → 筛选 → 生成综述，全程约 60 秒。
> **你会怎么设计这 60 秒的用户体验？考虑正常流程和出错流程。**

> [!success]- 参考答案 · 点击展开
> **正常流程**
> 1. 用户提交后，立即展示"正在搜索相关论文..."（而非空白等待）
> 2. 搜到论文后，先展示"找到 12 篇相关论文，正在阅读..."并列出论文标题（渐进式结果）
> 3. 筛选完成后展示"已筛选 5 篇高相关度论文，正在生成综述..."
> 4. 综述生成使用流式输出，边生成边展示
> 5. 每条观点标注来源论文（引用可点击展开原文段落）
>
> **出错流程**
> - 搜索超时：展示"搜索耗时较长，正在重试..."而非直接报错
> - 搜不到论文：展示"未找到完全匹配的论文，建议调整关键词"并给出修改建议
> - 生成中断：保留已生成的部分，标注"综述未完成，以下是已整理的部分"
>
> **关键原则：60 秒不是一个整体等待，是 4-5 个小步骤——每个步骤都要有反馈。**

> [!note] 导航
> - 加速版对照：[[Agent AI 加速学习计划（4-6周版）#第4周 · 体验 Agent 产品，建立设计直觉]]
> - 上一模块：[[#模块 3 · MCP / RAG / Memory 工程体系]] · 下一模块：[[#模块 5 · Agent 评测（Eval）]]

---

## 模块 5 · Agent 评测（Eval）

> [!tip] 学什么
> 一个 Agent 功能做完了，怎么判断它好不好？这不是测试工程师的问题，而是产品定义"好"的标准。这个模块会改变你对"功能上线标准"的理解。
> - 为什么传统软件测试（pass/fail）不够用于 Agent
> - Task Success（任务是否完成）/ Tool Selection Accuracy（工具选对了吗）/ Groundedness（有没有瞎编）
> - Trace-level evaluation：不只看最终答案，要看每一步
> - LLM-as-a-Judge：用另一个模型来打分，适合大规模评测
> - 如何从真实失败案例倒推出你需要的测试集

### 学习资料

> [!info] 评测课程与材料 · 约 3-5h
> - [ ] **Evaluating AI Agents**（DeepLearning.AI，~2.5h，免费）— 专讲 Agent 评测：Trace 追踪、LLM-as-a-Judge、轨迹评测、生产监控
>   - [打开课程](https://www.deeplearning.ai/courses/evaluating-ai-agents)
>   - 有 Python 代码实验，**只看视频讲解即可**，跳过代码部分
> - [ ] **Evaluating, Governing, and Scaling AI Agents**（Coursera / LearnQuest，~4h，免费旁听）— 零代码，讲如何评估 Agent 可靠性、A/B 实验、向管理层汇报效果
>   - [打开课程](https://www.coursera.org/learn/evaluate-govern-and-scale-ai-agents)
>   - 入门级，专门讲"怎么向老板证明 Agent 有用"，非常适合 PM
> - [ ] **Anthropic — Demystifying evals for AI agents**（博客，~20min）
>   - [打开文章](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
>   - 核心：Agent 评测三层——单步行为 / 轨迹 / 最终结果，建立评测词汇表
> - [ ] **OpenAI — How Evals Drive the Next Chapter in AI for Businesses**（博客，~10min）
>   - [打开文章](https://openai.com/index/evals-drive-next-chapter-of-ai/)
>   - 写给业务负责人看的，把 Eval 类比成产品需求文档
> - [ ] 体验 **ChatGPT Arena**（https://lmarena.ai）— 看用户怎么通过对比投票来评价模型好坏，理解"评测"的产品化形态

> [!abstract]- 更多评测资料 · 按需选看
> - [ ] **LLM Evaluations for AI Product Teams**（Evidently AI，7 天邮件课，完全免费）— 零代码，专为产品团队设计
>   - [打开课程](https://www.evidentlyai.com/courses)
> - [ ] **Automated Testing for LLMOps**（DeepLearning.AI，~52min，免费）— 讲 AI 系统的自动化测试和 CI/CD
>   - [打开课程](https://www.deeplearning.ai/courses/automated-testing-llmops)
> - [ ] **LLM Evaluation: A Beginner's Guide**（Evidently AI，2026 年更新）— 从入门到各类评测方法的完整参考
>   - [打开指南](https://www.evidentlyai.com/llm-guide/llm-evaluation)
> - [ ] **OpenAI — Evaluation Best Practices**（开发者文档）— 评测驱动开发的方法论
>   - [打开文档](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

### 产品经理的评测框架

> [!quote] 5 个评测维度（PM 视角）
> 不需要写代码也能用这个框架评价任何 Agent 功能：
> | 维度 | 核心问题 | 典型指标 |
> | --- | --- | --- |
> | 任务完成 | 用户想做的事做到了吗？ | Task Success Rate |
> | 结果可信 | 答案有依据还是编的？ | Groundedness / Hallucination Rate |
> | 过程合理 | 每一步都做对了吗？ | Tool Selection Accuracy / Trace 评审 |
> | 体验可接受 | 等多久？花多少钱？ | 延迟 P95 / 单次调用成本 |
> | 用户满意 | 用户自己觉得好不好？ | 放弃率 / 追问率 / NPS |

> [!quote] 5 种评测方法
> | 方法 | 适用场景 | 优缺点 |
> | --- | --- | --- |
> | 人工评测 | 上线初期、重要功能 | 最准确，但慢且贵 |
> | LLM-as-a-Judge | 大规模评测、快速迭代 | 快且便宜，但需要和人工评测校准 |
> | A/B 测试 | 对比两个方案谁更好 | 最终裁判，但需要足够流量 |
> | 用户反馈 | 真实场景发现盲区 | 最真实，但有偏——不满的人更爱反馈 |
> | Trace 审查 | 排查失败根因 | 能看到每一步决策，但需要工程支持 |

> [!abstract]- 进阶阅读 · 偏技术，选看
> - [ ] **OpenAI — Evaluate agent workflows**（开发者向）
>   - [打开指南](https://platform.openai.com/docs/guides/evaluation)
>   - 实操指南，讲 Eval Set 设计和自动化评测
> - [ ] **Evaluating AI Agents**（DeepLearning.AI，~2.5h）的代码实验部分 — 如果想动手跑 Eval 流程
> - [ ] **Hugging Face — Evaluation Guidebook**（开源，有中文版）
>   - [打开指南](https://huggingface.co/spaces/OpenEvals/evaluation-guidebook)
>   - 从管理 Open LLM Leaderboard 的经验总结的评测方法论

### 动手实践

> [!example] 两个产出
> - [ ] 拿你们科研助手的一个**真实失败 case**，写出它在 Trace 里的哪步出错了、根本原因是什么
> - [ ] 为一个具体功能设计 Eval：写出任务集（至少 5 条）+ 期望结果 + 评分标准

### 自测题

> [!warning] 必须 3 题全对才算通过

**问题 1 · 评测指标解读**

> [!question] 题目
> 以下四个指标分别在测量什么？各举一个"指标好但产品差"的反例。
> - Task Success Rate
> - Tool Selection Accuracy
> - Groundedness
> - Hallucination Rate

> [!success]- 参考答案 · 点击展开
> | 指标 | 测量什么 | 好但产品差的反例 |
> | --- | --- | --- |
> | Task Success Rate | 任务是否完成用户的真实意图 | 用户想要"简短总结"，Agent 输出了一万字详尽报告——任务"完成"了，但用户不满意 |
> | Tool Selection Accuracy | Agent 是否选对了工具 | 工具选对了，但工具本身有 bug 返回错数据——指标好但答案错 |
> | Groundedness | 回答是否有依据（基于检索内容） | 所有回答都有引用，但引用的内容和答案其实没关系——引用了但没用上 |
> | Hallucination Rate | 编造不存在信息的比例 | 幻觉率 0%，但因为过度保守，很多问题都回答"我不确定"——没幻觉但没用 |

**问题 2 · Eval Set 设计**

> [!question] 题目
> 你要评测"科研文献搜索 Agent"的能力。
> **请设计一个最小可用的测试集（包括覆盖哪些场景、怎么打分）。**

> [!success]- 参考答案 · 点击展开
> **测试集（20 条左右）**
> | 场景类型 | 数量 | 例子 |
> | --- | --- | --- |
> | 明确查询 | 6 条 | "找关于 BERT 的综述论文" |
> | 模糊查询 | 4 条 | "找最近的 AI 研究" |
> | 跨领域查询 | 4 条 | "找把机器学习用于蛋白质折叠的论文" |
> | 应该无结果的查询 | 3 条 | "找2099年发表的论文" |
> | 需要追问的查询 | 3 条 | "找那篇 Attention is All You Need" |
>
> **评分标准**
> - Task Success（人工判断）：是否找到了用户真正需要的论文？（0/1）
> - Tool Accuracy（自动判断）：是否调用了正确的搜索工具？
> - Groundedness（自动判断）：返回的论文是否真实存在？（验证 DOI 或 arXiv ID）
> - 延迟 / 成本：同等质量下更快更省是优势

**问题 3 · 失败后的行动**

> [!question] 题目
> 你的科研 Agent 上线后，Eval 显示 Task Success Rate 是 65%，低于目标的 85%。
> **下一步最该做什么？**

> [!success]- 参考答案 · 点击展开
> **正确做法：先分类失败，再对症下药**
> 1. **拉出所有失败 case 的 Trace**，人工看 10-20 条
> 2. **按失败原因分类**（常见分法）：
>    - 工具调用失败：占 X%
>    - 模型理解错误（没理解用户意图）：占 X%
>    - 检索失败（RAG 没找到）：占 X%
>    - 幻觉（找到了但答案错）：占 X%
> 3. **优先修占比最高的那类**，不要同时改多处
> 4. **修完后重跑 Eval**，确认指标提升，并确认没有引入新的失败
>
> **常见错误：** 看到低分就改 prompt，不知道失败原因就乱改，结果 A 问题修了 B 问题变差了。

> [!warning] 补充视角
> 这份材料只覆盖**离线 Eval**。上线后还要盯三类在线信号：**放弃率**（用户中途关掉）、**追问率**（答完还得再问）、**人工接管率**。它们往往比 Task Success 更早暴露真实体验问题。另外别漏掉**单次成本**——它决定这个功能能不能长期活下去。

> [!note] 导航
> - 加速版对照：[[Agent AI 加速学习计划（4-6周版）#第5-6周 · Eval + 产品落地]]
> - 上一模块：[[#模块 4 · 体验搭建 + 产品设计视角]] · 下一模块：[[#模块 6 · 结合工作实战]]

---

## 模块 6 · 结合工作实战

> [!tip] 学什么
> 这个模块没有新概念，只有一件事：把前五个模块学到的东西，落进你实际负责的产品场景里。重点是用产品语言输出，而不是技术语言。
> - 科研场景的 Agent 架构选择（什么固定、什么动态）
> - Agent 功能的产品需求怎么写：不只是功能描述，还要定义架构选型、UX 规范、Eval 标准
> - Agent UX 三原则：过程透明、用户控制、失败恢复
> - 把产品决策建立在 Eval 数据之上，而不是直觉之上
> - 竞品分析：怎么结构化地评价一个 AI 产品的体验

### 学习资料

> [!info] 产品视角的参照 · 约 2-3h
> - [ ] 深度体验 **Google Gemini Deep Research** 或 **Perplexity Deep Research**
>   - 不是学技术，是感受当前最好的产品形态：信息透明度、进度展示、引用样式、错误处理
> - [ ] **AI Leadership**（OpenAI Academy，~3h，完全免费）— 讲 AI 策略、治理、路线图，帮你把 Agent 能力放进业务上下文
>   - [打开课程](https://academy.openai.com/pages/courses)
> - [ ] **Google Prompting Essentials**（Google / Coursera，~10h，7 天免费试用）— 讲如何用 AI 完成工作，含评估输出偏见
>   - [打开课程](https://www.coursera.org/specializations/prompting-essentials-google)

> [!abstract]- 进阶阅读 · 偏技术，选看
> - [ ] **LangChain Deep Research Tutorial**（搜索 "langchain deep research agent"）
>   - 看多步骤研究 Agent 的实现思路，理解工程复杂度
> - [ ] **Microsoft AI Product Manager Certificate**（Microsoft / Coursera，~109h，付费）— 微软 AI 产品经理认证，覆盖完整产品生命周期
>   - [打开课程](https://www.coursera.org/professional-certificates/microsoft-ai-product-manager)

### 动手实践

> [!example] 选一个你实际负责的科研功能，完整输出
> - [ ] 需求定义：用户的真实目标是什么（不只是功能描述）
> - [ ] 架构方案：Workflow 还是 Agent？哪些步骤固定，哪些动态？写清楚选择理由
> - [ ] UX 设计：用户看到什么、等待过程怎么展示、失败了怎么提示、哪些决策需要用户介入
> - [ ] Eval 方案：用什么指标衡量好坏，测试集怎么构建
> - [ ] 竞品参照：同类产品怎么做的，你的方案和它们的差异点在哪

### 最终项目

> [!warning] 开放题，需要完整输出
> **场景：** 用户上传一篇论文 PDF，想知道"这篇论文的研究方法有什么局限性？"
>
> 请完整输出以下五项：
> 1. **需求定义**：用户的真实目标是什么？"找局限性"背后的动机是什么？
> 2. **架构选择**：用 Workflow 还是 Agent？为什么？
> 3. **UX 设计**：60 秒的等待过程怎么设计？结果怎么呈现？出错了怎么办？
> 4. **Eval 设计**：怎么定义这个功能的"好"？用什么指标？
> 5. **竞品参照**：有没有类似的产品/功能？它们怎么做的？

> [!success]- 参考答案 · 点击展开
> **1. 需求定义**
> - 表面需求：找论文方法的局限性
> - 真实动机：用户在写论文或做研究评审，需要快速理解一篇论文的方法弱点，节省自己逐行阅读的时间
> - 产品定义的"好"：不只是列出局限性，而是每条局限性都有依据（原文引用或外部文献），且覆盖用户自己也能想到的点
>
> **2. 架构选择**
> - **推荐 Workflow 为主**：解析 PDF → 定位方法章节 → 分析局限性 → 输出，这个流程基本固定
> - 搜索外部文献可以是可选的 Agent 步骤（根据论文类型决定要不要搜）
> - 混合架构：Workflow 主干保证稳定性 + 局部 Agent 决策增加灵活性
>
> **3. UX 设计**
> - 上传后立即反馈"正在解析论文..."（不要让用户等在空白页面）
> - 分步展示："已识别论文结构 → 正在分析方法部分 → 正在搜索相关文献 → 生成结论"
> - 每条局限性旁边标注来源（来自原文第几页 or 来自哪篇引用文献），用户可以展开看原文依据
> - 失败处理：PDF 解析失败 →"请确认 PDF 未加密"；搜索超时 → 仍然输出基于原文的分析，标注"未补充外部文献"
>
> **4. Eval 设计**
> - 测试集：20 篇不同领域论文（ML / 生物 / 社科），覆盖不同论文结构
> - 评分指标：
>   - 局限性是否真实存在（专家打分 0-2）
>   - 是否有来源标注（有据性）
>   - 有没有编造不存在的局限性（幻觉率）
>   - 与专家参考答案相比，遗漏了多少重要点（覆盖度）
>
> **5. 竞品参照**
> - Elicit：会从多篇论文中提取方法对比，但不做局限性分析
> - Consensus：偏搜索聚合，不深入单篇论文分析
> - 差异点：我们的功能聚焦单篇深度分析 + 外部文献交叉验证，比搜索类产品更深入

> [!note] 导航
> - 上一模块：[[#模块 5 · Agent 评测（Eval）]]
> - 完成后回到：[[Agent AI 加速学习计划（4-6周版）#能力自检（6周后你应该能做到）]] 做总自检

---

## 术语速查表

> [!note] 学习过程中遇到不懂的词，直接来这里查

> [!quote] 模型与基础
> | 术语 | 解释 |
> | --- | --- |
> | **LLM** | Large Language Model，大语言模型，如 GPT、Claude |
> | **Reasoning Model** | 推理模型，边思考边生成答案的模型，如 o1 |
> | **Multimodal** | 多模态，能处理文字+图片+音频的模型 |
> | **Embedding** | 嵌入向量，把文字转成数字表示，用于搜索和相似度计算 |
> | **Context Window** | 上下文窗口，模型一次能看到的最大范围 |
> | **Token** | 模型处理的最小单位，约 1 个中文字 = 1-2 token |
> | **Temperature** | 温度参数，控制回答随机程度，0=确定，1=发散 |
> | **Hallucination** | 幻觉，模型编造不存在的内容 |

> [!quote] Agent 架构
> | 术语 | 解释 |
> | --- | --- |
> | **Agent** | 智能体，能自主决策、调用工具、完成任务的 AI 系统 |
> | **Workflow** | 工作流，预定义的固定流程，人设计步骤，AI 执行 |
> | **Agent Loop** | Agent 循环：思考→行动→观察→再思考 |
> | **ReAct** | Reasoning + Acting，边推理边行动的模式 |
> | **Planning** | 规划，Agent 分解任务、安排步骤的能力 |
> | **Tool Calling** | 工具调用，模型决定调用外部函数/API |
> | **Function Calling** | 函数调用，同 Tool Calling |
> | **Orchestration** | 编排，多个 Agent 的协调和任务分配 |
> | **Handoff** | 交接，一个 Agent 把任务交给另一个 |
> | **MCP** | Model Context Protocol，让 Agent 连接外部工具/数据的协议 |
> | **RAG** | Retrieval-Augmented Generation，先搜索相关内容再回答 |
> | **Memory** | 记忆，Agent 的短期（当前对话）和长期（跨对话）记忆 |
> | **Context Engineering** | 上下文工程，设计给模型的输入信息 |
> | **Prompt Engineering** | 提示词工程，设计输入文本让模型更好理解 |

> [!quote] 评测与体验
> | 术语 | 解释 |
> | --- | --- |
> | **Grounding** | 事实基础，回答基于真实数据而非编造 |
> | **Citation** | 引用，标注信息来源 |
> | **Trace** | 追踪日志，记录 Agent 每步决策和工具调用 |
> | **Eval** | Evaluation，评测 |
> | **LLM-as-a-Judge** | 用另一个模型来评分打分 |
> | **Task Success** | 任务成功率，完成用户真实意图的比例 |
> | **Groundedness** | 有据性，回答是否有依据而非编造 |
> | **Human-in-the-loop** | 人在回路中，关键决策需要人确认 |
> | **Progressive Disclosure** | 渐进式展示，不一次性展示全部信息 |
> | **Transparency** | 透明度，让用户看到 AI 的思考过程 |
> | **Explainability** | 可解释性，AI 能说明为什么这样决策 |

---

## 学习进度追踪

> [!todo] 逐模块打勾
> - [ ] 模块 1：AI / LLM 基础认知 - 自测 3 题全对
> - [ ] 模块 2：Agent 核心原理 - 自测 3 题全对
> - [ ] 模块 3：MCP / RAG / Memory - 自测 3 题全对 + 完成 1 个动手项目
> - [ ] 模块 4：体验搭建 + 产品设计视角 - 自测 3 题全对 + 拆解 2 个 AI 产品
> - [ ] 模块 5：Agent 评测 - 自测 3 题全对 + 设计 1 套 Eval
> - [ ] 模块 6：结合工作实战 - 完成最终设计项目

---

## 官方免费课程资源库

> [!note] 不需要全学，按需选。标 ★ 的是最推荐的。

> [!quote] 入门级（零基础友好）
> | 课程 | 来源 | 时长 | 费用 | 说明 |
> | --- | --- | --- | --- | --- |
> | ★ AI for Everyone | DeepLearning.AI / Coursera | ~6h | 免费旁听 | Andrew Ng，最适合非技术人的 AI 入门 |
> | ★ Claude 101 | Anthropic Academy | ~2h | 完全免费 | 从零学会用 Claude，有完成证书 |
> | ★ AI Foundations | OpenAI Academy | ~1h | 完全免费 | OpenAI 官方入门，含练习和徽章 |
> | Generative AI for Everyone | DeepLearning.AI / Coursera | ~6h | 免费旁听 | 聚焦生成式 AI，比 AI for Everyone 更新 |
> | Google AI Essentials | Google / Coursera | ~10h | 7天免费 | 基础 AI 概念和应用 |
> | Generative AI for Beginners | 微软 GitHub | 21课 | 完全免费 | 开源课程，可只看"Learn"部分跳过代码 |

> [!quote] Agent 与工作流
> | 课程 | 来源 | 时长 | 费用 | 说明 |
> | --- | --- | --- | --- | --- |
> | ★ Agentic AI | DeepLearning.AI / Coursera | ~10h | 免费旁听 | 四种 Agent 模式，有代码但可只看视频 |
> | ★ Agents and Workflows | OpenAI Academy | ~1-2h | 完全免费 | Agent 辅助的工作流设计，动手练习 |
> | Hugging Face Agents Course | Hugging Face | 自定节奏 | 完全免费 | 需要 Python，适合想深入的人 |

> [!quote] 提示词技巧
> | 课程 | 来源 | 时长 | 费用 | 说明 |
> | --- | --- | --- | --- | --- |
> | ★ AI Prompting for Everyone | DeepLearning.AI | ~6h | 视频免费 | Andrew Ng 2026 新课，零代码 |
> | Prompting Essentials | Google / Coursera | ~10h | 7天免费 | 用 Gemini 讲提示词，含评估偏见 |
> | 提示词工程 | OpenAI Academy | 自定节奏 | 完全免费 | OpenAI 官方提示词课 |

> [!quote] AI 素养与框架
> | 课程 | 来源 | 时长 | 费用 | 说明 |
> | --- | --- | --- | --- | --- |
> | ★ AI Fluency: Framework & Foundations | Anthropic Academy | ~3h | 完全免费 | 有效、高效、安全地使用 AI 的框架 |
> | Applied AI Foundations | OpenAI Academy | ~1.5h | 完全免费 | 把 AI 嵌入实际工作流 |

> [!quote] 评测（Eval）
> | 课程 | 来源 | 时长 | 费用 | 说明 |
> | --- | --- | --- | --- | --- |
> | ★ Evaluating AI Agents | DeepLearning.AI | ~2.5h | 免费 | 专讲 Agent 评测，Trace/LLM-as-a-Judge/轨迹评测 |
> | ★ Evaluating, Governing, and Scaling AI Agents | Coursera / LearnQuest | ~4h | 免费旁听 | 零代码，讲评估可靠性和向管理层汇报，最适合 PM |
> | LLM Evaluations for AI Product Teams | Evidently AI | 7天邮件 | 完全免费 | 零代码，专为产品团队设计，有证书 |
> | Automated Testing for LLMOps | DeepLearning.AI | ~52min | 免费 | AI 系统的自动化测试和 CI/CD |

> [!quote] 产品经理 / 领导力
> | 课程 | 来源 | 时长 | 费用 | 说明 |
> | --- | --- | --- | --- | --- |
> | ★ AI Leadership | OpenAI Academy | ~3h | 完全免费 | AI 策略、治理、路线图——PM 专属 |
> | AI Product Manager Certificate | 微软 / Coursera | ~109h | 付费 | 微软 AI 产品经理认证，覆盖完整产品周期 |

> [!quote] 实用视频（非课程）
> | 视频 | 说明 |
> | --- | --- |
> | Karpathy — How I use LLMs | AI 专家的实际使用技巧，不讲原理 |
> | 3Blue1Brown — But what is a GPT? | 可视化讲 Transformer，零数学门槛 |
> | Karpathy — Intro to LLMs | 最经典的 LLM 入门，偏技术 |

---

## 补丁包 · 补齐这份路线没覆盖的能力

> [!warning] 为什么有这三张卡
> 这份路线教的是"Agent 是什么、怎么搭"，但缺三件做产品决策必须有的东西：
> **可靠性怎么算账、成本与延迟的红线、科研场景的特殊约束。**
> 建议学完模块 3 后插进来，每张约 1h，全是判断规则，没有代码。

> [!info] 三张判断卡
> - [[补丁A · 可靠性判断卡]] — 步数越多越不可靠，先砍步骤再调 prompt
> - [[补丁B · 成本与延迟判断卡]] — 单次成本决定这个功能能不能活
> - [[补丁D · 科研场景专项卡]] — 科研要的是可溯源，不是看起来专业
>
> 未写：补丁 C（什么时候不该做 Agent · 负面清单）

---

## 不需要学的内容（省时间）

> [!failure] 明确划掉的部分
> - ~~Transformer 数学推导、Attention 论文~~ → 看视频理解机制就行
> - ~~Stanford CS25 讲座~~ → 太学术
> - ~~5 个 Framework 横向对比~~ → 先只用一个跑通
> - ~~模型训练/微调/RLHF 细节~~ → 不是你的工作
> - ~~分布式训练/GPU/CUDA~~ → 完全不需要
> - ~~LangChain 全套文档~~ → 用到哪查哪，不用通读

---

> [!note] 导航
> - 前置：[[Agent AI 加速学习计划（4-6周版）]]
> - 同目录还有：`Agent_AI系统学习课程_2026版.docx`（未整理）
