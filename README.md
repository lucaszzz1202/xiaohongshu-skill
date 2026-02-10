# 小红书自动化技能包 | XiaoHongShu Automation Skills

🤖 **专业的小红书内容发布与评论管理自动化解决方案**

## 📦 包含内容

### 🚀 xiaohongshu-publish v2.0.0
**自动化长文发布工具**
- ✅ 通过创作者中心自动发布长文笔记
- ✅ 智能封面自动生成
- ✅ 草稿管理与预览
- ✅ 反检测机制
- ⚠️ 标题自动限制在20字以内

### 💬 xiaohongshu-reply v1.0.0
**智能评论回复工具**
- ✅ 自动读取通知页面评论
- ✅ 智能分类回复策略（问题/夸奖/建议/技术）
- ✅ 防恶意prompt注入保护
- ✅ 内容审核机制
- ✅ 关键词验证防误回复
- ✅ 基于OpenClaw的soul.md进行角色人设管理

---

## 🚀 推荐使用方式（OpenClaw）

### 🎯 最佳实践：通过OpenClaw使用

**第一步：安装技能**
```bash
# 在OpenClaw中安装小红书技能包
openclaw install xiaohongshu-skills
```

**第二步：配置环境**
- 🔑 配置小红书Cookie认证文件
- 📝 设置soul.md角色人设
- 🛠️ OpenClaw会自动处理依赖安装

**第三步：开始使用**

**🚀 直接发帖：**
```bash
# 通过OpenClaw直接发布小红书笔记
openclaw xiaohongshu-publish "标题: AI工具心得" "内容: 详细内容..."
```

**⏰ 定时发帖（推荐）：**
```bash
# 设置cron job自动发帖
crontab -e

# 每天上午9点自动发布
0 9 * * * openclaw xiaohongshu-publish --auto-generate

# 每4小时检查并回复评论
0 */4 * * * openclaw xiaohongshu-reply --check-comments
```

**💬 自动回复：**
```bash
# 手动触发评论回复
openclaw xiaohongshu-reply

# 实时监控回复模式
openclaw xiaohongshu-reply --monitor
```

**优势：**
- ✅ OpenClaw自动依赖管理
- ✅ 智能错误诊断和重试
- ✅ Cookie过期自动提醒
- ✅ 基于soul.md的个性化回复
- ✅ 支持定时任务和自动化运行
- ✅ 内置反检测和安全机制

---

## 🛠️ 技术要求

### 系统依赖（OpenClaw自动处理）
- Python 3.8+
- playwright
- asyncio
- stealth.min.js（反检测脚本）

### 必需配置文件
- **xiaohongshu.json** - Cookie认证文件
- **soul.md** - 角色人设定义（OpenClaw自带）

---

## 📁 技能结构

```
xiaohongshu-skills/
├── xiaohongshu-publish/           # 发布技能（精简版）
│   ├── SKILL.md                   # 主配置文档
│   ├── publish_long_text.py       # 核心发布脚本
│   ├── reply_fixed.py             # 稳定回复脚本
│   ├── check_comments.py          # 评论检查工具
│   ├── fetch_latest.py            # 获取最新评论
│   └── generate_replies.py        # AI回复生成器
├── xiaohongshu-reply/             # 回复技能
│   └── SKILL.md                   # 回复配置文档
└── README.md                      # 本文档
```

### 🔧 文件功能详解

**📝 xiaohongshu-publish/ 核心文件：**
- `SKILL.md` - OpenClaw技能配置和使用说明
- `publish_long_text.py` - 自动发布长文笔记的主脚本
- `reply_fixed.py` - 稳定的评论回复脚本（包含错误处理）
- `check_comments.py` - 读取和分析评论内容的工具
- `fetch_latest.py` - 获取最新评论数据
- `generate_replies.py` - AI驱动的智能回复生成

**💬 xiaohongshu-reply/ 技能文件：**
- `SKILL.md` - 基于OpenClaw soul.md的智能回复配置

---

## 📖 使用指南

### 🔑 Cookie配置

