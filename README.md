# 小红书自动化工具集

这是一个用于小红书内容发布和评论管理的自动化工具集合。

## 项目结构

```
├── xiaohongshu-publish/     # 发布相关工具
│   ├── SKILL.md            # 发布技能说明文档
│   └── publish_long_text.py # 长文发布脚本
│
└── xiaohongshu-reply/       # 评论回复工具
    ├── SKILL.md            # 回复技能说明文档
    ├── check_comments.py   # 主要的评论检查和回复工具
    ├── reply_fixed.py      # 修复版回复工具（备用）
    ├── generate_replies.py # 回复模板生成器
    └── fetch_latest.py     # 最新评论获取工具
```

## 功能说明

### 📝 发布工具 (xiaohongshu-publish)

- **publish_long_text.py**: 自动发布小红书长文内容
  - 支持标题和正文内容输入
  - 自动排版和发布
  - 命令行参数支持

### 💬 评论管理工具 (xiaohongshu-reply)

- **check_comments.py**: 主要的评论管理工具
  - 自动获取最新评论
  - 批量回复指定评论
  - 支持自定义回复模板

- **reply_fixed.py**: 备用的评论回复工具
  - 提供额外的回复功能
  - 包含错误处理和调试功能

- **generate_replies.py**: 回复模板生成器
  - 生成标准化的回复模板
  - 便于批量回复管理

- **fetch_latest.py**: 评论获取工具
  - 专门用于获取最新评论
  - 保存评论数据和截图

## 环境配置

### 必需文件

1. **Cookie配置**: `~/.openclaw/secrets/xiaohongshu.json`
   ```json
   {
     "a1": "your_a1_cookie",
     "web_session": "your_web_session",
     "webId": "your_webId",
     "websectiga": "your_websectiga"
   }
   ```

2. **Stealth脚本**: `~/stealth.min.js`
   - 用于绕过反爬虫检测
   - 需要用户自行获取和配置

### 依赖安装

```bash
pip install playwright
playwright install chromium
```

## 使用方法

### 发布长文

```bash
# 基本使用
python xiaohongshu-publish/publish_long_text.py --title "文章标题" --content "文章内容"

# 显示浏览器窗口（调试用）
python xiaohongshu-publish/publish_long_text.py --title "标题" --content "内容" --visible
```

### 管理评论

```bash
# 检查并回复评论
python xiaohongshu-reply/check_comments.py

# 获取最新评论
python xiaohongshu-reply/fetch_latest.py

# 生成回复模板
python xiaohongshu-reply/generate_replies.py
```

## 注意事项

1. **Cookie安全**: 请妥善保管cookie文件，不要泄露给他人
2. **使用频率**: 建议合理控制使用频率，避免被平台检测
3. **内容合规**: 确保发布和回复的内容符合平台规范
4. **路径配置**: 首次使用前请确保所有必需文件路径正确配置

## 技术特性

- 基于 Playwright 的自动化操作
- 支持无头模式和可视化调试
- 通用路径配置，适配不同用户环境
- 模板化回复，便于批量管理
- 完善的错误处理和日志记录

## 许可证

本项目仅供学习和研究使用，请遵守相关平台的使用条款。
