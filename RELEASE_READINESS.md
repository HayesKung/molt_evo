# RELEASE_READINESS

## Public release surface
This repository's intended public release surface excludes:
- `release-excluded/compat/`
- `release-excluded/archive/internal-docs/`

These directories are retained locally for migration history and compatibility review, but are not part of the strict public product surface.

## Required public entrypoints
- `molt_evo_*` scripts
- `molt-evo-*` units
- `manage.sh`
- `Makefile`
- `README.md`
- `INSTALL.md`
- `CONFIG.md`
- `PRIVACY_AND_SECURITY.md`
- `RELEASE.md`
- `CHANGELOG.md`
- `LEGACY.md`
