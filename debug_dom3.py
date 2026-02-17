#!/usr/bin/env python3
import json
import os
from time import sleep
from playwright.sync_api import sync_playwright

cookie_path = os.path.expanduser('~/.openclaw/secrets/xiaohongshu.json')
stealth_path = os.path.join(os.path.dirname(__file__), 'stealth.min.js')
out_dir = '/home/node/.openclaw/workspace'

with open(cookie_path, 'r') as f:
    data = json.load(f)

cookies = [{'name': k, 'value': str(v), 'domain': '.xiaohongshu.com', 'path': '/'} for k, v in data.items()]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_init_script(path=stealth_path)
    context.add_cookies(cookies)
    page = context.new_page()
    page.set_default_timeout(30000)

    page.goto('https://creator.xiaohongshu.com/publish/publish')
    sleep(5)
    
    # 点击写长文
    page.click('text=写长文')
    print('点击了写长文，等待10秒...')
    sleep(10)
    
    # 截图看看
    page.screenshot(path=f'{out_dir}/debug3_after_wait.png')
    
    # 获取完整HTML结构（前5000字符）
    html = page.evaluate("() => document.body.innerHTML.slice(0, 8000)")
    print('=== HTML片段 ===')
    print(html[:5000])
    
    # 再试试获取body文本
    body = page.text_content('body')
    print('\n=== Body文本(前800字) ===')
    print(body[:800])
    
    browser.close()
