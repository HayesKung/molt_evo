# LEGACY

This repository keeps a legacy compatibility area under `release-excluded/compat/legacy-jarvis/`.

## Purpose
- preserve migration history during the rename from older private/internal naming
- keep old scripts available for controlled reference during transition

## Release policy
- legacy content is not part of the public primary entrypoint
- new integrations must use the `molt_evo_*` scripts and `molt-evo-*` units
- legacy content should be removed or separately archived before a strict public release tag
