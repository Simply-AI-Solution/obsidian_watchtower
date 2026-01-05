"""Unit tests for Artifact model."""

import pytest
from datetime import datetime
from watchtower.models.artifact import Artifact


def test_artifact_creation() -> None:
    """Test basic artifact creation."""
    artifact = Artifact(
        artifact_type="evidence",
        content='{"data": "test"}',
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    assert artifact.artifact_type == "evidence"
    assert artifact.content == '{"data": "test"}'
    assert artifact.parent_artifact_id is None
    assert isinstance(artifact.timestamp, datetime)


def test_artifact_with_parent() -> None:
    """Test artifact with parent for versioning."""
    artifact = Artifact(
        artifact_type="derived",
        content='{"result": "processed"}',
        parent_artifact_id="parent_123",
    )
    
    assert artifact.parent_artifact_id == "parent_123"


def test_artifact_types() -> None:
    """Test different artifact types."""
    types = ["evidence", "claim", "derived", "report"]
    
    for artifact_type in types:
        artifact = Artifact(
            artifact_type=artifact_type,  # type: ignore
            content="test",
        )
        assert artifact.artifact_type == artifact_type


def test_artifact_sha256() -> None:
    """Test SHA-256 hash computation."""
    artifact = Artifact(
        artifact_type="evidence",
        content="Test content",
    )
    
    sha256 = artifact.sha256
    assert len(sha256) == 64
    
    # Same content should produce same hash
    assert artifact.sha256 == sha256


def test_artifact_fingerprint() -> None:
    """Test fingerprint generation."""
    artifact = Artifact(
        artifact_type="claim",
        content="Test content",
        tool_name="watchtower",
        tool_version="0.1.0",
    )
    
    fingerprint = artifact.fingerprint
    assert len(fingerprint) == 64
    
    # Fingerprint should be consistent
    assert artifact.fingerprint == fingerprint


def test_artifact_fingerprint_includes_parent() -> None:
    """Test that fingerprint includes parent information."""
    artifact1 = Artifact(
        artifact_type="derived",
        content="Same content",
        parent_artifact_id=None,
    )
    
    artifact2 = Artifact(
        artifact_type="derived",
        content="Same content",
        parent_artifact_id="parent_123",
    )
    
    # Different parents should produce different fingerprints
    assert artifact1.fingerprint != artifact2.fingerprint
