# PROJECT_STATUS -- mempalace

> **Cosa e questo file**
> Single source of truth dello stato del progetto. Pensato per allineamento immediato di IA o umani in meno di 60 secondi.
> Aggiornato automaticamente al termine di ogni sessione Claude Code (hook SessionEnd) e iniettato nel context all avvio (hook SessionStart).
> Le sezioni 1-3 e 9-10 sono **stabili** (cambiano solo se cambia il progetto).
> Le sezioni 4-8 sono **dinamiche** (refreshate ogni sessione).

**Last Updated:** 2026-08-23T00:00:00Z (audit autonomo m710q; stato canonico aggiornato = STATUS.md + NEXT.md)
**Last Session ID:** init-2026-05-10
**Owner:** FaZio (fork user-scope) â€” upstream: MemPalace org / milla-jovovich

---

## 1. Project Identity
- Name: mempalace
- Path: `~/Projects/mempalace` (m710q: `/data/Projects/mempalace`, runtime editable; PC Windows: `E:\Projects\mempalace`)
- Repo / Remote: origin = `git@github.com:FaZios/mempalace.git` (fork privato); upstream = https://github.com/MemPalace/mempalace (ex milla-jovovich) â€” upstream e fork distinti dell'organizzazione MemPalace; user FaZio usa user-scope binary `mempalace-mcp` (vedi memoria utente)
- One-line purpose: Local-first AI memory engine â€” verbatim conversation storage + semantic retrieval (ChromaDB di default, backend pluggable). Wings (people/projects), Rooms (time-based), Drawers (verbatim content) + AAAK compression. MCP server espone tool read/write a Claude/Gemini/Codex. Zero API key richiesta. (NB: questo e un fork upstream di terze parti, NON un progetto Fazio originale.)
- Status: stable (v3.8.0 adottata da upstream il 2026-08-23, Development Status :: 4 - Beta) â€” attivo, recently merged PRs

## 2. Tech Stack
- Languages: Python (~30+ moduli mempalace/, ~25+ test files), YAML (config), Markdown
- Frameworks: ChromaDB >=1.5.4,<2 (vector DB default), MCP (Model Context Protocol server), pytest 7+
- Key Dependencies: chromadb, pyyaml >=6, tomli (py<3.11); optional autocorrect (spellcheck), psutil (dev); NO LLM SDK richiesto per core
- Runtime / Tooling: Python 3.9..3.14 (test matrix wide); hatchling build backend; ruff (lint+format, line-length 100, max-complexity 25); pytest cov 85% fail_under
- OS Target: Cross-platform (no OS-specific code in core); Windows 10/11 dev usato da FaZio
- Special Requirements: ChromaDB persistent dir (`~/.mempalace/palace` per FaZio, 2831+ drawers); plugin system via entry-points group `mempalace.backends` e `mempalace.sources`

## 3. Architecture & Key Files
- mempalace/mcp_server.py -- MCP server, espone tool read/write (mempalace-mcp binary entry point)
- mempalace/cli.py -- CLI dispatcher (mempalace binary entry point: init, mine, search, wake-up, ecc.)
- mempalace/miner.py + convo_miner.py + convo_scanner.py -- mining file progetto + transcript di conversazioni
- mempalace/searcher.py -- hybrid search (BM25 + vector); 96.6% R@5 raw su LongMemEval, 98.4% held-out
- mempalace/knowledge_graph.py + palace_graph.py -- temporal entity-relationship graph (SQLite) + traversal stanze + cross-wing tunnels
- mempalace/backends/{base.py, chroma.py, registry.py} -- pluggable backend interface (ChromaDB default)
- mempalace/sources/{base.py, registry.py, context.py, transforms.py} -- source-adapter framework (RFC 002, plugin via entry-points)
- mempalace/dialect.py + normalize.py -- AAAK compression dialect + transcript format normalization
- mempalace/entity_detector.py + entity_registry.py + room_detector_local.py -- entity disambiguation (people/projects/rooms)
- mempalace/{palace,layers,dedup,sweeper,migrate,repair}.py -- core palace ops, layered storage, dedup, sweep cycles, schema migrate, repair
- mempalace/{llm_client,llm_refine,fact_checker,closet_llm,query_sanitizer,spellcheck}.py -- optional LLM-assisted layer (rerank, refine, fact-check)
- mempalace/{exporter,diary_ingest,onboarding,split_mega_files,project_scanner,hooks_cli,instructions_cli}.py -- import/export, onboarding flow, hook CLIs
- .claude-plugin/, .codex-plugin/ -- plugin manifests + skills + commands (help, init, mine, search, status)
- benchmarks/ + tests/benchmarks/ -- LongMemEval suite, ingest/search/MCP/recall benchmarks
- pyproject.toml -- entry points: `mempalace`, `mempalace-mcp`; ruff + pytest + coverage config

## 4. Current State  (dinamico)
- What works: v3.3.3 released, MCP server stable, ChromaDB backend production-ready, hybrid search BM25+vector, knowledge graph SQLite + temporal, AAAK compression, plugin framework (backends + sources entry-points), per-language i18n module
- Work in progress: source adapters core migration (miner.py + convo_miner.py to BaseSourceAdapter, follow-up PR pending per RFC 002); recent PRs su entity-detection init overhaul (3.3.3 changelog), security palace path env normalize, init project dedup case-insensitive
- Broken / Disabled: 1 TODO in `mcp_server.py:961` (AAAK expand before embedding per migliorare retrieval)
- Open branches: `main` (upstream tree + meta Fazio) e `develop` (mirror 1:1 di upstream develop, è il runtime editable su m710q — mai commit locali)

