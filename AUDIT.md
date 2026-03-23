# AUDIT

## Audit status

Current status: **not yet ready for direct public release**.

## Why

Although the repository has been flattened and generic documentation has been added, the codebase still requires a second-pass scrub for:

- file and symbol names still using `legacy_*`
- hard-coded workspace paths
- service descriptions naming molt_evo explicitly
- historical documentation files whose names and contents are still molt_evo-specific
- runtime scripts that may still assume private deployment conventions

## Required next pass before public release

1. rename files and script entrypoints from `legacy_*` to `molt_evo_*` where appropriate
2. replace hard-coded `/root/.openclaw/workspace` assumptions with configurable paths
3. remove or archive internal migration docs not meant for public consumers
4. review systemd units for generic descriptions and paths
5. run a full sensitive-string scan again after renaming

## Current judgment

- good enough for internal migration work: **yes**
- good enough for public GitHub/Gitee open-source release right now: **no**
