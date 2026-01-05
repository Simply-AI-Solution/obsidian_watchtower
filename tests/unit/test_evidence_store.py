"""Unit tests for EvidenceStore."""

import pytest
from datetime import datetime, timedelta
from watchtower.storage.evidence_store import EvidenceStore


def test_store_evidence() -> None:
    """Test storing evidence."""
    store = EvidenceStore()
    
    evidence = store.store_evidence(
        content="Test evidence",
        source="manual",
        metadata={"key": "value"},
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    assert evidence.id is not None
    assert evidence.content == "Test evidence"
    assert evidence.source == "manual"
    assert store.count_evidence() == 1


def test_get_evidence() -> None:
    """Test retrieving evidence."""
    store = EvidenceStore()
    
    evidence = store.store_evidence(
        content="Test content",
        source="manual",
    )
    
    retrieved = store.get_evidence(evidence.id)  # type: ignore
    assert retrieved is not None
    assert retrieved.id == evidence.id
    assert retrieved.content == evidence.content


def test_get_nonexistent_evidence() -> None:
    """Test retrieving non-existent evidence."""
    store = EvidenceStore()
    
    result = store.get_evidence("nonexistent_id")
    assert result is None


def test_list_evidence() -> None:
    """Test listing all evidence."""
    store = EvidenceStore()
    
    # Store multiple evidence items
    for i in range(3):
        store.store_evidence(
            content=f"Evidence {i}",
            source="manual",
        )
    
    evidence_list = store.list_evidence()
    assert len(evidence_list) == 3


def test_list_evidence_with_source_filter() -> None:
    """Test listing evidence with source filter."""
    store = EvidenceStore()
    
    store.store_evidence(content="Manual 1", source="manual")
    store.store_evidence(content="API 1", source="api")
    store.store_evidence(content="Manual 2", source="manual")
    
    manual_evidence = store.list_evidence(source="manual")
    assert len(manual_evidence) == 2
    
    api_evidence = store.list_evidence(source="api")
    assert len(api_evidence) == 1


def test_list_evidence_with_limit() -> None:
    """Test listing evidence with limit."""
    store = EvidenceStore()
    
    for i in range(5):
        store.store_evidence(
            content=f"Evidence {i}",
            source="manual",
        )
    
    limited = store.list_evidence(limit=3)
    assert len(limited) == 3


def test_verify_evidence() -> None:
    """Test evidence verification."""
    store = EvidenceStore()
    
    evidence = store.store_evidence(
        content="Test content",
        source="manual",
    )
    
    # Should verify successfully
    assert store.verify_evidence(evidence.id) is True  # type: ignore
    
    # Non-existent evidence should not verify
    assert store.verify_evidence("nonexistent") is False


def test_append_only_behavior() -> None:
    """Test that evidence store is append-only."""
    store = EvidenceStore()
    
    evidence1 = store.store_evidence(content="First", source="manual")
    evidence2 = store.store_evidence(content="Second", source="manual")
    
    # Both should be stored
    assert store.count_evidence() == 2
    assert store.get_evidence(evidence1.id) is not None  # type: ignore
    assert store.get_evidence(evidence2.id) is not None  # type: ignore
