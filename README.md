# molt_evo

molt_evo is a reusable local capability pack for OpenClaw that adds a persistent local learning layer.

## Capabilities
- local persistent memory database (SQLite)
- structured daily summaries
- tracked preference / rule / objective / profile evolution
- conversation ingestion pipeline
- normalization and conflict detection
- alert, push, and feedback closure workflows
- backup / export / import / merge
- install / upgrade / uninstall / bootstrap / healthcheck / selftest

## Public entrypoints
The public primary entrypoints are now:
- `molt_evo_*` scripts
- `molt-evo-*` service/timer units
- `manage.sh`
- `Makefile`

Legacy `jarvis_*` files are currently kept only as a compatibility layer during migration.

## Quick start
```bash
bash manage.sh install
bash manage.sh healthcheck
bash manage.sh selftest
```

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
- `VERSION`
- `SKILL.md`

## Important note
This repository is still in active generalization work. Before public release, complete the remaining cleanup listed in `AUDIT.md` and `SECOND_PASS_REVIEW.md`.
