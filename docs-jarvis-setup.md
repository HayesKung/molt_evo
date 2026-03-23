# Jarvis 核心模式落地说明

## 本次已完成
1. 创建本地持久化数据库脚本：`jarvis_memory.py`
2. 创建每日自动摘要脚本：`jarvis_daily_summary.py`
3. 创建常驻守护 systemd service 模板：`jarvis-agent.service`
4. 创建 Jarvis 模式说明：`JARVIS_MODE.md`

## 数据位置
- 数据库：`/root/.openclaw/workspace/.openclaw/jarvis/jarvis_memory.db`

## 建议的下一步
1. 安装 service 到 `/etc/systemd/system/jarvis-agent.service`
2. `systemctl daemon-reload`
3. `systemctl enable --now jarvis-agent.service`
4. 配置 cron / openclaw cron 定时执行 `jarvis_daily_summary.py`

## 说明
- 本次未启用语音唤醒；那属于下一阶段扩展。
- “永久不丢失”无法做绝对承诺，但已开始采用本地持久化数据库 + memory 文件双写思路。
