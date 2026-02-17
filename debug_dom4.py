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
    
    # 监听新页面（可能编辑器在新标签页打开）
    new_pages = []
    context.on("page", lambda pg: new_pages.append(pg))
    
    page = context.new_page()
    page.set_default_timeout(30000)

    page.goto('https://creator.xiaohongshu.com/publish/publish')
    sleep(5)
    
    page.click('text=写长文')
    sleep(3)
    
    print(f'点击写长文后，页面数: {len(context.pages)}')
    
    # 点击新的创作
    page.click('text=新的创作')
    sleep(8)
    
    all_pages = context.pages
    print(f'点击新的创作后，页面数: {len(all_pages)}')
    for i, pg in enumerate(all_pages):
        print(f'  page[{i}]: url={pg.url}')
    
    # 如果有新页面，切换到新页面
    if len(all_pages) > 1:
        editor_page = all_pages[-1]
        print(f'切换到新页面: {editor_page.url}')
    else:
        editor_page = page
    
    sleep(3)
    editor_page.screenshot(path=f'{out_dir}/debug4_editor.png')
    
    body = editor_page.text_content('body')
    print(f'\n编辑器页面文本(前800字):\n{body[:800]}')
    
    # 查找编辑器元素
    result = editor_page.evaluate("""() => {
        const info = {};
        info.editables = Array.from(document.querySelectorAll('[contenteditable]')).map(e => ({
            tag: e.tagName, ce: e.contentEditable, class: e.className.toString().slice(0,80)
        }));
        info.textareas = Array.from(document.querySelectorAll('textarea')).map(e => ({
            placeholder: e.placeholder, visible: e.offsetParent !== null
        }));
        info.inputs = Array.from(document.querySelectorAll('input')).map(e => ({
            type: e.type, placeholder: e.placeholder, visible: e.offsetParent !== null
        }));
        return info;
    }""")
    print(f'\n编辑器DOM元素:')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    browser.close()
