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
    page.set_default_timeout(60000)

    print('1. 访问创作者中心...')
    page.goto('https://creator.xiaohongshu.com/publish/publish')
    sleep(5)
    page.screenshot(path=f'{out_dir}/step1_landing.png')
    print(f'   URL: {page.url}')
    print(f'   Title: {page.title()}')

    print('2. 点击写长文...')
    page.click('text=写长文')
    sleep(3)
    page.screenshot(path=f'{out_dir}/step2_longtext.png')
    print(f'   URL: {page.url}')

    print('3. 点击新的创作...')
    try:
        page.click('text=新的创作')
        sleep(5)
    except Exception as e:
        print(f'   新的创作按钮未找到: {e}')
        # 尝试其他方式
        try:
            page.click('text=开始创作')
            sleep(5)
        except:
            print('   开始创作也没找到')
    
    page.screenshot(path=f'{out_dir}/step3_editor.png')
    print(f'   URL: {page.url}')

    # 打印页面上所有可见文本，帮助调试
    body = page.text_content('body')
    print(f'   页面文本(前500字): {body[:500]}')

    browser.close()
    print('调试完成')
