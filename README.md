# Obsidian Watchtower

**Obsidian Watchtower** is a local-first **fraud, corruption, and public-funds intelligence** system that automates evidence collection, network tracing, anomaly detection, and **case-file generation** on user-defined subjects (organizations, companies, individuals, and connected networks).

It’s built to produce **audit-ready intelligence**, not vibes:
- **Provenance-first storage** (every claim links to evidence)
- **Immutable evidence snapshots** (append-only, hashed artifacts)
- **Claim ledger** (structured findings + confidence + supporting/counter evidence)
- **Reproducible runs** (“re-run evidence set v12 → same results”)

> Core rule: **No claim without evidence. No narrative sentence without a claim ID.**

---

## Why This Exists

Public funding and procurement ecosystems are fragmented across portals, PDFs, dashboards, and APIs—exactly the kind of environment where waste, conflicts, and corruption can hide in plain sight. Obsidian Watchtower turns that chaos into a **traceable, queryable, defensible case-building workflow** that:
- accelerates legitimate investigations
- preserves chain-of-custody
- keeps outputs transparent and reviewable

---

## Core Goals

1. **Collect & Preserve Evidence (Chain-of-Custody)**
   - Snapshot raw sources (HTML/PDF/JSON) with SHA-256 hashes
   - Capture retrieval timestamps, parse method/version, and tool/model fingerprints

2. **Normalize & Resolve Entities**
   - Merge aliases and misspellings (DBA names, subsidiaries, address overlaps)
   - Maintain resolution confidence and supporting evidence

3. **Map Networks (“Show me the money”)**
   - Track relationships between recipients, agencies, vendors, contracts, officers, addresses
   - Enable graph queries like:
     - “Recipients within 2 hops of Org X that received funds within 30 days of Contract Y”

4. **Detect Patterns & Risk Signals**
   - Temporal anomalies (spikes, repeats, suspicious proximity to key events)
   - Structural anomalies (award splitting, round-number clustering, address reuse)
   - Cross-source conflicts (contradictory amounts, names, dates)

5. **Produce Case Files**
   - Publication-ready, human-editable narratives with inline citations
   - Exportable evidence packs for auditors, journalists, investigators

---

## Key Outputs

| Output Type | Purpose | Examples |
|------------|---------|----------|
| **Evidence Vault** | Immutable snapshots + manifests | Raw HTML/PDF/JSON, hashes, signed run manifest |
| **Data Catalogs** | Searchable normalized datasets | JSON/CSV of entities, awards, recipients, vendors, links |
| **Claim Ledger** | Structured, auditable findings | `claims.jsonl` with confidence + evidence refs + counter-evidence |
| **Network Graph** | Relationship tracing | Neo4j/AGE graph exports, 2-hop queries, temporal edges |
| **Insight Reports** | Case file narrative | Markdown/PDF with timelines, money flows, anomalies, appendix |
| **Visualizations** | Pattern communication | Plotly dashboards, network maps, time-series charts |
| **Alerts/Notices** | Ongoing monitoring | Watchlists + run-to-run diffs + anomaly triggers |
| **Raw Traces** | Auditability of reasoning | Logs of agent decisions, tool runs, prompt template hashes |

---

## Evidence & Reproducibility (Non-Negotiable)

### Provenance-first storage
Every claim must include:
- Evidence references (artifact IDs) + extraction coordinates when possible (page/line/bbox)
- Source URI, retrieval time, collector fingerprint (UA/delay profile)
- Parse method + version
- Model + prompt template hash
- Transformation lineage (queries + aggregations)

### Immutable snapshots
Artifacts are **append-only**. A new run creates new artifacts; nothing is overwritten.

### Repro runs
Each run records a **repro fingerprint**:
- Git commit hash
- Container image digests
- Dependency lock hash
- Model identity (tag/digest)
- Prompt template hashes
- Case config hash

---

## Graph-Native Investigation Layer

SQL is great for records. Investigations are **networks**.

Obsidian Watchtower adds a **property graph** (Neo4j or Postgres + Apache AGE) for:
- Entity resolution links (alias/DBA/subsidiary)
- Recipient webs and shared infrastructure (address/phone/domain overlaps)
- People/org link analysis (officers, board members, vendor relationships)
- Temporal reasoning (events and “within X days of” patterns)

---

## Time Machine Mode (Diffs + Alerts)

