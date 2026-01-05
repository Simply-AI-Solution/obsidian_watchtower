# Architecture and Design Decisions

## Overview

Obsidian Watchtower is designed as a local-first fraud/corruption investigation system that prioritizes data integrity, provenance tracking, and reproducibility. This document explains the key architectural decisions and design patterns used in the system.

## Core Design Principles

### 1. No Claim Without Evidence

**Principle**: Every claim must be backed by at least one piece of evidence.

**Implementation**: The `Claim` model enforces this rule in `model_post_init()`:

```python
def model_post_init(self, __context: Any) -> None:
    total_evidence = len(self.supporting_evidence_ids) + len(self.counter_evidence_ids)
    if total_evidence == 0:
        raise ValueError("No claim without evidence_ref: Claims must have at least one...")
```

**Rationale**: This ensures all investigations are evidence-based and prevents speculation or unfounded accusations from entering the system.

### 2. Append-Only Architecture

**Principle**: Once stored, evidence and artifacts cannot be modified or deleted.

**Implementation**: 
- `EvidenceStore` and `ArtifactStore` only provide `store_*` methods, not update or delete
- All items receive SHA-256 hashes computed from content
- Timestamps are recorded at creation

**Rationale**: 
- Maintains audit trail
- Prevents evidence tampering
- Supports forensic analysis
- Enables time-machine diffs

### 3. Cryptographic Fingerprints

**Principle**: All data has reproducible cryptographic fingerprints for integrity verification.

**Implementation**:
- Evidence: SHA-256 hash of content + fingerprint including tool/model versions
- Claims: Run fingerprint including statement hash, evidence IDs, confidence, and tool versions
- Artifacts: SHA-256 hash + fingerprint with lineage information

**Rationale**:
- Enables integrity verification
- Supports reproducibility
- Facilitates deduplication
- Provides tamper evidence

### 4. Tool and Model Version Tracking

**Principle**: Record what tools and models created each piece of data.

**Implementation**: All models include optional fields:
- `tool_name`: Name of the tool (e.g., "watchtower")
- `tool_version`: Semantic version (e.g., "0.1.0")
- `model_name`: AI model if applicable (e.g., "gpt-4")
- `model_version`: Model version

**Rationale**:
- Essential for reproducibility
- Helps understand how conclusions were reached
- Enables comparison across tool versions
- Critical for scientific rigor

## Data Models

### Evidence

The foundation of the system. Evidence is immutable and cryptographically verified.

**Key Features**:
- Computed SHA-256 hash using Pydantic's `@computed_field`
- Automatic timestamp on creation
- Metadata support for flexible extensibility
- Reproducible fingerprint

### Claim

Assertions backed by evidence with confidence scoring.

**Key Features**:
- Confidence range validation (0-1)
- Separate supporting and counter-evidence lists
- Validation ensures at least one evidence reference
- Run fingerprint for reproducibility

### Artifact

Generic container for any snapshot with versioning support.

**Key Features**:
- Type system: evidence, claim, derived, report
- Parent-child relationships via `parent_artifact_id`
- Lineage tracking
- SHA-256 and fingerprint

## Storage Layer

### In-Memory Stores

Current implementation uses in-memory dictionaries for simplicity and testing.

**Benefits**:
- Fast for development and testing
- No external dependencies
- Easy to understand

**Limitations**:
- Data lost on restart
- No scaling beyond single machine
- No concurrent access

### PostgreSQL Integration

`PostgresStore` provides persistent storage with schema definition.

**Features**:
- pgvector extension for similarity search
- JSONB for flexible metadata
- Indexes for performance
- Foreign key relationships for referential integrity

**Design Decision**: Schema uses VARCHAR(36) for UUIDs instead of native UUID type for broader compatibility.

## Plugin System

### Architecture

**Pattern**: Registry pattern with abstract base class

**Components**:
1. `SourcePlugin`: Abstract base defining interface
2. `PluginRegistry`: Centralized plugin management
3. Concrete implementations (e.g., `ManualEntryPlugin`)

**Design Decisions**:
- Plugins are stateless (initialized per extraction)
- Configuration validation is optional but recommended
- Extract method returns list for batch support
- Registry prevents duplicate names

### Extensibility

New plugins can be created by:
1. Extending `SourcePlugin`
2. Implementing required abstract methods
3. Registering with `PluginRegistry`

Example sources:
- API clients (REST, GraphQL)
- Web scrapers
- Database connectors
- File parsers (PDF, CSV, JSON)
- Email extractors

## Export System

### Design Pattern

**Strategy Pattern**: Different exporters implement common interface

**Exporters**:
1. `MarkdownExporter`: Human-readable case files
2. `JSONExporter`: Machine-readable structured data
3. `PDFExporter`: Audit-ready documents

