"""Plugin registry for managing source plugins."""

from typing import Dict, Optional, List
from watchtower.plugins.base import SourcePlugin


class PluginRegistry:
    """
    Registry for managing source plugins.
    
    Provides centralized registration and discovery of data source plugins.
    """
    
    def __init__(self) -> None:
        """Initialize the plugin registry."""
        self._plugins: Dict[str, SourcePlugin] = {}
    
    def register(self, plugin: SourcePlugin) -> None:
        """
        Register a plugin.
        
        Args:
            plugin: Plugin to register
            
        Raises:
            ValueError: If plugin with same name already registered
        """
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin '{plugin.name}' is already registered")
        
        self._plugins[plugin.name] = plugin
    
    def unregister(self, plugin_name: str) -> None:
        """
        Unregister a plugin.
        
        Args:
            plugin_name: Name of plugin to unregister
        """
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
    
    def get_plugin(self, plugin_name: str) -> Optional[SourcePlugin]:
        """
        Get a plugin by name.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin instance or None if not found
        """
        return self._plugins.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """
        List all registered plugin names.
        
        Returns:
            List of plugin names
        """
        return list(self._plugins.keys())
    
    def get_all_plugins(self) -> List[SourcePlugin]:
        """
        Get all registered plugins.
        
        Returns:
            List of plugin instances
        """
        return list(self._plugins.values())
