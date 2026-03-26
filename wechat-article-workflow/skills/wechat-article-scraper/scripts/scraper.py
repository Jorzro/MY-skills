#!/usr/bin/env python3
"""
微信公众号爬虫 - 核心引擎
支持多方案自动切换：Selenium登录 -> Cookie复用 -> 搜狗搜索
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import Optional, List, Dict

# 配置路径
CONFIG_DIR = Path.home() / ".wechat_scraper"
COOKIE_PATH = CONFIG_DIR / "cookies.json"
TOKEN_PATH = CONFIG_DIR / "token.json"

# 确保目录存在
CONFIG_DIR.mkdir(exist_ok=True)


class WeChatScraper:
    """微信公众号爬虫引擎"""
    
    def __init__(self):
        self.session = requests.Session()
        self.cookies = self._load_cookies()
        self.token = self._load_token()
    
    # ==================== 状态管理 ====================
    
    def _load_cookies(self) -> Optional[dict]:
        """加载Cookie"""
        if COOKIE_PATH.exists():
            try:
                with open(COOKIE_PATH, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def _save_cookies(self, cookies: dict):
        """保存Cookie"""
        with open(COOKIE_PATH, 'w') as f:
            json.dump(cookies, f)
        self.cookies = cookies
    
    def _load_token(self) -> Optional[str]:
        """加载Token"""
        if TOKEN_PATH.exists():
            try:
                with open(TOKEN_PATH, 'r') as f:
                    data = json.load(f)
                    return data.get('token')
            except:
                return None
        return None
    
    def _save_token(self, token: str):
        """保存Token"""
        with open(TOKEN_PATH, 'w') as f:
            json.dump({'token': token, 'time': time.time()}, f)
        self.token = token
    
    # ==================== 方案1: Cookie复用 ====================
    
    def check_cookie_valid(self) -> bool:
        """检查Cookie是否有效"""
        if not self.cookies:
            return False
        
        try:
            url = "https://mp.weixin.qq.com/"
            response = self.session.get(url, cookies=self.cookies, timeout=10)
            # 如果跳转到了登录页，说明Cookie失效
            return "login" not in response.url
        except:
            return False
    
    def crawl_article(self, url: str) -> Optional[Dict]:
        """爬取单篇文章（需要Cookie）"""
        if not self.check_cookie_valid():
            print("⚠️ Cookie失效，请先运行 selenium_login() 扫码")
            return None
        
        try:
            # 访问文章页
            response = self.session.get(url, cookies=self.cookies, timeout=30)
            
            # 提取文章内容（简化版）
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find('title').text if soup.find('title') else ""
            content = soup.find('div', id='js_content')
            text = content.get_text() if content else ""
            
            return {
                'title': title,
                'content': text,
                'url': url,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"❌ 爬取失败: {e}")
            return None
    
    def crawl_account(self, account_name: str) -> List[Dict]:
        """爬取公众号所有文章（需要Cookie）"""
        if not self.check_cookie_valid():
            print("⚠️ Cookie失效，请先运行 selenium_login() 扫码")
            return []
        
        # 这里需要调用微信搜索API，略复杂
        # 简化版本返回空列表
        print(f"📱 爬取公众号: {account_name}")
        return []
    
    # ==================== 方案2: Selenium登录 ====================
    
    def selenium_login(self) -> bool:
        """Selenium扫码登录（需要安装selenium和chrome）"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            import selenium.webdriver.support.ui as ui
            
            print("=" * 50)
            print("📱 启动 Selenium 扫码登录")
            print("请在弹出的浏览器中扫码登录微信")
            print("=" * 50)
            
            # 配置Chrome
            options = Options()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1200,800')
            
            driver = webdriver.Chrome(options=options)
            
            # 访问登录页
            driver.get("https://mp.weixin.qq.com/")
            
            # 等待用户扫码（最多60秒）
            print("⏳ 等待扫码中...")
            time.sleep(60)
            
            # 检查是否登录成功
            current_url = driver.url
            
            if "login" not in current_url:
                # 获取Cookie
                cookies = driver.get_cookies()
                cookie_dict = {c['name']: c['value'] for c in cookies}
                self._save_cookies(cookie_dict)
                
                # 获取Token（从Cookie或URL）
                token = cookie_dict.get('token', '')
                if token:
                    self._save_token(token)
                
                driver.quit()
                print("✅ 登录成功！Cookie已保存")
                return True
            else:
                driver.quit()
                print("❌ 登录超时")
                return False
                
        except ImportError:
            print("❌ 请安装 selenium: pip install selenium")
            print("   并下载 ChromeDriver")
            return False
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False
    
    # ==================== 方案3: 搜狗+Stealth ====================
    
    def sogou_search(self, query: str) -> List[Dict]:
        """搜狗微信搜索 + Playwright Stealth"""
        try:
            from playwright.sync_api import sync_playwright
            
            print(f"🔍 搜狗搜索: {query}")
            
            with sync_playwright() as p:
                # 启动Stealth浏览器
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
                
                # 注入反检测脚本
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    window.navigator.chrome = true;
                """)
                
                page = context.new_page()
                
                # 访问搜狗
                page.goto(f"https://weixin.sogou.com/weixin?type=2&query={query}")
                page.wait_for_timeout(3000)
                
                # 提取链接
                results = []
                links = page.query_selector_all('a[href*="mp.weixin.qq.com"]')
                
                for link in links[:10]:
                    try:
                        title = link.inner_text().strip()
                        href = link.get_attribute('href')
                        if title and href:
                            results.append({
                                'title': title,
                                'url': href
                            })
                    except:
                        continue
                
                browser.close()
                
                if results:
                    print(f"✅ 找到 {len(results)} 篇文章")
                else:
                    print("⚠️ 未找到文章（可能被反爬）")
                
                return results
                
        except ImportError:
            print("❌ 请安装 playwright: pip install playwright")
            print("   并运行: playwright install chromium")
            return []
        except Exception as e:
            print(f"❌ 搜狗搜索失败: {e}")
            return []
    
    # ==================== 智能入口 ====================
    
    def smart_crawl(self, target: str) -> Dict:
        """
        智能爬取 - 自动选择方案
        target: 公众号名称 或 文章链接 或 关键词
        """
        
        # 判断输入类型
        is_url = target.startswith('http')
        
        print(f"\n{'='*50}")
        print(f"🎯 目标: {target}")
        print(f"{'='*50}\n")
        
        # 方案1: 如果是URL，尝试Cookie
        if is_url:
            print("📋 检测为文章链接，尝试Cookie方案...")
            result = self.crawl_article(target)
            if result:
                return {'method': 'cookie', 'data': result}
            
            print("📋 Cookie失效，尝试搜狗方案...")
            results = self.sogou_search(target)
            if results:
                return {'method': 'sogou', 'data': results}
        
        # 方案2: 如果是公众号名，尝试Cookie
        else:
            print("📋 检测为公众号名称，尝试Cookie方案...")
            results = self.crawl_account(target)
            if results:
                return {'method': 'cookie', 'data': results}
            
            print("📋 尝试搜狗搜索...")
            results = self.sogou_search(target)
            if results:
                return {'method': 'sogou', 'data': results}
        
        # 所有方案都失败
        return {
            'method': 'failed',
            'message': '所有方案都失败，请尝试: scraper.selenium_login() 扫码登录'
        }


# ==================== 命令行接口 ====================

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
微信公众号爬虫 CLI
用法:
  python -m wechat_scraper login      # Selenium扫码登录
  python -m wechat_scraper crawl <目标>  # 爬取
  python -m wechat_scraper search <关键词> # 搜狗搜索
        """)
        return
    
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    target = sys.argv[2] if len(sys.argv) > 2 else ""
    
    scraper = WeChatScraper()
    
    if action == "login":
        scraper.selenium_login()
    elif action == "crawl":
        result = scraper.smart_crawl(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif action == "search":
        results = scraper.sogou_search(target)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}\n")
    else:
        print(f"未知命令: {action}")


if __name__ == "__main__":
    main()
