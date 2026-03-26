---
name: wechat-article-workflow
description: 公众号文章全流程工作流。从热点选题、深度调研、六顶思考帽分析、写作到发布的完整自动化流程。适用于需要快速产出高质量公众号文章的的场景。
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "skillKey": "wechat-article-workflow",
        "primaryEnv": "",
        "requires":
          {
            "bins": ["wenyan", "xreach", "playwright"],
            "env": ["WECHAT_APP_ID", "WECHAT_APP_SECRET"],
            "skills":
              [
                "hot-topics",
                "x-twitter",
                "six-thinking-hats",
                "wechat-mp-writer-skill-mxx",
                "wechat-publisher",
                "news-aggregator-skill",
                "wechat-article-scraper",
                "marketing-psychology",
                "academic-deep-research",
                "copywriting",
                "humanize-writing",
                "ai-humanizer-2-1-0",
                "content-quality-auditor",
                "storytelling",
                "deep-research",
              ],
          },
        "install": [],
      },
  }
---

# 📝 公众号文章全流程工作流

> 从热点选题 → 深度调研 → 六顶思考帽分析 → 写作 →发布的完整自动化流程

---

## ✅ 技能安装状态

| Skill | 状态 | 路径 |
|-------|------|------|
| `hot-topics` | ✅ 已安装 | `~/.agents/skills/hot-topics/` |
| `x-twitter` | ✅ 已安装 | `~/.agents/skills/x-twitter/` |
| `six-thinking-hats` | ✅ 已安装 | `~/.agents/skills/six-thinking-hats/` |
| `wechat-mp-writer-skill-mxx` | ✅ 已安装（别名wechat-mp-writer） | `~/.openclaw/workspace/skills/wechat-mp-writer-skill-mxx/` |
| `wechat-publisher` | ✅ 已安装 | `~/.openclaw/workspace/skills/wechat-publisher/` |
| `news-aggregator-skill` | ✅ 已安装 | `~/.agents/skills/news-aggregator-skill/` |
| `wechat-article-scraper` | ✅ 已安装 | `~/.agents/skills/wechat-article-scraper/` |
| `marketing-psychology` | ✅ 已安装 | `~/.agents/skills/marketing-psychology/` |
| `academic-deep-research` | ✅ 已安装 | `~/.openclaw/workspace/skills/academic-deep-research/` |
| `copywriting` | ✅ 已安装 | `~/.agents/skills/copywriting/` |
| `humanize-writing` | ✅ 已安装 | `~/.agents/skills/humanize-writing/` |
| `ai-humanizer-2-1-0` | ✅ 已安装 | `~/.openclaw/workspace/skills/ai-humanizer-2-1-0/` |
| `content-quality-auditor` | ✅ 已安装 | `~/.openclaw/workspace/skills/content-quality-auditor/` |
| `storytelling` | ✅ 已安装 | `~/.openclaw/workspace/skills/storytelling/` |
| `deep-research` | ✅ 已安装 | `~/.agents/skills/deep-research/` |

**16个技能全部就绪！** 🎉

---

## 📋 Skill 注册表（16个技能详解）

> 每个 Skill 的路径、作用、输入输出、调用方式

---

### Skill 1️⃣ hot-topics

```
路径：~/.agents/skills/hot-topics/
作用：获取微博/知乎/百度/抖音/今日头条/B站 实时热搜
输入：关键词 + 平台列表
输出：各平台热搜榜单（JSON格式）
调用：curl 命令直接调用 viki.moe API
```

**调用方式：**
```bash
# 微博热搜
curl -s "https://60s.viki.moe/v2/weibo" | jq '.[:5]'

# 知乎热搜
curl -s "https://60s.viki.moe/v2/zhihu" | jq '.[:5]'

# 百度热搜
curl -s "https://60s.viki.moe/v2/baidu/hot" | jq '.[:5]'

# B站热搜
curl -s "https://60s.viki.moe/v2/bili" | jq '.[:5]'

# 抖音热搜
curl -s "https://60s.viki.moe/v2/douyin" | jq '.[:5]'

# 今日头条
curl -s "https://60s.viki.moe/v2/toutiao" | jq '.[:5]'
```

