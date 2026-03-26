#!/usr/bin/env node

/**
 * 每日热点捕获系统 v5 (稳定版)
 * 使用稳定的 viki.moe API
 * 
 * 支持平台：微博、抖音、B站、今日头条、V2EX
 * (小红书需要MCP手动获取)
 * 
 * v6: 增加推送给飞书用户功能
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
  outputDir: path.join(__dirname, 'hot-topics-output'),
  defaultLimit: 15,
  baseUrl: 'https://60s.viki.moe/v2',
  // 推送给飞书用户
  notifyUser: process.env.HOT_TOPICS_NOTIFY === 'true',
  feishuUserId: process.env.FEISHU_USER_ID || 'ou_ec471637ffb545a3ef0b272bd5c497bb'
};

const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

// 带重试的HTTP请求
async function httpGetWithRetry(url, retries = 2) {
  for (let i = 0; i < retries; i++) {
    try {
      return await httpGet(url);
    } catch (e) {
      if (i === retries - 1) throw e;
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname,
      method: 'GET',
      headers: { 'User-Agent': getRandomUA() },
      timeout: 15000
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch { resolve(null); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => reject(new Error('超时')));
    req.end();
  });
}

async function getWeiboHot() {
  try {
    const data = await httpGetWithRetry(`${CONFIG.baseUrl}/weibo`);
    const list = (data.data || []).slice(0, CONFIG.defaultLimit).map((item, i) => ({
      rank: i + 1, title: item.title, hot: item.hot_value
    }));
    return { platform: '微博', icon: '🔥', list };
  } catch (e) {
    return { platform: '微博', icon: '🔥', error: e.message };
  }
}

async function getDouyinHot() {
  try {
    const data = await httpGetWithRetry(`${CONFIG.baseUrl}/douyin`);
    const list = (data.data || []).slice(0, CONFIG.defaultLimit).map((item, i) => ({
      rank: i + 1, title: item.title, hot: item.hot_value
    }));
    return { platform: '抖音', icon: '🎵', list };
  } catch (e) {
    return { platform: '抖音', icon: '🎵', error: e.message };
  }
}

async function getBiliHot() {
  try {
    const data = await httpGetWithRetry(`${CONFIG.baseUrl}/bili`);
    const list = (data.data || []).slice(0, CONFIG.defaultLimit).map((item, i) => ({
      rank: i + 1, title: item.title, hot: item.desc
    }));
    return { platform: 'B站', icon: '📺', list };
  } catch (e) {
    return { platform: 'B站', icon: '📺', error: e.message };
  }
}

async function getToutiaoHot() {
  try {
    const data = await httpGetWithRetry(`${CONFIG.baseUrl}/toutiao`);
    const list = (data.data || []).slice(0, CONFIG.defaultLimit).map((item, i) => ({
      rank: i + 1, title: item.title, hot: item.HotValue
    }));
    return { platform: '今日头条', icon: '📰', list };
  } catch (e) {
    return { platform: '今日头条', icon: '📰', error: e.message };
  }
}

async function getV2exHot() {
  try {
    const data = await httpGetWithRetry('https://www.v2ex.com/api/topics/hot.json');
    const list = (data || []).slice(0, CONFIG.defaultLimit).map((item, i) => ({
      rank: i + 1, title: item.title, hot: item.replies + ' 回复'
    }));
    return { platform: 'V2EX', icon: '💬', list };
  } catch (e) {
    return { platform: 'V2EX', icon: '💬', error: e.message };
  }
}

// 推送给飞书用户
async function sendToFeishu(content) {
  try {
    const userId = CONFIG.feishuUserId;
    const cmd = `openclaw message send --channel feishu --account secretary -t "${userId}" -m "${content.replace(/"/g, '\\"')}"`;
    console.log(`📤 正在推送给飞书用户...`);
    execSync(cmd, { encoding: 'utf8' });
    console.log(`✅ 已推送给飞书用户`);
    return true;
  } catch (e) {
    console.error(`❌ 推送失败:`, e.message);
    return false;
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  const funcs = {
    weibo: getWeiboHot,
    douyin: getDouyinHot,
    bili: getBiliHot,
    toutiao: getToutiaoHot,
    v2ex: getV2exHot
  };
  
  let selected = Object.keys(funcs);
  if (args.includes('--platform')) {
    const idx = args.indexOf('--platform');
    selected = (args[idx + 1] || '').split(',').filter(p => funcs[p]);
  }
  
  // 检查是否需要推送
  const shouldNotify = args.includes('--notify') || process.env.HOT_TOPICS_NOTIFY === 'true';
  
  console.log(`📡 正在获取 ${selected.length} 个平台热点...\n`);
  
  const results = await Promise.all(selected.map(name => funcs[name]()));
  
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  let md = `# 📈 每日热点速览\n\n> 更新时间：${now}\n\n---\n\n`;
  
  for (const item of results) {
    if (item.error) {
      md += `### ${item.icon} ${item.platform}\n\n> 获取失败：${item.error}\n\n---\n\n`;
      continue;
    }
    
    md += `### ${item.icon} ${item.platform}\n\n`;
    if (item.list?.length > 0) {
      for (const t of item.list) {
        md += `${t.rank}. **${t.title}**${t.hot ? ` (${typeof t.hot === 'number' ? t.hot.toLocaleString() : t.hot})` : ''}\n`;
      }
    } else {
      md += '_暂无数据_\n';
    }
    md += '\n---\n\n';
  }
  
  // 添加小红书提示
  md += `### 📕 小红书\n\n> 小红书需要通过MCP获取，请运行：\`node scripts/daily-hot-topics-xhs.js\`\n\n---\n\n`;
  
  console.log(md);
  
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }
  
  const date = new Date().toISOString().slice(0, 10);
  fs.writeFileSync(
    path.join(CONFIG.outputDir, `hot-${date}.md`),
    md
  );
  console.log(`✅ 已保存到: ${CONFIG.outputDir}/hot-${date}.md`);
  
  // 推送给用户
  if (shouldNotify) {
    const notifyContent = `📈 **每日热点速览** ${now}\n\n${md}`;
    await sendToFeishu(notifyContent);
  }
}

main().catch(console.error);
