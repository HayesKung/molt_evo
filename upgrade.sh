#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="/root/.openclaw/workspace"
SYSTEMD_DIR="/etc/systemd/system"

echo "[jarvis] upgrade sync to $TARGET_DIR"
cp "$SRC_DIR"/jarvis_*.py "$TARGET_DIR"/
cp "$SRC_DIR"/JARVIS_MODE.md "$TARGET_DIR"/
cp "$SRC_DIR"/docs-jarvis-"*".md "$TARGET_DIR"/ 2>/dev/null || true
cp "$SRC_DIR"/jarvis_backup.sh "$TARGET_DIR"/
chmod +x "$TARGET_DIR"/jarvis_*.py "$TARGET_DIR"/jarvis_backup.sh || true

cp "$SRC_DIR"/jarvis-agent.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_sync.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_sync.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_backup.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_backup.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_message_ingest.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/jarvis_message_ingest.timer "$SYSTEMD_DIR"/

systemctl daemon-reload
systemctl restart jarvis-agent.service || true
systemctl restart jarvis_sync.timer || true
systemctl restart jarvis_backup.timer || true
systemctl restart jarvis_message_ingest.timer || true
python3 "$TARGET_DIR"/jarvis_daily_summary.py >/dev/null || true

echo "[jarvis] upgrade complete"
