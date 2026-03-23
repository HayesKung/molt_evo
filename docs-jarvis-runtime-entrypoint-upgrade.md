# Jarvis Runtime Entrypoint Upgrade

## 本轮升级

已将 `jarvis_conversation_hook.py` 升级为统一运行入口：

1. 优先尝试聊天反馈指令闭环
2. 非反馈消息自动进入 ingest 队列
3. 保留 project_state_log / policy_feedback 写入

## 当前意义

这意味着 Jarvis 已开始具备：
- 真实聊天文本自动进入学习链
- 聊天里的反馈指令自动进入修正链
- 同时保留原有项目推进与运行时策略记录

## 当前边界

这一步已经把“统一入口脚本”打通。
如需彻底接到现网，需要宿主消息流调用本脚本。当前脚本层已准备好。
