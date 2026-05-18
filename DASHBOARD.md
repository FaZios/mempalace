# Dashboard — mempalace
_Auto-generato da dashboard-keeper · Ultimo refresh: 2026-05-13 14:30_

## Status

| Campo | Valore |
|---|---|
| Stato | PROD-STABLE |
| Stack | Python 3.x · uv · ChromaDB (backend default) · SQLite (knowledge graph) · MCP server |
| Repo | github.com/FaZios/mempalace (privato, fork divergente — 314 commit gap da upstream) |
| Branch attivo | main |
| Avanzamento | ~80% (MCP server operativo, KG attivo, hooks wired) |

## Attivita ultimi 30g

- Commit: 269
- Ultimo commit: `0bf877e` .upstream-sources.toml: mark as diverged fork (314 commit gap) (2026-05-12)

## Code metrics

- LoC: n/a (Python, ChromaDB, SQLite)
- Test: presente (`pytest tests/`, 85% coverage threshold)
- Sentrux Q: n/a

## Dipendenze interne (cross-progetto)

| Direzione | Progetto | Nota |
|---|---|---|
| Consumato da | exocortex | MCP memory server (riuso pattern, no duplicazione) |
| Consumato da | tutti | `~/.claude/knowledge-graph.jsonl` KG MCP — iniettato da hook sessione |

## Deploy state

- PC fisso: running — MCP server attivo (Claude Code hooks)
- Path: `~/.claude/knowledge-graph.jsonl` (KG condiviso)
- Healthcheck: n/a (MCP server, verifica via tool `read_graph`)

## Open gaps

- **[ARCH]** Fork divergente 314 commit da upstream — verify improvements upstream periodicamente
- **[PERF]** Performance budget: hooks < 500ms, startup injection < 100ms (da verificare)
- **[POLICY]** Verbatim always — verificare che nessuna PR introduca summarization
- **[WATCH]** Upstream: `jcartu/rasputin-memory`, `topoteretes/cognee`, `supermemoryai/supermemory`, `letta-ai/claude-subconscious` — watch per pattern importabili

## Prossimi passi suggeriti

1. **Upstream audit** — verificare 314 commit gap e portare improvements low-risk senza breaking
2. **Performance verify** — misurare hook latency e startup injection (devono stare nei budget)
3. **exocortex integration** — allineare pattern MCP con esocortex brain layer
