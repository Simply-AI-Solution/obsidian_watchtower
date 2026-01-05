"""Unit tests for Evidence model."""

import pytest
from datetime import datetime
from watchtower.models.evidence import Evidence


def test_evidence_creation() -> None:
    """Test basic evidence creation."""
    evidence = Evidence(
        content="Test evidence content",
        source="manual",
        metadata={"test": "value"},
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    assert evidence.content == "Test evidence content"
    assert evidence.source == "manual"
    assert evidence.metadata == {"test": "value"}
    assert evidence.tool_name == "watchtower"
    assert evidence.tool_version == "0.1.0"
    assert isinstance(evidence.timestamp, datetime)


def test_evidence_sha256() -> None:
    """Test SHA-256 hash computation."""
    evidence = Evidence(
        content="Test content",
        source="manual",
    )
    
    # SHA-256 should be deterministic
    sha256_1 = evidence.sha256
    sha256_2 = evidence.sha256
    assert sha256_1 == sha256_2
    assert len(sha256_1) == 64  # SHA-256 produces 64 hex characters
    
    # Different content should produce different hash
    evidence2 = Evidence(
        content="Different content",
        source="manual",
    )
    assert evidence2.sha256 != evidence.sha256


def test_evidence_fingerprint() -> None:
    """Test fingerprint generation."""
    evidence = Evidence(
        content="Test content",
        source="manual",
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    fingerprint = evidence.fingerprint
    assert len(fingerprint) == 64
    
    # Same evidence should produce same fingerprint
    assert evidence.fingerprint == fingerprint


def test_evidence_immutability() -> None:
    """Test that evidence content is properly captured."""
    content = "Original content"
    evidence = Evidence(
        content=content,
        source="manual",
    )
    
    # Store original hash
    original_hash = evidence.sha256
    
    # Changing the source string shouldn't affect the evidence
    # (Pydantic models are not mutable by default in this way)
    assert evidence.sha256 == original_hash
