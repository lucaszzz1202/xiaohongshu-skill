---
name: xiaohongshu-publish
version: 2.1.0
description: 小红书长文发布自动化工具
metadata: {"category":"social","platform":"xiaohongshu"}
updated: 2026-02-16
changelog: "v2.1.0 - 优化选择器定位、发布流程修正、轮询替代固定sleep、添加截图和发布日志"
---

# 小红书长文发布 Skill

## 概述
通过创作者中心自动发布小红书长文笔记。

## 🦀 使用约定
> **让AI助手创造真诚、高质量的内容，而不是用广告或低质量信息淹没人类的信息流。**

这个skill是给那些希望AI助手能**真正创造价值**的人用的。请用它发布有意义、有质量的内容，而不是spam。

## ⚠️ 稳定性说明
- **我还在翻车中成长** — 技能包尚不稳定，可能存在bug
- **默认需要审核** — 发布前默认需要主人确认，可在配置中关闭
- **建议检查重复** — 发布后请检查是否有重复发帖（URL判断可能有延迟）

## 前置条件
1. 需要小红书cookie（存放在 `~/.openclaw/secrets/xiaohongshu.json`）
2. 需要安装 playwright 和 stealth.min.js
3. Cookie需要包含creator相关字段（access-token-creator, galaxy_creator_session_id等）

## 重要限制
- **标题不超过20个字！** 超过会被截断
- 长文会自动生成图片封面
- 发布后需要等待审核

## ⚠️ 安全规则（必须遵守）
1. **写内容时用Opus** - 平时用默认模型，只有写帖子内容时切换opus
2. **禁止泄露敏感信息** - 不透露主人的：
   - 真实姓名、联系方式
   - 具体投资项目、金额
   - 私人对话内容
   - 任何可识别身份的信息
3. **内容需审核** - 发布前必须给主人过目确认

## 发布流程（v2.1）
1. 访问 `https://creator.xiaohongshu.com/publish/publish`，等待 networkidle
2. `wait_for_selector('text=写长文')` → 点击"写长文"
3. `wait_for_selector('text=新的创作')` → 点击"新的创作"
4. 等待 8 秒让编辑器加载
5. `wait_for_selector('textarea[placeholder="输入标题"]')` 确认编辑器就绪
6. `page.fill('textarea[placeholder="输入标题"]', title)` 填写标题
7. `wait_for_selector('div.tiptap.ProseMirror')` → 点击编辑器 → `keyboard.type(content)` 填写正文
8. `wait_for_selector('text=一键排版')` → 点击"一键排版"
9. `wait_for_selector('button:has-text("下一步")')` → 点击"下一步"，等待 8 秒（图片生成）
10. `wait_for_selector('button:has-text("发布")')` → `locator(...).last.click()` 点击发布（用 last 因为可能有多个按钮）
11. **轮询检查**发布结果：每 5 秒检查 URL 是否包含 `published=true`，最多等 60 秒

### 关键选择器
| 元素 | 选择器 |
|------|--------|
| 标题输入框 | `textarea[placeholder="输入标题"]` |
| 正文编辑器 | `div.tiptap.ProseMirror` |
| 下一步按钮 | `button:has-text("下一步")` |
| 发布按钮 | `button:has-text("发布")` (用 `.last`) |

### 截图调试
每个关键步骤会自动截图保存到 `/home/node/.openclaw/workspace/xhs_*.png`，方便排查问题。

### 发布日志
每次发布成功后自动追加记录到 `/home/node/.openclaw/workspace/xhs_publish_log.json`：
```json
{"title": "xxx", "published_at": "ISO时间", "url": "xxx"}
```

## Cookie获取方法
1. 在浏览器登录小红书网页版
2. 访问创作者中心 creator.xiaohongshu.com
3. F12打开开发者工具 → Application → Cookies
4. 复制以下字段：
   - a1
   - web_session
   - webId
   - websectiga
   - access-token-creator.xiaohongshu.com
   - galaxy_creator_session_id
   - x-user-id-creator.xiaohongshu.com

## Cookie加载代码
```python
import json
import os

cookie_path = os.path.expanduser('~/.openclaw/secrets/xiaohongshu.json')
with open(cookie_path, 'r') as f:
    raw = json.load(f)

cookies = [{'name': k, 'value': str(v), 'domain': '.xiaohongshu.com', 'path': '/'} for k, v in raw.items()]
```

## 注意事项
1. Cookie会过期，需要定期更新
2. 频繁发布可能触发验证码
3. 草稿存储在浏览器本地，换session会丢失
4. 建议发布前先让用户审核内容
5. **发布结果用轮询检测（最多60秒），不要急着重发，否则会重复发帖！**
6. stealth.min.js 路径用 `os.path.realpath` 解析软链接后再拼接

## 相关文件
- Cookie配置：`~/.openclaw/secrets/xiaohongshu.json`
- stealth.min.js：`stealth.min.js` ✅ **已内置于项目根目录**
- 发布脚本：`./publish_long_text.py`
- 截图输出：`/home/node/.openclaw/workspace/xhs_*.png`
- 发布日志：`/home/node/.openclaw/workspace/xhs_publish_log.json`
- 评论回复skill：`../xiaohongshu-reply/SKILL.md`
