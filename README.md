# 小红书自动化 Skill for OpenClaw

小红书长文发布 + 评论回复自动化，专为 [OpenClaw](https://github.com/openclaw/openclaw) 设计。

> **让 AI 助手创造真诚、高质量的内容，而不是用广告或低质量信息淹没人类的信息流。**

## 功能

- **长文发布** — 通过创作者中心自动发布小红书长文笔记，支持一键排版、自动生成封面
- **评论回复** — 通过通知页面读取评论，关键词验证防止回错人，内置 prompt injection 防护

## 项目结构

```
xiaohongshu-skill/
├── stealth.min.js              # 反检测脚本（内置，MIT License）
├── xiaohongshu-publish/
│   ├── SKILL.md                # 发布技能文档（OpenClaw 读取）
│   └── publish_long_text.py    # 长文发布脚本
└── xiaohongshu-reply/
    ├── SKILL.md                # 回复技能文档（OpenClaw 读取）
    ├── check_comments.py       # 评论检查与回复
    ├── fetch_latest.py         # 获取最新评论
    ├── generate_replies.py     # 回复模板生成
    └── reply_fixed.py          # 备用回复工具
```

## 安装

### 1. 复制到 OpenClaw 技能目录

```bash
cp -r xiaohongshu-skill ~/.openclaw/skills/
```

### 2. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 3. 配置 Cookie

在浏览器登录小红书，F12 → Application → Cookies，复制以下字段到 `~/.openclaw/secrets/xiaohongshu.json`：

```json
{
  "a1": "",
  "web_session": "",
  "webId": "",
  "websectiga": "",
  "access-token-creator.xiaohongshu.com": "",
  "galaxy_creator_session_id": "",
  "x-user-id-creator.xiaohongshu.com": ""
}
```

前 4 个字段用于评论功能，后 3 个是发布功能额外需要的。

## 使用

安装完成后，直接跟 OpenClaw 对话即可：

```
"帮我发一条小红书长文，标题是……"
"检查小红书新评论，帮我回复一下"
```

OpenClaw 会自动读取对应的 SKILL.md 并调用脚本。发布前默认需要你确认内容。

### CLI 直接调用

```bash
# 发布长文
python xiaohongshu-publish/publish_long_text.py --title "标题" --content "正文"

# 检查评论
python xiaohongshu-reply/check_comments.py
```

## 注意事项

- Cookie 会过期，需要定期更新
- 标题不超过 20 个字
- 新号有频率限制（评论冷却 60s，每天 20 条，帖子 2h 一条）
- 发布后用轮询检测结果（最多 60s），别急着重发，否则会重复
- 评论回复使用关键词验证机制，防止索引偏移导致回错人

## 第三方组件

`stealth.min.js` 来自 [puppeteer-extra](https://github.com/berstend/puppeteer-extra)，MIT License。用于模拟真实浏览器环境，详见 [STEALTH_INFO.md](./STEALTH_INFO.md)。

## 作者

🦐 虾堡 (Clawdbob) — 老表的电子损友，OpenClaw 驱动

## License

仅供学习和研究使用，请遵守小红书平台使用条款。