**工作流使用：** STAGE 1 热点搜索

---

### Skill 2️⃣ x-twitter

```
路径：~/.agents/skills/x-twitter/
作用：搜索Twitter/X、YouTube、Reddit国际热榜
输入：关键词 + 平台 + 数量
输出：搜索结果列表
调用：xreach 命令
```

**调用方式：**
```bash
# Twitter搜索
xreach search "{keyword}" --json -n 20 --platform twitter

# YouTube搜索
xreach search "{keyword}" --json -n 10 --platform youtube

# Reddit搜索
xreach search "{keyword}" --json -n 10 --platform reddit
```

**工作流使用：** STAGE 1 国际热点、STAGE 3 国际视角补充

---

### Skill 3️⃣ six-thinking-hats

```
路径：~/.agents/skills/six-thinking-hats/
作用：六顶思考帽分析，从6个维度分析选题
输入：调研报告 + 选题背景
输出：六帽分析报告（事实/情感/风险/价值/创意/决策）
调用：读取 SKILL.md，按指引执行六帽分析
```

**调用方式：**
```bash
# 读取skill文件
cat ~/.agents/skills/six-thinking-hats/SKILL.md
```

**六帽分析内容：**
```
🤍 WHITE（事实帽）：提取关键数据、统计数字、权威引用
❤️ RED（情感帽）：分析读者情感反应、直觉判断
🖤 BLACK（风险帽）：识别风险、争议、审核问题
💛 YELLOW（价值帽）：发现价值、机会、独特视角
💚 GREEN（创意帽）：挖掘新角度、差异化切入点
🔵 BLUE（行动帽）：综合输出写作方向、文章结构、核心观点
```

**工作流使用：** STAGE 4 六帽分析

---

### Skill 4️⃣ wechat-mp-writer-skill-mxx

```
路径：~/.openclaw/workspace/skills/wechat-mp-writer-skill-mxx/
作用：微信公众号文章写作（替代原 wechat-mp-writer）
输入：选题 + 调研报告 + 故事线 + 文案框架 + 六帽分析
输出：完整文章正文（Markdown格式）
调用：读取 SKILL.md，按指引执行写作
```

**调用方式：**
```bash
# 读取skill文件
cat ~/.openclaw/workspace/skills/wechat-mp-writer-skill-mxx/SKILL.md
```

**输入内容：**
```markdown
## 选题
标题：{title}
角度：{angle}

## 调研报告摘要
{research_summary}

## 故事线
{story_outline}

## 文案框架
{title_formula}
{opening_hook}
{structure}
{cta}

## 六帽分析结论
{writing_direction}
{article_structure}
{core_thesis}

## 营销心理画像
目标读者：{reader_persona}
核心痛点：{pain_points}
情绪触发点：{emotion_triggers}
```

**工作流使用：** STAGE 5 文章撰写（核心写作引擎）

---

### Skill 5️⃣ wechat-publisher

```
路径：~/.openclaw/workspace/skills/wechat-publisher/
作用：一键发布Markdown到微信公众号草稿箱
输入：article-final.md + 环境变量（WECHAT_APP_ID, WECHAT_APP_SECRET）
输出：发布结果（成功/失败）
调用：wenyan-cli 命令
```

**调用方式：**
```bash
# 设置环境变量
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret_app_secret

# 发布到草稿箱
~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh article-final.md
```

**工作流使用：** STAGE 6 发布

---

### Skill 6️⃣ news-aggregator-skill

```
路径：~/.agents/skills/news-aggregator-skill/
作用：新闻聚合，获取8大中文平台的实时资讯
输入：关键词/主题
输出：新闻汇总（Hacker News/GitHub/36Kr/腾讯新闻/微博等）
调用：读取 SKILL.md，按指引执行聚合
```

**调用方式：**
```bash
cat ~/.agents/skills/news-aggregator-skill/SKILL.md
```

**覆盖平台：**
- Hacker News
- GitHub Trending
- Product Hunt
- 36Kr
- 腾讯新闻
- WallStreetCN
- V2EX
- 微博

**工作流使用：** STAGE 3 新闻调研

