#!/usr/bin/env python3
"""
Example usage of Obsidian Watchtower.

This script demonstrates the core functionality of the system.
"""

from watchtower.storage import EvidenceStore, ArtifactStore
from watchtower.storage.claim_store import ClaimStore
from watchtower.export import MarkdownExporter, JSONExporter
from watchtower.plugins import PluginRegistry
from watchtower.plugins.manual_entry import ManualEntryPlugin
from watchtower.utils import compute_run_diff, AlertGenerator


def main() -> None:
    """Run example investigation workflow."""
    print("=== Obsidian Watchtower Demo ===\n")
    
    # Initialize stores
    print("1. Initializing stores...")
    evidence_store = EvidenceStore()
    claim_store = ClaimStore(evidence_store)
    artifact_store = ArtifactStore()
    
    # Store evidence
    print("\n2. Storing evidence...")
    evidence1 = evidence_store.store_evidence(
        content="Bank statement showing transfer of $500,000 to offshore account",
        source="manual",
        metadata={"document_type": "bank_statement", "date": "2024-01-15"},
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    print(f"   - Evidence 1 ID: {evidence1.id}")
    print(f"   - SHA-256: {evidence1.sha256[:16]}...")
    
    evidence2 = evidence_store.store_evidence(
        content="Corporate registration documents showing shell company structure",
        source="manual",
        metadata={"document_type": "corporate_filing", "date": "2024-02-01"},
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    print(f"   - Evidence 2 ID: {evidence2.id}")
    print(f"   - SHA-256: {evidence2.sha256[:16]}...")
    
    evidence3 = evidence_store.store_evidence(
        content="Email correspondence discussing 'special arrangement' with vendor",
        source="manual",
        metadata={"document_type": "email", "date": "2024-03-10"},
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    print(f"   - Evidence 3 ID: {evidence3.id}")
    print(f"   - SHA-256: {evidence3.sha256[:16]}...")
    
    # Create claims
    print("\n3. Creating claims...")
    claim1 = claim_store.store_claim(
        statement="Company X engaged in money laundering through offshore accounts",
        confidence=0.85,
        supporting_evidence_ids=[evidence1.id, evidence2.id],  # type: ignore
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    print(f"   - Claim 1 ID: {claim1.id}")
    print(f"   - Confidence: {claim1.confidence}")
    print(f"   - Run Fingerprint: {claim1.run_fingerprint[:16]}...")
    
    claim2 = claim_store.store_claim(
        statement="Vendor received kickbacks for inflated invoices",
        confidence=0.72,
        supporting_evidence_ids=[evidence3.id],  # type: ignore
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    print(f"   - Claim 2 ID: {claim2.id}")
    print(f"   - Confidence: {claim2.confidence}")
    
    # Generate alerts
    print("\n4. Generating alerts...")
    alert_gen = AlertGenerator()
    alerts = alert_gen.generate_alerts([claim1, claim2])
    print(f"   - Total alerts: {len(alerts)}")
    for alert in alerts:
        print(f"   - {alert.severity.upper()}: {alert.message[:80]}...")
    
    # Export case file
    print("\n5. Exporting case files...")
    
    # Markdown export
    md_exporter = MarkdownExporter()
    markdown = md_exporter.export_case(
        claims=[claim1, claim2],
        evidence=[evidence1, evidence2, evidence3],
        title="Investigation: Company X Financial Fraud",
        metadata={
            "case_id": "2024-001",
            "investigator": "Jane Doe",
            "status": "active"
        }
    )
    print("   - Markdown export complete")
    print(f"   - Length: {len(markdown)} characters")
    
    # JSON export
    json_exporter = JSONExporter()
    json_data = json_exporter.export_case(
        claims=[claim1, claim2],
        evidence=[evidence1, evidence2, evidence3],
        title="Investigation: Company X Financial Fraud",
        metadata={"case_id": "2024-001"}
    )
    print("   - JSON export complete")
    print(f"   - Length: {len(json_data)} characters")
    
    # Store artifacts
    print("\n6. Storing artifacts...")
    artifact = artifact_store.store_artifact(
        artifact_type="report",
        content=json_data,
        metadata={"format": "json", "case_id": "2024-001"},
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    print(f"   - Artifact ID: {artifact.id}")
    print(f"   - Type: {artifact.artifact_type}")
    print(f"   - SHA-256: {artifact.sha256[:16]}...")
    
    # Demonstrate plugin system
    print("\n7. Using plugin system...")
    registry = PluginRegistry()
    plugin = ManualEntryPlugin()
    registry.register(plugin)
    print(f"   - Registered plugin: {plugin.name} v{plugin.version}")
    
    # Simulate run comparison
    print("\n8. Computing run diffs...")
    # Create modified claim for comparison
    claim1_modified = claim_store.store_claim(
        statement="Company X engaged in money laundering through offshore accounts",
        confidence=0.92,  # Increased confidence
        supporting_evidence_ids=[evidence1.id, evidence2.id, evidence3.id],  # type: ignore
        tool_name="watchtower",
        tool_version="0.1.0"
    )
    
    diff = compute_run_diff([claim1, claim2], [claim1_modified, claim2])
    print(f"   - Total changes: {diff['total_changes']}")
    print(f"   - Modified claims: {len(diff['modified_claims'])}")
    if diff['modified_claims']:
        print(f"   - Confidence delta: {diff['modified_claims'][0]['confidence_delta']:.2f}")
    
    # Summary
    print("\n9. Summary:")
    print(f"   - Total Evidence: {evidence_store.count_evidence()}")
    print(f"   - Total Claims: {claim_store.count_claims()}")
    print(f"   - Total Artifacts: {artifact_store.count_artifacts()}")
    print(f"   - Total Alerts: {len(alerts)}")
    
    # Save markdown report
    print("\n10. Saving report...")
    with open("/tmp/investigation_report.md", "w") as f:
        f.write(markdown)
    print("   - Report saved to /tmp/investigation_report.md")
    
    # Display sample of markdown
    print("\n=== Sample Report (first 500 chars) ===")
    print(markdown[:500])
    print("...\n")
    
    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()
