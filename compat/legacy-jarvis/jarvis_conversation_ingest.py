#!/usr/bin/env python3
import re, sqlite3, sys, time
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace')
DB = ROOT / '.openclaw' / 'jarvis' / 'jarvis_memory.db'
text = ' '.join(sys.argv[1:]).strip()
if not text:
    raise SystemExit('usage: jarvis_conversation_ingest.py <text>')

now = int(time.time())
summary_date = time.strftime('%Y-%m-%d')
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS intake_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,
  content TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'new',
  created_ts INTEGER NOT NULL,
  processed_ts INTEGER
);
CREATE TABLE IF NOT EXISTS preferences (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS rules (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS objectives (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
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
CREATE TABLE IF NOT EXISTS profile_history (
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
CREATE TABLE IF NOT EXISTS project_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_key TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT NOT NULL,
  changed_ts INTEGER NOT NULL,
  source TEXT NOT NULL,
  summary_date TEXT NOT NULL
);
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
CREATE TABLE IF NOT EXISTS canonical_rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_key TEXT NOT NULL,
  alias TEXT NOT NULL,
  canonical_value TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS merge_aliases (
  alias TEXT PRIMARY KEY,
  canonical TEXT NOT NULL,
  updated_ts INTEGER NOT NULL
);
''')

def normalize_value(value: str):
    value = value.strip()
    alias = cur.execute('SELECT canonical FROM merge_aliases WHERE alias = ?', (value,)).fetchone()
    if alias:
        return alias[0], f'alias:{value}'
    canonical = cur.execute('SELECT canonical_value FROM canonical_rules WHERE alias = ? ORDER BY updated_ts DESC LIMIT 1', (value,)).fetchone()
    if canonical:
        return canonical[0], f'canonical:{value}'
    return value, None

def detect_conflict(key, table, old_value, new_value):
    if old_value is None or old_value == new_value:
        return None
    old_norm, _ = normalize_value(old_value)
    new_norm, norm_source = normalize_value(new_value)
    if old_norm == new_norm:
        return None
    severity = 'high' if key in {'memory_policy', 'daemon_policy', 'response_style', 'delivery_style'} else 'medium'
    reason = f'value_changed:{old_value} -> {new_value}'
    return (key, table, old_value, new_value, new_norm, severity, reason, norm_source)

def upsert_with_history(table, history_table, key, value):
    normalized_value, norm_source = normalize_value(value)
    old = cur.execute(f'SELECT value FROM {table} WHERE key=?', (key,)).fetchone()
    old_value = old[0] if old else None
    conflict = detect_conflict(key, table, old_value, normalized_value)
    cur.execute(
        f'INSERT INTO {table}(key,value,updated_ts) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_ts=excluded.updated_ts',
        (key, normalized_value, now)
    )
    if old_value != normalized_value:
        cur.execute(
            f'INSERT INTO {history_table}(item_key, old_value, new_value, changed_ts, source, summary_date) VALUES(?,?,?,?,?,?)',
            (key, old_value, normalized_value, now, 'jarvis_conversation_ingest.py', summary_date)
        )
    if conflict:
        cur.execute(
            'INSERT INTO conflict_log(item_key, table_name, old_value, new_value, canonical_value, severity, reason, source, created_ts) VALUES(?,?,?,?,?,?,?,?,?)',
            (key, table, conflict[2], conflict[3], conflict[4], conflict[5], conflict[6], norm_source or 'jarvis_conversation_ingest.py', now)
        )

extractions = []
lines = [line.strip(' -：:') for line in text.splitlines() if line.strip()]
whole = ' '.join(lines)

rule_patterns = [
    ('delivery_style', r'真实交付优先[^，。\n]*'),
    ('work_pattern', r'小步改动[^，。\n]*'),
    ('acceptance_rule', r'每轮必须[^。\n]*'),
    ('memory_policy', r'禁止清除记忆[^。\n]*|所有历史永久保存'),
    ('daemon_policy', r'开机自动启动[^。\n]*|崩溃自动重启[^。\n]*|24 小时持续运行'),
]

pref_patterns = [
    ('response_style', r'主动提醒[^。\n]*高执行力[^。\n]*'),
    ('response_style_short', r'不啰嗦[^。\n]*高执行力|专业[^。\n]*主动总结[^。\n]*'),
]

objective_patterns = [
    ('jarvis_upgrade_goal', r'高质量自动学习系统'),
    ('jarvis_autolearn_goal', r'自动增量学习'),
    ('jarvis_summary_goal', r'每天自动总结[^。\n]*专属个人模型'),
]

for key, pat in rule_patterns:
    m = re.search(pat, whole)
    if m:
        val = m.group(0).strip()
        upsert_with_history('rules', 'rule_history', key, val)
        extractions.append(('rule', key, val))

for key, pat in pref_patterns:
    m = re.search(pat, whole)
    if m:
        val = m.group(0).strip()
        upsert_with_history('preferences', 'preference_history', key, val)
        extractions.append(('preference', key, val))

for key, pat in objective_patterns:
    m = re.search(pat, whole)
    if m:
        val = m.group(0).strip()
        upsert_with_history('objectives', 'project_history', key, val)
        extractions.append(('objective', key, val))

for category, _, value in extractions:
    cur.execute('INSERT INTO intake_queue(category, content, status, created_ts, processed_ts) VALUES(?,?,?,?,?)', (category, value, 'done', now, now))

conn.commit()
print({'extractions': extractions})
