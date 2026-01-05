"""Unit tests for export functionality."""

import pytest
from watchtower.models.evidence import Evidence
from watchtower.models.claim import Claim
from watchtower.export.markdown_exporter import MarkdownExporter
from watchtower.export.json_exporter import JSONExporter
from watchtower.export.pdf_exporter import PDFExporter
import json


def test_markdown_export() -> None:
    """Test Markdown export."""
    exporter = MarkdownExporter()
    
    evidence = Evidence(
        id="ev1",
        content="Test evidence content",
        source="manual",
    )
    
    claim = Claim(
        id="claim1",
        statement="Test claim statement",
        confidence=0.85,
        supporting_evidence_ids=["ev1"],
    )
    
    markdown = exporter.export_case(
        claims=[claim],
        evidence=[evidence],
        title="Test Case",
    )
    
    # Check that key elements are present
    assert "# Test Case" in markdown
    assert "Test claim statement" in markdown
    assert "0.85" in markdown or "85" in markdown
    assert "ev1" in markdown
    assert "Test evidence content" in markdown
    assert "SHA-256" in markdown


def test_json_export() -> None:
    """Test JSON export."""
    exporter = JSONExporter()
    
    evidence = Evidence(
        id="ev1",
        content="Test evidence content",
        source="manual",
    )
    
    claim = Claim(
        id="claim1",
        statement="Test claim statement",
        confidence=0.85,
        supporting_evidence_ids=["ev1"],
    )
    
    json_str = exporter.export_case(
        claims=[claim],
        evidence=[evidence],
        title="Test Case",
    )
    
    # Parse JSON to verify it's valid
    data = json.loads(json_str)
    
    assert data["title"] == "Test Case"
    assert len(data["claims"]) == 1
    assert len(data["evidence"]) == 1
    assert data["claims"][0]["id"] == "claim1"
    assert data["claims"][0]["confidence"] == 0.85
    assert data["evidence"][0]["id"] == "ev1"


def test_json_export_with_metadata() -> None:
    """Test JSON export with metadata."""
    exporter = JSONExporter()
    
    evidence = Evidence(
        id="ev1",
        content="Test",
        source="manual",
    )
    
    claim = Claim(
        id="claim1",
        statement="Test",
        confidence=0.5,
        supporting_evidence_ids=["ev1"],
    )
    
    json_str = exporter.export_case(
        claims=[claim],
        evidence=[evidence],
        title="Test",
        metadata={"case_id": "123", "investigator": "John Doe"},
    )
    
    data = json.loads(json_str)
    assert data["metadata"]["case_id"] == "123"
    assert data["metadata"]["investigator"] == "John Doe"


def test_pdf_export() -> None:
    """Test PDF export."""
    exporter = PDFExporter()
    
    evidence = Evidence(
        id="ev1",
        content="Test evidence content",
        source="manual",
    )
    
    claim = Claim(
        id="claim1",
        statement="Test claim statement",
        confidence=0.85,
        supporting_evidence_ids=["ev1"],
    )
    
    pdf_bytes = exporter.export_case(
        claims=[claim],
        evidence=[evidence],
        title="Test Case",
    )
    
    # Check that we got bytes back
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
