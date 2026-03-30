# 宁雪思维框架目录 (Brain Router - 框架检索索引)

> 所有思维框架的意图分类索引。用户提问 → 匹配框架 → 按需读取执行。
> **不是把所有框架塞进上下文，而是通过这个目录检索，按需调用。**

---

## 一、意图分类索引（核心查询表）

### 1.1 用户问题类型 → 匹配框架

| 问题类型 | 触发关键词 | 推荐框架 | 优先级 |
|---------|-----------|---------|-------|
| **做决定/选哪个** | "要不要" "选A还是B" "应该怎么选" "help me decide" | Binary Evaluation + Type1/2分类 | ⭐⭐⭐ |
| **分析/评估** | "分析一下" "评估这个" "怎么样" "好不好" | Por

ter's Five Forces + Moat Assessment + Decision Quality Rubric | ⭐⭐⭐ |
| **战略规划** | "怎么竞争" "战略" "未来规划" "市场进入" | Wardley Mapping + Scenario Planning + GTM Strategy | ⭐⭐⭐ |
| **危机/紧急** | "出事了" "怎么办" "紧急" "危机" | Crisis Navigation (CEO) + OODA Loop + Antifragility | ⭐⭐⭐ |
| **追根溯源** | "为什么" "原因" "根本原因" "为什么失败" | 5 Whys + Inversion + Pre-Mortem | ⭐⭐⭐ |
| **团队决策分歧** | "团队意见不统一" "谁说了算" "吵" | Structured Disagreement + RACI + Hanlon's Razor | ⭐⭐ |
| **机会/投资判断** | "要不要投" "这个机会怎么样" "值不值" | Expected Value + Margin of Safety + BATNA | ⭐⭐ |
| **创意生成** | "有什么好主意" "创新" "想不到办法" | Inversion + First Principles + Combinatorial Creativity | ⭐⭐ |
| **优先排序** | "先做什么" "优先级" "怎么排" | ICE Scoring + Eisenhower Matrix + Compounding (哪个收益最大) | ⭐⭐ |
| **理解复杂概念** | "帮我理解" "解释" "是什么" | Socratic Decomposition + Thinking Partner + 5 Whys | ⭐ |
| **自我复盘** | "哪里做错了" "复盘" "反思" | Decision Record + Pre-Mortem + Bias Checklist | ⭐ |
| **资源配置** | "资源分配" "先投哪个" "预算怎么花" | Compounding + Opportunity Cost + Via Negativa | ⭐ |
| **谈判/说服** | "怎么谈" "说服" "谈判" | BATNA + Cialdini + Second-Order Effects | ⭐ |
| **个人重大决定** | "要不要离职" "转行" "人生选择" | Regret Minimization + Circle of Competence + 24h Rule | ⭐ |

---

## 二、框架详细目录

### 2.1 决策框架 (Decision)

#### 🔷 Binary Evaluation (Rationality - CF)
- **文件**: `rationality/frameworks/decision.md`
- **核心**: 想法只有两种状态——被证伪 vs 未被证伪。不打分不加权，一个关键缺陷即否决
- **适用**: 所有决策的过滤阶段——先二元过滤，再考虑其他
- **流程**: 定义 Goal → 设约束 Breakpoint → 二元过滤 → 如都通过则随机挑一个或设新约束
- **宁雪何时用**: 任何决策第一步，先问"这个方案有什么致命缺陷？"

#### 🔷 Type 1 vs Type 2 分类 (afrexai-strategic-thinking)
- **核心**: 区分可逆决策（快）和不可逆决策（慢）
- **Type 1**: 一次做错无法挽回 → 充分分析、多次审视、一人心决
- **Type 2**: 错了容易改 → 快速决定、迭代、不完美也行
- **宁雪何时用**: 拿到任何决策，先判断"这是 Type 1 还是 Type 2？"决定投入多少分析资源

#### 🔷 Decision Quality Rubric (afrexai-strategic-thinking)
- **核心**: 评估决策流程质量（0-100分），不只看结果
- **维度**: 问题定义清晰度、选项数量、证据质量、偏见防御、利益相关者、二阶效应、可逆性、时间配比
- **宁雪何时用**: 复盘时或重大决策后打分，总结决策过程质量

#### 🔷 Pre-Mortem (afrexai-strategic-thinking)
- **核心**: "想象6个月后这事彻底失败，哪里出了问题？"
- **流程**: 独立头脑风暴 → 合并 → 找预防措施和早期信号
- **宁雪何时用**: 任何计划实施前必做，防止乐观偏见

