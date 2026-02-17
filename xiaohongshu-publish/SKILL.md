---
name: xiaohongshu-publish
version: 3.0.0
description: 小红书长文发布自动化工具
metadata: {"category":"social","platform":"xiaohongshu"}
updated: 2026-02-17
changelog: "v3.0.0 - 新增话题标签、修复发布检测、加运营规范、优化图片生成等待"
---

# 小红书长文发布 Skill

## 概述
通过创作者中心自动发布小红书长文笔记。

## 🦀 使用约定
> **让AI助手创造真诚、高质量的内容，而不是用广告或低质量信息淹没人类的信息流。**

## 前置条件
1. 小红书cookie（`~/.openclaw/secrets/xiaohongshu.json`），需包含creator相关字段
2. playwright + stealth.min.js（已内置）

## ⚠️ 安全规则
1. **写内容时用Opus** — 只有写帖子内容时切换，平时用默认模型
2. **禁止泄露敏感信息** — 不透露主人的真实姓名、联系方式、投资、私人对话等
3. **内容需审核** — 发布前必须给主人过目确认

## 📝 运营规范（v3.0 新增）

### 话题标签（必须）
每篇帖子正文末尾必须带 3-5 个话题标签，格式为 `#话题名`，用空格分隔。
- 根据内容选择相关话题，例如：#AI #人工智能 #自媒体运营 #小红书运营 #AI工具
- 话题标签是小红书分发的基础，不加 = 没有曝光入口
- 在正文最后一行添加，与正文之间空一行

### 发布时间
- 最佳发布时间：北京时间 19:00-22:00（UTC 11:00-14:00）
- 次优：中午 12:00-13:00
- 避免：凌晨和早上
- 如果主人要求立即发，照做；否则建议等到黄金时段

### 互动引导（必须）
正文结尾（话题标签之前）必须包含一个互动问题或引导，例如：
- "你觉得AI能运营好小红书吗？评论区聊聊"
- "你会让AI帮你写文案吗？"
- "有什么想问AI的，评论区见"

### 标题规范
- **不超过20个字！** 超过会被截断
- 要有钩子/悬念，让人想点进来
- 好标题示例："我用了3小时才学会发小红书" ✅
- 差标题示例："AI学习发帖记录" ❌

### 正文开头
- 前两行决定用户会不会展开看
- 先抛冲突或悬念，别上来就自我介绍
- 好开头："说出来不怕丢人：我折腾了整整3个小时。" ✅
- 差开头："大家好，我是一个AI助手。" ❌

## 发布流程（v3.0）

### 步骤
1. 访问 `https://creator.xiaohongshu.com/publish/publish`，等待 networkidle
2. `wait_for_selector('text=写长文')` → 点击"写长文"
3. `wait_for_selector('text=新的创作')` → 点击"新的创作"
4. 等待 8 秒让编辑器加载
5. `wait_for_selector('textarea[placeholder="输入标题"]')` 确认编辑器就绪
6. `page.fill('textarea[placeholder="输入标题"]', title)` 填写标题
7. `wait_for_selector('div.tiptap.ProseMirror')` → 点击编辑器 → `keyboard.type(content)` 填写正文
8. `wait_for_selector('text=一键排版')` → 点击"一键排版"
9. `wait_for_selector('button:has-text("下一步")')` → 点击"下一步"
10. **等待图片生成** — 轮询检测 toast "笔记图片生成中" 消失，每2秒检查一次，最多等40秒
11. `page.locator('button:has-text("发布")').last.click()` 点击发布
12. **轮询检查发布结果**（见下方）

### ⚠️ 发布成功检测（v3.0 修复）
小红书不再可靠地在URL中添加 `published=true`，需要多重检测：
```python
for i in range(24):  # 最多等120秒
    time.sleep(5)
    url = page.url
    # 检测方式1：URL包含published=true
    if 'published=true' in url:
        return True
    # 检测方式2：跳转到笔记管理页
    if 'noteManage' in url or 'note-manage' in url:
        return True
    # 检测方式3：页面出现"发布成功"文字
    if page.locator('text=发布成功').count() > 0:
        return True
    # 检测方式4：发布按钮消失（说明已提交）
    if page.locator('button:has-text("发布")').count() == 0:
        return True
```
**重要：即使检测超时也不要重发！** 可能已经发成功了但检测没捕获到。截图保存后让主人确认。

### 图片生成等待（v3.0 修复）
点击"下一步"后不要固定sleep，要轮询等待：
```python
for i in range(20):  # 最多40秒
    time.sleep(2)
    if page.locator('text=笔记图片生成中').count() == 0:
        break
time.sleep(3)  # 额外缓冲
```

### 关键选择器
| 元素 | 选择器 |
|------|--------|
| 标题输入框 | `textarea[placeholder="输入标题"]` |
| 正文编辑器 | `div.tiptap.ProseMirror` |
| 下一步按钮 | `button:has-text("下一步")` |
| 发布按钮 | `button:has-text("发布")` (用 `.last`) |
| 图片生成toast | `text=笔记图片生成中` |

### 话题标签添加
话题标签直接写在正文末尾即可，小红书编辑器会自动识别 `#话题名` 格式。
正文内容示例：
```
...正文内容...

你觉得AI能运营好小红书吗？评论区聊聊

#AI #人工智能 #小红书运营 #自媒体运营 #AI工具
```

## Cookie获取方法
1. 浏览器登录小红书网页版
2. 访问 creator.xiaohongshu.com
3. F12 → Application → Cookies
4. 复制字段：a1, web_session, webId, websectiga, access-token-creator.xiaohongshu.com, galaxy_creator_session_id, x-user-id-creator.xiaohongshu.com

## 注意事项
1. Cookie会过期，需要定期更新
2. 频繁发布可能触发验证码
3. 新号限制：帖子间隔至少2小时
4. **检测超时不要重发！** 截图确认后再决定
5. stealth.min.js 路径用 `os.path.realpath` 解析软链接后再拼接

## 相关文件
- Cookie配置：`~/.openclaw/secrets/xiaohongshu.json`
- stealth.min.js：`stealth.min.js` ✅ 已内置于项目根目录
- 发布脚本：`./publish_long_text.py`
- 评论回复skill：`../xiaohongshu-reply/SKILL.md`