Each run computes diffs against prior runs:
- changed amounts/descriptions/recipients
- newly discovered documents or “silent edits” (same URL, new hash)
- entity resolution changes (merged/split identities)

Watchlists + triggers:
- entities, vendors, agencies, ZIP codes, keywords
- anomaly triggers: spikes, repeats, splitting patterns, address reuse, round-number clusters

---

## Multi-Agent “Intel Team”

Agents are bounded by authority (tools + allowed actions). Typical team:

- **Supervisor**: orchestration + budgets + stop conditions + policy enforcement  
- **Collector**: network retrieval + immutable snapshots (no summarizing)  
- **Extractor**: sandbox parsing (PDF/HTML → structured extractions)  
- **Normalizer**: canonical records (no narrative)  
- **Resolver**: entity resolution + confidence + rationale  
- **Analyst**: aggregates + anomaly detection + clustering  
- **Skeptic**: adversarial review; hunts contradictions; forces confidence downgrades  
- **Counsel**: compliance + phrasing guardrails; scraping etiquette; FOIA-ready logging  
- **Narrator**: builds the case file *only from the claim ledger*  

> The Skeptic agent is mandatory before export.

---

## Evaluation & Quality Gates

### Targets (initial benchmarks)
- **Fact extraction precision/recall**: ≥ 90% on a validated test set
- **Claim evidence completeness**: 100% of claims have evidence refs
- **Contradiction handling**: counter-evidence recorded and confidence adjusted
- **Reproducibility**: rerun from evidence set produces identical claim hashes
- **Utility**: “actionable leads” confirmed by human review

### Hard gates
- Fail export if:
  - any claim lacks evidence refs
  - Skeptic did not run
  - narrative contains sentences not linked to claim IDs

---

## Ethics, Safety, and Language

This system supports investigations into potential fraud/corruption by surfacing **evidence-linked facts**, **anomalies**, and **testable hypotheses**.

It does **not** declare guilt. Reports must clearly label:
- **Fact** (directly evidenced)
- **Inference** (supported but not definitive)
- **Hypothesis** (needs verification)
- **Unknown/Conflicted** (contradictory evidence)

---

## Roadmap

### Phase 1 — Evidence Vault + Claim Ledger MVP
- Immutable snapshots + manifests + hashing
- One source plugin (USASpending API)
- Claim ledger + basic export pack (MD/JSON)

### Phase 2 — Time Machine + Command Center v1
- Run diffs + alerts + watchlists
- Streamlit UI: cases, runs, evidence drawer, claim viewer

### Phase 3 — Graph + Entity Resolution
- Alias/DBA resolution with confidence
- Graph storage + 2-hop + temporal queries
- Graph view in UI

### Phase 4 — Full Case-File Grade Narrative Builder
- Skeptic contradiction engine + confidence downgrades
- Counsel guardrails
- PDF/MD/JSON exports with evidence appendix

---

## References (background reading)
[1] https://generative-ai-newsroom.com/agentic-search-for-investigative-journalism-43faa44ade99  
[2] https://www.linkedin.com/pulse/journalism-ai-automated-investigative-reporting-andre-g9wse  
[3] https://network.aljazeera.net/en/press-releases/al-jazeera-media-network-launches-%E2%80%98-core%E2%80%99-ai-integrated-news-model-built-google  
[4] https://pressgazette.co.uk/platforms/how-ai-could-save-investigative-journalists-time-and-test-their-hunches/  
[5] https://arxiv.org/pdf/2510.01193.pdf  
[6] https://aws.amazon.com/blogs/machine-learning/part-3-building-an-ai-powered-assistant-for-investment-research-with-multi-agent-collaboration-in-amazon-bedrock-and-amazon-bedrock-data-automation/  
[7] https://hai.stanford.edu/news/a-trustworthy-ai-assistant-for-investigative-journalists  
[8] https://www.datagrid.com/blog/ai-agents-report-writing  
[9] https://dev.to/aakas/beyond-the-dashboard-how-i-built-an-ai-agent-to-revolutionize-data-reporting-19kk  
[10] https://www.anthropic.com/engineering/multi-agent-research-system  
[11] https://www.linkedin.com/pulse/agentic-ai-comparative-analysis-langgraph-crewai-hardik-shah-ujdrc  
[12] https://www.tandfonline.com/doi/full/10.1080/17512786.2025.2605212?src=
