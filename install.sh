#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}"
SYSTEMD_DIR="/etc/systemd/system"

echo "[molt_evo] ensure workspace exists: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

cp "$SRC_DIR"/molt_evo_*.py "$TARGET_DIR"/
cp "$SRC_DIR"/molt_evo_backup.sh "$TARGET_DIR"/
chmod +x "$TARGET_DIR"/molt_evo_*.py "$TARGET_DIR"/molt_evo_backup.sh || true

echo "[molt_evo] install systemd units"
cp "$SRC_DIR"/molt-evo-agent.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-sync.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-sync.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-backup.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-backup.timer "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-message-ingest.service "$SYSTEMD_DIR"/
cp "$SRC_DIR"/molt-evo-message-ingest.timer "$SYSTEMD_DIR"/

systemctl daemon-reload
systemctl enable --now molt-evo-agent.service
systemctl enable --now molt-evo-sync.timer
systemctl enable --now molt-evo-backup.timer
systemctl enable --now molt-evo-message-ingest.timer

echo "[molt_evo] initialize db"
MOLT_EVO_REPO_DIR="$SRC_DIR" python3 "$SRC_DIR"/molt_evo_memory.py init >/dev/null
MOLT_EVO_REPO_DIR="$SRC_DIR" python3 "$SRC_DIR"/molt_evo_daily_summary.py >/dev/null || true

echo "[molt_evo] done"
systemctl status molt-evo-agent.service --no-pager -l || true
echo '---'
systemctl status molt-evo-sync.timer --no-pager -l || true
echo '---'
systemctl status molt-evo-backup.timer --no-pager -l || true
