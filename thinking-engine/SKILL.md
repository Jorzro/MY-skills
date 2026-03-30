---
name: thinking-engine
description: >
  宁雪思维引擎 — 复杂问题分析、决策判断、战略规划的智能路由系统。
  触发条件：用户提出需要分析、评估、决策、规划、优先级排序等问题。
  包含50+决策框架，支持意图识别、框架匹配、执行推导、结论输出全流程。
  当用户说"分析一下"、"怎么选"、"帮我决定"、"优先级"、"为什么"等关键词时激活。
  也会在用户提到"战略"、"竞争"、"机会"、"风险"、"复盘"、"创意"等场景时激活。
---

# Thinking Engine — 宁雪思维引擎

自包含的思维框架整合包，无需外部依赖，装完即可使用。

---

## 工作流程（4步）

```
用户问题 → Step1 复杂度评分 → Step2 意图匹配 → Step3 读取框架 → Step4 执行+结论输出
```

---

### Step 1：复杂度评分（0-10）

| 加分维度 | +分 |
|---------|-----|
| 多步骤逻辑/规划 | +3 |
| 模糊性/权衡取舍 | +2 |
| 代码架构/系统设计 | +2 |
| 数学/形式推理 | +2 |
| 高风险/不可逆 | +1 |
| 创新/无明显先例 | +1 |

**扣分**：简单查找 -3、清晰单一答案 -2、例行任务 -2

| 评分 | 动作 |
|------|------|
| ≤2 | 直接回答，不需要框架 |
| 3-5 | 标准回答 + 必要时加 1-2 个框架 |
| 6-7 | 开启推理模式 + 2-3 个相关框架 |
| ≥8 | 深度思考 + 多学科框架组合 |

---

### Step 2：意图匹配

根据问题类型，在 `references/framework-catalog.md` 中查找对应框架。

**快速匹配表**：

| 问题类型 | 触发关键词 | 推荐框架 |
|---------|-----------|---------|
| 做决定/选哪个 | "要不要" "选A还是B" "help me decide" | Binary Evaluation + Type1/2分类 |
| 分析/评估 | "分析一下" "评估这个" "怎么样" | Porter's Five Forces + Moat Assessment |
| 战略规划 | "怎么竞争" "战略" "市场进入" | Wardley + Scenario Planning + GTM |
| 危机/紧急 | "出事了" "怎么办" "危机" | Crisis Navigation + OODA Loop |
| 追根溯源 | "为什么" "根本原因" "为什么失败" | 5 Whys + Inversion + Pre-Mortem |
| 机会/投资判断 | "要不要投" "这个机会怎么样" | Expected Value + Margin of Safety + BATNA |
| 优先级排序 | "先做什么" "优先级" | ICE Scoring + Eisenhower Matrix |
| 团队分歧 | "团队意见不统一" "谁说了算" | Structured Disagreement + RACI |
| 个人重大决定 | "要不要离职" "转行" | Regret Minimization + Circle of Competence |
| 创意生成 | "有什么好主意" "创新" | Inversion + First Principles + 六学科透镜 |

---

### Step 3：框架检索与读取

**框架文件路径（自包含，无需外部安装）**：

| 框架 | 路径 |
|------|------|
| afrexai 核心框架（50+，主要来源） | `references/afrexai/SKILL.md` |
| 六顶思考帽 | `references/mental-models/six-thinking-hats/SKILL.md` |
| 第一性原理 | `references/mental-models/first-principles/SKILL.md` |
| 意图分类索引 | `references/framework-catalog.md` |

**读取原则**：
- 只读取本次用到的框架文件，不要全部加载
- 先读 `framework-catalog.md` 确认框架位置
- 再按需读具体框架文件

---

### Step 4：执行 + 结论输出

**输出格式（结论先行）**：
```
【结论】一句话核心判断

【依据】支撑结论的核心逻辑（2-3条）

【风险】结论成立的前提条件和潜在风险

【建议】下一步具体行动（1-3条）
```

**必须标注**：使用的框架名称

---

## 常用框架组合

| 场景 | 框架组合 |
|------|---------|
| 重大战略决策 | Pre-Mortem + Scenario Planning + Porter's + Second-Order |
| 日常优先级 | Eisenhower + ICE + Compounding |
| 问题根因分析 | 5 Whys + Inversion + First Principles |
| 机会评估 | Expected Value + Margin of Safety + BATNA |
| 团队分歧 | Structured Disagreement + Hanlon's Razor + RACI |
| 个人重大决定 | Regret Minimization + Circle of Competence |
| 创意生成 | Inversion + First Principles + 六学科透镜 |

---

## 禁止事项

- ❌ 不做复杂度评分直接开始分析
- ❌ 所有问题都用最复杂框架
- ❌ 把所有框架文件全部读进上下文
- ❌ 输出没有结论先行，铺垫很长
- ❌ 只给框架名称，不实际执行框架分析
