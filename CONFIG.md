# CONFIG

## Default assumptions

The current scripts assume an OpenClaw workspace under:

- `/root/.openclaw/workspace`

and store local data under:

- `.openclaw/jarvis/`

## Recommended future hardening

For broader reuse, convert these assumptions into environment variables such as:

- `MOLT_EVO_WORKSPACE`
- `MOLT_EVO_DATA_DIR`
- `MOLT_EVO_DB_PATH`
- `MOLT_EVO_DEFAULT_CHANNEL`
- `MOLT_EVO_DEFAULT_TARGET`

## Outbound notifications

Before publishing widely, review any default target/channel logic and ensure there are no user-specific identifiers embedded in scripts or service units.
