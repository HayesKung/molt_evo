# INSTALL

## Requirements
- Linux
- Python 3
- systemd
- an OpenClaw workspace with write access

## Primary entrypoint
```bash
bash manage.sh help
```

## Public command surface
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

## Compatibility note
During migration, legacy `jarvis_*` scripts may still exist. New integrations should prefer the `molt_evo_*` naming surface and the unified `manage.sh` entrypoint.

## Release readiness
Before open-source release, review:
- `AUDIT.md`
- `SECOND_PASS_REVIEW.md`
- `PRIVACY_AND_SECURITY.md`
