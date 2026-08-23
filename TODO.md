# mempalace — TODO

Aggiornato 2026-08-23 (audit autonomo su m710q).

## P0 (blocking)
- [ ] **[claude-config] MCP `mempalace` user-scope rotto su m710q** — `~/.claude.json` → binario uv-tool inesistente; reale: `~/.mempalace-venv/bin/mempalace-mcp`. Comandi esatti in NEXT.md. verify: `claude mcp get mempalace` → Connected.
- [ ] **[claude-config] `scripts/mempalace-install.sh`** scrive `~/.claude/.mcp.json` (non letto da Claude Code) e passa env `MEMPALACE_DATA_DIR` (non esiste in mempalace — `grep -rn MEMPALACE_DATA_DIR mempalace/` = 0). Usare `claude mcp add -s user … -- <bin> --palace ~/.mempalace/palace` (o `MEMPALACE_PALACE_PATH`). verify: dopo re-run dello script su un host pulito, `claude mcp get mempalace` → Connected.

## P1 (next session)
- [ ] Riallineare `~/.mempalace-venv` dist-info (dice 3.7.1, albero 3.8.0): `uv pip install --python ~/.mempalace-venv/bin/python -e /data/Projects/mempalace` (idempotente, no restart). verify: `~/.mempalace-venv/bin/python -c "import importlib.metadata as m;print(m.version('mempalace'))"` → 3.8.0.
- [ ] Decidere se il mirror `develop` va anche pushato su `FaZios/mempalace` da un job (oggi arriva già aggiornato: ff-only quotidiano da qualche sync esterno — origine non documentata). verify: una riga in DECISIONS.md o in `.upstream-sources.toml` che dice chi aggiorna `origin/develop`.

## P2 (this week)
- [x] ~~Full test suite su host non di produzione (PC)~~ — fatta il 2026-08-23 su m710q a load basso (nice 19, venv scratch, albero 3.8.0): `pytest tests/ -q --ignore=tests/benchmarks` → 4468 passed, 31 skipped, 0 failed in 230s.
- [ ] `DASHBOARD.md` / `PROJECT_STATUS.md` sono "auto-generati" ma nessun hook li tocca da maggio: o si riattiva il generatore o si declassano a puntatori verso STATUS.md. verify: data "Ultimo refresh" ≤ 30 giorni oppure file ridotto a 5 righe.

## P3 (nice to have)
- [ ] `.gemini/settings.json` contiene path Windows (`C:\Users\FaZio\...`): valido solo sul PC Windows; su m710q è ignorato. Renderlo per-host o documentarlo. verify: nota in STATUS.md o file rimosso dal tracking.

## Chiusi / WONTFIX
- ~~Fork divergente 314 commit (DASHBOARD 2026-05-13)~~ — falso positivo CRLF (manifest 2026-07-06); da 2026-08-23 `main` = upstream 3.8.0 + soli meta Fazio.
- ~~RFC 002 migrazione miner→BaseSourceAdapter / TODO `mcp_server.py:961` AAAK pre-embed~~ — item upstream, non del fork: si seguono adottando l'albero upstream, non qui.
- ~~Rebase `--ours` per gruppo (sessione 2026-05-18)~~ — sostituito da `adopt-upstream-tree` (ADR-002), zero logica custom da preservare.
