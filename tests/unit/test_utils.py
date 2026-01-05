"""Unit tests for diff and alert utilities."""

import pytest
from watchtower.models.claim import Claim
from watchtower.models.artifact import Artifact
from watchtower.utils.diff import compute_run_diff, compute_artifact_diff
from watchtower.utils.alerts import AlertGenerator


def test_compute_run_diff_added_claims() -> None:
    """Test computing diff with added claims."""
    claims_a = [
        Claim(id="c1", statement="Claim 1", confidence=0.8, supporting_evidence_ids=["e1"]),
    ]
    claims_b = [
        Claim(id="c1", statement="Claim 1", confidence=0.8, supporting_evidence_ids=["e1"]),
        Claim(id="c2", statement="Claim 2", confidence=0.7, supporting_evidence_ids=["e2"]),
    ]
    
    diff = compute_run_diff(claims_a, claims_b)
    
    assert len(diff["added_claims"]) == 1
    assert "c2" in diff["added_claims"]
    assert len(diff["removed_claims"]) == 0
    # Note: high confidence claim also triggers an alert
    assert diff["total_changes"] >= 1


def test_compute_run_diff_removed_claims() -> None:
    """Test computing diff with removed claims."""
    claims_a = [
        Claim(id="c1", statement="Claim 1", confidence=0.8, supporting_evidence_ids=["e1"]),
        Claim(id="c2", statement="Claim 2", confidence=0.7, supporting_evidence_ids=["e2"]),
    ]
    claims_b = [
        Claim(id="c1", statement="Claim 1", confidence=0.8, supporting_evidence_ids=["e1"]),
    ]
    
    diff = compute_run_diff(claims_a, claims_b)
    
    assert len(diff["added_claims"]) == 0
    assert len(diff["removed_claims"]) == 1
    assert "c2" in diff["removed_claims"]


def test_compute_run_diff_modified_claims() -> None:
    """Test computing diff with modified claims."""
    claims_a = [
        Claim(id="c1", statement="Original", confidence=0.5, supporting_evidence_ids=["e1"]),
    ]
    claims_b = [
        Claim(id="c1", statement="Modified", confidence=0.8, supporting_evidence_ids=["e1"]),
    ]
    
    diff = compute_run_diff(claims_a, claims_b)
    
    assert len(diff["modified_claims"]) == 1
    modified = diff["modified_claims"][0]
    assert modified["id"] == "c1"
    assert modified["statement_changed"] is True
    assert modified["confidence_changed"] is True
    assert abs(modified["confidence_delta"] - 0.3) < 0.001  # Floating point comparison


def test_compute_artifact_diff() -> None:
    """Test computing diff between artifacts."""
    artifact_a = Artifact(
        id="a1",
        artifact_type="evidence",
        content="Same content",
    )
    artifact_b = Artifact(
        id="a1",
        artifact_type="evidence",
        content="Different content",
    )
    
    diff = compute_artifact_diff(artifact_a, artifact_b)
    
    assert diff["id_match"] is True
    assert diff["type_match"] is True
    assert diff["content_match"] is False
    assert diff["sha256_match"] is False


def test_alert_generator_high_confidence() -> None:
    """Test alert generation for high-confidence claims."""
    generator = AlertGenerator(confidence_high_threshold=0.9)
    
    claims = [
        Claim(id="c1", statement="High confidence claim", confidence=0.95, supporting_evidence_ids=["e1"]),
        Claim(id="c2", statement="Low confidence claim", confidence=0.5, supporting_evidence_ids=["e2"]),
    ]
    
    alerts = generator.generate_alerts(claims)
    
    # Should have one high-confidence alert
    high_conf_alerts = [a for a in alerts if a.alert_type == "high_confidence_claim"]
    assert len(high_conf_alerts) == 1
    assert high_conf_alerts[0].severity == "high"


def test_alert_generator_well_supported_claim() -> None:
    """Test alert generation for well-supported claims."""
    generator = AlertGenerator()
    
    claims = [
        Claim(
            id="c1",
            statement="Well supported",
            confidence=0.8,
            supporting_evidence_ids=["e1", "e2", "e3", "e4", "e5"],
        ),
    ]
    
    alerts = generator.generate_alerts(claims)
    
    well_supported = [a for a in alerts if a.alert_type == "well_supported_claim"]
    assert len(well_supported) == 1


def test_alert_generator_confidence_changes() -> None:
    """Test alert generation for confidence changes."""
    generator = AlertGenerator(confidence_drop_threshold=0.2)
    
    previous_claims = [
        Claim(id="c1", statement="Claim 1", confidence=0.9, supporting_evidence_ids=["e1"]),
    ]
    current_claims = [
        Claim(id="c1", statement="Claim 1", confidence=0.6, supporting_evidence_ids=["e1"]),
    ]
    
    alerts = generator.generate_alerts(current_claims, previous_claims)
    
    # Should have confidence drop alert
    drop_alerts = [a for a in alerts if a.alert_type == "confidence_drop"]
    assert len(drop_alerts) == 1
    assert drop_alerts[0].severity == "high"
    assert abs(drop_alerts[0].details["change"] - (-0.3)) < 0.001  # Floating point comparison


def test_alert_summary() -> None:
    """Test alert summary generation."""
    generator = AlertGenerator()
    
    claims = [
        Claim(id="c1", statement="High confidence", confidence=0.95, supporting_evidence_ids=["e1"]),
        Claim(id="c2", statement="Another high", confidence=0.92, supporting_evidence_ids=["e2"]),
    ]
    
    alerts = generator.generate_alerts(claims)
    summary = generator.generate_summary(alerts)
    
    assert summary["total_alerts"] == len(alerts)
    assert "severity_counts" in summary
    assert "type_counts" in summary
    assert "alerts" in summary
