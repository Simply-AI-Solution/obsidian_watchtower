"""Alert generation for significant changes."""

from typing import List, Dict, Any, Optional
from watchtower.models.claim import Claim
from datetime import datetime


class Alert:
    """Alert for significant changes or anomalies."""
    
    def __init__(
        self,
        alert_type: str,
        severity: str,
        message: str,
        details: Dict[str, Any],
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Initialize an alert.
        
        Args:
            alert_type: Type of alert (e.g., 'confidence_drop', 'new_claim')
            severity: Severity level ('low', 'medium', 'high', 'critical')
            message: Human-readable alert message
            details: Additional details about the alert
            timestamp: Alert timestamp
        """
        self.alert_type = alert_type
        self.severity = severity
        self.message = message
        self.details = details
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "alert_type": self.alert_type,
            "severity": self.severity,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }


class AlertGenerator:
    """
    Generate alerts for significant changes or anomalies.
    
    Monitors claims and evidence for notable patterns or changes.
    """
    
    def __init__(
        self,
        confidence_drop_threshold: float = 0.2,
        confidence_high_threshold: float = 0.9,
    ) -> None:
        """
        Initialize the alert generator.
        
        Args:
            confidence_drop_threshold: Threshold for confidence drop alerts
            confidence_high_threshold: Threshold for high-confidence alerts
        """
        self.confidence_drop_threshold = confidence_drop_threshold
        self.confidence_high_threshold = confidence_high_threshold
    
    def generate_alerts(
        self,
        claims: List[Claim],
        previous_claims: Optional[List[Claim]] = None,
    ) -> List[Alert]:
        """
        Generate alerts based on claims.
        
        Args:
            claims: Current claims
            previous_claims: Previous claims for comparison
            
        Returns:
            List of generated alerts
        """
        alerts = []
        
        # Alert for high-confidence claims
        for claim in claims:
            if claim.confidence >= self.confidence_high_threshold:
                alerts.append(Alert(
                    alert_type="high_confidence_claim",
                    severity="high",
                    message=f"High-confidence claim detected: {claim.statement[:100]}",
                    details={
                        "claim_id": claim.id,
                        "confidence": claim.confidence,
                        "statement": claim.statement,
                    },
                ))
        
        # Alert for claims with many evidence items
        for claim in claims:
            total_evidence = len(claim.supporting_evidence_ids) + len(claim.counter_evidence_ids)
            if total_evidence >= 5:
                alerts.append(Alert(
                    alert_type="well_supported_claim",
                    severity="medium",
                    message=f"Claim with substantial evidence: {claim.statement[:100]}",
                    details={
                        "claim_id": claim.id,
                        "total_evidence": total_evidence,
                        "supporting_count": len(claim.supporting_evidence_ids),
                        "counter_count": len(claim.counter_evidence_ids),
                    },
                ))
        
        # Compare with previous claims if available
        if previous_claims:
            prev_claims_map = {c.id: c for c in previous_claims if c.id}
            
            for claim in claims:
                if claim.id in prev_claims_map:
                    prev_claim = prev_claims_map[claim.id]
                    confidence_change = claim.confidence - prev_claim.confidence
                    
                    # Alert for significant confidence drop
                    if confidence_change <= -self.confidence_drop_threshold:
                        alerts.append(Alert(
                            alert_type="confidence_drop",
                            severity="high",
                            message=f"Significant confidence drop in claim: {claim.statement[:100]}",
                            details={
                                "claim_id": claim.id,
                                "previous_confidence": prev_claim.confidence,
                                "current_confidence": claim.confidence,
                                "change": confidence_change,
                            },
                        ))
                    
                    # Alert for significant confidence increase
                    elif confidence_change >= self.confidence_drop_threshold:
                        alerts.append(Alert(
                            alert_type="confidence_increase",
                            severity="medium",
                            message=f"Significant confidence increase in claim: {claim.statement[:100]}",
                            details={
                                "claim_id": claim.id,
                                "previous_confidence": prev_claim.confidence,
                                "current_confidence": claim.confidence,
                                "change": confidence_change,
                            },
                        ))
        
        return alerts
    
    def generate_summary(self, alerts: List[Alert]) -> Dict[str, Any]:
        """
        Generate a summary of alerts.
        
        Args:
            alerts: List of alerts
            
        Returns:
            Summary dictionary
        """
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        type_counts: Dict[str, int] = {}
        
        for alert in alerts:
            severity_counts[alert.severity] += 1
            type_counts[alert.alert_type] = type_counts.get(alert.alert_type, 0) + 1
        
        return {
            "total_alerts": len(alerts),
            "severity_counts": severity_counts,
            "type_counts": type_counts,
            "alerts": [alert.to_dict() for alert in alerts],
        }
