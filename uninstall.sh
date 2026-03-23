#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}"
SYSTEMD_DIR="/etc/systemd/system"

echo "[molt_evo] stopping timers/services"
systemctl disable --now molt-evo-backup.timer 2>/dev/null || true
systemctl disable --now molt-evo-sync.timer 2>/dev/null || true
systemctl disable --now molt-evo-agent.service 2>/dev/null || true

rm -f "$SYSTEMD_DIR"/molt-evo-agent.service
rm -f "$SYSTEMD_DIR"/molt-evo-sync.service
rm -f "$SYSTEMD_DIR"/molt-evo-sync.timer
rm -f "$SYSTEMD_DIR"/molt-evo-backup.service
rm -f "$SYSTEMD_DIR"/molt-evo-backup.timer
systemctl daemon-reload

rm -f "$TARGET_DIR"/molt_evo_*.py
rm -f "$TARGET_DIR"/molt_evo_backup.sh

echo "[molt_evo] uninstall complete (db and memory files preserved)"
