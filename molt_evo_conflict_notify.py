#!/usr/bin/env python3
import os
import sqlite3, json
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
DB = ROOT / '.openclaw' / 'molt_evo' / 'molt_evo_memory.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()
row = cur.execute('''
SELECT id, item_key, table_name, old_value, new_value, severity, reason
FROM conflict_log
WHERE severity = 'high'
ORDER BY id DESC
LIMIT 1
''').fetchone()
if not row:
    print('NO_CONFLICT')
    raise SystemExit(0)
_, item_key, table_name, old_value, new_value, severity, reason = row
msg = f"molt_evo 冲突提醒：{table_name}.{item_key} 出现 {severity} 级变化\n旧值：{old_value or '<empty>'}\n新值：{new_value}\n原因：{reason}"
print(msg)
