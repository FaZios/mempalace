---
date: 2026-05-16
device: PC-fisso
model: claude-opus-4-7
branch: main
commits: ad0f82a, 57ef98d
session_origin: /mnt/data/Projects (cross-repo session)
---

# Master Plan — mempalace housekeeping

Da sessione cross-repo `/mnt/data/Projects/`. Solo housekeeping (fork è diverged, no logic changes).

## Fatto

- **Gitignore preventivo** `.session-handoff-history.jsonl` (file non presente su disco, preventivo). Commit `ad0f82a`.
- **Renovate config** Atlas-style conservative (commit `57ef98d`).

## NOT touched (deferred — diverged fork)

- **R3-1 AAAK pre-embedding TODO** (`mcp_server.py:961` da PROJECT_STATUS): file non esiste più (refactored). SKIP.
- **RFC 002 BaseSourceAdapter migration**: framework esiste già (`mempalace/sources/`), migration miner.py + convo_miner.py pending.
- **mempalace è FORK DIVERGED** (314 commit gap, sync_blocked=true). Logic changes locali aumentano divergence → escluse intenzionalmente.

## Token

~3k (gitignore + renovate copia + audit upstream-sources.toml).
