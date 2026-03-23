# Javis OpenClaw

Javis OpenClaw 是一套可复用的本地 Jarvis 能力包，面向 OpenClaw 环境，提供：

- 本地长期记忆数据库（SQLite）
- 每日自动摘要
- 结构化摘要入库
- 偏好 / 规则 / 目标 / 画像变更历史追踪
- 真实对话自动抽取链
- 规范化与冲突检测
- 冲突主动提醒
- 冲突自动推送
- 冲突反馈闭环
- 自动备份
- 健康检查
- 一键 bootstrap
- 一键 selftest
- export / import / merge

## 文档入口
- `INSTALL.md`
- `CHAT_COMMANDS.md`
- `RELEASE.md`
- `CHANGELOG.md`
- `VERSION`
- `Makefile`

## 统一入口
```bash
cd /root/Javis_openclaw
bash manage.sh help
```

## Makefile 常用入口
```bash
make install
make healthcheck
make selftest
make release
```

## manage.sh 常用入口
```bash
bash manage.sh install
bash manage.sh upgrade
bash manage.sh healthcheck
bash manage.sh selftest
bash manage.sh bootstrap
bash manage.sh export
bash manage.sh import /path/to/jarvis_export.json merge
bash manage.sh uninstall
```

## 重要说明
- 默认数据库位置：`/root/.openclaw/workspace/.openclaw/jarvis/jarvis_memory.db`
- 默认摘要位置：`/root/.openclaw/workspace/memory/YYYY-MM-DD.md`
- 默认 export 路径：`/root/.openclaw/workspace/.openclaw/jarvis/jarvis_export.json`
- “永久不丢失”不能做绝对承诺，建议搭配备份与远端仓库。


## 自动消息 ingest

- `jarvis_message_autoload.py`
- `jarvis_message_ingest.service`
- `jarvis_message_ingest.timer`

可用于把真实聊天文本排队后自动进入 Jarvis 学习链。
