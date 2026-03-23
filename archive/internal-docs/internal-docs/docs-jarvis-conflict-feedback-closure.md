# Jarvis 冲突提醒反馈闭环说明

## 本轮新增

新增脚本：
- `jarvis_conflict_feedback.py`

## 当前闭环

现在 Jarvis 已具备：
1. 发现冲突
2. 生成提醒
3. 输出到真实提醒出口
4. 接收反馈动作
5. 根据反馈修正主表与 history
6. 必要时写入 canonical / alias 规则

## 支持的反馈动作

- `keep_old`
- `accept_new`
- `canonicalize_new <canonical_value>`
- `false_positive`

## 当前意义

这使 Jarvis 从：
- 会提醒

升级为：
- 会提醒
- 能接收处理意见
- 能修正自己的长期记忆系统

## 下一步建议

1. 把反馈动作接到聊天指令格式
2. 自动对已解决冲突做关闭标记
3. 对高频冲突做聚类与规则推荐
