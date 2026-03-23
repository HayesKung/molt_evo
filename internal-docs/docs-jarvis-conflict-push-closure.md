# Jarvis 冲突自动推送闭环说明

## 本轮新增

新增脚本：
- `jarvis_conflict_push.py`

## 闭环结构

当前最小自动推送闭环为：

1. `jarvis_conversation_ingest.py` 写入 `conflict_log`
2. `jarvis_conflict_alerts.py` 生成冲突提醒事件
3. `jarvis_conflict_push.py` 读取尚未推送的高优先级冲突
4. 外层消息发送器将其发到当前 Feishu 会话
5. 发送成功后写入 `conflict_notify_state` 防止重复推送

## 当前状态

本轮已完成到：
- 生成待发送消息体
- 准备推送目标
- 准备防重状态表

下一步只需把消息发送和状态落库接上，即可成为完整自动推送链。
