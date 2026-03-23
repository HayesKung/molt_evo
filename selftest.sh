#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="/root/.openclaw/workspace"
DB="$WORKSPACE/.openclaw/jarvis/jarvis_memory.db"
TEST_KEY="selftest_response_style"
TEST_CONFLICT_ID=""

cleanup() {
python3 - <<'PY'
import sqlite3
p='/root/.openclaw/workspace/.openclaw/jarvis/jarvis_memory.db'
conn=sqlite3.connect(p)
cur=conn.cursor()
for sql in [
    "DELETE FROM preferences WHERE key='selftest_response_style'",
    "DELETE FROM preference_history WHERE item_key='selftest_response_style'",
    "DELETE FROM conflict_log WHERE item_key='selftest_response_style'",
    "DELETE FROM conflict_feedback WHERE conflict_id IN (SELECT id FROM conflict_log WHERE item_key='selftest_response_style')",
    "DELETE FROM conflict_alert_state WHERE conflict_id IN (SELECT id FROM conflict_log WHERE item_key='selftest_response_style')",
    "DELETE FROM events WHERE kind='conflict_alert' AND content LIKE '%selftest_response_style%'",
    "DELETE FROM merge_aliases WHERE alias LIKE 'selftest_%' OR canonical LIKE 'selftest_%'",
]:
    try:
        cur.execute(sql)
    except Exception:
        pass
conn.commit()
print('selftest cleanup done')
PY
}

trap cleanup EXIT

echo '[selftest] write test preference v1'
python3 "$WORKSPACE/jarvis_memory.py" pref "$TEST_KEY" "selftest_v1"

echo '[selftest] force conflict via conversation ingest equivalent update'
python3 - <<'PY'
import sqlite3, time
p='/root/.openclaw/workspace/.openclaw/jarvis/jarvis_memory.db'
conn=sqlite3.connect(p)
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS conflict_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_key TEXT NOT NULL,
  table_name TEXT NOT NULL,
  old_value TEXT,
  new_value TEXT NOT NULL,
  canonical_value TEXT,
  severity TEXT NOT NULL,
  reason TEXT NOT NULL,
  source TEXT NOT NULL,
  created_ts INTEGER NOT NULL)
''')
cur.execute("INSERT INTO conflict_log(item_key, table_name, old_value, new_value, canonical_value, severity, reason, source, created_ts) VALUES(?,?,?,?,?,?,?,?,?)",
            ('selftest_response_style', 'preferences', 'selftest_v1', 'selftest_v2', 'selftest_v2', 'high', 'selftest conflict', 'selftest.sh', int(time.time())))
conn.commit()
print(cur.execute("SELECT id FROM conflict_log WHERE item_key='selftest_response_style' ORDER BY id DESC LIMIT 1").fetchone()[0])
PY

CONFLICT_ID=$(python3 - <<'PY'
import sqlite3
p='/root/.openclaw/workspace/.openclaw/jarvis/jarvis_memory.db'
conn=sqlite3.connect(p)
cur=conn.cursor()
print(cur.execute("SELECT id FROM conflict_log WHERE item_key='selftest_response_style' ORDER BY id DESC LIMIT 1").fetchone()[0])
PY
)

echo "[selftest] conflict_id=$CONFLICT_ID"

echo '[selftest] trigger alert generation'
python3 "$WORKSPACE/jarvis_conflict_alerts.py" >/dev/null

echo '[selftest] trigger notify text'
python3 "$WORKSPACE/jarvis_conflict_notify.py" >/dev/null

echo '[selftest] apply feedback canonicalize_new'
python3 "$WORKSPACE/jarvis_conflict_feedback.py" "$CONFLICT_ID" canonicalize_new selftest_v1 >/dev/null

echo '[selftest] verify chain'
python3 - <<'PY'
import sqlite3
p='/root/.openclaw/workspace/.openclaw/jarvis/jarvis_memory.db'
conn=sqlite3.connect(p)
cur=conn.cursor()
checks = {
  'conflict_log': cur.execute("SELECT COUNT(*) FROM conflict_log WHERE item_key='selftest_response_style'").fetchone()[0],
  'conflict_feedback': cur.execute("SELECT COUNT(*) FROM conflict_feedback WHERE conflict_id IN (SELECT id FROM conflict_log WHERE item_key='selftest_response_style')").fetchone()[0],
  'preference_history': cur.execute("SELECT COUNT(*) FROM preference_history WHERE item_key='selftest_response_style'").fetchone()[0],
}
print(checks)
assert checks['conflict_log'] >= 1
assert checks['conflict_feedback'] >= 1
PY

echo '[selftest] success'