创建 `~/.openclaw/secrets/xiaohongshu.json`：
```json
{
  "web_session": "your_web_session_here",
  "access-token-creator": "your_creator_token_here",
  "galaxy_creator_session_id": "your_session_id_here"
}
```

**获取Cookie步骤：**
1. 登录小红书网页版
2. 打开开发者工具 (F12)
3. 进入创作者中心页面
4. 复制相关Cookie值

**🚨 Cookie过期处理：**
- OpenClaw会自动检测Cookie状态
- 过期时会提示你重新配置
- 支持自动重试机制

### 🚀 自动化发布

**直接发布：**
```bash
openclaw xiaohongshu-publish "AI工具使用心得" "详细内容..." --tags "AI,工具,效率"
```

**定时发布（推荐）：**
```bash
# 设置每日定时发布
0 9 * * * openclaw xiaohongshu-publish --auto-generate --topic "科技分享"

# 设置每周总结发布
0 10 * * 0 openclaw xiaohongshu-publish --weekly-summary
```

### 💬 自动评论管理

**实时监控：**
```bash
# 启动评论监控（后台运行）
openclaw xiaohongshu-reply --monitor --daemon

# 检查并回复所有未读评论
openclaw xiaohongshu-reply --check-all
```

**定时回复：**
```bash
# 每2小时检查评论
0 */2 * * * openclaw xiaohongshu-reply --auto
```

---

## ⚠️ 重要注意事项

### 安全提醒
- 🔒 **Cookie保护**：OpenClaw会安全存储Cookie，定期检查有效性
- 🛡️ **内容审核**：所有回复内容基于soul.md生成，支持预览确认
- 🚫 **频率控制**：内置智能频率控制，避免触发平台限制
- 🔍 **日志监控**：OpenClaw提供详细日志，便于监控和调试

### 使用限制
- 📝 发布标题不能超过20字（会被自动截断）
- ⏱️ 发布后需要等待平台审核
- 🔄 Cookie会定期过期，OpenClaw会及时提醒更新
- 📱 仅支持长文发布，不支持图片/视频笔记

### 故障排除（OpenClaw智能处理）
- **Cookie过期** → 自动提醒并暂停操作，等待重新配置
- **验证码触发** → 智能降低操作频率，避免被限制
- **网络异常** → 自动重试机制，支持断点续传
- **发布失败** → 详细错误日志，智能诊断问题原因

---

## 🎯 核心特色

### 🧠 智能化
- 基于OpenClaw soul.md的个性化AI回复
- 智能评论分类和回复策略
- 自动内容生成和优化

### 🛡️ 安全性
- 反检测机制（stealth.min.js）
- 智能频率控制
- Cookie安全管理
- 恶意内容过滤

### 🔧 自动化
- 支持cron定时任务
- 实时监控和后台运行
- 自动错误恢复
- Cookie状态自动检测

### 🚀 易用性
- OpenClaw一键安装和使用
- 简单命令行接口
- 详细的使用文档和示例

---

## 🆕 版本更新

### v2.0.0 (2026-02-10)
- ✅ 重构为OpenClaw技能包架构
- ✅ 增强反检测机制和安全性
- ✅ 添加cron定时任务支持
- ✅ Cookie自动过期检测和提醒
- ✅ 智能频率控制和错误恢复
- ✅ 基于soul.md的个性化回复系统

### v1.0.0 (2026-02-04)
- 🎉 首次发布
- ✅ 基础发布和回复功能
- ✅ Cookie认证机制

---

## 📄 许可证

本技能包仅供学习和个人使用。请遵守小红书平台的使用条款和相关法律法规。

---

## 🤝 技术支持

如需技术支持或定制开发，请联系：
- 🦀 **小红书**: 练习赛博螃蟹 @clawdbob
- 🐙 **GitHub**: [@clawbob](https://github.com/clawbob)

---

**⚡ 立即通过OpenClaw开始您的小红书自动化之旅！**

**🔥 推荐工作流：**
1. 安装OpenClaw和xiaohongshu-skills
2. 配置Cookie和soul.md人设
3. 设置cron定时任务（发帖+回复）
4. 享受全自动的小红书内容管理！