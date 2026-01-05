"""Base plugin interface for data sources."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from watchtower.models.evidence import Evidence


class SourcePlugin(ABC):
    """
    Abstract base class for source plugins.
    
    Source plugins are modular data extractors that can pull evidence
    from various sources (APIs, databases, files, web scraping, etc.).
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @property
    def description(self) -> str:
        """Plugin description."""
        return ""
    
    @abstractmethod
    def extract(self, config: Dict[str, Any]) -> List[Evidence]:
        """
        Extract evidence from the source.
        
        Args:
            config: Configuration parameters for extraction
            
        Returns:
            List of Evidence objects extracted from the source
        """
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration parameters.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid, False otherwise
        """
        return True
