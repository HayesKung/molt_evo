#!/usr/bin/env python3
import json, sqlite3, sys, time
from pathlib import Path

ROOT = Path('${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}')
DATA = ROOT / '.openclaw' / 'jarvis'
DATA.mkdir(parents=True, exist_ok=True)
DB = DATA / 'molt_evo_memory.db'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL,
  kind TEXT NOT NULL,
  content TEXT NOT NULL,
  meta_json TEXT DEFAULT '{}'
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
'''


def conn():
    c = sqlite3.connect(DB)
    c.executescript(SCHEMA)
    return c


def add_event(kind: str, content: str, meta: dict | None = None):
    with conn() as c:
        c.execute('INSERT INTO events(ts, kind, content, meta_json) VALUES(?,?,?,?)', (int(time.time()), kind, content, json.dumps(meta or {}, ensure_ascii=False)))


def upsert(table: str, key: str, value: str):
    now = int(time.time())
    summary_date = time.strftime('%Y-%m-%d')
    history_table = {'preferences': 'preference_history', 'profiles': 'profile_history'}.get(table)
    with conn() as c:
        old = c.execute(f'SELECT value FROM {table} WHERE key = ?', (key,)).fetchone()
        old_value = old[0] if old else None
        c.execute(
            f'INSERT INTO {table}(key,value,updated_ts) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_ts=excluded.updated_ts',
            (key, value, now)
        )
        if history_table and old_value != value:
            c.execute(
                f'INSERT INTO {history_table}(item_key, old_value, new_value, changed_ts, source, summary_date) VALUES(?,?,?,?,?,?)',
                (key, old_value, value, now, 'jarvis_memory.py', summary_date)
            )


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'init'
    if cmd == 'init':
        conn().close()
        print(DB)
    elif cmd == 'event':
        kind = sys.argv[2]
        content = sys.argv[3]
        meta = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        add_event(kind, content, meta)
    elif cmd == 'pref':
        upsert('preferences', sys.argv[2], sys.argv[3])
    elif cmd == 'profile':
        upsert('profiles', sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(f'unknown command: {cmd}')
