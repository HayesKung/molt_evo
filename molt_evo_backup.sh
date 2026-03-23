#!/usr/bin/env bash
set -euo pipefail
ROOT="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}"
SRC_DB="$ROOT/.openclaw/molt_evo/molt_evo_memory.db"
BACKUP_DIR="$ROOT/.openclaw/molt_evo/backups"
EXPORT_DIR="$ROOT/.openclaw/molt_evo/exports"
mkdir -p "$BACKUP_DIR" "$EXPORT_DIR"
TS=$(date +%F-%H%M%S)
cp "$SRC_DB" "$BACKUP_DIR/molt_evo_memory-$TS.db"
python3 ${MOLT_EVO_REPO_DIR:-$(cd "$(dirname "$0")" && pwd)}/molt_evo_export.py "$EXPORT_DIR/molt_evo_export-$TS.json" >/dev/null 2>&1 || true
ls -1t "$BACKUP_DIR"/molt_evo_memory-*.db 2>/dev/null | tail -n +15 | xargs -r rm -f
ls -1t "$EXPORT_DIR"/molt_evo_export-*.json 2>/dev/null | tail -n +15 | xargs -r rm -f
printf 'backup ok: %s\n' "$BACKUP_DIR/molt_evo_memory-$TS.db"
printf 'export ok: %s\n' "$EXPORT_DIR/molt_evo_export-$TS.json"
