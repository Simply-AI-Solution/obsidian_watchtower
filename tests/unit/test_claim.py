"""Unit tests for Claim model."""

import pytest
from datetime import datetime
from watchtower.models.claim import Claim


def test_claim_creation() -> None:
    """Test basic claim creation."""
    claim = Claim(
        statement="Test claim",
        confidence=0.85,
        supporting_evidence_ids=["evidence_1", "evidence_2"],
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    assert claim.statement == "Test claim"
    assert claim.confidence == 0.85
    assert claim.supporting_evidence_ids == ["evidence_1", "evidence_2"]
    assert claim.counter_evidence_ids == []
    assert isinstance(claim.timestamp, datetime)


def test_claim_requires_evidence() -> None:
    """Test that claims require at least one evidence reference."""
    with pytest.raises(ValueError, match="No claim without evidence_ref"):
        Claim(
            statement="Claim without evidence",
            confidence=0.5,
            supporting_evidence_ids=[],
            counter_evidence_ids=[],
        )


def test_claim_with_counter_evidence() -> None:
    """Test claim with counter evidence."""
    claim = Claim(
        statement="Test claim",
        confidence=0.6,
        supporting_evidence_ids=["evidence_1"],
        counter_evidence_ids=["evidence_2"],
    )
    
    assert len(claim.supporting_evidence_ids) == 1
    assert len(claim.counter_evidence_ids) == 1
    assert len(claim.evidence_refs) == 2


def test_claim_confidence_range() -> None:
    """Test that confidence must be between 0 and 1."""
    # Valid confidence
    claim = Claim(
        statement="Test",
        confidence=0.5,
        supporting_evidence_ids=["ev1"],
    )
    assert claim.confidence == 0.5
    
    # Invalid confidence (too high)
    with pytest.raises(ValueError):
        Claim(
            statement="Test",
            confidence=1.5,
            supporting_evidence_ids=["ev1"],
        )
    
    # Invalid confidence (negative)
    with pytest.raises(ValueError):
        Claim(
            statement="Test",
            confidence=-0.1,
            supporting_evidence_ids=["ev1"],
        )


def test_claim_run_fingerprint() -> None:
    """Test run fingerprint generation."""
    claim = Claim(
        statement="Test claim",
        confidence=0.85,
        supporting_evidence_ids=["evidence_1"],
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    fingerprint = claim.run_fingerprint
    assert len(fingerprint) == 64
    
    # Same claim should produce same fingerprint
    assert claim.run_fingerprint == fingerprint


def test_claim_evidence_refs_property() -> None:
    """Test that evidence_refs property combines all evidence."""
    claim = Claim(
        statement="Test",
        confidence=0.7,
        supporting_evidence_ids=["ev1", "ev2"],
        counter_evidence_ids=["ev3"],
    )
    
    assert claim.evidence_refs == ["ev1", "ev2", "ev3"]
