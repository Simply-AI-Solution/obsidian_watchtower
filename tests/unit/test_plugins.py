"""Unit tests for plugin system."""

import pytest
from watchtower.plugins.base import SourcePlugin
from watchtower.plugins.registry import PluginRegistry
from watchtower.plugins.manual_entry import ManualEntryPlugin


def test_manual_entry_plugin() -> None:
    """Test manual entry plugin."""
    plugin = ManualEntryPlugin()
    
    assert plugin.name == "manual_entry"
    assert plugin.version == "0.1.0"
    
    config = {
        "content": "Test evidence",
        "metadata": {"key": "value"},
    }
    
    evidence_list = plugin.extract(config)
    assert len(evidence_list) == 1
    
    evidence = evidence_list[0]
    assert evidence.content == "Test evidence"
    assert evidence.source == "manual"
    assert evidence.metadata == {"key": "value"}


def test_manual_entry_plugin_validation() -> None:
    """Test manual entry plugin config validation."""
    plugin = ManualEntryPlugin()
    
    # Valid config
    assert plugin.validate_config({"content": "test"}) is True
    
    # Invalid config (missing content)
    assert plugin.validate_config({}) is False
    
    # Invalid config (wrong type)
    assert plugin.validate_config({"content": 123}) is False


def test_plugin_registry() -> None:
    """Test plugin registry."""
    registry = PluginRegistry()
    
    plugin = ManualEntryPlugin()
    registry.register(plugin)
    
    # Check plugin was registered
    assert "manual_entry" in registry.list_plugins()
    
    # Retrieve plugin
    retrieved = registry.get_plugin("manual_entry")
    assert retrieved is not None
    assert retrieved.name == "manual_entry"


def test_plugin_registry_duplicate() -> None:
    """Test that duplicate plugin names are rejected."""
    registry = PluginRegistry()
    
    plugin1 = ManualEntryPlugin()
    registry.register(plugin1)
    
    plugin2 = ManualEntryPlugin()
    with pytest.raises(ValueError, match="already registered"):
        registry.register(plugin2)


def test_plugin_registry_unregister() -> None:
    """Test unregistering plugins."""
    registry = PluginRegistry()
    
    plugin = ManualEntryPlugin()
    registry.register(plugin)
    
    assert "manual_entry" in registry.list_plugins()
    
    registry.unregister("manual_entry")
    
    assert "manual_entry" not in registry.list_plugins()
    assert registry.get_plugin("manual_entry") is None


def test_get_all_plugins() -> None:
    """Test getting all plugins."""
    registry = PluginRegistry()
    
    plugin = ManualEntryPlugin()
    registry.register(plugin)
    
    all_plugins = registry.get_all_plugins()
    assert len(all_plugins) == 1
    assert all_plugins[0].name == "manual_entry"
