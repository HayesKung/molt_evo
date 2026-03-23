#!/usr/bin/env bash
set -euo pipefail
ROOT="/root/.openclaw/workspace"
SRC_DB="$ROOT/.openclaw/jarvis/jarvis_memory.db"
BACKUP_DIR="$ROOT/.openclaw/jarvis/backups"
EXPORT_DIR="$ROOT/.openclaw/jarvis/exports"
mkdir -p "$BACKUP_DIR" "$EXPORT_DIR"
TS=$(date +%F-%H%M%S)
cp "$SRC_DB" "$BACKUP_DIR/jarvis_memory-$TS.db"
python3 /root/Javis_openclaw/jarvis_export.py "$EXPORT_DIR/jarvis_export-$TS.json" >/dev/null 2>&1 || true
ls -1t "$BACKUP_DIR"/jarvis_memory-*.db 2>/dev/null | tail -n +15 | xargs -r rm -f
ls -1t "$EXPORT_DIR"/jarvis_export-*.json 2>/dev/null | tail -n +15 | xargs -r rm -f
printf 'backup ok: %s\n' "$BACKUP_DIR/jarvis_memory-$TS.db"
printf 'export ok: %s\n' "$EXPORT_DIR/jarvis_export-$TS.json"
