"""JSON export functionality."""

from typing import List, Optional, Dict, Any
from watchtower.models.claim import Claim
from watchtower.models.evidence import Evidence
from datetime import datetime
import json


class JSONExporter:
    """
    Export case files to JSON format.
    
    Generates machine-readable case files with full claim and evidence data.
    """
    
    def __init__(self) -> None:
        """Initialize the JSON exporter."""
        pass
    
    def export_case(
        self,
        claims: List[Claim],
        evidence: List[Evidence],
        title: str = "Case File",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Export a case file to JSON.
        
        Args:
            claims: List of claims to include
            evidence: List of evidence to include
            title: Case file title
            metadata: Additional metadata
            
        Returns:
            JSON-formatted case file
        """
        case_data = {
            "title": title,
            "generated_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "summary": {
                "total_claims": len(claims),
                "total_evidence": len(evidence),
            },
            "claims": [
                {
                    "id": claim.id,
                    "statement": claim.statement,
                    "confidence": claim.confidence,
                    "supporting_evidence_ids": claim.supporting_evidence_ids,
                    "counter_evidence_ids": claim.counter_evidence_ids,
                    "run_fingerprint": claim.run_fingerprint,
                    "metadata": claim.metadata,
                    "tool": {
                        "name": claim.tool_name,
                        "version": claim.tool_version,
                    } if claim.tool_name else None,
                    "model": {
                        "name": claim.model_name,
                        "version": claim.model_version,
                    } if claim.model_name else None,
                    "timestamp": claim.timestamp.isoformat(),
                }
                for claim in claims
            ],
            "evidence": [
                {
                    "id": ev.id,
                    "content": ev.content,
                    "source": ev.source,
                    "sha256": ev.sha256,
                    "fingerprint": ev.fingerprint,
                    "metadata": ev.metadata,
                    "tool": {
                        "name": ev.tool_name,
                        "version": ev.tool_version,
                    } if ev.tool_name else None,
                    "model": {
                        "name": ev.model_name,
                        "version": ev.model_version,
                    } if ev.model_name else None,
                    "timestamp": ev.timestamp.isoformat(),
                }
                for ev in evidence
            ],
        }
        
        return json.dumps(case_data, indent=2)
