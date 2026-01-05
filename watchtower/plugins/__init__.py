"""Plugin system for modular data sources."""

from watchtower.plugins.base import SourcePlugin
from watchtower.plugins.registry import PluginRegistry

__all__ = ["SourcePlugin", "PluginRegistry"]
