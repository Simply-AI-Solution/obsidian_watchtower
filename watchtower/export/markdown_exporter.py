"""Markdown export functionality."""

from typing import List, Optional, Dict, Any
from watchtower.models.claim import Claim
from watchtower.models.evidence import Evidence
from datetime import datetime


class MarkdownExporter:
    """
    Export case files to Markdown format.
    
    Generates audit-ready case files with claim IDs and evidence appendix.
    """
    
    def __init__(self) -> None:
        """Initialize the Markdown exporter."""
        pass
    
    def export_case(
        self,
        claims: List[Claim],
        evidence: List[Evidence],
        title: str = "Case File",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Export a case file to Markdown.
        
        Args:
            claims: List of claims to include
            evidence: List of evidence to include
            title: Case file title
            metadata: Additional metadata
            
        Returns:
            Markdown-formatted case file
        """
        lines = []
        
        # Header
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"**Generated:** {datetime.utcnow().isoformat()}")
        lines.append("")
        
        # Metadata
        if metadata:
            lines.append("## Metadata")
            lines.append("")
            for key, value in metadata.items():
                lines.append(f"- **{key}:** {value}")
            lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total Claims:** {len(claims)}")
        lines.append(f"- **Total Evidence:** {len(evidence)}")
        lines.append("")
        
        # Claims section
        lines.append("## Claims")
        lines.append("")
        
        for i, claim in enumerate(claims, 1):
            lines.append(f"### Claim {i} (ID: `{claim.id}`)")
            lines.append("")
            lines.append(f"**Statement:** {claim.statement}")
            lines.append("")
            lines.append(f"**Confidence:** {claim.confidence:.2%}")
            lines.append("")
            lines.append(f"**Run Fingerprint:** `{claim.run_fingerprint}`")
            lines.append("")
            
            if claim.supporting_evidence_ids:
                lines.append(f"**Supporting Evidence:** {', '.join(f'`{eid}`' for eid in claim.supporting_evidence_ids)}")
                lines.append("")
            
            if claim.counter_evidence_ids:
                lines.append(f"**Counter Evidence:** {', '.join(f'`{eid}`' for eid in claim.counter_evidence_ids)}")
                lines.append("")
            
            if claim.tool_name:
                lines.append(f"**Tool:** {claim.tool_name} v{claim.tool_version}")
                lines.append("")
            
            if claim.model_name:
                lines.append(f"**Model:** {claim.model_name} v{claim.model_version}")
                lines.append("")
            
            lines.append(f"**Timestamp:** {claim.timestamp.isoformat()}")
            lines.append("")
        
        # Evidence appendix
        lines.append("## Evidence Appendix")
        lines.append("")
        
        for i, ev in enumerate(evidence, 1):
            lines.append(f"### Evidence {i} (ID: `{ev.id}`)")
            lines.append("")
            lines.append(f"**SHA-256:** `{ev.sha256}`")
            lines.append("")
            lines.append(f"**Source:** {ev.source}")
            lines.append("")
            lines.append(f"**Content:**")
            lines.append("")
            lines.append(f"```")
            lines.append(ev.content)
            lines.append(f"```")
            lines.append("")
            
            if ev.tool_name:
                lines.append(f"**Tool:** {ev.tool_name} v{ev.tool_version}")
                lines.append("")
            
            if ev.model_name:
                lines.append(f"**Model:** {ev.model_name} v{ev.model_version}")
                lines.append("")
            
            lines.append(f"**Timestamp:** {ev.timestamp.isoformat()}")
            lines.append("")
            lines.append(f"**Fingerprint:** `{ev.fingerprint}`")
            lines.append("")
        
        return "\n".join(lines)
