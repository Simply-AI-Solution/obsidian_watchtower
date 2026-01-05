"""Sample manual entry plugin."""

from typing import List, Dict, Any
from watchtower.plugins.base import SourcePlugin
from watchtower.models.evidence import Evidence
from datetime import datetime


class ManualEntryPlugin(SourcePlugin):
    """
    Sample plugin for manual evidence entry.
    
    Allows users to manually input evidence with metadata.
    """
    
    @property
    def name(self) -> str:
        """Plugin name."""
        return "manual_entry"
    
    @property
    def version(self) -> str:
        """Plugin version."""
        return "0.1.0"
    
    @property
    def description(self) -> str:
        """Plugin description."""
        return "Manual evidence entry plugin"
    
    def extract(self, config: Dict[str, Any]) -> List[Evidence]:
        """
        Extract evidence from manual input.
        
        Args:
            config: Must contain 'content' key with evidence text
            
        Returns:
            List containing single Evidence object
        """
        content = config.get("content", "")
        metadata = config.get("metadata", {})
        
        evidence = Evidence(
            content=content,
            source="manual",
            metadata=metadata,
            tool_name=self.name,
            tool_version=self.version,
            timestamp=datetime.utcnow(),
        )
        
        return [evidence]
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if 'content' key exists, False otherwise
        """
        return "content" in config and isinstance(config["content"], str)
