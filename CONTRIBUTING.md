# Contributing

Thanks for contributing to `molt_evo`.

## Ground rules
- keep the public repository free of private migration history, credentials, runtime databases, and personal deployment details
- prefer small, reviewable commits
- keep paths configurable through environment variables when practical
- update docs when changing the public command surface

## Before opening a PR
Run:

```bash
python3 -m py_compile *.py
bash manage.sh healthcheck || true
bash manage.sh selftest || true
```

## Scope
Good contributions include:
- runtime reliability improvements
- portability and configurability improvements
- documentation cleanup
- tests and safety checks

Please avoid bundling private deployment data, exports, or local memory artifacts into commits.
