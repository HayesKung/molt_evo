# SECOND_PASS_REVIEW

## First-pass high-risk residue cleanup

Completed in this pass:
- removed user-specific default push target
- removed project-specific routing logic
- replaced user-specific mode file with generic `MODE.md`
- moved internal migration docs out of the public root set

## Remaining blockers before public release

Still needs work:
- script and unit names still use `jarvis_*`
- some docs and strings still mention Jarvis/Javis branding
- hard-coded workspace/data paths still exist
- service descriptions still use Jarvis naming
- internal docs still need either rewrite or exclusion from public release

## Current publish judgment

- safer than previous state: **yes**
- ready for direct public GitHub/Gitee release: **not yet**
