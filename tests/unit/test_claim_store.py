"""Unit tests for ClaimStore."""

import pytest
from watchtower.storage.evidence_store import EvidenceStore
from watchtower.storage.claim_store import ClaimStore


def test_store_claim() -> None:
    """Test storing a claim."""
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    
    # First create evidence
    evidence = evidence_store.store_evidence(
        content="Test evidence",
        source="manual",
    )
    
    # Then create claim
    claim = claim_store.store_claim(
        statement="Test claim",
        confidence=0.85,
        supporting_evidence_ids=[evidence.id],  # type: ignore
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    assert claim.id is not None
    assert claim.statement == "Test claim"
    assert claim.confidence == 0.85
    assert claim_store.count_claims() == 1


def test_claim_requires_valid_evidence() -> None:
    """Test that claims require valid evidence references."""
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    
    # Try to create claim with non-existent evidence
    with pytest.raises(ValueError, match="Evidence not found"):
        claim_store.store_claim(
            statement="Invalid claim",
            confidence=0.5,
            supporting_evidence_ids=["nonexistent_id"],
        )


def test_get_claim() -> None:
    """Test retrieving a claim."""
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    
    evidence = evidence_store.store_evidence(content="Test", source="manual")
    claim = claim_store.store_claim(
        statement="Test claim",
        confidence=0.7,
        supporting_evidence_ids=[evidence.id],  # type: ignore
    )
    
    retrieved = claim_store.get_claim(claim.id)  # type: ignore
    assert retrieved is not None
    assert retrieved.id == claim.id
    assert retrieved.statement == claim.statement


def test_list_claims_with_confidence_filter() -> None:
    """Test listing claims with minimum confidence filter."""
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    
    evidence = evidence_store.store_evidence(content="Test", source="manual")
    
    claim_store.store_claim(
        statement="Low confidence",
        confidence=0.3,
        supporting_evidence_ids=[evidence.id],  # type: ignore
    )
    claim_store.store_claim(
        statement="High confidence",
        confidence=0.9,
        supporting_evidence_ids=[evidence.id],  # type: ignore
    )
    
    high_conf_claims = claim_store.list_claims(min_confidence=0.8)
    assert len(high_conf_claims) == 1
    assert high_conf_claims[0].confidence == 0.9


def test_get_claims_by_evidence() -> None:
    """Test getting claims that reference specific evidence."""
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    
    evidence1 = evidence_store.store_evidence(content="Evidence 1", source="manual")
    evidence2 = evidence_store.store_evidence(content="Evidence 2", source="manual")
    
    claim1 = claim_store.store_claim(
        statement="Claim 1",
        confidence=0.7,
        supporting_evidence_ids=[evidence1.id],  # type: ignore
    )
    claim2 = claim_store.store_claim(
        statement="Claim 2",
        confidence=0.8,
        supporting_evidence_ids=[evidence1.id, evidence2.id],  # type: ignore
    )
    
    # Get claims referencing evidence1
    claims_for_ev1 = claim_store.get_claims_by_evidence(evidence1.id)  # type: ignore
    assert len(claims_for_ev1) == 2
    
    # Get claims referencing evidence2
    claims_for_ev2 = claim_store.get_claims_by_evidence(evidence2.id)  # type: ignore
    assert len(claims_for_ev2) == 1


def test_claim_with_counter_evidence() -> None:
    """Test storing claim with counter evidence."""
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    
    supporting = evidence_store.store_evidence(content="Supporting", source="manual")
    counter = evidence_store.store_evidence(content="Counter", source="manual")
    
    claim = claim_store.store_claim(
        statement="Contested claim",
        confidence=0.6,
        supporting_evidence_ids=[supporting.id],  # type: ignore
        counter_evidence_ids=[counter.id],  # type: ignore
    )
    
    assert len(claim.supporting_evidence_ids) == 1
    assert len(claim.counter_evidence_ids) == 1
