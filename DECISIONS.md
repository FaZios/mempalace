# mempalace — Architecture Decision Records

Append-only. Format: data + ADR-NNN + titolo + contesto + decisione + conseguenze + alternative.

## 2026-05-15 — ADR-001: Adozione standard AGENTS.md (per-repo meta-files)

**Contesto:** Bootstrap globale del sistema AGENTS.md ecosystem (claude-config 2026-05-15). Triage portfolio assegna a questo repo bucket R.

**Decisione:** Aggiunti meta-file: AGENTS.md (rinominato da CLAUDE.md se preesistente), STATUS.md, ROADMAP.md, TODO.md, DECISIONS.md (questo file), sessions/.

**Conseguenze:** `/sync` e `/resume` da `~/.claude/commands/` ora funzionano in questo repo.

**Alternative considerate:** Mantenere solo CLAUDE.md legacy (rejected: standard cross-tool è AGENTS.md, vedi claude-config ADR-001).
