#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${MOLT_EVO_WORKSPACE:-/root/.openclaw/workspace}"

echo '[bootstrap] ensure workspace exists'
mkdir -p "$TARGET_DIR"

echo '[bootstrap] install python/runtime assets'
cp "$REPO_DIR"/molt_evo_*.py "$TARGET_DIR"/
cp "$REPO_DIR"/molt_evo_backup.sh "$TARGET_DIR"/
chmod +x "$TARGET_DIR"/molt_evo_*.py "$TARGET_DIR"/molt_evo_backup.sh || true

echo '[bootstrap] install systemd units'
cp "$REPO_DIR"/molt-evo-agent.service /etc/systemd/system/
cp "$REPO_DIR"/molt-evo-sync.service /etc/systemd/system/
cp "$REPO_DIR"/molt-evo-sync.timer /etc/systemd/system/
cp "$REPO_DIR"/molt-evo-backup.service /etc/systemd/system/
cp "$REPO_DIR"/molt-evo-backup.timer /etc/systemd/system/
cp "$REPO_DIR"/molt-evo-message-ingest.service /etc/systemd/system/
cp "$REPO_DIR"/molt-evo-message-ingest.timer /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now molt-evo-agent.service
systemctl enable --now molt-evo-sync.timer
systemctl enable --now molt-evo-backup.timer
systemctl enable --now molt-evo-message-ingest.timer

echo '[bootstrap] initialize database and first summary'
python3 "$TARGET_DIR"/molt_evo_memory.py init >/dev/null
python3 "$TARGET_DIR"/molt_evo_daily_summary.py >/dev/null || true

echo '[bootstrap] run healthcheck'
bash "$REPO_DIR"/healthcheck.sh || true

echo '[bootstrap] done'
