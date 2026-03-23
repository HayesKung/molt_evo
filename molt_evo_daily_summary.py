#!/usr/bin/env python3
import os
from pathlib import Path
import sqlite3, time, json

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
DB = ROOT / '.openclaw' / 'molt_evo' / 'molt_evo_memory.db'
OUT = ROOT / 'memory' / f"{time.strftime('%Y-%m-%d')}.md"
OUT.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, kind TEXT NOT NULL, content TEXT NOT NULL, meta_json TEXT DEFAULT "{}")')
cur.execute('CREATE TABLE IF NOT EXISTS conflict_log (id INTEGER PRIMARY KEY AUTOINCREMENT, item_key TEXT NOT NULL, table_name TEXT NOT NULL, old_value TEXT, new_value TEXT NOT NULL, canonical_value TEXT, severity TEXT NOT NULL, reason TEXT NOT NULL, source TEXT NOT NULL, created_ts INTEGER NOT NULL)')
for table in ['preferences','profiles','projects','rules']:
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table} (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_ts INTEGER NOT NULL)')

cur.execute('''
CREATE TABLE IF NOT EXISTS daily_summaries (
  summary_date TEXT PRIMARY KEY,
  generated_ts INTEGER NOT NULL,
  source TEXT NOT NULL,
  summary_json TEXT NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS summary_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  summary_date TEXT NOT NULL,
  category TEXT NOT NULL,
  item_key TEXT NOT NULL,
  item_value TEXT NOT NULL,
  created_ts INTEGER NOT NULL
)
''')

for table in ['preference_history', 'profile_history', 'project_history', 'rule_history']:
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {table} (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      item_key TEXT NOT NULL,
      old_value TEXT,
      new_value TEXT NOT NULL,
      changed_ts INTEGER NOT NULL,
      source TEXT NOT NULL,
      summary_date TEXT NOT NULL
    )
    ''')

summary_date = time.strftime('%Y-%m-%d')
now = int(time.time())
summary = []
summary_payload = {}
category_to_history = {
    'preferences': 'preference_history',
    'profiles': 'profile_history',
    'projects': 'project_history',
    'rules': 'rule_history',
}

for table in ['preferences','profiles','projects','rules']:
    rows = cur.execute(f'SELECT key, value FROM {table} ORDER BY updated_ts DESC LIMIT 5').fetchall()
    if rows:
        summary.append((table, rows))
        summary_payload[table] = [{'key': k, 'value': v} for k, v in rows]

existing_items = {}
for row in cur.execute('SELECT category, item_key, item_value FROM summary_items WHERE summary_date = ?', (summary_date,)).fetchall():
    existing_items[(row[0], row[1])] = row[2]

cur.execute('DELETE FROM summary_items WHERE summary_date = ?', (summary_date,))
change_records = []
for table, rows in summary:
    for k, v in rows:
        old_value = existing_items.get((table, k))
        cur.execute(
            'INSERT INTO summary_items(summary_date, category, item_key, item_value, created_ts) VALUES(?,?,?,?,?)',
            (summary_date, table, k, v, now)
        )
        if old_value != v:
            change_records.append((table, k, old_value, v))
            cur.execute(
                f'INSERT INTO {category_to_history[table]}(item_key, old_value, new_value, changed_ts, source, summary_date) VALUES(?,?,?,?,?,?)',
                (k, old_value, v, now, 'jarvis_daily_summary.py', summary_date)
            )

high_conflicts = cur.execute(
    'SELECT item_key, table_name, old_value, new_value FROM conflict_log WHERE severity = ? ORDER BY id DESC LIMIT 5',
    ('high',)
).fetchall()
summary_payload['high_conflicts'] = [
    {'item_key': k, 'table_name': t, 'old_value': o, 'new_value': n}
    for k, t, o, n in high_conflicts
]

cur.execute(
    'INSERT INTO daily_summaries(summary_date, generated_ts, source, summary_json) VALUES(?,?,?,?) '
    'ON CONFLICT(summary_date) DO UPDATE SET generated_ts=excluded.generated_ts, source=excluded.source, summary_json=excluded.summary_json',
    (summary_date, now, 'jarvis_daily_summary.py', json.dumps(summary_payload, ensure_ascii=False))
)
conn.commit()

with OUT.open('a', encoding='utf-8') as f:
    f.write('\n- Jarvis 自动知识摘要：\n')
    for table, rows in summary:
        f.write(f'  - {table}:\n')
        for k, v in rows:
            f.write(f'    - {k}: {v}\n')
    if change_records:
        f.write('  - tracked_changes:\n')
        for table, k, old_value, new_value in change_records:
            f.write(f'    - {table}.{k}: {old_value or "<empty>"} -> {new_value}\n')
    if high_conflicts:
        f.write('  - high_conflicts:\n')
        for k, t, o, n in high_conflicts:
            f.write(f'    - {t}.{k}: {o or "<empty>"} -> {n}\n')

print('daily summary updated, structured summary stored, change history tracked, high conflicts included')
