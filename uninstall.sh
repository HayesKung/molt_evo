#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}"
SYSTEMD_DIR="/etc/systemd/system"

echo "[jarvis] stopping timers/services"
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
rm -f "$TARGET_DIR"/JARVIS_MODE.md
rm -f "$TARGET_DIR"/docs-jarvis-setup.md
rm -f "$TARGET_DIR"/docs-jarvis-structured-summary-upgrade.md
rm -f "$TARGET_DIR"/docs-jarvis-preference-history-upgrade.md
rm -f "$TARGET_DIR"/docs-jarvis-conversation-ingest-upgrade.md
rm -f "$TARGET_DIR"/docs-jarvis-conflict-normalization-upgrade.md
rm -f "$TARGET_DIR"/docs-jarvis-conflict-alerts-upgrade.md
rm -f "$TARGET_DIR"/docs-jarvis-conflict-push-closure.md
rm -f "$TARGET_DIR"/docs-jarvis-conflict-feedback-closure.md

echo "[jarvis] uninstall complete (db and memory files preserved)"
