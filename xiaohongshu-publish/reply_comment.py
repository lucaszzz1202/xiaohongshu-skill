#!/usr/bin/env python3
"""
小红书评论回复脚本
通过playwright在通知页面回复评论
"""

import json
from time import sleep
from playwright.sync_api import sync_playwright

COOKIE_PATH = "/Users/jli/.openclaw/secrets/xiaohongshu.json"
STEALTH_JS_PATH = "/Users/jli/openclaw/stealth.min.js"


def load_cookies():
    """加载cookie配置"""
    with open(COOKIE_PATH, 'r') as f:
        data = json.load(f)
    
    cookies = [
        {'name': 'a1', 'value': data.get('a1', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
        {'name': 'web_session', 'value': data.get('web_session', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
        {'name': 'webId', 'value': data.get('webId', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
    ]
    
    return cookies


def list_comments(headless: bool = True) -> list:
    """
    列出通知页面的评论
    
    Returns:
        list: 评论列表，每项包含 {index, user, content}
    """
    cookies = load_cookies()
    comments = []
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        context.add_init_script(path=STEALTH_JS_PATH)
        context.add_cookies(cookies)
        
        page = context.new_page()
        page.set_default_timeout(30000)
        
        page.goto('https://www.xiaohongshu.com/notification')
        sleep(3)
        
        page.click('text=评论和@')
        sleep(2)
        
        # 获取页面文本来解析评论
        page_text = page.locator('body').inner_text()
        
        # 找到回复按钮数量
        reply_btns = page.get_by_text('回复', exact=True).all()
        print(f'找到 {len(reply_btns)} 条可回复的评论')
        
        browser.close()
    
    return comments


def reply_to_comment(comment_index: int, reply_text: str, headless: bool = True) -> dict:
    """
    回复指定索引的评论
    
    Args:
        comment_index: 评论索引（从0开始）
        reply_text: 回复内容
        headless: 是否无头模式
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    cookies = load_cookies()
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        context.add_init_script(path=STEALTH_JS_PATH)
        context.add_cookies(cookies)
        
        page = context.new_page()
        page.set_default_timeout(30000)
        
        try:
            print('🔍 访问通知页...')
            page.goto('https://www.xiaohongshu.com/notification')
            sleep(3)
            
            print('📝 点击评论和@标签...')
            page.click('text=评论和@')
            sleep(2)
            
            # 找所有回复按钮
            reply_btns = page.get_by_text('回复', exact=True).all()
            print(f'找到 {len(reply_btns)} 个回复按钮')
            
            if len(reply_btns) <= comment_index:
                browser.close()
                return {'success': False, 'message': f'评论索引 {comment_index} 超出范围（共 {len(reply_btns)} 条）'}
            
            print(f'💬 点击第 {comment_index + 1} 条评论的回复按钮...')
            reply_btns[comment_index].click()
            sleep(1)
            
            print(f'📝 输入回复: {reply_text[:30]}...')
            textarea = page.locator('textarea').first
            textarea.fill(reply_text)
            sleep(1)
            
            print('📤 点击发送...')
            send_btn = page.get_by_text('发送', exact=True)
            send_btn.click()
            sleep(3)
            
            browser.close()
            print('✅ 回复已发送！')
            return {'success': True, 'message': '回复已发送'}
            
        except Exception as e:
            browser.close()
            print(f'❌ 回复失败: {e}')
            return {'success': False, 'message': str(e)}


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='回复小红书评论')
    parser.add_argument('--index', type=int, required=True, help='评论索引（从0开始）')
    parser.add_argument('--reply', required=True, help='回复内容')
    parser.add_argument('--visible', action='store_true', help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    result = reply_to_comment(
        comment_index=args.index,
        reply_text=args.reply,
        headless=not args.visible
    )
    
    print(f"结果: {result}")
