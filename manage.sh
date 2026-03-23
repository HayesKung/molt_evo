#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CMD="${1:-help}"
shift || true

case "$CMD" in
  install)
    bash "$ROOT/install.sh" "$@"
    ;;
  upgrade)
    bash "$ROOT/upgrade.sh" "$@"
    ;;
  uninstall)
    bash "$ROOT/uninstall.sh" "$@"
    ;;
  healthcheck)
    bash "$ROOT/healthcheck.sh" "$@"
    ;;
  selftest)
    bash "$ROOT/selftest.sh" "$@"
    ;;
  bootstrap)
    bash "$ROOT/bootstrap.sh" "$@"
    ;;
  release)
    echo "Jarvis OpenClaw release"
    echo "VERSION: $(cat "$ROOT/VERSION")"
    echo "--- CHANGELOG (latest) ---"
    sed -n '1,80p' "$ROOT/CHANGELOG.md"
    ;;
  export)
    python3 "$ROOT/jarvis_export.py" "$@"
    ;;
  import)
    python3 "$ROOT/jarvis_import.py" "$@"
    ;;
  ingest)
    python3 "$ROOT/jarvis_message_autoload.py" "$@"
    ;;
  help|--help|-h)
    cat <<'EOF'
Usage: bash manage.sh <command>

Commands:
  install       Install Jarvis OpenClaw into /root/.openclaw/workspace
  upgrade       Upgrade installed files and restart timers/services
  uninstall     Remove installed files/services (preserve DB/memory)
  healthcheck   Run runtime health checks
  selftest      Run end-to-end self test and rollback test data
  bootstrap     New machine bootstrap from zero to working state
  release       Show version + latest changelog
  export        Export jarvis DB content to JSON
  import        Import JSON into jarvis DB (merge|replace)
  ingest        Queue or process real chat text into Jarvis learning pipeline
  help          Show this help
EOF
    ;;
  *)
    echo "Unknown command: $CMD" >&2
    exit 1
    ;;
esac
