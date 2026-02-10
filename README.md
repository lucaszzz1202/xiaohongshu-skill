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

## 🚀 推荐安装方式（Claude Code）

### 🎯 最佳实践：通过Claude Code加载

**第一步：上传技能包**
1. 将整个技能包文件夹上传到Claude Code工作区
2. 或者提供Git仓库链接让Claude Code克隆

**第二步：加载技能**
```
请Claude Code执行:
1. load_skill xiaohongshu-publish  # 加载发布技能
2. load_skill xiaohongshu-reply    # 加载回复技能
3. 测试基础功能
```

**第三步：环境配置**
Claude Code会自动:
- 📦 检查并安装必需的Python依赖
- 🔍 验证环境配置
- 🛠️ 设置Cookie认证文件路径
- 🧪 运行基础功能测试

**优势：**
- ✅ 自动依赖管理
- ✅ 智能错误诊断
- ✅ 实时功能测试
- ✅ 无需手动配置

---

## 🛠️ 技术要求

### 系统依赖（Claude Code自动处理）
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

### 🚀 发布长文笔记

通过Claude Code使用：
```
"帮我发布一篇小红书笔记：
标题：AI工具使用心得
内容：[您的长文内容]
标签：AI, 工具, 效率"
```

Claude Code会自动：
- 📝 调用xiaohongshu-publish技能
- 🔍 验证标题长度（≤20字）
- 🖼️ 生成封面图片
- 📤 发布到小红书平台

### 💬 自动回复评论

通过Claude Code使用：
```
"帮我处理小红书评论回复"
```

Claude Code会自动：
- 📥 读取待回复评论
- 🤖 基于soul.md生成回复内容
- 👀 显示回复预览供确认
- 📤 发送确认后的回复

---

## ⚠️ 重要注意事项

### 安全提醒
- 🔒 **Cookie保护**：定期更新Cookie，避免泄露
- 🛡️ **内容审核**：所有回复内容建议人工审核后发送
- 🚫 **频率控制**：避免过于频繁的操作触发平台限制
- 🔍 **日志监控**：定期查看操作日志，及时发现异常

### 使用限制
- 📝 发布标题不能超过20字（会被自动截断）
- ⏱️ 发布后需要等待平台审核
- 🔄 Cookie会定期过期，需要更新
- 📱 仅支持长文发布，不支持图片/视频笔记

### 故障排除（Claude Code辅助）
- **Cookie过期** → Claude Code会提示重新配置
- **验证码触发** → 自动建议降低操作频率
- **回复错位** → 自动启用关键词验证机制
- **发布失败** → 智能诊断网络和认证问题

---

## 🎯 核心特色

### 🧠 智能化
- AI驱动的内容审核
- 智能评论分类和回复策略
- 基于OpenClaw soul.md的个性化回复

### 🛡️ 安全性
- 反检测机制（stealth.min.js）
- 关键词验证防误回复
- 恶意内容过滤

### 🔧 易用性
- Claude Code一键加载
- 自动环境配置
- 实时功能测试

---

## 🆕 版本更新

### v2.0.0 (2026-02-10)
- ✅ 拆分发布和回复为独立技能
- ✅ 增强反检测机制
- ✅ 添加关键词验证防误回复
- ✅ 优化错误处理和日志记录
- ✅ 集成OpenClaw soul.md人设系统

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
- 📧 Email: [your-email@example.com]
- 💬 微信: [your-wechat-id]
- 🐙 GitHub: [your-github-profile]

---

**⚡ 立即通过Claude Code开始您的小红书自动化之旅！**