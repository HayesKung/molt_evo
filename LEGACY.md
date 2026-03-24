# LEGACY

Legacy migration material is retained under `release-excluded/` for local transition history only.

## Purpose
- preserve limited migration context during repository cleanup
- keep non-public transition material out of the primary runtime surface

## Release policy
- legacy material is not part of the public primary entrypoint
- new integrations must use the `molt_evo_*` scripts and `molt-evo-*` units
- legacy material should be removed or separately archived before a strict public release tag