#### 🔷 BATNA Analysis (afrexai-strategic-thinking)
- **核心**: 谈判前先算清自己的最佳替代方案，这决定了你的底线和谈判力
- **宁雪何时用**: 任何谈判场景前

---

### 2.2 战略框架 (Strategy)

#### 🔷 Porter's Five Forces (afrexai-strategic-thinking)
- **核心**: 评估行业吸引力——新进入者、供应商议价、买家议价、替代品、行业竞争
- **评分**: 每个力1-5分，合计≤10分=有吸引力，≥18=困难
- **宁雪何时用**: 进入新市场、评估行业竞争强度

#### 🔷 Moat Assessment (afrexai-strategic-thinking)
- **核心**: 护城河8种类型评分——网络效应、转换成本、品牌、规模经济、专有技术、监管、分销、反定位
- **宁雪何时用**: 评估公司或产品的持久竞争优势

#### 🔷 Wardley Mapping (afrexai-strategic-thinking)
- **核心**: X轴=进化阶段(Genesis→Custom→Product→Commodity)，Y轴=用户可见度
- **法则**: Genesis/Custom要自建（差异化），Product/Commodity要买（别重复造轮子）
- **宁雪何时用**: 制定技术或产品战略时

#### 🔷 Scenario Planning (afrexai-strategic-thinking)
- **核心**: 不预测未来，准备多种未来——乐观/基准/悲观/黑天鹅
- **宁雪何时用**: 重大战略决策前（市场进入、产品转型、投资）

#### 🔷 OODA Loop (afrexai-strategic-thinking)
- **核心**: Observe→Orient→Decide→Act，加速循环即可超越对手
- **宁雪何时用**: 竞争激烈需要快速响应时

#### 🔷 Executive Synthesis (MBB - mbb-strategist)
- **核心**: 麦肯锡风格结论先行，结构化表达
- **格式**: 结论→依据→风险→建议
- **宁雪何时用**: 汇报、方案展示、给用户清晰建议时

#### 🔷 SWOT + Porter's (MBB - mbb-strategist)
- **核心**: 经典战略定位组合
- **宁雪何时用**: 任何战略分析的标准开场

---

### 2.3 思维模型 (Mental Models)

#### 🔷 六学科透镜 (mental-models)
- **核心**: 任何问题用6个学科透镜看：物理/工程、生物/进化、心理/行为、经济/商业、数学/统计、历史/哲学
- **流程**: 每个学科选最相关模型 → 交叉验证 → 找共识（高置信）vs分歧（需深挖）
- **宁雪何时用**: 复杂问题分析，每个主要决策都应该用多学科交叉验证

#### 🔷 First Principles 三步法 (first-principles-thinking)
- **核心**: Decompose（拆解到物理/逻辑约束）→ Verify（追问每个假设来源）→ Rebuild（从验证后的基本事实重建）
- **隐藏假设检测**: 历史假设/权威假设/类比假设/社会假设/资源假设
- **宁雪何时用**: 遇到"一直这么做"或"专家说X"时，先做第一性原理拆解

#### 🔷 Inversion (afrexai-strategic-thinking)
- **核心**: 不问"怎么成功"，而问"怎么必然失败"
- **宁雪何时用**: 创意匮乏时、过度乐观时

#### 🔷 Second-Order Thinking (afrexai-strategic-thinking)
- **核心**: 1阶效应→2阶效应→3阶效应，追问"然后呢？"
- **宁雪何时用**: 任何重大决策前，防止只看表面

#### 🔷 Circle of Competence (afrexai-strategic-thinking)
- **核心**: 分清楚"我真懂"、"我知道自己不懂"、"我完全不懂"三个圈
- **宁雪何时用**: 遇到自己不熟悉的领域的决策时

#### 🔷 Antifragility Assessment (afrexai-strategic-thinking)
- **核心**: 系统在混乱中变强还是变弱？评分-10到+10
- **宁雪何时用**: 评估业务/团队/投资组合的韧性

#### 🔷 Via Negativa (afrexai-strategic-thinking)
- **核心**: 最好的决策是做减法——删功能、删目标、删复杂
- **宁雪何时用**: 感觉事情太多太杂时

#### 🔷 Lindy Effect (afrexai-strategic-thinking)
- **核心**: 存在越久的东西，未来存活概率越高
- **宁雪何时用**: 选技术、选方法论时——老祖宗的方法可能更可靠

---

### 2.4 分析框架 (Analysis)

#### 🔷 5 Whys (afrexai-strategic-thinking)
- **核心**: 追问5层"为什么"，找根本原因而非症状
- **宁雪何时用**: 问题排查、根因分析

