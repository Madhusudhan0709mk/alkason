import importlib
import os
from typing import Dict, Any

class PluginLoader:
    def __init__(self, plugin_dir: str):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Any] = {}

    async def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"{self.plugin_dir}.{module_name}")
                if hasattr(module, "register_plugin"):
                    plugin = module.register_plugin()
                    self.plugins[module_name] = plugin

    def get_plugin(self, name: str) -> Any:
        return self.plugins.get(name)
