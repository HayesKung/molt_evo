#!/usr/bin/env python3
import sqlite3, json, sys
from pathlib import Path

ROOT = Path('${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}')
DB = ROOT / '.openclaw' / 'jarvis' / 'molt_evo_memory.db'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / '.openclaw' / 'jarvis' / 'molt_evo_export.json'

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
export = {}
for t in tables:
    cols = [r[1] for r in cur.execute(f'PRAGMA table_info({t})').fetchall()]
    rows = [dict(zip(cols, row)) for row in cur.execute(f'SELECT * FROM {t}').fetchall()]
    export[t] = rows
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding='utf-8')
print(OUT)
