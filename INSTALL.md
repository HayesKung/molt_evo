# INSTALL

## Requirements

- Linux
- Python 3
- systemd
- An OpenClaw workspace with write access

## Recommended installation

```bash
cd /path/to/molt_evo
bash manage.sh install
```

## New machine bootstrap

```bash
bash manage.sh bootstrap
```

## Post-install verification

```bash
bash manage.sh healthcheck
bash manage.sh selftest
```

## Upgrade

```bash
bash manage.sh upgrade
```

## Uninstall

```bash
bash manage.sh uninstall
```

## Export / Import

```bash
bash manage.sh export
bash manage.sh import /path/to/export.json merge
```

## Notes

This package is intended to be environment-agnostic. Review configuration defaults before production use, especially workspace paths, systemd unit install paths, and outbound notification behavior.
