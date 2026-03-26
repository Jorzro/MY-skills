---
name: wechat-article-scraper-v2
description: |
  微信公众号文章爬虫 - 社区方案v2版
  
  核心方案（按优先级）：
  1. 微信PC端抓包（wechat_cookie + appmsg_token）- 最稳定
  2. 公众号后台登录（official_cookie + token）- 需要扫码
  3. 搜狗+Stealth - 快速测试（不稳定）
  
  关键：需要从微信客户端抓包获取参数，不能只靠Selenium模拟登录
---

# 微信公众号爬虫 v2 - 社区核心方案

## ⚠️ 重要发现（来自社区GitHub项目）

### 核心思路

微信爬虫的**关键不在于模拟登录**，而在于**获取两个关键参数**：

```
1. official_cookie + token     → 从公众号后台获取（扫码登录）
2. wechat_cookie + appmsg_token → 从微信PC端抓包获取（必须！）
```

### 为什么Selenium不够？

- 微信网页版功能有限
- 很多接口需要微信客户端登录态
- **必须用抓包工具获取参数**

---

## 方案详解

### 方案1：微信PC端抓包（推荐⭐）

**步骤**：
```
1. 在电脑上打开微信PC端
2. 设置代理，启动抓包工具（Charles/Fiddler/mitmproxy）
3. 打开任意微信公众号文章
4. 从抓包中提取 wechat_cookie 和 appmsg_token
```

**提取参数**：
```python
# 从抓包数据中找到类似这样的请求
# URL: https://mp.weixin.qq.com/s?xxx
# Cookie: wechatSkey=xxx; wap_sid=xxx; ...
# appmsg_token: xxx~xxx
```

### 方案2：公众号后台扫码

**步骤**：
```
1. 访问 https://mp.weixin.qq.com/
2. 扫码登录
3. 从Cookie和URL中提取 token
```

### 方案3：搜狗+Stealth（备选）

- 只适合搜索，无法获取完整文章
- 成功率低

---

## 完整代码框架

```python
import requests

class WeChatCrawlerV2:
    """微信爬虫v2 - 基于抓包参数"""
    
    def __init__(self, official_cookie, token, wechat_cookie, appmsg_token):
        self.official_cookie = official_cookie
        self.token = token
        self.wechat_cookie = wechat_cookie
        self.appmsg_token = appmsg_token
    
    def get_account_articles(self, biz_id, begin=0, count=5):
        """获取公众号文章列表"""
        url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
        params = {
            "action": "list_ex",
            "begin": begin,
            "count": count,
            "type": 9,
            "token": self.token,
            "lang": "zh_CN",
            "f": "json",
        }
        headers = {"Cookie": self.official_cookie}
        
        resp = requests.get(url, params=params, headers=headers)
        return resp.json()
    
    def get_article_stats(self, article_url):
        """获取文章阅读/点赞/评论"""
        # 需要 wechat_cookie 和 appmsg_token
        url = "https://mp.weixin.qq.com/s"
        # ... 提取阅读数和点赞数
        pass
    
    def download_article(self, article_url):
        """下载文章内容"""
        # 提取文章正文
        pass
```

---

## 参数获取指南

### 1. 获取 official_cookie 和 token

**方法A：Selenium扫码**
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://mp.weixin.qq.com/")

# 扫码后从driver获取cookies
cookies = driver.get_cookies()
token = # 从URL中提取 ?token=xxx
```

**方法B：手动**
1. 浏览器登录 mp.weixin.qq.com
2. F12 → Application → Cookies
3. 复制 cookie 和 URL中的 token

### 2. 获取 wechat_cookie 和 appmsg_token

**必须用抓包工具**：
```
1. 安装 Charles 或 mitmproxy
2. 配置手机/电脑代理
3. 用微信打开任意公众号文章
4. 从抓包请求中提取参数
```

**参数位置**：
- Cookie: 请求头中的 Cookie
- appmsg_token: URL参数中的 `appmsg_token=xxx~xxx`

---

## 自动保存和使用

```python
import json
from pathlib import Path

CONFIG_PATH = Path("~/.wechat_scraper").expanduser()

def save_params(official_cookie, token, wechat_cookie, appmsg_token):
    """保存参数到本地"""
    CONFIG_PATH.mkdir(exist_ok=True)
    
    data = {
        "official_cookie": official_cookie,
        "token": token,
        "wechat_cookie": wechat_cookie,
        "appmsg_token": appmsg_token,
        "update_time": time.time()
    }
    
    with open(CONFIG_PATH / "params.json", "w") as f:
        json.dump(data, f)

def load_params():
    """加载参数"""
    path = CONFIG_PATH / "params.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None
```

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 参数失效 | 重新扫码/抓包 |
| 访问频繁 | 每页间隔3-5分钟 |
| 被封 | 等待24小时或换账号 |
| 缺少参数 | 确保同时有4个参数 |

---

## 参考项目

- [wechat_articles_spider](https://github.com/wnma3mz/wechat_articles_spider) - 最火的Python方案
- [WeChat_Article](https://github.com/1061700625/WeChat_Article) - 带GUI

---

## 总结

**核心**：微信爬虫不是简单模拟登录，而是需要获取**真实微信客户端的登录态参数**。Selenium只能获取公众号后台参数，**必须配合抓包**才能完整工作。
