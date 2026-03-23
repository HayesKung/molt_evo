#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="/root/.openclaw/workspace"

echo '[bootstrap] ensure workspace exists'
mkdir -p "$TARGET_DIR"

echo '[bootstrap] install python/runtime assets'
cp "$REPO_DIR"/jarvis_*.py "$TARGET_DIR"/
cp "$REPO_DIR"/jarvis_backup.sh "$TARGET_DIR"/
cp "$REPO_DIR"/JARVIS_MODE.md "$TARGET_DIR"/
cp "$REPO_DIR"/docs-jarvis-"*".md "$TARGET_DIR"/ 2>/dev/null || true
chmod +x "$TARGET_DIR"/jarvis_*.py "$TARGET_DIR"/jarvis_backup.sh || true

echo '[bootstrap] install systemd units'
cp "$REPO_DIR"/jarvis-agent.service /etc/systemd/system/
cp "$REPO_DIR"/jarvis_sync.service /etc/systemd/system/
cp "$REPO_DIR"/jarvis_sync.timer /etc/systemd/system/
cp "$REPO_DIR"/jarvis_backup.service /etc/systemd/system/
cp "$REPO_DIR"/jarvis_backup.timer /etc/systemd/system/
cp "$REPO_DIR"/jarvis_message_ingest.service /etc/systemd/system/
cp "$REPO_DIR"/jarvis_message_ingest.timer /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now jarvis-agent.service
systemctl enable --now jarvis_sync.timer
systemctl enable --now jarvis_backup.timer
systemctl enable --now jarvis_message_ingest.timer

echo '[bootstrap] initialize database and first summary'
python3 "$TARGET_DIR"/jarvis_memory.py init >/dev/null
python3 "$TARGET_DIR"/jarvis_daily_summary.py >/dev/null || true

echo '[bootstrap] run healthcheck'
bash "$REPO_DIR"/healthcheck.sh || true

echo '[bootstrap] done'
