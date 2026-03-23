#!/usr/bin/env python3
import sqlite3, json, os
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}'))
DB = ROOT / '.openclaw' / 'jarvis' / 'molt_evo_memory.db'
DEFAULT_CHANNEL = os.environ.get('MOLT_EVO_DEFAULT_CHANNEL', '')
DEFAULT_TARGET = os.environ.get('MOLT_EVO_DEFAULT_TARGET', '')

def main():
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
    CREATE TABLE IF NOT EXISTS conflict_notify_state (
      conflict_id INTEGER PRIMARY KEY,
      notified_ts INTEGER NOT NULL,
      channel TEXT NOT NULL,
      target TEXT NOT NULL,
      message_text TEXT NOT NULL
    );
    ''')

    row = cur.execute('''
    SELECT c.id, c.item_key, c.table_name, c.old_value, c.new_value, c.severity, c.reason
    FROM conflict_log c
    LEFT JOIN conflict_notify_state s ON s.conflict_id = c.id
    WHERE c.severity = 'high' AND s.conflict_id IS NULL
    ORDER BY c.id ASC
    LIMIT 1
    ''').fetchone()

    if not row:
        print(json.dumps({'status': 'no_conflict'}, ensure_ascii=False))
        return

    cid, item_key, table_name, old_value, new_value, severity, reason = row
    msg = (
        f"molt_evo conflict alert\n"
        f"object: {table_name}.{item_key}\n"
        f"severity: {severity}\n"
        f"old: {old_value or '<empty>'}\n"
        f"new: {new_value}\n"
        f"reason: {reason}"
    )

    print(json.dumps({
        'status': 'ready',
        'conflict_id': cid,
        'channel': DEFAULT_CHANNEL,
        'target': DEFAULT_TARGET,
        'message': msg,
    }, ensure_ascii=False))

if __name__ == '__main__':
    main()
