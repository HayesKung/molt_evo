# Jarvis 偏好变更追踪链升级说明

## 本轮升级内容

已将 Jarvis 每日结构化摘要从“只存当前快照”升级为：

1. 存当天结构化摘要快照
2. 记录偏好/资料/项目/规则的变更历史

## 新增历史表

- `preference_history`
- `profile_history`
- `project_history`
- `rule_history`

字段：
- `item_key`
- `old_value`
- `new_value`
- `changed_ts`
- `source`
- `summary_date`

## 当前能力

现在 Jarvis 不只知道：
- 当前偏好是什么

还开始知道：
- 这个偏好什么时候变了
- 从什么值变成什么值
- 哪天摘要发现了变化
- 变化来源是哪个脚本

## 意义

这使 Jarvis 从：
- 静态记忆系统

进一步升级为：
- 可追踪偏好演化系统

## 下一步建议

1. 给 `jarvis_memory.py` 的 `pref/profile` 写入也直接记 history
2. 增加规则冲突检测
3. 对偏好变化做 diff 告警与主动提醒
4. 给数据库增加自动备份与归档
