---
name: wechat-article-scraper
description: |
  微信公众号文章爬虫 - 绕过微信验证墙的多方案智能爬取工具。
  
  支持4种方案按优先级自动切换：
  1. Selenium扫码登录（最稳定）
  2. Cookie复用（较快）
  3. 搜狗微信+Stealth（快速测试）
  4. 微信搜索接口（需要公众号权限）
  
  适用场景：
  - 爬取指定公众号的所有文章
  - 根据关键词搜索文章
  - 批量获取文章内容
  - 定时监控公众号更新
  
  自动处理：
  - 验证码识别（提示用户扫码）
  - Cookie过期自动刷新
  - 频率限制自动降速
  - 失败自动切换方案
---

# 微信公众号文章爬虫 Skill

## 核心能力

1. **多方案智能切换** - 根据成功率自动选择最优方案
2. **状态持久化** - 保存Cookie/Token避免重复登录
3. **自动降级** - 方案失败自动切换下一个
4. **错误恢复** - 验证码/频率限制自动处理

---

## 方案优先级

```
优先级从高到低：
┌────────────────────────────────────────────────────────────┐
│  层级   │     方案          │  成功率 │    适用场景        │
├─────────┼──────────────────┼─────────┼───────────────────┤
│  SSSS   │ 微信开放API       │  100%   │ 企业资质(官方)     │
│  SSS    │ Selenium扫码登录  │  85%    │ 长期稳定运行       │
│  SS     │ Cookie复用       │  70%    │ 中期批量爬取       │
│  S      │ 搜狗+Stealth     │  50%    │ 快速测试/少量     │
│  A      │ 微信搜索接口      │  60%    │ 有公众号权限       │
└─────────┴──────────────────┴─────────┴───────────────────┘
```

---

## 使用方式

### 方式1：直接调用（推荐）

根据用户输入自动判断并执行：

```python
# 用户输入：公众号名称
input_type = "公众号名称"  # 或 "文章链接"、"关键词"

# 自动选择方案
if input_type == "公众号名称":
   方案 = "Cookie复用"  # 或 Selenium
elif input_type == "文章链接":
    方案 = "搜狗+Stealth"  # 先尝试
elif input_type == "关键词":
    方案 = "搜狗搜索"
```

### 方式2：指定方案

```
!scraper --method selenium --target 公众号名称
!scraper --method cookie --target 文章链接
!scraper --method sogou --query 关键词
```

---

## 方案详解

### 方案1：Selenium扫码登录（SSS级）

**核心代码**：
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def selenium_login():
    """Selenium扫码登录，获取Token和Cookie"""
    
    # 1. 配置Chrome选项（反检测）
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # 2. 随机User-Agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...')
    
    # 3. 启动浏览器
    driver = webdriver.Chrome(options=options)
    
    # 4. 访问微信登录页
    driver.get("https://mp.weixin.qq.com/")
    
    # 5. 等待用户扫码（提示用户）
    print("请在30秒内扫码登录...")
    time.sleep(30)
    
    # 6. 获取Token和Cookie
    cookies = driver.get_cookies()
    token = # 从URL或Cookie中提取Token
    
    # 7. 保存状态
    save_state({"token": token, "cookies": cookies})
    
    return token, cookies
```

**关键点**：
- 必须使用反检测配置
- 扫码后立即保存Cookie
- Token有效期约2小时

### 方案2：Cookie复用（SS级）

**核心代码**：
```python
import json
import time
import requests

def load_cookies():
    """加载保存的Cookie"""
    try:
        with open('cookies.json', 'r') as f:
            return json.load(f)
    except:
        return None

def check_cookie_valid(cookies):
    """检查Cookie是否有效"""
    url = "https://mp.weixin.qq.com/"
    response = requests.get(url, cookies=cookies)
    return "登录" not in response.url  # 如果跳转了说明失效

def crawl_with_cookie(cookies, target):
    """使用Cookie爬取"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://mp.weixin.qq.com/'
    }
    
    # 根据目标类型构建请求
    if is_article_link(target):
        # 获取文章内容
        return crawl_article(cookies, target)
    else:
        # 获取公众号文章列表
        return crawl_account(cookies, target)
```

**关键点**：
- Cookie存储在本地文件
- 每次使用前验证有效性
- 失效则提示用户重新扫码

### 方案3：搜狗微信+Stealth（S级）

**核心代码**：
```python
from playwright.sync_api import sync_playwright

def sogou_stealth_search(query):
    """搜狗微信搜索 + Stealth模式"""
    
    with sync_playwright() as p:
        # 1. 启动Stealth浏览器
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        # 2. 注入反检测脚本
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.navigator.chrome = true;
        """)
        
        page = context.new_page()
        
        # 3. 访问搜狗微信搜索
        page.goto(f"https://weixin.sogou.com/weixin?type=2&query={query}")
        page.wait_for_timeout(2000)
        
        # 4. 提取文章链接
        links = page.query_selector_all('a[href*="mp.weixin.qq.com"]')
        
        results = []
        for link in links[:10]:
            title = link.inner_text()
            href = link.get_attribute('href')
            results.append({'title': title, 'url': href})
        
        return results
