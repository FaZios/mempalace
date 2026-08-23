*Update: 2026-08-23 | Device: m710q (audit autonomo) | Bucket: R*

## Stato
Active — fork di tracking di `MemPalace/mempalace`, policy `adopt-upstream-tree` (vedi `.upstream-sources.toml` + DECISIONS.md ADR-002).

- `main` = albero upstream **3.8.0** (+2 fix post-release, upstream `develop` `4bc0c43` del 2026-08-22) + soli file meta Fazio (STATUS/NEXT/TODO/DECISIONS/DASHBOARD/PROJECT_STATUS/HARVEST-FINDINGS, `.upstream-sources.toml`, `renovate.json`, `.gemini/`, `sessions/`). Zero logica custom: `git diff origin/develop main -- mempalace/ tests/` = vuoto.
- `develop` = mirror 1:1 di upstream `develop` (origin/HEAD). **Non committarci**: ogni commit locale rompe il fast-forward del mirror.

## Come gira nella flotta (m710q, verificato 2026-08-23)
- Venv `~/.mempalace-venv` = `pip install -e /data/Projects/mempalace` (install **editable**: il working tree di questo clone, branch `develop`, È il runtime di `mempalace` CLI e `mempalace-mcp`). Cambiare branch nel clone = cambiare il codice live → non farlo; per lavorare su `main` usare un `git worktree` separato.
- `mempalace --version` → 3.8.0. Il dist-info del venv dice ancora 3.7.1 (metadata stale, innocuo: l'editable carica il codice dell'albero).
- CLI usata dagli hook claude-config (`session-kg-sync.sh` → `mempalace mine ~/.claude/skills/learned --wing learned_skills --agent skill-sync`): OK, `mempalace` in PATH via `~/.local/bin`.
- **MCP `mempalace` in user-scope è ROTTO** su m710q: `~/.claude.json` punta a `~/.local/share/uv/tools/mempalace/bin/mempalace-mcp` (non esiste; `claude mcp get mempalace` → ENOENT). Lo script `claude-config/scripts/mempalace-install.sh` scrive `~/.claude/.mcp.json` (file che Claude Code non legge) e passa `MEMPALACE_DATA_DIR` (env var inesistente in mempalace: quella vera è `MEMPALACE_PALACE_PATH` o `--palace`). Fix = TODO.md P0 (repo claude-config, non questo).

## Ultima attività reale
2026-08-23 — sync upstream 3.5.0 → 3.8.0 (953 commit adottati in blocco, ruff pulito, subset test verde, vedi NEXT.md).

## Prossimo passo
Vedi NEXT.md.

## Blocker
Nessuno sul repo. P0 cross-repo in TODO.md (MCP user-scope rotto su m710q).
