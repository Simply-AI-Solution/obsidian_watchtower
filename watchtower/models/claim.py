"""Claim model with evidence references and confidence scoring."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, computed_field
import hashlib
import json


class Claim(BaseModel):
    """
    A claim about fraud/corruption that must be backed by evidence.
    
    Every claim requires at least one evidence reference and includes
    confidence scoring plus reproducible run fingerprint.
    """
    
    id: Optional[str] = None
    statement: str = Field(description="The claim being made")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score (0-1)")
    supporting_evidence_ids: List[str] = Field(
        default_factory=list,
        description="IDs of supporting evidence"
    )
    counter_evidence_ids: List[str] = Field(
        default_factory=list,
        description="IDs of counter evidence"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    tool_name: Optional[str] = Field(None, description="Tool that created this claim")
    tool_version: Optional[str] = Field(None, description="Version of the tool")
    model_name: Optional[str] = Field(None, description="AI model name if applicable")
    model_version: Optional[str] = Field(None, description="AI model version if applicable")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    @field_validator('supporting_evidence_ids', 'counter_evidence_ids')
    @classmethod
    def validate_evidence_refs(cls, v: List[str], info: Any) -> List[str]:
        """Ensure claim has at least one evidence reference."""
        # We'll check total evidence in model_validator
        return v
    
    def model_post_init(self, __context: Any) -> None:
        """Validate that claim has at least one evidence reference."""
        total_evidence = len(self.supporting_evidence_ids) + len(self.counter_evidence_ids)
        if total_evidence == 0:
            raise ValueError(
                "No claim without evidence_ref: Claims must have at least one "
                "supporting or counter evidence reference"
            )
    
    @computed_field  # type: ignore[misc]
    @property
    def evidence_refs(self) -> List[str]:
        """Get all evidence references (supporting + counter)."""
        return self.supporting_evidence_ids + self.counter_evidence_ids
    
    @computed_field  # type: ignore[misc]
    @property
    def run_fingerprint(self) -> str:
        """
        Generate a reproducible run fingerprint for this claim.
        
        Includes all evidence IDs, confidence, tool/model versions for full reproducibility.
        """
        fingerprint_data = {
            "statement_hash": hashlib.sha256(self.statement.encode('utf-8')).hexdigest(),
            "confidence": self.confidence,
            "supporting_evidence": sorted(self.supporting_evidence_ids),
            "counter_evidence": sorted(self.counter_evidence_ids),
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
                "statement": "Company X received suspicious payment",
                "confidence": 0.85,
                "supporting_evidence_ids": ["evidence_1", "evidence_2"],
                "counter_evidence_ids": [],
                "tool_name": "watchtower",
                "tool_version": "0.1.0"
            }
        }
