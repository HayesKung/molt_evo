# PRIVACY_AND_SECURITY

## Publishing rule

This package must not include:

- personal names tied to a private deployment
- private project names or internal business context
- channel/user IDs
- API tokens
- embedded private repository URLs
- private chat transcripts

## Before publishing

Run a repository-wide scan for:

- account identifiers
- repository credentials
- private paths
- provider-specific personal targets
- sensitive operational notes

## Runtime caution

Even when the repository is clean, runtime databases, backups, exports, and memory files may still contain sensitive data. Do not publish those artifacts.