#### 🔷 Socratic Decomposition (first-principles-thinking)
- **核心**: 递归追问"为什么"，直到触达物理/逻辑/数学不可反驳的层面
- **宁雪何时用**: 深度理解复杂概念，拆解到最基本

#### 🔷 Expected Value + Kelly Criterion (afrexai-strategic-thinking)
- **核心**: EV = (win概率 × win金额) - (loss概率 × loss金额)，正值才值得下注
- **宁雪何时用**: 投资机会、重大资源投入决策

#### 🔷 Margin of Safety (afrexai-strategic-thinking)
- **核心**: 内在价值和当前价格的差值——安全边际越大越好
- **应用**: 不只用于投资，可用于招聘（此人能力是否超出需求30%？）

#### 🔷 Build vs Buy Matrix (afrexai-strategic-thinking)
- **核心**: 核心差异化要自建，通用能力要外购
- **宁雪何时用**: 技术选型、资源分配决策

---

### 2.5 优先级框架 (Prioritization)

#### 🔷 ICE Scoring (afrexai-strategic-thinking)
- **核心**: Score = Impact × Confidence × Ease，三维度评分
- **宁雪何时用**: 功能优先级、资源分配优先级

#### 🔷 Eisenhower Matrix (afrexai-strategic-thinking)
- **核心**: 重要/紧急四象限，Q2（重要不紧急）是最有价值的时间投资
- **宁雪何时用**: 时间管理、日程安排

#### 🔷 Compounding (afrexai-strategic-thinking)
- **核心**: 找1%每天在哪个维度能改善的东西——复利效应巨大
- **宁雪何时用**: 长期规划、日常优先级

#### 🔷 Opportunity Cost (afrexai-strategic-thinking)
- **核心**: 每一个Yes都是对其他所有选项的No
- **宁雪何时用**: 接受新项目、新任务前

---

### 2.6 认知防御 (Cognitive Defense)

#### 🔷 Bias Checklist (afrexai-strategic-thinking)
- **核心**: 确认偏见、锚定、沉没成本、幸存者、Dunning-Kruger等12种认知偏见
- **防御**: 每个决策前主动检查
- **宁雪何时用**: 任何重大决策前作为 checklist

#### 🔷 Confidence Calibration (afrexai-strategic-thinking)
- **核心**: 大多数人过度自信——以为90%确定，实际可能70%
- **宁雪何时用**: 评估自己或他人的判断时

---

### 2.7 深度思考流程 (Thinking Processes)

#### 🔷 Deep Thinking Protocol (deep-thinking)
- **核心**: 七步：初始理解→分解→多假设→自然发现→验证纠错→综合→递归应用
- **特点**: 有机探索式，不是机械步骤
- **宁雪何时用**: 复杂问题（评分≥8）、多系统问题、架构决策

#### 🔷 Sequential Thinking (sequential-thinking)
- **核心**: 分解→逐步解决→验证一致性→综合→置信度评分
- **特点**: 强制逐步分解，防止过早下结论
- **宁雪何时用**: 有明确步骤的多阶段问题

#### 🔷 Adaptive Reasoning (adaptive-reasoning)
- **核心**: 复杂度自评估（0-10分），决定用多少推理资源
- **≤2分**: 快速直接回答
- **3-5分**: 标准分析
- **6-7分**: 开启推理模式
- **≥8分**: 深度思考模式
- **宁雪何时用**: 每个问题先做复杂度评分，再决定处理深度

#### 🔷 Thinking Partner (thinking-partner)
- **核心**: 提问优先于回答，保持探索模式，不急于给答案
- **关键提问**: "这背后真正的问题是什么？" "反过来的观点是什么？" "我们忽略了什么？"
- **宁雪何时用**: 用户需要一起探索而非直接要答案时

#### 🔷 六顶思考帽 (six-thinking-hats)
- **核心**: 白(事实)→红(直觉)→黑(风险)→黄(优势)→绿(创意)→蓝(流程)
- **宁雪何时用**: 团队讨论、决策评审、方案评估

---

### 2.8 CEO/管理层框架

#### 🔷 Crisis Navigation (ceo)
- **核心**: 24小时→一周→恢复期，分阶段危机处理
- **原则**: 快但不要慌、一个声音、记录一切
- **宁雪何时用**: 危机事件

#### 🔷 Pre-Mortem (CEO+afrexai)
- **见2.1**

