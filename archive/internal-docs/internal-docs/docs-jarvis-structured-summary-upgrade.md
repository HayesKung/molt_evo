# Jarvis 结构化入库升级说明

## 本轮升级内容

已将 `jarvis_daily_summary.py` 从“只追加 Markdown 摘要”升级为：

1. 继续写入 `memory/YYYY-MM-DD.md`
2. 同时结构化写入 SQLite 数据库

## 新增数据表

### `daily_summaries`
按天存一份结构化摘要快照：
- `summary_date`
- `generated_ts`
- `source`
- `summary_json`

### `summary_items`
把每天抽出的条目拆开存：
- `summary_date`
- `category`
- `item_key`
- `item_value`
- `created_ts`

## 当前意义

这使 Jarvis 从：
- 文本摘要可读

升级为：
- 文本摘要可读
- 结构化摘要可查
- 可以继续做增量分析、偏好变更跟踪、规则冲突检测

## 下一步建议

1. 给 `jarvis_incremental_capture.py` 接入 structured summary 结果
2. 增加偏好变更 diff 追踪
3. 增加禁忌/偏好/命令/目标的分类提纯规则
4. 增加数据库自动备份
