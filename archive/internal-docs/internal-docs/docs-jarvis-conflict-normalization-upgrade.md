# Jarvis 冲突检测与规范化升级说明

## 本轮新增

已将 `jarvis_conversation_ingest.py` 升级为支持：

1. 规范化（canonical / alias）
2. 冲突检测（conflict log）

## 新增能力

### 规范化
会先检查：
- `merge_aliases`
- `canonical_rules`

把同义表达尽量收敛为统一 canonical value。

### 冲突检测
当某个关键 key 的旧值与新值不一致，且规范化后仍不一致时，会写入：
- `conflict_log`

字段包括：
- `item_key`
- `table_name`
- `old_value`
- `new_value`
- `canonical_value`
- `severity`
- `reason`
- `source`
- `created_ts`

## 当前意义

Jarvis 不再只是：
- 抽取
- 入库
- 记历史

而开始能：
- 识别同义表达
- 识别新旧规则/偏好冲突
- 为后续主动提醒和自动纠偏提供依据

## 下一步建议

1. 给 conflict_log 增加主动提醒链
2. 增加更多 alias / canonical 规则
3. 对 response_style / memory_policy / daemon_policy 做更强优先级处理
4. 把冲突检测接入日常定时摘要
