"""Evidence model with SHA-256 hashing and timestamps."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, computed_field
import hashlib
import json


class Evidence(BaseModel):
    """
    Immutable evidence artifact with cryptographic fingerprint.
    
    All evidence is append-only and includes SHA-256 hash for integrity verification.
    """
    
    id: Optional[str] = None
    content: str = Field(description="Raw evidence content")
    source: str = Field(description="Source of the evidence (e.g., 'manual', 'scraped', 'api')")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    tool_name: Optional[str] = Field(None, description="Tool that created this evidence")
    tool_version: Optional[str] = Field(None, description="Version of the tool")
    model_name: Optional[str] = Field(None, description="AI model name if applicable")
    model_version: Optional[str] = Field(None, description="AI model version if applicable")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    @computed_field  # type: ignore[misc]
    @property
    def sha256(self) -> str:
        """Compute SHA-256 hash of the evidence content."""
        content_bytes = self.content.encode('utf-8')
        return hashlib.sha256(content_bytes).hexdigest()
    
    @computed_field  # type: ignore[misc]
    @property
    def fingerprint(self) -> str:
        """
        Generate a reproducible fingerprint for this evidence.
        
        Includes content hash, tool/model versions for full reproducibility.
        """
        fingerprint_data = {
            "sha256": self.sha256,
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
                "content": "Document showing transaction of $10,000",
                "source": "manual",
                "metadata": {"document_type": "bank_statement"},
                "tool_name": "watchtower",
                "tool_version": "0.1.0"
            }
        }
