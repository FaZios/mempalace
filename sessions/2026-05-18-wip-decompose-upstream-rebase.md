---
date: 2026-05-18
device: PC-fisso
model: claude-opus-4-7
branch: main
---

# WIP commit decompose + upstream rebase su 3.3.5

## Lavoro fatto

**WIP commit 3dfcef1 (267 file) decomposto in 8 thematic commits:**
- `chore(plugin)`: .claude-plugin + .codex-plugin meta (22 file)
- `chore(meta)`: .agents + .devcontainer + .github (12 file)
- `test`: tests/ refresh (73 file)
- `refactor(mempalace)`: mempalace/ core (67 file)
- `docs(website)`: website/ (48 file)
- `chore`: hooks + examples + benchmarks (16 file)
- `chore`: docs + pyproject + uv.lock + pre-commit + gitignore (8 file)
- `chore`: root docs + integrations + .gemini (catchall)

Force-pushed origin/main, history linear, no monster commit.

**Upstream rebase su upstream/main 3.3.5 (`d0163a7`):**
- Conflict resolution `--ours` per ogni gruppo divergente (Fazio integrations preserved)
- Risolti manualmente: .gitignore (kept .envrc + benchmark patterns), CLAUDE.md
- Conflict groups: plugin/codex (8), .github (3), tests (30), mempalace core (29), website (5), hooks (8), pyproject+lock (5), root docs (5)
- Backup branch `backup/pre-rebase-2026-05-18`
- Post-rebase: 19 commits ahead / 0 behind upstream/main 3.3.5
- pyproject + mempalace import smoke OK

## Decisioni
- Fork divergence intentional (Fazio plugin + integrations layer)
- Future upstream releases: same `--ours` strategy per gruppo, conflict surface gestibile
- Rebase NON forza adoption upstream code — preserva Fazio customizations

## Deferred
- Test contextlib.closing semantic port (df5ca11) — low-value defensive test fix
