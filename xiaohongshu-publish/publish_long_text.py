#!/usr/bin/env python3
"""
小红书长文发布脚本 v3.0
- 多重发布成功检测
- 图片生成轮询等待
- 截图调试 + 发布日志
"""

import json
import os
import time
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

COOKIE_PATH = os.path.expanduser("~/.openclaw/secrets/xiaohongshu.json")
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
STEALTH_JS_PATH = os.path.join(_SCRIPT_DIR, '..', 'stealth.min.js')

SCREENSHOT_DIR = "/home/node/.openclaw/workspace"
PUBLISH_LOG_PATH = "/home/node/.openclaw/workspace/xhs_publish_log.json"


def _screenshot(page, name: str):
    path = os.path.join(SCREENSHOT_DIR, f"xhs_{name}.png")
    try:
        page.screenshot(path=path, full_page=True)
        print(f"📸 {path}")
    except Exception as e:
        print(f"⚠️ 截图失败({name}): {e}")


def _append_publish_log(title: str, url: str):
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
    print(f"📋 发布记录已写入")


def load_cookies():
    with open(COOKIE_PATH, 'r') as f:
        data = json.load(f)
    cookies = [{'name': k, 'value': str(v), 'domain': '.xiaohongshu.com', 'path': '/'} for k, v in data.items()]
    return cookies


def _check_publish_success(page):
    """多重检测发布是否成功"""
    url = page.url
    if 'published=true' in url:
        return True, 'URL contains published=true'
    if 'noteManage' in url or 'note-manage' in url:
        return True, 'Redirected to note management'
    try:
        if page.locator('text=发布成功').count() > 0:
            return True, 'Found "发布成功" text'
    except:
        pass
    try:
        if page.locator('button:has-text("发布")').count() == 0:
            return True, 'Publish button disappeared'
    except:
        pass
    return False, None


def publish_long_text(title: str, content: str, headless: bool = True) -> dict:
    """
    发布小红书长文

    Args:
        title: 标题（不超过20字）
        content: 正文内容（建议末尾带话题标签和互动引导）
        headless: 是否无头模式

    Returns:
        dict: {'success': bool, 'url': str, 'message': str}
    """
    if len(title) > 20:
        print(f"⚠️ 标题超过20字，截断: {title[:20]}...")
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
            print('1. 访问创作者中心...')
            page.goto('https://creator.xiaohongshu.com/publish/publish')
            page.wait_for_load_state('networkidle')
            _screenshot(page, "01_creator_home")

            # 2. 点击写长文
            print('2. 点击写长文...')
            page.wait_for_selector('text=写长文', timeout=15000)
            page.click('text=写长文')

            # 3. 点击新的创作
            print('3. 点击新的创作...')
            page.wait_for_selector('text=新的创作', timeout=15000)
            page.click('text=新的创作')
            time.sleep(8)

            # 4. 等待编辑器就绪
            print('4. 等待编辑器...')
            page.wait_for_selector('textarea[placeholder="输入标题"]', timeout=30000)

            # 5. 填写标题
            print(f'5. 填标题: {title}')
            page.fill('textarea[placeholder="输入标题"]', title)

            # 6. 填写正文
            print('6. 填正文...')
            editor = page.wait_for_selector('div.tiptap.ProseMirror', timeout=15000)
            editor.click()
            page.keyboard.type(content)
            _screenshot(page, "06_content_filled")

            # 7. 一键排版
            print('7. 一键排版...')
            page.wait_for_selector('text=一键排版', timeout=10000)
            page.click('text=一键排版')
            time.sleep(3)

            # 8. 下一步
            print('8. 下一步...')
            page.wait_for_selector('button:has-text("下一步")', timeout=10000)
            page.click('button:has-text("下一步")')

            # 9. 等待图片生成（轮询，最多40秒）
            print('9. 等待图片生成...')
            for i in range(20):
                time.sleep(2)
                if page.locator('text=笔记图片生成中').count() == 0:
                    print(f'   图片生成完成 ({(i+1)*2}s)')
                    break
                print(f'   生成中... ({(i+1)*2}s)')
            time.sleep(3)
            _screenshot(page, "09_ready_to_publish")

            # 10. 点击发布
            print('10. 点击发布...')
            page.locator('button:has-text("发布")').last.click()
            _screenshot(page, "10_publish_clicked")

            # 11. 多重检测发布结果（最多120秒）
            print('11. 等待发布结果...')
            success = False
            reason = None
            for i in range(24):
                time.sleep(5)
                success, reason = _check_publish_success(page)
                if success:
                    print(f'   ✅ 发布成功! ({reason})')
                    break
                print(f'   轮询 {i+1}/24...')

            _screenshot(page, "12_final")
            current_url = page.url
            browser.close()

            if success:
                print('🎉 发布成功！')
                _append_publish_log(title, current_url)
                return {'success': True, 'url': current_url, 'message': f'发布成功 ({reason})'}
            else:
                print('⚠️ 检测超时，但可能已发布成功，请手动确认！不要重发！')
                return {'success': False, 'url': current_url, 'message': '检测超时，可能已成功，请手动确认'}

        except Exception as e:
            _screenshot(page, "error")
            browser.close()
            print(f'❌ 发布失败: {e}')
            return {'success': False, 'url': '', 'message': str(e)}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='发布小红书长文 v3.0')
    parser.add_argument('--title', required=True, help='标题（不超过20字）')
    parser.add_argument('--content', required=True, help='正文内容')
    parser.add_argument('--visible', action='store_true', help='显示浏览器窗口')
    args = parser.parse_args()
    result = publish_long_text(title=args.title, content=args.content, headless=not args.visible)
    print(f"结果: {result}")
