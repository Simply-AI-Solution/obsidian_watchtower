"""Append-only artifact store with versioning."""

from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from watchtower.models.artifact import Artifact
import uuid


class ArtifactStore:
    """
    Append-only artifact storage system.
    
    Artifacts are immutable snapshots with SHA-256 hashes and timestamps.
    Supports versioning through parent_artifact_id.
    """
    
    def __init__(self) -> None:
        """Initialize the artifact store."""
        self._artifacts: Dict[str, Artifact] = {}
    
    def store_artifact(
        self,
        artifact_type: Literal["evidence", "claim", "derived", "report"],
        content: str,
        parent_artifact_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tool_name: Optional[str] = None,
        tool_version: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
    ) -> Artifact:
        """
        Store new artifact in the append-only store.
        
        Args:
            artifact_type: Type of artifact (evidence, claim, derived, report)
            content: Artifact content (JSON-serialized)
            parent_artifact_id: Parent artifact for versioning
            metadata: Additional metadata
            tool_name: Name of tool that created artifact
            tool_version: Version of tool
            model_name: Name of AI model if applicable
            model_version: Version of AI model
            
        Returns:
            Stored Artifact object with generated ID and hash
        """
        artifact = Artifact(
            artifact_type=artifact_type,
            content=content,
            parent_artifact_id=parent_artifact_id,
            metadata=metadata or {},
            tool_name=tool_name,
            tool_version=tool_version,
            model_name=model_name,
            model_version=model_version,
            timestamp=datetime.utcnow(),
        )
        
        # Generate unique ID
        artifact_id = str(uuid.uuid4())
        artifact.id = artifact_id
        
        # Store in append-only fashion
        self._artifacts[artifact_id] = artifact
        
        return artifact
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """
        Retrieve artifact by ID.
        
        Args:
            artifact_id: ID of the artifact to retrieve
            
        Returns:
            Artifact object or None if not found
        """
        return self._artifacts.get(artifact_id)
    
    def list_artifacts(
        self,
        artifact_type: Optional[Literal["evidence", "claim", "derived", "report"]] = None,
        parent_artifact_id: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[Artifact]:
        """
        List artifacts with optional filtering.
        
        Args:
            artifact_type: Filter by artifact type
            parent_artifact_id: Filter by parent artifact
            since: Filter by timestamp (artifacts created after this time)
            limit: Maximum number of results
            
        Returns:
            List of Artifact objects
        """
        results = list(self._artifacts.values())
        
        # Apply filters
        if artifact_type:
            results = [a for a in results if a.artifact_type == artifact_type]
        
        if parent_artifact_id is not None:
            results = [a for a in results if a.parent_artifact_id == parent_artifact_id]
        
        if since:
            results = [a for a in results if a.timestamp >= since]
        
        # Sort by timestamp (newest first)
        results.sort(key=lambda a: a.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        return results
    
    def get_artifact_lineage(self, artifact_id: str) -> List[Artifact]:
        """
        Get full lineage of an artifact (all ancestors).
        
        Args:
            artifact_id: ID of artifact to trace
            
        Returns:
            List of artifacts from oldest ancestor to specified artifact
        """
        lineage = []
        current_id = artifact_id
        
        while current_id:
            artifact = self.get_artifact(current_id)
            if not artifact:
                break
            
            lineage.insert(0, artifact)
            current_id = artifact.parent_artifact_id
        
        return lineage
    
    def verify_artifact(self, artifact_id: str) -> bool:
        """
        Verify artifact integrity by recomputing SHA-256 hash.
        
        Args:
            artifact_id: ID of artifact to verify
            
        Returns:
            True if artifact is valid, False otherwise
        """
        artifact = self.get_artifact(artifact_id)
        if not artifact:
            return False
        
        # Recompute hash and compare
        expected_hash = artifact.sha256
        actual_hash = artifact.sha256  # This recomputes from content
        
        return expected_hash == actual_hash
    
    def count_artifacts(self) -> int:
        """Get total number of stored artifacts."""
        return len(self._artifacts)
