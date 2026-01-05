"""Artifact model for append-only snapshots."""

from datetime import datetime
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, computed_field
import hashlib
import json


class Artifact(BaseModel):
    """
    Append-only artifact snapshot with SHA-256 and timestamp.
    
    Artifacts are immutable snapshots that can be evidence, claims, or derived data.
    """
    
    id: Optional[str] = None
    artifact_type: Literal["evidence", "claim", "derived", "report"] = Field(
        description="Type of artifact"
    )
    content: str = Field(description="Artifact content (JSON-serialized)")
    parent_artifact_id: Optional[str] = Field(None, description="Parent artifact for versioning")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    tool_name: Optional[str] = Field(None, description="Tool that created this artifact")
    tool_version: Optional[str] = Field(None, description="Version of the tool")
    model_name: Optional[str] = Field(None, description="AI model name if applicable")
    model_version: Optional[str] = Field(None, description="AI model version if applicable")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    @computed_field  # type: ignore[misc]
    @property
    def sha256(self) -> str:
        """Compute SHA-256 hash of the artifact content."""
        content_bytes = self.content.encode('utf-8')
        return hashlib.sha256(content_bytes).hexdigest()
    
    @computed_field  # type: ignore[misc]
    @property
    def fingerprint(self) -> str:
        """
        Generate a reproducible fingerprint for this artifact.
        
        Includes content hash, tool/model versions, and lineage information.
        """
        fingerprint_data = {
            "sha256": self.sha256,
            "artifact_type": self.artifact_type,
            "parent_id": self.parent_artifact_id,
            "timestamp": self.timestamp.isoformat(),
            "tool": f"{self.tool_name}:{self.tool_version}" if self.tool_name else None,
            "model": f"{self.model_name}:{self.model_version}" if self.model_name else None,
        }
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_str.encode('utf-8')).hexdigest()
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "artifact_type": "evidence",
                "content": '{"text": "Transaction record"}',
                "tool_name": "watchtower",
                "tool_version": "0.1.0"
            }
        }
