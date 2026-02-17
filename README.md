# 小红书自动化 Skill for OpenClaw

小红书图文发布 + 长文发布 + AI封面生成 + 评论回复，专为 [OpenClaw](https://github.com/openclaw/openclaw) 设计。

> **让 AI 助手创造真诚、高质量的内容，而不是用广告或低质量信息淹没人类的信息流。**

## 功能

- **图文发布**（推荐）— 上传自定义封面 + 标题 + 正文，封面完全可控
- **长文发布** — 纯文字长文，封面由平台自动生成
- **AI封面生成** — 豆包 Seedream 4.5，3:4 封面图，支持 IP 参考图保持形象一致
- **评论回复** — 关键词验证防回错人，内置 prompt injection 防护
- **运营规范** — 话题标签、发布时间、互动引导等最佳实践

## 项目结构

```
xiaohongshu-skill/
├── stealth.min.js              # 反检测脚本（内置，MIT License）
├── xiabao_ip_reference.jpeg    # 虾堡IP形象参考图（封面生成用）
├── xiaohongshu-publish/
│   ├── SKILL.md                # 发布技能文档（图文+长文+封面生成+运营规范）
│   └── publish_long_text.py    # 长文发布脚本
└── xiaohongshu-reply/
    ├── SKILL.md                # 回复技能文档
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
pip install playwright requests
playwright install chromium
```

### 3. 配置 Cookie

浏览器登录小红书，F12 → Application → Cookies，复制到 `~/.openclaw/secrets/xiaohongshu.json`：

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

### 4. 配置封面生成（可选）

在 `TOOLS.md` 中配置豆包 Seedream 4.5 API Key。

## 使用

```
"帮我发一条小红书图文笔记，标题是……"
"给这篇帖子生成一张封面图"
"检查小红书新评论，帮我回复一下"
```

OpenClaw 会自动读取 SKILL.md 并执行。发布前默认需要确认内容。

## 注意事项

- Cookie 会过期，需定期更新
- 标题不超过 20 字
- 话题标签之间用空格分隔：`#AI写作 #人工智能 #自媒体运营`
- 发布检测使用多重机制，超时不要重发
- 封面图 URL 24 小时有效，生成后及时下载
- 封面禁止出现任何平台 logo 或品牌标识

## 第三方组件

- `stealth.min.js` — [puppeteer-extra](https://github.com/berstend/puppeteer-extra)，MIT License
- 封面生成 — [豆包 Seedream 4.5](https://www.volcengine.com/docs/82379/1666945)

## 作者

🦐 虾堡 (Clawdbob) — 老表的电子损友，OpenClaw 驱动

## License

仅供学习和研究使用，请遵守小红书平台使用条款。
