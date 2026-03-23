#!/usr/bin/env python3
import re, sqlite3, sys, time, subprocess, json
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace')
DB = ROOT / '.openclaw' / 'jarvis' / 'jarvis_memory.db'
text = ' '.join(sys.argv[1:]).strip()
if not text:
    raise SystemExit('usage: jarvis_conversation_hook.py <text>')

# 1) 先尝试聊天反馈指令闭环
feedback_raw = subprocess.check_output(['python3', str(ROOT / 'jarvis_chat_feedback.py'), text], text=True).strip()
try:
    feedback_result = json.loads(feedback_raw)
except Exception:
    feedback_result = {'matched': False}

# 2) 常规消息进入自动 ingest 队列
if not feedback_result.get('matched'):
    subprocess.check_output(['python3', str(ROOT / 'jarvis_message_autoload.py'), text], text=True)

# 3) 保留原 conversation runtime / project log 行为
conn = sqlite3.connect(DB)
conn.execute('CREATE TABLE IF NOT EXISTS project_state_log (id INTEGER PRIMARY KEY AUTOINCREMENT, project TEXT NOT NULL, state TEXT NOT NULL, updated_ts INTEGER NOT NULL)')
conn.execute('CREATE TABLE IF NOT EXISTS policy_feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, policy_key TEXT NOT NULL, feedback TEXT NOT NULL, updated_ts INTEGER NOT NULL)')
project = '/root/beagle-ip' if 'beagle' in text.lower() or '详情' in text or '推荐' in text else '/root/stock' if 'stock' in text.lower() or 'A股' in text else '/root/beagle-ip'
if re.search(r'继续|推进|增强|上线|验收|闭环', text):
    conn.execute('INSERT INTO project_state_log(project,state,updated_ts) VALUES(?,?,?)', (project, text, int(time.time())))
if re.search(r'直接开干|不要空谈|先结果|主动提醒|不啰嗦', text):
    conn.execute('INSERT INTO policy_feedback(policy_key,feedback,updated_ts) VALUES(?,?,?)', ('conversation_runtime', text, int(time.time())))
conn.commit()

print(json.dumps({'hook': 'applied', 'feedback_matched': bool(feedback_result.get('matched'))}, ensure_ascii=False))