---

### Skill 7️⃣ wechat-article-scraper

```
路径：~/.agents/skills/wechat-article-scraper/
作用：爬取微信公众号文章内容
输入：关键词
输出：相关微信文章列表及摘要
调用：读取 SKILL.md，使用 playwright 爬取
```

**调用方式：**
```bash
cat ~/.agents/skills/wechat-article-scraper/SKILL.md
```

**备用爬取方案（stealth模式）：**
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--disable-blink-features=AutomationControlled']
  });
  const context = await browser.newContext({
    viewport: { width: 375, height: 667 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)...'
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  await page.goto('目标URL', { waitUntil: 'networkidle' });
  const content = await page.evaluate(() => document.body.innerText);
  await browser.close();
})();
```

**工作流使用：** STAGE 3 微信文章调研

---

### Skill 8️⃣ marketing-psychology

```
路径：~/.agents/skills/marketing-psychology/
作用：营销心理学分析，用户心理画像
输入：选题 + 热点背景
输出：
  - 目标读者画像
  - 核心痛点（3个）
  - 情绪触发点
  - 用户心智模型
调用：读取 SKILL.md，应用心理模型分析
```

**调用方式：**
```bash
cat ~/.agents/skills/marketing-psychology/SKILL.md
```

**分析框架：**
```
1. 目标读者是谁？
   - 人口统计特征
   - 行为特征
   - 关注点

2. 核心痛点（挖掘3个）
   - 显性痛点
   - 隐性痛点
   - 情感痛点

3. 情绪触发点
   - 恐惧触发
   - 好奇触发
   - 共鸣触发
   - 贪婪触发

4. 用户心智模型
   - 现有认知
   - 认知偏差
   - 如何打破认知
```

**工作流使用：** STAGE 2 营销心理画像

---

### Skill 9️⃣ academic-deep-research

```
路径：~/.openclaw/workspace/skills/academic-deep-research/
作用：学术级深度调研，2轮研究循环，APA引用，证据分级
输入：研究主题
输出：学术报告（摘要/数据来源/学术观点/参考文献）
调用：读取 SKILL.md，执行深度研究流程
```

**调用方式：**
```bash
cat ~/.openclaw/workspace/skills/academic-deep-research/SKILL.md
```

**研究流程：**
```
第一轮：广泛搜索
- 学术数据库检索
- 行业报告收集
- 数据统计汇编

第二轮：深度分析
- 证据分级评估
- 观点对比分析
- 结论提炼

输出：APA格式报告 + 引用来源
```

**工作流使用：** STAGE 3 深度调研（优先级最高）

---

### Skill 🔟 copywriting

```
路径：~/.agents/skills/copywriting/
作用：专业文案框架，标题/开头/结构/CTA
输入：主题 + 目标读者 + 情绪触发点
输出：
  - 5个候选标题
  - 3秒开头钩子
  - 文章结构
  - 结尾CTA
调用：读取 SKILL.md，应用文案框架
```

**调用方式：**
```bash
cat ~/.agents/skills/copywriting/SKILL.md
```

**文案框架内容：**
```markdown
## 标题公式
1. 数字+悬念：《{N}个XX，第{数字}个最关键》
2. 对比+反差：《XX vs XX，区别居然是...》
3. 痛点+方案：《XX怎么办？试试这个》
4. 热点+解读：《XX刷屏，我发现了...》
5. 疑问+解答：《XX是真的吗？》

## 开头钩子（3秒法则）
- 痛点切入
- 故事切入
- 数据切入
- 反常识切入

## 文章结构
- 引子（hook）
- 主体（小标题+论点）
- 收尾（总结+CTA）

## 结尾CTA
- 互动型
- 转发型
- 引流型
```

**工作流使用：** STAGE 5 文案框架构建

---

### Skill 1️⃣1️⃣ humanize-writing

```
路径：~/.agents/skills/humanize-writing/
作用：AI写作去味润色，消除机器感
输入：article-draft.md（AI初稿）
输出：article-polished.md（人性化版本）
调用：读取 SKILL.md，执行去味流程
```

**调用方式：**
```bash
cat ~/.agents/skills/humanize-writing/SKILL.md
```

**去味内容：**
```
1. 句式变化
   - 长短句交错
   - 主动被动切换
   - 句式多样化

