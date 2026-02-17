#!/usr/bin/env python3
"""
小红书长文发布脚本
使用playwright通过创作者中心发布长文笔记
"""

import json
import os
import time
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

# 路径配置
COOKIE_PATH = os.path.expanduser("~/.openclaw/secrets/xiaohongshu.json")
# 用 realpath 解析软链接后再拼路径
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
STEALTH_JS_PATH = os.path.join(_SCRIPT_DIR, '..', 'stealth.min.js')

SCREENSHOT_DIR = "/home/node/.openclaw/workspace"
PUBLISH_LOG_PATH = "/home/node/.openclaw/workspace/xhs_publish_log.json"


def _screenshot(page, name: str):
    """关键步骤截图，方便调试"""
    path = os.path.join(SCREENSHOT_DIR, f"xhs_{name}.png")
    try:
        page.screenshot(path=path, full_page=True)
        print(f"📸 截图已保存: {path}")
    except Exception as e:
        print(f"⚠️ 截图失败({name}): {e}")


def _append_publish_log(title: str, url: str):
    """追加发布记录到日志文件"""
    record = {
        "title": title,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "url": url,
    }
    logs = []
    if os.path.exists(PUBLISH_LOG_PATH):
        try:
            with open(PUBLISH_LOG_PATH, "r") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    logs.append(record)
    with open(PUBLISH_LOG_PATH, "w") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    print(f"📋 发布记录已写入: {PUBLISH_LOG_PATH}")


def load_cookies():
    """加载cookie配置"""
    with open(COOKIE_PATH, 'r') as f:
        data = json.load(f)

    # 转换为playwright格式
    cookies = [
        {'name': 'a1', 'value': data.get('a1', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
        {'name': 'web_session', 'value': data.get('web_session', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
        {'name': 'webId', 'value': data.get('webId', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
        {'name': 'websectiga', 'value': data.get('websectiga', ''), 'domain': '.xiaohongshu.com', 'path': '/'},
    ]

    creator_cookies = [
        'access-token-creator.xiaohongshu.com',
        'galaxy_creator_session_id',
        'x-user-id-creator.xiaohongshu.com',
        'customer-sso-sid',
        'customerClientId',
    ]

    for key in creator_cookies:
        if key in data:
            cookies.append({
                'name': key,
                'value': data[key],
                'domain': '.xiaohongshu.com',
                'path': '/',
            })

    return cookies


def publish_long_text(title: str, content: str, headless: bool = True) -> dict:
    """
    发布小红书长文

    Args:
        title: 标题（不超过20字！）
        content: 正文内容
        headless: 是否无头模式

    Returns:
        dict: {'success': bool, 'url': str, 'message': str}
    """

    if len(title) > 20:
        print(f"⚠️ 标题超过20字，将被截断: {title[:20]}...")
        title = title[:20]

    cookies = load_cookies()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        context.add_init_script(path=STEALTH_JS_PATH)
        context.add_cookies(cookies)

        page = context.new_page()
        page.set_default_timeout(60000)

        try:
            # 1. 访问创作者中心
            print('🔍 访问创作者中心...')
            page.goto('https://creator.xiaohongshu.com/publish/publish')
            page.wait_for_load_state('networkidle')
            _screenshot(page, "01_creator_home")

            # 2. 点击"写长文"
            print('📝 点击写长文...')
            page.wait_for_selector('text=写长文', timeout=15000)
            page.click('text=写长文')
            _screenshot(page, "02_write_long_text")

            # 3. 点击"新的创作"，等8秒让编辑器加载
            print('🆕 点击新的创作...')
            page.wait_for_selector('text=新的创作', timeout=15000)
            page.click('text=新的创作')
            time.sleep(8)
            _screenshot(page, "03_new_creation")

            # 4. 等待标题输入框出现，确认编辑器就绪
            print('⏳ 等待编辑器就绪...')
            page.wait_for_selector('textarea[placeholder="输入标题"]', timeout=30000)
            _screenshot(page, "04_editor_ready")

            # 5. 填写标题
            print(f'📝 填写标题: {title}')
            page.fill('textarea[placeholder="输入标题"]', title)
            _screenshot(page, "05_title_filled")

            # 6. 填写内容 — 点击编辑器再用keyboard.type
            print('📝 填写正文...')
            editor = page.wait_for_selector('div.tiptap.ProseMirror', timeout=15000)
            editor.click()
            page.keyboard.type(content)
            _screenshot(page, "06_content_filled")

            # 7. 一键排版
            print('🎨 一键排版...')
            page.wait_for_selector('text=一键排版', timeout=10000)
            page.click('text=一键排版')
            time.sleep(3)
            _screenshot(page, "07_auto_format")

            # 8. 点击"下一步"
            print('➡️ 下一步...')
            page.wait_for_selector('button:has-text("下一步")', timeout=10000)
            page.click('button:has-text("下一步")')
            time.sleep(8)  # 等待图片生成
            _screenshot(page, "08_next_step")

            # 9. 点击"发布"（用last，可能有多个按钮）
            print('🚀 发布...')
            page.wait_for_selector('button:has-text("发布")', timeout=15000)
            page.locator('button:has-text("发布")').last.click()
            _screenshot(page, "09_publish_clicked")

            # 10. 轮询检查发布结果，最多60秒，每5秒一次
            print('⏳ 等待发布结果...')
            success = False
            current_url = page.url
            for i in range(12):  # 12 * 5s = 60s
                time.sleep(5)
                current_url = page.url
                if 'published=true' in current_url:
                    success = True
                    break
                print(f'  轮询 {i+1}/12 — URL: {current_url}')

            _screenshot(page, "10_final_result")
            browser.close()

            if success:
                print('🎉 发布成功！')
                _append_publish_log(title, current_url)
                return {'success': True, 'url': current_url, 'message': '发布成功'}
            else:
                print(f'❌ 发布可能失败，URL: {current_url}')
                return {'success': False, 'url': current_url, 'message': '发布结果不确定，60秒内未检测到published=true'}

        except Exception as e:
            _screenshot(page, "error")
            browser.close()
            print(f'❌ 发布失败: {e}')
            return {'success': False, 'url': '', 'message': str(e)}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='发布小红书长文')
    parser.add_argument('--title', required=True, help='标题（不超过20字）')
    parser.add_argument('--content', required=True, help='正文内容')
    parser.add_argument('--visible', action='store_true', help='显示浏览器窗口')

    args = parser.parse_args()

    result = publish_long_text(
        title=args.title,
        content=args.content,
        headless=not args.visible,
    )

    print(f"结果: {result}")
