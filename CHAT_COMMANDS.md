# molt_evo Chat Commands

## 冲突反馈指令

当前支持直接在聊天中使用以下格式：

### 1. 保留旧值
```text
保留旧值 <conflict_id>
```

### 2. 接受新值
```text
接受新值 <conflict_id>
```

### 3. 规范化为指定 canonical 值
```text
规范化 <conflict_id> <canonical_value>
```

### 4. 标记误报
```text
误报 <conflict_id>
```

## 示例

```text
保留旧值 12
接受新值 12
规范化 12 主动提醒，主动总结，主动优化任务，不啰嗦，高执行力
误报 12
```

## 当前作用

这些指令会驱动：
- `molt_evo_chat_feedback.py`
- `molt_evo_conflict_feedback.py`

形成：
- 冲突提醒
- 人工反馈
- 主表修正
- history 留痕
- alias/canonical 更新

## 注意

- `conflict_id` 必须存在
- `规范化` 必须提供 canonical 值
- 当前是脚本级解析，后续可继续接入实时会话处理器
