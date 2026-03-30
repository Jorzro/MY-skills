# Thinking Engine

> 宁雪思维引擎 — 复杂问题分析、决策判断、战略规划的智能路由系统

## 功能

- **意图识别**：自动判断问题类型（决策、分析、规划、优先级等）
- **复杂度评分**：0-10分，自动选择推理深度
- **框架匹配**：50+决策框架，精准匹配场景
- **结构化输出**：结论先行，包含依据、风险、建议

## 快速开始

### 安装

```bash
# 克隆到本地 skills 目录
git clone https://github.com/Jorzro/MY-skills.git
cd MY-skills/thinking-engine

# 或复制到 OpenClaw skills 目录
cp -r thinking-engine ~/.openclaw/skills/
```

### 使用

在支持 OpenClaw Skills 的 Agent 中直接提问：

```
帮我分析一下这个机会靠不靠谱...
我该不该离职去创业...
团队吵起来了怎么决策...
```

## 目录结构

```
thinking-engine/
├── SKILL.md                          # 主入口（路由逻辑）
├── references/
│   ├── afrexai/SKILL.md              # 核心框架（50+决策框架）
│   ├── mental-models/
│   │   ├── six-thinking-hats/SKILL.md # 六顶思考帽
│   │   └── first-principles/SKILL.md  # 第一性原理
│   └── framework-catalog.md           # 意图分类索引
├── scripts/
│   └── clean-temp-docs.sh             # 7天清理脚本
└── evals/
    └── evals.json                    # 测试用例
```

## 工作流

```
用户问题
  ↓
Step1: 复杂度评分（0-10）
  ↓
Step2: 意图匹配 → 确定框架类型
  ↓
Step3: 读取对应框架文件（按需，无则不读）
  ↓
Step4: 执行框架 + 结论输出
```

## 测试

```bash
# 运行测试用例
openclaw skills test thinking-engine
```

## 开源协议

MIT License
