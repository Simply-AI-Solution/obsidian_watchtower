"""Claim store with evidence reference validation."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from watchtower.models.claim import Claim
from watchtower.storage.evidence_store import EvidenceStore
import uuid


class ClaimStore:
    """
    Claim storage system with evidence reference validation.
    
    Enforces the rule: no claim without evidence_ref.
    All claims must reference at least one piece of evidence.
    """
    
    def __init__(self, evidence_store: EvidenceStore) -> None:
        """
        Initialize the claim store.
        
        Args:
            evidence_store: Evidence store for validation
        """
        self._claims: Dict[str, Claim] = {}
        self._evidence_store = evidence_store
    
    def store_claim(
        self,
        statement: str,
        confidence: float,
        supporting_evidence_ids: List[str],
        counter_evidence_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tool_name: Optional[str] = None,
        tool_version: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
    ) -> Claim:
        """
        Store new claim with evidence validation.
        
        Args:
            statement: The claim being made
            confidence: Confidence score (0-1)
            supporting_evidence_ids: IDs of supporting evidence
            counter_evidence_ids: IDs of counter evidence
            metadata: Additional metadata
            tool_name: Name of tool that created claim
            tool_version: Version of tool
            model_name: Name of AI model if applicable
            model_version: Version of AI model
            
        Returns:
            Stored Claim object with generated ID
            
        Raises:
            ValueError: If evidence references are invalid
        """
        # Validate evidence exists
        all_evidence_ids = supporting_evidence_ids + (counter_evidence_ids or [])
        for evidence_id in all_evidence_ids:
            if not self._evidence_store.get_evidence(evidence_id):
                raise ValueError(f"Evidence not found: {evidence_id}")
        
        # Create claim (will validate that at least one evidence exists)
        claim = Claim(
            statement=statement,
            confidence=confidence,
            supporting_evidence_ids=supporting_evidence_ids,
            counter_evidence_ids=counter_evidence_ids or [],
            metadata=metadata or {},
            tool_name=tool_name,
            tool_version=tool_version,
            model_name=model_name,
            model_version=model_version,
            timestamp=datetime.utcnow(),
        )
        
        # Generate unique ID
        claim_id = str(uuid.uuid4())
        claim.id = claim_id
        
        # Store claim
        self._claims[claim_id] = claim
        
        return claim
    
    def get_claim(self, claim_id: str) -> Optional[Claim]:
        """
        Retrieve claim by ID.
        
        Args:
            claim_id: ID of the claim to retrieve
            
        Returns:
            Claim object or None if not found
        """
        return self._claims.get(claim_id)
    
    def list_claims(
        self,
        min_confidence: Optional[float] = None,
        since: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[Claim]:
        """
        List claims with optional filtering.
        
        Args:
            min_confidence: Filter by minimum confidence
            since: Filter by timestamp (claims created after this time)
            limit: Maximum number of results
            
        Returns:
            List of Claim objects
        """
        results = list(self._claims.values())
        
        # Apply filters
        if min_confidence is not None:
            results = [c for c in results if c.confidence >= min_confidence]
        
        if since:
            results = [c for c in results if c.timestamp >= since]
        
        # Sort by confidence (highest first), then by timestamp
        results.sort(key=lambda c: (c.confidence, c.timestamp), reverse=True)
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        return results
    
    def get_claims_by_evidence(self, evidence_id: str) -> List[Claim]:
        """
        Get all claims that reference a specific evidence.
        
        Args:
            evidence_id: ID of evidence
            
        Returns:
            List of claims referencing the evidence
        """
        results = []
        for claim in self._claims.values():
            if evidence_id in claim.evidence_refs:
                results.append(claim)
        
        return results
    
    def count_claims(self) -> int:
        """Get total number of stored claims."""
        return len(self._claims)
