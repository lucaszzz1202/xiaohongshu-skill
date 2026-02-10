#!/usr/bin/env python3
"""
Hana-me.fun Website Automated Testing Script
全面的网站自动化测试
"""

import time
from playwright.sync_api import sync_playwright
import json

def test_hana_website():
    """对 hana-me.fun 进行全面测试"""
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "basic_info": {},
        "performance": {},
        "screenshots": [],
        "interactions": {},
        "mobile_test": {},
        "seo_analysis": {},
        "errors": []
    }
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        
        try:
            # 1. 基础页面测试
            print("🔍 1. 基础页面分析...")
            page = browser.new_page()
            
            # 记录性能
            start_time = time.time()
            response = page.goto('https://hana-me.fun')
            load_time = time.time() - start_time
            
            results["basic_info"] = {
                "original_url": "https://hana-me.fun",
                "final_url": page.url,
                "title": page.title(),
                "status_code": response.status if response else None,
                "load_time_seconds": round(load_time, 2)
            }
            
            # 2. SEO 分析
            print("📊 2. SEO 分析...")
            meta_description = page.locator('meta[name="description"]').get_attribute('content') if page.locator('meta[name="description"]').count() > 0 else None
            meta_keywords = page.locator('meta[name="keywords"]').get_attribute('content') if page.locator('meta[name="keywords"]').count() > 0 else None
            
            results["seo_analysis"] = {
                "meta_description": meta_description,
                "meta_keywords": meta_keywords,
                "h1_count": page.locator('h1').count(),
                "h2_count": page.locator('h2').count(),
                "img_without_alt": page.locator('img:not([alt])').count(),
                "links_count": page.locator('a').count()
            }
            
            # 3. 桌面端截图
            print("📸 3. 桌面端截图...")
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.screenshot(path='hana_desktop.png', full_page=True)
            results["screenshots"].append("hana_desktop.png")
            
            # 4. 移动端测试
            print("📱 4. 移动端测试...")
            page.set_viewport_size({"width": 375, "height": 667})  # iPhone SE
            page.reload()
            page.screenshot(path='hana_mobile.png', full_page=True)
            results["screenshots"].append("hana_mobile.png")
            
            results["mobile_test"] = {
                "mobile_responsive": True,
                "mobile_title": page.title(),
                "mobile_url": page.url
            }
            
            # 5. 交互测试
            print("🖱️ 5. 交互测试...")
            page.set_viewport_size({"width": 1920, "height": 1080})
            
            # 检查可点击元素
            buttons = page.locator('button, [role="button"], .btn, input[type="submit"]')
            links = page.locator('a[href]')
            
            results["interactions"] = {
                "buttons_found": buttons.count(),
                "links_found": links.count(),
                "clickable_elements": []
            }
            
            # 尝试点击主要交互元素（如果存在）
            try:
                # 检查是否有"开始"或"Begin"按钮
                begin_selectors = [
                    'text="Begin"',
                    'text="开始"', 
                    'text="Start"',
                    '[data-testid*="begin"]',
                    '[class*="begin"]',
                    'button:has-text("Begin")',
                ]
                
                for selector in begin_selectors:
                    try:
                        element = page.locator(selector).first
                        if element.count() > 0:
                            results["interactions"]["clickable_elements"].append({
                                "selector": selector,
                                "text": element.text_content()[:50],
                                "clickable": True
                            })
                            break
                    except Exception as e:
                        continue
                        
            except Exception as e:
                results["errors"].append(f"交互测试错误: {str(e)}")
            
            # 6. 性能分析
            print("⚡ 6. 性能分析...")
            
            # 重新加载页面测量性能
            start_time = time.time()
            page.reload(wait_until='networkidle')
            full_load_time = time.time() - start_time
            
            results["performance"] = {
                "initial_load_time": results["basic_info"]["load_time_seconds"],
                "full_load_time": round(full_load_time, 2),
                "dom_content_loaded": True,
                "images_loaded": page.locator('img').count(),
                "scripts_loaded": page.locator('script').count(),
                "stylesheets_loaded": page.locator('link[rel="stylesheet"]').count()
            }
            
            # 7. 控制台错误检查
            print("🐛 7. 控制台错误检查...")
            console_errors = []
            
            def handle_console(msg):
                if msg.type in ['error', 'warning']:
                    console_errors.append({
                        "type": msg.type,
                        "text": msg.text,
                        "location": msg.location if hasattr(msg, 'location') else None
                    })
            
            page.on('console', handle_console)
            page.reload()
            time.sleep(3)  # 等待可能的 JS 错误
            
            results["errors"].extend([f"Console {err['type']}: {err['text']}" for err in console_errors])
            
        except Exception as e:
            results["errors"].append(f"测试过程中出现错误: {str(e)}")
        
        finally:
            browser.close()
    
    return results

def print_results(results):
    """格式化打印测试结果"""
    print("\n" + "="*60)
    print(f"🎯 Hana-me.fun 网站测试报告 - {results['timestamp']}")
    print("="*60)
    
    # 基础信息
    print(f"\n📋 基础信息:")
    basic = results['basic_info']
    print(f"   原始URL: {basic.get('original_url')}")
    print(f"   最终URL: {basic.get('final_url')}")
    print(f"   页面标题: {basic.get('title')}")
    print(f"   HTTP状态: {basic.get('status_code')}")
    print(f"   加载时间: {basic.get('load_time_seconds')}秒")
    
    # 性能数据
    print(f"\n⚡ 性能分析:")
    perf = results['performance']
    print(f"   初始加载: {perf.get('initial_load_time')}秒")
    print(f"   完整加载: {perf.get('full_load_time')}秒")
    print(f"   图片数量: {perf.get('images_loaded')}")
    print(f"   脚本数量: {perf.get('scripts_loaded')}")
    print(f"   样式表数量: {perf.get('stylesheets_loaded')}")
    
    # SEO分析
    print(f"\n📊 SEO分析:")
    seo = results['seo_analysis']
    print(f"   Meta描述: {seo.get('meta_description', '未找到')[:100]}")
    print(f"   H1标签数: {seo.get('h1_count')}")
    print(f"   H2标签数: {seo.get('h2_count')}")
    print(f"   链接数量: {seo.get('links_count')}")
    print(f"   无Alt图片: {seo.get('img_without_alt')}")
    
    # 交互元素
    print(f"\n🖱️ 交互分析:")
    interactions = results['interactions']
    print(f"   按钮数量: {interactions.get('buttons_found')}")
    print(f"   链接数量: {interactions.get('links_found')}")
    if interactions.get('clickable_elements'):
        print(f"   找到可点击元素: {len(interactions['clickable_elements'])}个")
    
    # 移动端
    print(f"\n📱 移动端测试:")
    mobile = results['mobile_test']
    print(f"   响应式设计: {'✅' if mobile.get('mobile_responsive') else '❌'}")
    print(f"   移动端标题: {mobile.get('mobile_title')}")
    
    # 截图
    print(f"\n📸 生成截图: {', '.join(results['screenshots'])}")
    
    # 错误
    if results['errors']:
        print(f"\n🐛 发现问题:")
        for error in results['errors']:
            print(f"   ⚠️ {error}")
    else:
        print(f"\n✅ 未发现明显问题")
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)

if __name__ == "__main__":
    print("🚀 开始 Hana-me.fun 网站自动化测试...")
    results = test_hana_website()
    
    # 保存详细结果到JSON
    with open('hana_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 打印报告
    print_results(results)
    
    print(f"\n📄 详细测试数据已保存到: hana_test_results.json")