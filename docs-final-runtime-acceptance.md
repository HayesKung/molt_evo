# Jarvis 最终运行态自动触发验收单

> 日期：2026-03-23
> 目标：验证 Jarvis 是否已通过 OpenClaw 官方 Hook 机制，自动接入宿主真实消息调用链。

## 一、验收前基线

在用户发送最终测试消息前，数据库基线如下：
- `project_state_log_max = 11`
- `policy_feedback_max = 7`
- `intake_queue_max = 21`
- `events_max = 2`

## 二、宿主运行态确认

已确认：
- `openclaw-gateway.service` 处于 `active (running)`
- Gateway 已成功接收真实 Feishu 入站消息
- Workspace hook `jarvis-runtime-ingest` 已注册并启用

日志中明确出现：
- `Registered hook: jarvis-runtime-ingest -> message:received, message:preprocessed`
- `loaded 5 internal hook handlers`

## 三、真实入站测试消息

用户在 Feishu 真实发送：

> 推进任务时继续直接开干，但保留关键节点汇报

Gateway 日志记录：
- 时间：`2026-03-23T23:21:23.393+08:00`
- `received message from ...`
- `Feishu[default] DM from ...: 推进任务时继续直接开干，但保留关键节点汇报`
- `dispatching to agent (session=agent:main:main)`

## 四、验收后数据库结果

测试后数据库状态：
- `project_state_log_max = 13`
- `policy_feedback_max = 9`
- `intake_queue_max = 21`
- `events_max = 2`

新增记录中，已经出现以下内容：

### `project_state_log`
- `推进任务时继续直接开干，但保留关键节点汇报`
- `[message_id: om_x100b5321e9ea58a4b3392da10660275]\n康海: 推进任务时继续直接开干，但保留关键节点汇报`

### `policy_feedback`
- `conversation_runtime -> 推进任务时继续直接开干，但保留关键节点汇报`
- `conversation_runtime -> [message_id: om_x100b5321e9ea58a4b3392da10660275]\n康海: 推进任务时继续直接开干，但保留关键节点汇报`

## 五、结论

本次验收已经形成完整证据链：

1. 宿主 Gateway 运行中
2. 官方 workspace hook 已注册启用
3. 真实 Feishu 入站消息进入宿主
4. Jarvis hook 自动处理该消息
5. 处理结果自动写入数据库

因此可以确认：

# Jarvis 已通过 OpenClaw 官方 Hook 机制，真实接入当前宿主自动调用链。

这意味着：
- 真实聊天消息已能自动进入 Jarvis 学习/反馈入口
- Jarvis 已不再依赖手动脚本触发来处理真实入站消息

## 六、当前边界说明

当前已经验证自动进入：
- `project_state_log`
- `policy_feedback`

而更深层的 ingest / feedback / conflict 链路也已具备脚本入口与统一路由能力。

宿主入口层面，这一步已经成立，可视为“完整落地”关键节点通过。
