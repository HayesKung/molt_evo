#!/usr/bin/env python3
import os
import sqlite3, sys, time, json
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
DB = ROOT / '.openclaw' / 'molt_evo' / 'molt_evo_memory.db'

if len(sys.argv) < 3:
    raise SystemExit('usage: molt_evo_conflict_feedback.py <conflict_id> <keep_old|accept_new|canonicalize_new|false_positive> [canonical_value]')

conflict_id = int(sys.argv[1])
action = sys.argv[2]
canonical_value = sys.argv[3] if len(sys.argv) > 3 else None
now = int(time.time())
summary_date = time.strftime('%Y-%m-%d')

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
CREATE TABLE IF NOT EXISTS conflict_feedback (
  conflict_id INTEGER PRIMARY KEY,
  action TEXT NOT NULL,
  feedback_value TEXT,
  resolved_ts INTEGER NOT NULL,
  note TEXT
);
CREATE TABLE IF NOT EXISTS merge_aliases (
  alias TEXT PRIMARY KEY,
  canonical TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS preference_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_key TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT NOT NULL,
  changed_ts INTEGER NOT NULL,
  source TEXT NOT NULL,
  summary_date TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS rule_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_key TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT NOT NULL,
  changed_ts INTEGER NOT NULL,
  source TEXT NOT NULL,
  summary_date TEXT NOT NULL
);
''')

row = cur.execute('SELECT item_key, table_name, old_value, new_value FROM conflict_log WHERE id = ?', (conflict_id,)).fetchone()
if not row:
    raise SystemExit(f'conflict {conflict_id} not found')
item_key, table_name, old_value, new_value = row
history_table = 'preference_history' if table_name == 'preferences' else 'rule_history'

if action == 'keep_old':
    if old_value is not None:
        cur.execute(f'UPDATE {table_name} SET value = ?, updated_ts = ? WHERE key = ?', (old_value, now, item_key))
        cur.execute(f'INSERT INTO {history_table}(item_key, old_value, new_value, changed_ts, source, summary_date) VALUES(?,?,?,?,?,?)',
                    (item_key, new_value, old_value, now, 'jarvis_conflict_feedback.py', summary_date))
elif action == 'accept_new':
    pass
elif action == 'canonicalize_new':
    if not canonical_value:
        raise SystemExit('canonicalize_new requires canonical_value')
    cur.execute('INSERT INTO merge_aliases(alias, canonical, updated_ts) VALUES(?,?,?) ON CONFLICT(alias) DO UPDATE SET canonical=excluded.canonical, updated_ts=excluded.updated_ts',
                (new_value, canonical_value, now))
    cur.execute(f'UPDATE {table_name} SET value = ?, updated_ts = ? WHERE key = ?', (canonical_value, now, item_key))
    cur.execute(f'INSERT INTO {history_table}(item_key, old_value, new_value, changed_ts, source, summary_date) VALUES(?,?,?,?,?,?)',
                (item_key, new_value, canonical_value, now, 'jarvis_conflict_feedback.py', summary_date))
elif action == 'false_positive':
    pass
else:
    raise SystemExit(f'unknown action: {action}')

cur.execute('INSERT INTO conflict_feedback(conflict_id, action, feedback_value, resolved_ts, note) VALUES(?,?,?,?,?) ON CONFLICT(conflict_id) DO UPDATE SET action=excluded.action, feedback_value=excluded.feedback_value, resolved_ts=excluded.resolved_ts, note=excluded.note',
            (conflict_id, action, canonical_value, now, f'resolved by jarvis_conflict_feedback.py'))
conn.commit()
print(json.dumps({'conflict_id': conflict_id, 'action': action, 'feedback_value': canonical_value}, ensure_ascii=False))
