#!/usr/bin/env bash
set -euo pipefail

DB="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}/.openclaw/molt_evo/molt_evo_memory.db"
BACKUP_DIR="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}/.openclaw/molt_evo/backups"

echo '== molt_evo Healthcheck =='

echo '[1] DB check'
if [ -f "$DB" ]; then
  echo "DB OK: $DB"
else
  echo "DB MISSING: $DB"
fi

echo '---'
echo '[2] Service status'
systemctl is-active molt-evo-agent.service >/dev/null 2>&1 && echo 'molt-evo-agent.service: active' || echo 'molt-evo-agent.service: inactive'

echo '---'
echo '[3] Timer status'
systemctl is-enabled molt-evo-sync.timer >/dev/null 2>&1 && echo 'molt-evo-sync.timer: enabled' || echo 'molt-evo-sync.timer: disabled'
systemctl is-enabled molt-evo-backup.timer >/dev/null 2>&1 && echo 'molt-evo-backup.timer: enabled' || echo 'molt-evo-backup.timer: disabled'

echo '---'
echo '[4] Recent backup'
LATEST_BACKUP=$(ls -1t "$BACKUP_DIR"/molt_evo_memory-*.db 2>/dev/null | head -n 1 || true)
if [ -n "${LATEST_BACKUP:-}" ]; then
  echo "latest backup: $LATEST_BACKUP"
else
  echo 'latest backup: none'
fi

echo '---'
echo '[5] Conflict alert chain'
python3 - <<'PY'
import sqlite3
p=os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace') + '/.openclaw/molt_evo/molt_evo_memory.db'
conn=sqlite3.connect(p)
cur=conn.cursor()
try:
    latest_conflict = cur.execute("SELECT id, item_key, severity FROM conflict_log ORDER BY id DESC LIMIT 1").fetchone()
    latest_alert = cur.execute("SELECT kind, content FROM events WHERE kind='conflict_alert' ORDER BY id DESC LIMIT 1").fetchone()
    print('latest_conflict:', latest_conflict)
    print('latest_alert:', latest_alert)
except Exception as e:
    print('conflict check err:', e)
PY

echo '== Healthcheck done =='
