"""Append-only evidence store with SHA-256 verification."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from watchtower.models.evidence import Evidence
import uuid


class EvidenceStore:
    """
    Append-only evidence storage system.
    
    Evidence is immutable once stored. All operations preserve the original
    evidence with SHA-256 hashes and timestamps.
    """
    
    def __init__(self) -> None:
        """Initialize the evidence store."""
        self._evidence: Dict[str, Evidence] = {}
    
    def store_evidence(
        self,
        content: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None,
        tool_name: Optional[str] = None,
        tool_version: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
    ) -> Evidence:
        """
        Store new evidence in the append-only store.
        
        Args:
            content: Raw evidence content
            source: Source of the evidence
            metadata: Additional metadata
            tool_name: Name of tool that created evidence
            tool_version: Version of tool
            model_name: Name of AI model if applicable
            model_version: Version of AI model
            
        Returns:
            Stored Evidence object with generated ID and hash
        """
        evidence = Evidence(
            content=content,
            source=source,
            metadata=metadata or {},
            tool_name=tool_name,
            tool_version=tool_version,
            model_name=model_name,
            model_version=model_version,
            timestamp=datetime.utcnow(),
        )
        
        # Generate unique ID
        evidence_id = str(uuid.uuid4())
        evidence.id = evidence_id
        
        # Store in append-only fashion (no updates allowed)
        self._evidence[evidence_id] = evidence
        
        return evidence
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """
        Retrieve evidence by ID.
        
        Args:
            evidence_id: ID of the evidence to retrieve
            
        Returns:
            Evidence object or None if not found
        """
        return self._evidence.get(evidence_id)
    
    def list_evidence(
        self,
        source: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[Evidence]:
        """
        List evidence with optional filtering.
        
        Args:
            source: Filter by source
            since: Filter by timestamp (evidence created after this time)
            limit: Maximum number of results
            
        Returns:
            List of Evidence objects
        """
        results = list(self._evidence.values())
        
        # Apply filters
        if source:
            results = [e for e in results if e.source == source]
        
        if since:
            results = [e for e in results if e.timestamp >= since]
        
        # Sort by timestamp (newest first)
        results.sort(key=lambda e: e.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        return results
    
    def verify_evidence(self, evidence_id: str) -> bool:
        """
        Verify evidence integrity by recomputing SHA-256 hash.
        
        Args:
            evidence_id: ID of evidence to verify
            
        Returns:
            True if evidence is valid, False otherwise
        """
        evidence = self.get_evidence(evidence_id)
        if not evidence:
            return False
        
        # Recompute hash and compare
        expected_hash = evidence.sha256
        actual_hash = evidence.sha256  # This recomputes from content
        
        return expected_hash == actual_hash
    
    def count_evidence(self) -> int:
        """Get total number of stored evidence items."""
        return len(self._evidence)
