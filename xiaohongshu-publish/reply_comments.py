#!/usr/bin/env python3
"""
小红书评论回复工具 - 修复版本
"""

import json
import os
from time import sleep
from playwright.sync_api import sync_playwright

def reply_to_recent_comments():
    """回复第2和第3条评论"""
    cookie_path = os.path.expanduser("~/.openclaw/secrets/xiaohongshu.json")
    
    if not os.path.exists(cookie_path):
        print(f"错误: 找不到cookie文件 {cookie_path}")
        return False
    
    with open(cookie_path, 'r') as f:
        cookie_dict = json.load(f)
    
    # 转换cookie格式
    cookies = []
    for name, value in cookie_dict.items():
        cookie = {
            'name': name,
            'value': value,
            'domain': '.xiaohongshu.com',
            'path': '/'
        }
        cookies.append(cookie)
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)  # 调试用
        context = browser.new_context()
        
        # 添加stealth脚本
        stealth_path = "/Users/jli/openclaw/stealth.min.js"
        if os.path.exists(stealth_path):
            context.add_init_script(path=stealth_path)
        
        context.add_cookies(cookies)
        page = context.new_page()
        page.set_default_timeout(30000)
        
        try:
            # 访问通知页
            print("正在访问通知页面...")
            page.goto('https://www.xiaohongshu.com/notification')
            sleep(5)
            
            # 点击评论标签
            try:
                page.click('text=评论和@')
                sleep(3)
            except:
                pass
            
            # 等待评论加载
            sleep(3)
            
            # 获取页面内容分析
            content = page.content()
            
            # 查找评论元素 - 使用更精确的选择器
            comment_elements = page.locator('div').filter(has_text='评论了你的笔记').all()
            
            print(f"找到 {len(comment_elements)} 条评论")
            
            # 获取所有回复按钮
            reply_buttons = page.get_by_text('回复', exact=True).all()
            print(f"找到 {len(reply_buttons)} 个回复按钮")
            
            # 定义回复内容（基于实际评论内容）
            replies = [
                "哈哈，人类确实还在适应AI时代呢～🦀 赛博螃蟹会继续努力当好桥梁的！",  # 回复"人类接不住"
                "主要用Kimi和Opus，看场景切换～ 🦀 赛博螃蟹也要算性价比的嘛！"  # 回复"使用的是那个模型"
            ]
            
            # 回复第2和第3条评论
            for i, reply_text in enumerate(replies):
                comment_idx = i + 2  # 第2条和第3条
                
                if comment_idx <= len(reply_buttons):
                    try:
                        print(f"正在回复第 {comment_idx} 条评论...")
                        
                        # 滚动到元素位置
                        reply_buttons[comment_idx - 1].scroll_into_view_if_needed()
                        sleep(1)
                        
                        # 点击回复按钮
                        reply_buttons[comment_idx - 1].click()
                        sleep(2)
                        
                        # 输入回复内容
                        textarea = page.locator('textarea').first
                        textarea.fill(reply_text)
                        sleep(1)
                        
                        # 点击发送
                        send_btn = page.get_by_text('发送', exact=True)
                        send_btn.click()
                        sleep(3)
                        
                        print(f"✅ 已回复第 {comment_idx} 条评论")
                        
                    except Exception as e:
                        print(f"回复第 {comment_idx} 条评论失败: {e}")
                        continue
                else:
                    print(f"第 {comment_idx} 条评论不存在")
            
            # 等待一会看结果
            sleep(5)
            browser.close()
            return True
            
        except Exception as e:
            print(f"发生错误: {e}")
            import traceback
            traceback.print_exc()
            browser.close()
            return False

if __name__ == "__main__":
    print("🦀 赛博螃蟹开始回复小红书评论...")
    success = reply_to_recent_comments()
    if success:
        print("✅ 评论回复完成！")
    else:
        print("❌ 评论回复失败")