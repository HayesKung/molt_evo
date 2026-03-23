#!/usr/bin/env python3
import os
import sqlite3, json, sys, time, shutil
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
DB = ROOT / '.openclaw' / 'molt_evo' / 'molt_evo_memory.db'
SRC = Path(sys.argv[1])
MODE = sys.argv[2] if len(sys.argv) > 2 else 'merge'
if not SRC.exists():
    raise SystemExit(f'missing import file: {SRC}')

backup_dir = ROOT / '.openclaw' / 'molt_evo' / 'backups'
backup_dir.mkdir(parents=True, exist_ok=True)
ts = time.strftime('%Y-%m-%d-%H%M%S')
shutil.copy2(DB, backup_dir / f'pre-import-{ts}.db')

data = json.loads(SRC.read_text(encoding='utf-8'))
conn = sqlite3.connect(DB)
cur = conn.cursor()

for table, rows in data.items():
    if not rows:
        continue
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    if not cur.fetchone():
        continue
    cols = [r[1] for r in cur.execute(f'PRAGMA table_info({table})').fetchall()]
    if MODE == 'replace':
        cur.execute(f'DELETE FROM {table}')
    for row in rows:
        keys = [k for k in row.keys() if k in cols]
        vals = [row[k] for k in keys]
        placeholders = ','.join(['?'] * len(keys))
        columns = ','.join(keys)
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        try:
            cur.execute(sql, vals)
        except sqlite3.IntegrityError:
            if 'key' in keys and 'updated_ts' in cols:
                key = row.get('key')
                value = row.get('value')
                updated_ts = row.get('updated_ts', int(time.time()))
                cur.execute(f'INSERT INTO {table}(key,value,updated_ts) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_ts=excluded.updated_ts', (key, value, updated_ts))
            elif 'alias' in keys and 'canonical' in keys:
                cur.execute(f'INSERT INTO {table}(alias,canonical,updated_ts) VALUES(?,?,?) ON CONFLICT(alias) DO UPDATE SET canonical=excluded.canonical, updated_ts=excluded.updated_ts', (row.get('alias'), row.get('canonical'), row.get('updated_ts', int(time.time()))))
            else:
                pass

conn.commit()
print(f'imported {SRC} with mode={MODE}; snapshot={backup_dir / f"pre-import-{ts}.db"}')