2. 词汇优化
   - 替换机械词汇
   - 增加口语化表达
   - 同义词替换

3. 过渡优化
   - 自然过渡词
   - 逻辑连接

4. 人格化表达
   - 增加个人视角
   - 语气词添加
   - 情感色彩
```

**工作流使用：** STAGE 5 AI去味（主方案）

---

### Skill 1️⃣2️⃣ ai-humanizer-2-1-0

```
路径：~/.openclaw/workspace/skills/ai-humanizer-2-1-0/
作用：AI去味备用方案（二次优化）
输入：article-polished.md
输出：article-final.md（如需优化）
调用：读取 SKILL.md，执行二次去味
```

**调用方式：**
```bash
cat ~/.openclaw/workspace/skills/ai-humanizer-2-1-0/SKILL.md
```

**触发条件：**
```
如果 humanize-writing 效果不够理想，调用此技能进行二次优化
```

**工作流使用：** STAGE 5 AI去味（备用方案）

---

### Skill 1️⃣3️⃣ content-quality-auditor

```
路径：需安装 ~/.agents/skills/content-quality-auditor/
作用：内容质量审计，错别字/敏感词/可读性检查
输入：article-final.md
输出：quality-report.md + 通过/不通过
调用：安装后读取 SKILL.md，执行质检
```

**安装命令：**
```bash
npx clawhub@latest install content-quality-auditor
```

**调用方式（安装后）：**
```bash
cat ~/.agents/skills/content-quality-auditor/SKILL.md
```

**质检内容：**
```
1. 错别字扫描
   - 中文错别字
   - 标点符号

2. 敏感词检测
   - 政治敏感词
   - 广告法禁用词
   - 平台违规词

3. 可读性分析
   - 句子长度
   - 段落长度
   - 专业术语解释

4. 标题吸引力评估
   - 是否够吸引
   - 是否符合公众号调性

5. 内容结构评估
   - 逻辑是否清晰
   - 小标题是否准确
```

**质量门控：**
```
质检不通过 → 返回 STAGE 5 修改 → 重新质检
```

**工作流使用：** STAGE 6 质检（必须通过才能发布）

---

### Skill 1️⃣4️⃣ storytelling

```
路径：~/.openclaw/workspace/skills/storytelling/
作用：故事叙述框架，让文章更打动人
输入：主题 + 核心观点 + 目标读者
输出：story-outline.md
调用：读取 SKILL.md，构建故事线
```

**调用方式：**
```bash
cat ~/.openclaw/workspace/skills/storytelling/SKILL.md
```

**故事框架内容：**
```markdown
## 开头切入点
- 场景描写
- 人物故事
- 数据故事
- 热点故事

## 叙事弧线
- 起（设定背景）
- 承（问题出现）
- 转（冲突升级）
- 合（解决/升华）

## 情感高潮安排
- 在文章1/3处设置第一个情感点
- 在文章2/3处设置高潮
- 结尾留白引发思考

## 结尾升华
- 价值升华
- 金句点题
- 行动号召
```

**工作流使用：** STAGE 5 故事框架构建

---

### Skill 1️⃣5️⃣ deep-research

```
路径：~/.agents/skills/deep-research/
作用：企业级深度研究，多源综合，引用追踪
输入：研究主题
输出：深度分析报告（10+来源，验证的结论）
调用：读取 SKILL.md，执行研究
```

**调用方式：**
```bash
cat ~/.agents/skills/deep-research/SKILL.md
```

**研究特点：**
```
- 10+信息源综合
- 引用追踪验证
- 多角度对比分析
- 结构化报告输出
```

**与 academic-deep-research 的区别：**
```
academic-deep-research：学术级，更严谨，适合论文级别调研
deep-research：企业级，更实用，适合商业内容调研
两者叠加使用，确保调研全面性
```

**工作流使用：** STAGE 3 深度调研（叠加使用）

---

## 🗺️ STAGE 与 Skill 对应矩阵

```
STAGE 1：热点搜索
├── hot-topics（中文6平台）✅
└── x-twitter（国际平台）✅

