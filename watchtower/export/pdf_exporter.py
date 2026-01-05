"""PDF export functionality."""

from typing import List, Optional, Dict, Any
from watchtower.models.claim import Claim
from watchtower.models.evidence import Evidence
from datetime import datetime
import io


class PDFExporter:
    """
    Export case files to PDF format.
    
    Generates audit-ready PDF case files with claim IDs and evidence appendix.
    """
    
    def __init__(self) -> None:
        """Initialize the PDF exporter."""
        pass
    
    def export_case(
        self,
        claims: List[Claim],
        evidence: List[Evidence],
        title: str = "Case File",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        Export a case file to PDF.
        
        Args:
            claims: List of claims to include
            evidence: List of evidence to include
            title: Case file title
            metadata: Additional metadata
            
        Returns:
            PDF file as bytes
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
        except ImportError:
            # Fallback if reportlab not available
            return b"PDF generation requires reportlab library"
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='black',
            alignment=TA_CENTER,
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.3 * inch))
        
        # Generated timestamp
        story.append(Paragraph(f"<b>Generated:</b> {datetime.utcnow().isoformat()}", styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Metadata
        if metadata:
            story.append(Paragraph("<b>Metadata</b>", styles['Heading2']))
            for key, value in metadata.items():
                story.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Summary
        story.append(Paragraph("<b>Summary</b>", styles['Heading2']))
        story.append(Paragraph(f"Total Claims: {len(claims)}", styles['Normal']))
        story.append(Paragraph(f"Total Evidence: {len(evidence)}", styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Claims
        story.append(Paragraph("<b>Claims</b>", styles['Heading2']))
        story.append(Spacer(1, 0.2 * inch))
        
        for i, claim in enumerate(claims, 1):
            story.append(Paragraph(f"<b>Claim {i} (ID: {claim.id})</b>", styles['Heading3']))
            story.append(Paragraph(f"<b>Statement:</b> {claim.statement}", styles['Normal']))
            story.append(Paragraph(f"<b>Confidence:</b> {claim.confidence:.2%}", styles['Normal']))
            story.append(Paragraph(f"<b>Run Fingerprint:</b> {claim.run_fingerprint}", styles['Normal']))
            
            if claim.supporting_evidence_ids:
                ev_ids = ', '.join(claim.supporting_evidence_ids)
                story.append(Paragraph(f"<b>Supporting Evidence:</b> {ev_ids}", styles['Normal']))
            
            if claim.counter_evidence_ids:
                ev_ids = ', '.join(claim.counter_evidence_ids)
                story.append(Paragraph(f"<b>Counter Evidence:</b> {ev_ids}", styles['Normal']))
            
            if claim.tool_name:
                story.append(Paragraph(f"<b>Tool:</b> {claim.tool_name} v{claim.tool_version}", styles['Normal']))
            
            story.append(Paragraph(f"<b>Timestamp:</b> {claim.timestamp.isoformat()}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Evidence appendix
        story.append(PageBreak())
        story.append(Paragraph("<b>Evidence Appendix</b>", styles['Heading2']))
        story.append(Spacer(1, 0.2 * inch))
        
        for i, ev in enumerate(evidence, 1):
            story.append(Paragraph(f"<b>Evidence {i} (ID: {ev.id})</b>", styles['Heading3']))
            story.append(Paragraph(f"<b>SHA-256:</b> {ev.sha256}", styles['Normal']))
            story.append(Paragraph(f"<b>Source:</b> {ev.source}", styles['Normal']))
            story.append(Paragraph(f"<b>Content:</b> {ev.content[:500]}...", styles['Normal']))
            
            if ev.tool_name:
                story.append(Paragraph(f"<b>Tool:</b> {ev.tool_name} v{ev.tool_version}", styles['Normal']))
            
            story.append(Paragraph(f"<b>Timestamp:</b> {ev.timestamp.isoformat()}", styles['Normal']))
            story.append(Paragraph(f"<b>Fingerprint:</b> {ev.fingerprint}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
        
        # Build PDF
        doc.build(story)
        
        return buffer.getvalue()
