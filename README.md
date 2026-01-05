
# Obsidian Watchtower

Local-first **funding fraud & corruption intelligence** system for investigating user-defined subjects (organizations, companies, individuals, and networks) with **evidence-grade provenance**, **graph-native link analysis**, **time-machine diffs**, and **audit-ready case files**.

> Core rule: **No claim without evidence.** Every claim links to immutable source artifacts (URL/PDF/HTML/screenshot hash), retrieval timestamps, parse method, and model/tool versions.

---

## What It Does

Obsidian Watchtower helps you **collect, preserve, connect, analyze, and narrate** evidence about suspected fraud/corruption patterns in funding and procurement ecosystems.

### Key Capabilities
- **Provenance-first evidence vault**
  - Immutable snapshots of raw HTML/PDF/JSON + extracted text/tables + normalized fields
  - SHA-256 hashing + signed manifests per run
  - Model/tool/prompt fingerprints logged for reproducibility
- **Claim Ledger (audit-ready findings)**
  - All outputs stored as structured claims with confidence
  - Supporting + counter-evidence IDs (no “trust me bro” summaries)
- **Graph-native network tracing**
  - Entity resolution (aliases, DBA names, misspellings)
  - Relationship analysis (vendors, contracts, officers, shared addresses)
  - Queries like: *“Show recipients within 2 hops of Org X who received funds within 30 days of Contract Y.”*
- **Time Machine mode**
  - Run-to-run diffs (silent edits, amount changes, renamed recipients, new docs)
  - Watchlists + alert triggers (spikes, splitting patterns, address reuse)
- **Narrative Builder**
  - Generates case files that read like **journalism + audit**
  - Export packs: **Markdown / PDF / JSON claims + evidence manifest + evidence folder**
- **Multi-agent intel team**
  - Collector, Extractor, Normalizer, Resolver, Analyst, Skeptic, Counsel, Narrator, Supervisor
  - Supervisor enforces budgets + rules; Skeptic hunts contradictions

---

## Design Principles (Non-Negotiable)

1. **No claim without `evidence_refs`.**
2. **Artifacts are append-only** (never overwrite evidence; create new runs).
3. **Reproducible runs**: re-run from evidence set `v12` and reproduce claims.
4. **Clear epistemics**: separate **facts**, **inferences**, **hypotheses**, **unknowns**.
5. **Threat-modeled parsing**: untrusted PDFs/HTML handled in sandbox; UI uses sanitized renders.

---

## High-Level Architecture

Pipeline:
**Collect → Snapshot → Extract → Normalize → Resolve → Graph-Link → Analyze → Skeptic → Narrative → Diff/Alert → Export**

Storage:
- **Postgres**: structured records, claims, run metadata
- **pgvector**: semantic retrieval over documents/notes
- **Graph (Neo4j or Postgres + Apache AGE)**: relationship networks & temporal queries
- **Evidence Vault (filesystem)**: raw artifacts + manifests + hashes

---
