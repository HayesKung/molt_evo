# molt_evo

molt_evo is a reusable local learning and runtime memory layer for OpenClaw.

It provides:
- persistent local memory storage
- structured daily summaries
- conversation ingestion
- normalization and conflict detection
- conflict alert / notify / feedback workflows
- backup / export / import support
- systemd-based background automation helpers

## Quick start
```bash
bash manage.sh install
bash manage.sh healthcheck
bash manage.sh selftest
```

## Public entrypoints
- `molt_evo_*` scripts
- `molt-evo-*` service and timer units
- `manage.sh`
- `Makefile`

## Common commands
```bash
bash manage.sh install
bash manage.sh upgrade
bash manage.sh healthcheck
bash manage.sh selftest
bash manage.sh bootstrap
bash manage.sh export
bash manage.sh import /path/to/export.json merge
bash manage.sh uninstall
```

## Documentation
- `INSTALL.md`
- `CONFIG.md`
- `PRIVACY_AND_SECURITY.md`
- `RELEASE.md`
- `CHANGELOG.md`
- `CHAT_COMMANDS.md`
- `VERSION`
- `SKILL.md`

## Runtime notes
- default runtime data root: `.openclaw/molt_evo`
- default database filename: `molt_evo_memory.db`
- path and runtime behavior should be configured through environment variables where needed

## Release surface
This repository is intended to contain only the public `molt_evo` runtime surface.
Private migration history and legacy compatibility material should be archived outside the public Git repository.
