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

    print('1. 访问创作者中心...')
    page.goto('https://creator.xiaohongshu.com/publish/publish')
    sleep(5)

    print('2. 点击写长文...')
    page.click('text=写长文')
    sleep(5)
    
    page.screenshot(path=f'{out_dir}/debug_editor.png')
    print(f'   URL: {page.url}')

    # 打印所有input/textarea/contenteditable元素
    print('\n=== 所有输入元素 ===')
    
    textareas = page.locator('textarea').all()
    print(f'textarea数量: {len(textareas)}')
    for i, ta in enumerate(textareas):
        try:
            ph = ta.get_attribute('placeholder')
            vis = ta.is_visible()
            print(f'  textarea[{i}]: placeholder="{ph}", visible={vis}')
        except Exception as e:
            print(f'  textarea[{i}]: error={e}')

    inputs = page.locator('input[type="text"]').all()
    print(f'input[text]数量: {len(inputs)}')
    for i, inp in enumerate(inputs):
        try:
            ph = inp.get_attribute('placeholder')
            vis = inp.is_visible()
            print(f'  input[{i}]: placeholder="{ph}", visible={vis}')
        except Exception as e:
            print(f'  input[{i}]: error={e}')

    editables = page.locator('[contenteditable="true"]').all()
    print(f'contenteditable数量: {len(editables)}')
    for i, ed in enumerate(editables):
        try:
            tag = ed.evaluate('el => el.tagName')
            cls = ed.evaluate('el => el.className')
            vis = ed.is_visible()
            print(f'  editable[{i}]: tag={tag}, class="{cls[:60]}", visible={vis}')
        except Exception as e:
            print(f'  editable[{i}]: error={e}')

    # 查找包含"标题"的placeholder
    title_els = page.locator('[placeholder*="标题"]').all()
    print(f'\n包含"标题"placeholder的元素: {len(title_els)}')
    for i, el in enumerate(title_els):
        try:
            tag = el.evaluate('el => el.tagName')
            vis = el.is_visible()
            print(f'  [{i}]: tag={tag}, visible={vis}')
        except Exception as e:
            print(f'  [{i}]: error={e}')

    # 查找iframe
    frames = page.frames
    print(f'\niframe数量: {len(frames)}')
    for i, f in enumerate(frames):
        print(f'  frame[{i}]: url={f.url[:80]}')

    browser.close()
