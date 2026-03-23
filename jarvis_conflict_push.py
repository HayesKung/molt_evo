#!/usr/bin/env python3
import sqlite3, json, sys
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace')
DB = ROOT / '.openclaw' / 'jarvis' / 'jarvis_memory.db'
DEFAULT_TARGET = 'user:ou_a78e8c3060bcc9aaa06ce4f44096d6ba'

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
        f"Jarvis 冲突提醒\n"
        f"对象：{table_name}.{item_key}\n"
        f"等级：{severity}\n"
        f"旧值：{old_value or '<empty>'}\n"
        f"新值：{new_value}\n"
        f"原因：{reason}"
    )

    # 输出 JSON，交给外层调用 message 工具发送
    print(json.dumps({
        'status': 'ready',
        'conflict_id': cid,
        'channel': 'feishu',
        'target': DEFAULT_TARGET,
        'message': msg,
    }, ensure_ascii=False))

if __name__ == '__main__':
    main()