## 5. Last Session Summary  (dinamico)
- Date: 2026-05-10
- Goal: Initial status creation (deep-dive manual review)
- What was done: Letti README, CLAUDE.md, pyproject.toml, struttura mempalace/, git history
- Files touched: PROJECT_STATUS.md (riscritto)
- Outcome: file di stato dettagliato
- Decisions taken: [non deducibile dal codice]

## 6. Recent Changes  (dinamico, max 10 entry)
| Date | Session | Change | Impact |
|------|---------|--------|--------|
| - | recent | chore: add gemini config (2f41738) | Gemini CLI compat |
| - | recent | Merge PR #1159 from MemPalace/develop (94f1689) | upstream sync |
| - | recent | Merge PR #1176 docs/changelog-3.3.3-init-overhaul (7a75791) | doc 3.3.3 |
| - | recent | Update CHANGELOG.md (174ecaf) | doc |
| - | recent | docs(changelog): document init entity-detection overhaul in 3.3.3 (431e42a) | doc |
| - | recent | Merge PR #1166 fix/security-palace-path-env-normalize (f246d25) | security fix path |
| - | recent | Merge PR #1175 chore/rescue-stacked-prs-into-develop (8a6ebbe) | infra |
| - | recent | fix(init): case-insensitive project dedup across manifest and convo sources (55c83e9) | bugfix init |
| - | recent | chore: rescue merged stacked PRs #1150 and #1157 into develop (19ce58c) | infra |
| - | recent | Merge PR #1157 feat/wire-entities-to-miner (61d6c3c) | feat: entity wiring |

## 7. Next Steps  (dinamico)
- (TODO mcp_server.py:961) Espandere AAAK prima dell'embedding per migliorare retrieval
- (RFC 002) Migrare miner.py + convo_miner.py a BaseSourceAdapter (follow-up PR)
- Mantenere fork allineato a upstream (origin punta a `milla-jovovich/mempalace` ma upstream canonico e `MemPalace/mempalace` da PR origin)
- Per FaZio: continuare uso user-scope binary `mempalace-mcp` con palace in `~/.mempalace/palace` (2831+ drawers)
- Coverage target 85% â€” verificare attuale `pytest --cov`

## 8. Known Issues / Blockers  (dinamico)
- 1 TODO in mcp_server.py (AAAK pre-embed expansion)
- Scam alert documentato: `mempalace.tech` e impostor; sources ufficiali = github.com/MemPalace/mempalace + PyPI + mempalaceofficial.com
- LongMemEval 100% non headlinato perche ultimo 0.6% e "teaching to test" (honesty disclaimer)
- (risolto 2026-08-23) origin = FaZios/mempalace; upstream canonico MemPalace/mempalace registrato in `.upstream-sources.toml`

## 9. How to Run / Test  (stabile)
```
# Install (dev)
pip install -e ".[dev]"

# CLI
mempalace init ~/projects/myapp
mempalace mine ~/projects/myapp
mempalace mine ~/.claude/projects/ --mode convos
mempalace search "why did we switch to GraphQL"
mempalace wake-up

# MCP server (FaZio user-scope)
mempalace-mcp        # binary in PYTHONPATH

# Tests
python -m pytest tests/ -v --ignore=tests/benchmarks
python -m pytest tests/ -v --ignore=tests/benchmarks --cov=mempalace --cov-report=term-missing

# Lint / format
ruff check .
ruff format .
ruff format --check .
```

## 10. Handoff Notes for Other AI  (stabile, critico)
- Conventions: ruff line-length 100, target py39, mccabe max-complexity 25, double quotes; pytest markers `benchmark`/`slow`/`stress` esclusi di default; hatchling build; coverage fail_under 85%
- Gotchas: questo e un FORK upstream di terze parti â€” design principles in CLAUDE.md sono NON-NEGOZIABILI (verbatim, incremental only, entity-first, local-first, zero API, perf <500ms hook / <100ms startup, privacy by architecture, background everything); per FaZio palace e in `~/.mempalace/palace`; entry-point `mempalace.backends` e `mempalace.sources` per plugin terze parti; AAAK e dialect compatto via `dialect.py`
- Architectural decisions: pluggable backend (ChromaDB default ma interface-driven via backends/base.py); knowledge_graph SQLite separato dal vector store; hybrid search BM25+vector; entity-first storage (Wings = people/projects, Rooms = time, Drawers = verbatim content); LLM e OPZIONALE (rerank/refine), core funziona senza API key; MCP server come superficie principale per Claude/Gemini/Codex
- DO NOT: aggiungere summarization/paraphrasing su user content (viola design principle); aggiungere telemetry/phone-home; introdurre API key requirements per core memory; bypassare verbatim storage; toccare benchmarks/ con ruff (extend-exclude); rompere compat py3.9 (lower bound)
- Style preferences: PowerShell 5.1 compat; preferenza single comprehensive script; preservare hook/plugin esistenti (questi sono FaZio prefs â€” il repo upstream e cross-platform pure)
---

Maintained by Claude Code Status Tracker. Manual override: /status update