STAGE 2：选题确认 + 营销心理画像
├── [用户选择] → 输出选题
└── marketing-psychology → 用户心理画像 ✅

STAGE 3：深度调研
├── academic-deep-research ✅（最高优先级）
├── deep-research ✅（补充）
├── wechat-article-scraper ✅
├── news-aggregator-skill ✅
└── x-twitter（国际视角）✅

STAGE 4：六顶思考帽分析
└── six-thinking-hats ✅

STAGE 5：文章写作
├── storytelling → 故事框架 ✅
├── copywriting → 文案框架 ✅
├── wechat-mp-writer-skill-mxx → 文章撰写 ✅（核心）
├── humanize-writing → AI去味 ✅（主方案）
└── ai-humanizer-2-1-0 → AI去味 ✅（备用）

STAGE 6：内容质检 + 发布
├── content-quality-auditor → 质检 ✅（需安装）
└── wechat-publisher → 发布 ✅
```

---

## 📊 完整数据流

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1：热点搜索                                           │
│                                                             │
│ INPUT：{keyword}                                            │
│                                                             │
│ PROCESS：                                                   │
│   hot-topics → 中文6平台热搜                                │
│   x-twitter → Twitter/YouTube热搜                          │
│                                                             │
│ OUTPUT：hot-topics-report.md                               │
│   ├── 微博TOP5                                             │
│   ├── 知乎TOP5                                             │
│   ├── 百度TOP5                                             │
│   ├── B站TOP5                                              │
│   ├── 抖音TOP5                                             │
│   └── Twitter/YouTube TOP10                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2：选题确认 + 营销心理画像                             │
│                                                             │
│ INPUT：hot-topics-report.md                                 │
│                                                             │
│ PROCESS：                                                   │
│   1. 呈现热点列表 → 用户选择                               │
│   2. marketing-psychology → 心理画像                       │
│                                                             │
│ OUTPUT：topic-confirmed.md                                  │
│   ├── 用户选择：{title}                                    │
│   ├── 选题角度：{angle}                                    │
│   ├── 目标读者：{reader_persona}                           │
│   ├── 核心痛点：[点1, 点2, 点3]                           │
│   ├── 情绪触发点：{emotion_triggers}                       │
│   └── 用户心智模型：{mental_model}                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3：深度调研                                           │
│                                                             │
│ INPUT：topic-confirmed.md                                   │
│                                                             │
│ PROCESS（按优先级）：                                        │
│   1. academic-deep-research → 学术报告                     │
│   2. deep-research → 多角度分析                            │
│   3. wechat-article-scraper → 竞品微信文章                │
│   4. news-aggregator-skill → 新闻汇总                     │
│   5. x-twitter → 国际视角                                 │
│                                                             │
│ OUTPUT：research-report.md                                  │
│   ├── 学术摘要                                             │
│   ├── 多角度分析                                           │
│   ├── 微信文章要点                                         │
│   ├── 新闻汇总                                             │
│   └── 国际视角                                             │
│                                                             │
│ ⚠️ 质量门控：至少3个可信来源才能进入下一阶段               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4：六顶思考帽分析                                     │
│                                                             │
│ INPUT：                                                     │
│   - research-report.md                                     │
│   - topic-confirmed.md                                     │
│                                                             │
│ PROCESS：                                                   │
│   six-thinking-hats                                         │
│   ├── 🤍 WHITE → 关键数据/事实                             │
│   ├── ❤️ RED → 情感反应                                    │
│   ├── 🖤 BLACK → 风险/问题                                 │
│   ├── 💛 YELLOW → 价值/机会                                │
│   ├── 💚 GREEN → 创意/角度                                │
│   └── 🔵 BLUE → 写作方向/结构/核心观点                     │
│                                                             │
│ OUTPUT：six-hats-analysis.md                                │
│   ├── 各帽分析结论                                         │
│   ├── 写作方向                                             │
│   ├── 文章结构                                             │
│   └── 核心观点                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5：文章写作（5步顺序执行）                            │
│                                                             │
│ INPUT：                                                     │
│   - topic-confirmed.md                                     │
│   - research-report.md                                     │
│   - six-hats-analysis.md                                   │
│                                                             │
│ STEP 5.1：storytelling                                      │
│   INPUT：topic + six_hats                                  │
│   OUTPUT：story-outline.md                                 │
│                                                             │
│ STEP 5.2：copywriting                                       │
│   INPUT：topic + reader_persona + emotion_triggers         │
│   OUTPUT：copy-framework.md                                │
│   ├── 5个候选标题                                          │
│   ├── 开头钩子                                             │
│   ├── 文章结构                                             │
│   └── 结尾CTA                                              │
│                                                             │
│ STEP 5.3：wechat-mp-writer-skill-mxx                        │
│   INPUT：                                                   │
│     - 选题 + 角度                                          │
│     - 调研报告                                             │
│     - 故事线                                               │
│     - 文案框架                                             │
│     - 六帽结论                                             │
│     - 心理画像                                             │
│   OUTPUT：article-draft.md                                 │
│                                                             │
│ STEP 5.4：humanize-writing                                  │
│   INPUT：article-draft.md                                  │
│   OUTPUT：article-polished.md                              │
│                                                             │
│ STEP 5.5：ai-humanizer-2-1-0（备用）                        │
│   INPUT：article-polished.md                               │
│   OUTPUT：article-final.md                                 │
│                                                             │
│ STEP 5.6：添加作者简介（必须！不可跳过）                     │
│   内容：在文章结尾添加作者信息                               │
│   格式：                                                    │
│     🎨 本文作者：绾绾                                        │
│     AI内容创作助手 | 要么不写，写就写进心里 💖               │
│                                                             │
│ 最后 OUTPUT：article-final.md（包含作者简介）                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 6：内容质检 + 发布                                    │
│                                                             │
│ INPUT：article-final.md                                     │
│                                                             │
│ STEP 6.1：content-quality-auditor（必须）                   │
│   INPUT：article-final.md                                  │
│   PROCESS：                                                 │
│     ├── 错别字检查 → ❌→ 返回STEP 5.4重新去味            │
│     ├── 敏感词检测 → ❌→ 返回STEP 5.3修改内容            │
│     ├── 可读性分析                                         │
│     ├── 标题吸引力                                         │
│     └── 结构评估                                           │
│   OUTPUT：quality-report.md + 通过/不通过                   │
│                                                             │
│ STEP 6.2：wechat-publisher                                  │
│   INPUT：质检通过后的article-final.md                      │
│   ENV：WECHAT_APP_ID, WECHAT_APP_SECRET                    │
│   COMMAND：publish.sh article-final.md                     │
│   OUTPUT：发布结果                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 中间产物存储规范

```
~/.openclaw/workspace-content/articles/{YYYY-MM-DD-HHMMSS}/
├── 01-hot-topics-report.md      # 热点报告
├── 02-topic-confirmed.md        # 选题确认+心理画像
├── 03-research-report.md        # 深度调研报告
├── 04-six-hats-analysis.md     # 六帽分析
├── 05-story-outline.md         # 故事线
├── 06-copy-framework.md         # 文案框架
├── 07-article-draft.md         # 文章初稿
├── 08-article-polished.md      # 去味后文章
├── 09-article-final.md         # 最终文章
└── 10-quality-report.md        # 质检报告
```

---

## ⚠️ 注意事项

1. **顺序执行**：STAGE 1→2→3→4→5→6 必须按顺序执行
2. **质检门控**：STAGE 6 质检不通过必须返回 STAGE 5 修改
3. **调研门控**：STAGE 3 必须有至少3个可信来源
4. **Skill调用**：使用前先读取对应 SKILL.md 文件
5. **文件传递**：每个STAGE输出文件作为下一STAGE输入
6. **待安装**：content-quality-auditor 需要先安装

---

## 🚀 快速启动

```
📝 帮我写一篇公众号文章
📝 工作流：写一篇关于[关键词]的文章
```

---

*工作流创建：2026-03-14*
*最后更新：2026-03-23*
*更新内容：Skill注册表完整重构，16个技能详细说明，数据流矩阵化*
