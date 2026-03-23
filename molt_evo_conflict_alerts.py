#!/usr/bin/env python3
import os
import sqlite3, time, json
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
DB = ROOT / '.openclaw' / 'molt_evo' / 'molt_evo_memory.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS conflict_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_key TEXT NOT NULL,
  table_name TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT NOT NULL,
  canonical_value TEXT,
  severity TEXT NOT NULL,
  reason TEXT NOT NULL,
  source TEXT NOT NULL,
  created_ts INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,
  kind TEXT NOT NULL,
  content TEXT NOT NULL,
  meta_json TEXT DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS conflict_alert_state (
  conflict_id INTEGER PRIMARY KEY,
  alerted_ts INTEGER NOT NULL
);
''')

rows = cur.execute('''
SELECT c.id, c.item_key, c.table_name, c.old_value, c.new_value, c.canonical_value, c.severity, c.reason, c.created_ts
FROM conflict_log c
LEFT JOIN conflict_alert_state s ON s.conflict_id = c.id
WHERE s.conflict_id IS NULL
ORDER BY c.id ASC
LIMIT 50
''').fetchall()

alerts = []
now = int(time.time())
for row in rows:
    cid, item_key, table_name, old_value, new_value, canonical_value, severity, reason, created_ts = row
    content = f"molt_evo 检测到{severity}级冲突：{table_name}.{item_key} 从【{old_value or '<empty>'}】变为【{new_value}】"
    meta = {
        'conflict_id': cid,
        'item_key': item_key,
        'table_name': table_name,
        'old_value': old_value,
        'new_value': new_value,
        'canonical_value': canonical_value,
        'severity': severity,
        'reason': reason,
        'created_ts': created_ts,
    }
    cur.execute('INSERT INTO events(ts, kind, content, meta_json) VALUES(?,?,?,?)', (now, 'conflict_alert', content, json.dumps(meta, ensure_ascii=False)))
    cur.execute('INSERT INTO conflict_alert_state(conflict_id, alerted_ts) VALUES(?,?)', (cid, now))
    alerts.append(meta)

conn.commit()
print(json.dumps({'alerts': alerts}, ensure_ascii=False))
