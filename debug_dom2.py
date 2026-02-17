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
    page.click('text=写长文')
    sleep(5)

    # 用JS直接查DOM
    result = page.evaluate("""() => {
        const info = {};
        
        // 查所有iframe
        const iframes = document.querySelectorAll('iframe');
        info.iframes = iframes.length;
        info.iframeUrls = Array.from(iframes).map(f => f.src);
        
        // 查shadow roots
        const allEls = document.querySelectorAll('*');
        const shadowHosts = [];
        allEls.forEach(el => {
            if (el.shadowRoot) {
                shadowHosts.push({tag: el.tagName, id: el.id, class: el.className.toString().slice(0,50)});
            }
        });
        info.shadowHosts = shadowHosts;
        
        // 查所有可编辑元素
        const editables = document.querySelectorAll('[contenteditable]');
        info.editables = Array.from(editables).map(e => ({
            tag: e.tagName, 
            ce: e.contentEditable,
            class: e.className.toString().slice(0,50),
            text: e.textContent.slice(0,30)
        }));
        
        // 查所有textarea和input
        const tas = document.querySelectorAll('textarea, input');
        info.inputs = Array.from(tas).map(e => ({
            tag: e.tagName,
            type: e.type,
            placeholder: e.placeholder,
            visible: e.offsetParent !== null
        }));
        
        // 查body的直接子元素结构
        info.bodyChildren = Array.from(document.body.children).map(c => ({
            tag: c.tagName,
            id: c.id,
            class: c.className.toString().slice(0,60)
        }));
        
        // 查找包含"标题"文字的元素
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const titleNodes = [];
        while(walker.nextNode()) {
            if (walker.currentNode.textContent.includes('标题') || walker.currentNode.textContent.includes('排版')) {
                const parent = walker.currentNode.parentElement;
                titleNodes.push({
                    text: walker.currentNode.textContent.slice(0,50),
                    parentTag: parent ? parent.tagName : 'none',
                    parentClass: parent ? parent.className.toString().slice(0,50) : ''
                });
            }
        }
        info.titleNodes = titleNodes.slice(0, 10);
        
        return info;
    }""")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    browser.close()
