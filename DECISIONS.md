# mempalace — Architecture Decision Records

Append-only. Format: data + ADR-NNN + titolo + contesto + decisione + conseguenze + alternative.

## 2026-05-15 — ADR-001: Adozione standard AGENTS.md (per-repo meta-files)

**Contesto:** Bootstrap globale del sistema AGENTS.md ecosystem (claude-config 2026-05-15). Triage portfolio assegna a questo repo bucket R.

**Decisione:** Aggiunti meta-file: AGENTS.md (rinominato da CLAUDE.md se preesistente), STATUS.md, ROADMAP.md, TODO.md, DECISIONS.md (questo file), sessions/.

**Conseguenze:** `/sync` e `/resume` da `~/.claude/commands/` ora funzionano in questo repo.

**Alternative considerate:** Mantenere solo CLAUDE.md legacy (rejected: standard cross-tool è AGENTS.md, vedi claude-config ADR-001).

## 2026-07-06 — ADR-002: Sync policy `adopt-upstream-tree` (registrato 2026-08-23)

**Contesto:** La sessione 2026-05-18 aveva trattato il fork come divergente (rebase `--ours` per gruppo, "Fazio plugin + integrations layer" da preservare). La review del 2026-07-06 ha misurato la divergenza: `git diff -w` = 0, era un flip CRLF. I file custom Fazio sono solo meta-doc (STATUS/NEXT/TODO/DECISIONS/DASHBOARD/PROJECT_STATUS/HARVEST-FINDINGS, `.upstream-sources.toml`, `renovate.json`, `.gemini/`, `sessions/`), zero logica.

**Decisione:** `main` = albero upstream adottato in blocco (`git checkout origin/develop -- .` su un worktree di `main`) + file meta Fazio. `origin/develop` = mirror 1:1 di upstream `develop`, mai commit locali. Nessun patch Fazio sul codice: se serve una fix va proposta upstream, non tenuta nel fork (`push_to_upstream = false` resta: il fork non pusha, al massimo apre PR da branch dedicati).

**Conseguenze:** Sync = operazione meccanica (procedura in NEXT.md "After done"); conflitti = 0 per costruzione; `.gitignore` è l'unico file condiviso da ri-mergiare (3 righe Fazio in coda). Il runtime su m710q è un venv **editable** sul clone (branch `develop`), quindi il clone non cambia mai branch: il lavoro su `main` avviene in un worktree. Applicato la prima volta il 2026-08-23 (3.5.0 → 3.8.0).

**Alternative considerate:** Rebase `--ours` per gruppo (rejected: preservava una divergenza che non esisteva, costo di merge a ogni release). Merge commit di upstream in main (rejected: 953 commit upstream nella storia del fork non aggiungono informazione; l'albero adottato + `last_synced_sha` nel manifest bastano).
