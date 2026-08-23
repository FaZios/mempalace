# NEXT — mempalace

**Next**: riparare l'entry MCP `mempalace` user-scope su m710q (repo `claude-config`, non qui) — `~/.claude.json` punta a un binario inesistente.
**Why**: `claude mcp get mempalace` → ENOENT su `~/.local/share/uv/tools/mempalace/bin/mempalace-mcp`; il binario reale è `~/.mempalace-venv/bin/mempalace-mcp` (editable su questo clone). Finché è rotto, `mcp__mempalace__*` (recall semantico skill, regola 23 globale "Cross-Project Knowledge Graph") non esiste nelle sessioni su m710q.
**Steps**:
1. `claude mcp remove mempalace -s user`
2. `claude mcp add -s user mempalace -- /home/dietpi/.mempalace-venv/bin/mempalace-mcp --palace /home/dietpi/.mempalace/palace`
3. In `claude-config/scripts/mempalace-install.sh`: scrivere l'entry in `~/.claude.json` (o via `claude mcp add -s user`) invece di `~/.claude/.mcp.json`; sostituire `MEMPALACE_DATA_DIR` (inesistente) con `--palace <dir>/palace` o env `MEMPALACE_PALACE_PATH`.
4. Aggiornare il `comment` dell'entry (dice "uv tool install mempalace": falso, l'install è venv editable).
**Verify**: `claude mcp get mempalace` → "Connected"; in sessione `mcp__mempalace__mempalace_search` risponde.

**After done**:
- Prossimo sync upstream: dal clone (branch `develop` già mirror) `git worktree add /tmp/mp-main main && cd /tmp/mp-main && git checkout origin/develop -- . && git checkout main -- .gitignore` → riaggiungere le 3 righe Fazio in `.gitignore` se upstream lo tocca → aggiornare `last_synced_sha` in `.upstream-sources.toml` → test subset + ruff → commit `sync: adopt upstream mempalace X.Y.Z` → push main → `git worktree remove`. Verify: `git diff origin/develop main --stat` mostra SOLO i file meta Fazio.
- Vedi TODO.md per il resto.

**Last commit**: vedi `git log -1 main`
**Branch**: main (worktree); il clone resta su `develop` perché è il runtime editable.

---
_Aggiornato 2026-08-23 (audit autonomo m710q). Riscrivi al prossimo /sync._
