#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}"
SYSTEMD_DIR="/etc/systemd/system"

echo "[molt_evo] upgrade sync to $TARGET_DIR"
cp "$SRC_DIR"/molt_evo_*.py "$TARGET_DIR"/
cp "$SRC_DIR"/molt_evo_backup.sh "$TARGET_DIR"/
chmod +x "$TARGET_DIR"/molt_evo_*.py "$TARGET_DIR"/molt_evo_backup.sh || true

cp "$SRC_DIR"/molt-evo-agent.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-sync.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-sync.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-backup.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-backup.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-message-ingest.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-message-ingest.timer "$SYSTEMD_DIR"/

systemctl daemon-reload
systemctl restart molt-evo-agent.service || true
systemctl restart molt-evo-sync.timer || true
systemctl restart molt-evo-backup.timer || true
systemctl restart molt-evo-message-ingest.timer || true
python3 "$TARGET_DIR"/molt_evo_daily_summary.py >/dev/null || true

echo "[molt_evo] upgrade complete"