**Key Features**:
- All include claim IDs for traceability
- Evidence appendix with full provenance
- Metadata support
- Consistent structure across formats

## Utility Functions

### Diff Computation

**Purpose**: Compare runs to track changes over time

**Implementation**:
- `compute_run_diff()`: Compares sets of claims
- `compute_artifact_diff()`: Compares individual artifacts
- Tracks additions, removals, and modifications

**Use Cases**:
- Monitor investigation progress
- Identify changing conclusions
- Track confidence evolution
- Generate change reports

### Alert Generation

**Purpose**: Notify investigators of significant events

**Alert Types**:
- High-confidence claims
- Well-supported claims (≥5 evidence items)
- Confidence drops
- Confidence increases

**Design**:
- Configurable thresholds
- Severity levels (low, medium, high, critical)
- Structured alert objects
- Summary generation

## Type Safety

**Principle**: Use Python type hints throughout for IDE support and static analysis

**Implementation**:
- All functions have return type annotations
- All parameters have type annotations
- Pydantic models provide runtime validation
- mypy compatible

**Benefits**:
- Catches errors before runtime
- Better IDE autocomplete
- Self-documenting code
- Easier refactoring

## Testing Strategy

### Unit Tests

**Coverage**:
- All data models
- All storage implementations
- All utility functions
- Plugin system
- Export functionality

**Pattern**: Each module has corresponding test file

**Tools**: pytest with assertions

### Test Organization

```
tests/
├── unit/           # Fast, isolated tests
│   ├── test_evidence.py
│   ├── test_claim.py
│   └── ...
└── integration/    # Cross-component tests
```

## Future Enhancements

### Graph Database Integration

**Options**: Neo4j or Apache AGE (PostgreSQL extension)

**Use Cases**:
- Network analysis
- Connection discovery
- Shortest path queries
- Community detection

**Design**: Graph layer would sit alongside relational storage, with edges representing relationships between entities.

### Vector Similarity Search

**Implementation**: pgvector already in schema

**Use Cases**:
- Find similar evidence
- Cluster related claims
- Semantic search
- Anomaly detection

**Approach**: Generate embeddings via API (OpenAI, local models) and store in vector column.

### Multi-Agent Pipeline

**Architecture**: Orchestration layer coordinating specialized agents

**Agents**:
- Evidence extraction agents
- Analysis agents
- Verification agents
- Report generation agents

**Communication**: Message passing via queue system (RabbitMQ, Redis)

## Security Considerations

### Data Integrity

- SHA-256 hashes prevent tampering
- Append-only prevents deletion
- Fingerprints enable verification

### Access Control

**Not Yet Implemented**: Future versions should include:
- User authentication
- Role-based access control
- Audit logging
- Encryption at rest

### Input Validation

- Pydantic provides validation
- Evidence references checked before claim creation
- Plugin config validation

## Performance Considerations

### Current Implementation

- In-memory stores: O(1) access, O(n) list operations
- No caching
- Single-threaded

### Optimization Opportunities

1. **Database Indexes**: Already defined in PostgreSQL schema
2. **Caching**: Add LRU cache for frequently accessed items
3. **Batch Operations**: Support bulk inserts
4. **Pagination**: Add cursor-based pagination
5. **Lazy Loading**: Load evidence only when needed

## Deployment Considerations

### Dependencies

Minimal core dependencies:
- pydantic: Data validation
- Python standard library

Optional dependencies:
- psycopg2-binary: PostgreSQL
- pgvector: Vector search
- reportlab: PDF export
- markdown: Markdown processing

### Environment Variables

**Recommended**:
```
WATCHTOWER_DB_URL=postgresql://user:pass@host/db
WATCHTOWER_LOG_LEVEL=INFO
WATCHTOWER_STORAGE_BACKEND=postgres|memory
```

### Docker Deployment

**Future**: Create Dockerfile with:
- Python 3.9+
- PostgreSQL client libraries
- Application code
- Health checks

## Contributing Guidelines

### Code Style

- Black formatting (100 char line length)
- Ruff linting
- Type hints required
- Docstrings for public APIs

### Testing

- All new features require tests
- Maintain >80% coverage
- Tests must pass before merge

### Documentation

- Update README for user-facing changes
- Update ARCHITECTURE.md for design changes
- Add docstrings for new APIs

## Conclusion

Obsidian Watchtower is designed to be a robust, extensible platform for fraud and corruption investigation. The architecture prioritizes data integrity, reproducibility, and auditability while remaining simple enough for rapid development and deployment.

Key strengths:
- **Integrity**: Cryptographic verification throughout
- **Traceability**: Complete provenance tracking
- **Extensibility**: Plugin system for data sources
- **Flexibility**: Multiple export formats
- **Testability**: Comprehensive test coverage

Future development will focus on scaling, advanced analytics (graph + vector search), and multi-agent orchestration while maintaining these core strengths.