```

**关键点**：
- 使用Playwright Stealth模式
- 搜狗搜索可能被限制
- 成功率约50%

### 方案4：微信搜索接口（A级）

**核心思路**：
利用公众号管理员"写新文章"时能搜索其他公众号的功能

```python
def wechat_search_api(cookies, keyword):
    """微信搜索API（需要公众号登录）"""
    
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    
    params = {
        'action': 'search_appmsg',
        'keyword': keyword,
        'type': 'search_appmsg',
        'token': cookies.get('token'),
        'lang': 'zh_CN'
    }
    
    response = requests.get(url, cookies=cookies, params=params)
    return response.json()
```

**关键点**：
- 需要有公众号权限
- 接口相对稳定
- 但有频率限制

---

## 自动降级机制

```python
def smart_crawl(target, input_type):
    """智能爬取 - 自动降级"""
    
    # 定义方案链（按优先级）
    methods = [
        ('cookie', crawl_with_cookie),      # 优先Cookie
        ('selenium', selenium_login_crawl),  # 次选Selenium
        ('sogou', sogou_stealth_search),    # 备选搜狗
    ]
    
    # 依次尝试
    for method_name, method_func in methods:
        try:
            print(f"尝试方案: {method_name}")
            result = method_func(target)
            
            if result:
                print(f"✓ {method_name} 成功")
                return result
                
        except Exception as e:
            print(f"✗ {method_name} 失败: {e}")
            continue  # 自动切换下一个方案
    
    return None  # 所有方案都失败
```

---

## 状态管理

### Cookie存储
```python
# 保存路径
COOKIE_PATH = "~/.wechat_scraper/cookies.json"
TOKEN_PATH = "~/.wechat_scraper/token.json"
```

### 状态检查
```python
def check_and_refresh_state():
    """检查并刷新状态"""
    cookies = load_cookies()
    
    if not cookies or not check_cookie_valid(cookies):
        print("Cookie失效，需要重新登录...")
        # 提示用户扫码
        token, cookies = selenium_login()
    
    return cookies
```

---

## 错误处理

| 错误类型 | 错误码 | 处理方式 |
|----------|--------|----------|
| 验证码 | freq_control | 提示用户、等待后重试 |
| 频率限制 | -c | 自动降速、增加延迟 |
| Cookie失效 | 401 | 自动刷新Cookie |
| IP被封 | - | 切换代理IP |
| 网络超时 | timeout | 重试3次 |

---

## 完整使用示例

### 示例1：爬取公众号文章
```python
# 输入：公众号名称
target = "OpenClaw"

# 自动选择方案
result = smart_crawl(target, input_type="公众号名称")

# 输出：文章列表
for article in result:
    print(f"标题: {article['title']}")
    print(f"链接: {article['url']}")
    print(f"日期: {article['date']}")
```

### 示例2：爬取单篇文章
```python
# 输入：文章链接
url = "https://mp.weixin.qq.com/s/xxxxx"

# 先尝试搜狗方案
result = sogou_stealth_crawl(url)

# 失败则用Cookie
if not result:
    result = cookie_crawl(url)

print(result['content'])
```

### 示例3：关键词搜索
```python
# 输入：关键词
query = "OpenClaw 教程"

# 使用搜狗搜索
results = sogou_stealth_search(query)

for r in results:
    print(f"{r['title']}: {r['url']}")
```

---

## 安装依赖

```bash
pip install selenium playwright requests beautifulsoup4
playwright install chromium
```

---

## 注意事项

1. **合规使用** - 仅用于学习研究，尊重公众号版权
2. **频率控制** - 不要短时间内大量请求
3. **Cookie安全** - 本地存储，不要分享给他人
4. **微信政策** - 微信可能随时更改接口，方案需要持续更新

---

## 相关项目参考

- [WeChat_Article](https://github.com/1061700625/WeChat_Article) - 带GUI的爬虫
- [wechat_articles_spider](https://github.com/wnma3mz/wechat_articles_spider) - Python版爬虫
- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) - Web版

---

## 维护者

- 创建日期：2026-03-11
- 基于社区方案整合
- 持续更新以适应微信反爬升级