#### 🔷 RACI (afrexai-strategic-thinking)
- **核心**: 每个决策明确 Responsible/Accountable/Consulted/Informed
- **关键**: Accountable必须只有一个人
- **宁雪何时用**: 团队决策、跨部门项目

#### 🔷 Structured Disagreement (afrexai-strategic-thinking)
- **核心**: 独立写出观点→同时公开→steel man对方→找核心分歧事实问题
- **宁雪何时用**: 团队意见严重分歧时

#### 🔷 Decision Record (afrexai-strategic-thinking)
- **核心**: 每个重大决策记录：背景/选项/依据/风险/成功标准/复盘日期
- **宁雪何时用**: 战略级决策，记录并定期复盘

---

## 三、宁雪大脑工作流 (执行流程)

### 收到用户问题 → 标准处理流程

```
Step 1: 复杂度评分 (Adaptive Reasoning)
  → 0-2分: 直接回答，不需要框架
  → 3-5分: 标准回答 + 必要时加1-2个框架
  → 6-7分: 开启推理 + 2-3个相关框架
  → 8+分: 深度思考 + 多学科框架组合

Step 2: 意图匹配 (查"一、意图分类索引")
  → 找到对应问题类型 → 锁定推荐框架

Step 3: 框架检索
  → 查"二、框架详细目录" → 找到框架名称和文件位置
  → 读取目标框架文件（如需要）

Step 4: 执行框架分析
  → 按框架步骤执行
  → 如需要多框架，组合使用

Step 5: 输出结论
  → 结论先行（Executive Synthesis格式）
  → 附上框架依据
```

### 框架组合参考（常见场景）

| 场景 | 框架组合 |
|------|---------|
| 重大战略决策 | Pre-Mortem + Scenario Planning + Porter's + Second-Order + Bias Check |
| 日常优先级 | Eisenhower + ICE + Compounding + Opportunity Cost |
| 问题根因分析 | 5 Whys + Inversion + First Principles + 六学科透镜 |
| 机会评估 | Expected Value + Margin of Safety + BATNA + Asymmetric Risk |
| 团队分歧 | Structured Disagreement + Hanlon's Razor + RACI |
| 个人重大决定 | Regret Minimization + Circle of Competence + 24h Rule + 六学科透镜 |
| 创意生成 | Inversion + First Principles + 六学科透镜 + Via Negativa |
| 竞争分析 | Porter's + Moat + OODA + Wardley Mapping |

---

## 四、文件索引（按需读取）

| 框架名称 | 文件路径 |
|---------|---------|
| Binary Evaluation | `workspace/skills/rationality/frameworks/decision.md` |
| Type1/2分类 | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 1 |
| Decision Quality Rubric | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 10 |
| Pre-Mortem | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 4 |
| BATNA | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 6 |
| Porter's Five Forces | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| Moat Assessment | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| Wardley Mapping | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| Scenario Planning | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 4 |
| OODA Loop | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| 六学科透镜 | `workspace/skills/mental-models/SKILL.md` |
| First Principles | `workspace/skills/first-principles-thinking/SKILL.md` |
| Inversion | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 2 |
| Second-Order | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 5 |
| ICE Scoring | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| Eisenhower Matrix | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| Bias Checklist | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 4 |
| Deep Thinking Protocol | `workspace/skills/deep-thinking/SKILL.md` |
| Sequential Thinking | `workspace/skills/sequential-thinking/SKILL.md` |
| Adaptive Reasoning | `workspace/skills/adaptive-reasoning/SKILL.md` |
| Thinking Partner | `workspace/skills/thinking-partner/SKILL.md` |
| 六顶思考帽 | `workspace/skills/six-thinking-hats/SKILL.md` |
| Crisis Navigation | `workspace/skills/ceo/SKILL.md` |
| Executive Synthesis | `workspace/skills/mbb-strategist/SKILL.md` |
| MBB Frameworks | `workspace/skills/mbb-strategist/references/frameworks.md` |
| CEO Suite | `workspace/skills/ceo/SKILL.md` (strategy/decisions/board/finance/people/operations) |
| Expected Value | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 5 |
| Margin of Safety | `workspace/skills/afrexai-strategic-thinking/SKILL.md` Phase 3 |
| Rationality CF | `workspace/skills/rationality/SKILL.md` |
| Rationality Errors | `workspace/skills/rationality/patterns/errors.md` |
| Rationality Overreach | `workspace/skills/rationality/patterns/overreach.md` |
| Rationality Paths-Forward | `workspace/skills/rationality/frameworks/paths-forward.md` |
| mental-models-cn | `workspace/skills/mental-models-cn/SKILL.md` |
