#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="/root/.openclaw/workspace"
SYSTEMD_DIR="/etc/systemd/system"

echo "[jarvis] sync scripts to $TARGET_DIR"
mkdir -p "$TARGET_DIR"

cp "$SRC_DIR"/jarvis_*.py "$TARGET_DIR"/
cp "$SRC_DIR"/JARVIS_MODE.md "$TARGET_DIR"/
cp "$SRC_DIR"/docs-jarvis-"*".md "$TARGET_DIR"/ 2>/dev/null || true
cp "$SRC_DIR"/jarvis_backup.sh "$TARGET_DIR"/
chmod +x "$TARGET_DIR"/jarvis_*.py "$TARGET_DIR"/jarvis_backup.sh || true

echo "[jarvis] install systemd units"
cp "$SRC_DIR"/jarvis-agent.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_sync.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_sync.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_backup.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_backup.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_message_ingest.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_message_ingest.timer "$SYSTEMD_DIR"/

systemctl daemon-reload
systemctl enable --now jarvis-agent.service
systemctl enable --now jarvis_sync.timer
systemctl enable --now jarvis_backup.timer
systemctl enable --now jarvis_message_ingest.timer

echo "[jarvis] initialize db"
python3 "$TARGET_DIR"/jarvis_memory.py init >/dev/null
python3 "$TARGET_DIR"/jarvis_daily_summary.py >/dev/null || true

echo "[jarvis] done"
systemctl status jarvis-agent --no-pager -l || true
echo '---'
systemctl status jarvis_sync.timer --no-pager -l || true
echo '---'
systemctl status jarvis_backup.timer --no-pager -l || true
