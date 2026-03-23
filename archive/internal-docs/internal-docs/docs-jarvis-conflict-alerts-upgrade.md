# Jarvis 冲突主动提醒链升级说明

## 本轮新增

新增脚本：
- `jarvis_conflict_alerts.py`

## 当前能力

它会：
1. 扫描 `conflict_log` 中尚未提醒的冲突
2. 生成 `conflict_alert` 类型事件
3. 写入 `events`
4. 在 `conflict_alert_state` 中标记已提醒，避免重复提醒

## 当前意义

这使 Jarvis 从：
- 只能记录冲突

升级为：
- 可以主动生成冲突提醒事件
- 为后续接消息提醒 / 每日摘要提醒 / 守护进程提醒打下基础

## 下一步建议

1. 把 `conflict_alert` 接到 daily summary
2. 把高优先级冲突接到主动消息提醒
3. 对同一 key 的频繁冲突做聚合
4. 给冲突增加“建议动作”
