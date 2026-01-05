"""Obsidian Watchtower: Local-first fraud/corruption investigation system."""

__version__ = "0.1.0"

from watchtower.models.evidence import Evidence
from watchtower.models.claim import Claim
from watchtower.models.artifact import Artifact

__all__ = ["Evidence", "Claim", "Artifact", "__version__"]
