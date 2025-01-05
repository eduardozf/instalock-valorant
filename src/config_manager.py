import json
import os
from typing import Dict, Any
from pynput import keyboard
from dataclasses import dataclass

@dataclass
class ConfigPaths:
    """Paths used by the configuration manager"""
    script_dir: str
    config_file: str

class ConfigManager:
    """Manages the application configuration, including loading, saving and updating settings"""
    
    DEFAULT_CONFIG = {
        "language": None,
        "confirmation_button": {"position": None},
        "margin_of_error": {"agent": [20, 20], "confirm": [60, 20]},
        "keybinds": {}
    }

    def __init__(self):
        """Initialize the configuration manager"""
        self.paths = ConfigPaths(
            script_dir=os.path.dirname(os.path.abspath(__file__)),
            config_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        )
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create with default configuration.
        Returns the loaded configuration dictionary.
        """
        if not os.path.exists(self.paths.config_file):
            return self._create_default_config()
            
        try:
            return self._load_and_validate_config()
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            return self.DEFAULT_CONFIG.copy()

    def _create_default_config(self) -> Dict[str, Any]:
        """Create and save default configuration file"""
        try:
            with open(self.paths.config_file, "w") as f:
                json.dump(self.DEFAULT_CONFIG, f, indent=2)
            return self.DEFAULT_CONFIG
        except Exception as e:
            print(f"⚠️ Error creating default config: {e}")
            return self.DEFAULT_CONFIG.copy()

    def _load_and_validate_config(self) -> Dict[str, Any]:
        """Load config from file and validate its contents"""
        with open(self.paths.config_file, "r") as f:
            data = json.load(f)
            
        # Add missing default keys
        self._add_missing_defaults(data)
        
        # Convert key strings to key objects
        self._convert_keybind_strings(data)
            
        return data

    def _add_missing_defaults(self, data: Dict[str, Any]) -> None:
        """Add any missing default keys to the configuration"""
        for key, default_value in self.DEFAULT_CONFIG.items():
            if key not in data:
                print(f"⚠️ Key '{key}' not found in config. Adding default value.")
                data[key] = default_value

    def _convert_keybind_strings(self, data: Dict[str, Any]) -> None:
        """Convert string key representations to keyboard key objects"""
        for agent in data.get("keybinds", {}).values():
            key_str = agent.get("key")
            if not key_str:
                continue
                
            try:
                agent["key_obj"] = (
                    getattr(keyboard.Key, key_str[4:])
                    if key_str.startswith("Key.")
                    else keyboard.KeyCode.from_char(key_str.replace("'", ""))
                )
            except (AttributeError, ValueError):
                continue

    def save_config(self, macro) -> None:
        """
        Save configuration to file, excluding non-serializable objects.
        Args:
            macro: The macro instance containing current settings
        """
        try:
            serializable_data = self._prepare_serializable_data(macro)
            self._write_config_to_file(serializable_data)
            print(f"{macro.strings['settings_saved']}")
            self.update_registered_keys(macro)
        except Exception as e:
            print(f"⚠️ Error saving config: {e}")

    def _prepare_serializable_data(self, macro) -> Dict[str, Any]:
        """Prepare configuration data for serialization"""
        serializable_data = {
            "language": macro.selected_language,
            "confirmation_button": {
                "position": self.config["confirmation_button"]["position"]
            },
            "margin_of_error": self.config.get("margin_of_error", self.DEFAULT_CONFIG["margin_of_error"]),
            "keybinds": {}
        }
        
        # Save only serializable key data
        for agent_name, data in self.config["keybinds"].items():
            serializable_data["keybinds"][agent_name] = {
                "key": data.get("key", None),
                "position": data.get("position", None)
            }
            
        return serializable_data

    def _write_config_to_file(self, data: Dict[str, Any]) -> None:
        """Write configuration data to file"""
        with open(self.paths.config_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_config(self, key: str) -> Any:
        """
        Get a config value with fallback to defaults
        Args:
            key: The configuration key to retrieve
        Returns:
            The configuration value for the given key
        """
        if self.config is None:
            return self.DEFAULT_CONFIG[key]
        return self.config.get(key, self.DEFAULT_CONFIG[key])

    def update_registered_keys(self, macro) -> None:
        """
        Update the set of registered keys based on current keybinds
        Args:
            macro: The macro instance to update
        """
        macro.key_manager.registered_keys.clear()
        if "keybinds" in self.config:
            for agent_data in self.config["keybinds"].values():
                if "key_obj" in agent_data:
                    macro.key_manager.registered_keys.add(agent_data["key_obj"])

    def unbind_agent(self, agent_name: str, macro) -> bool:
        """
        Unbind an agent from the configuration.
        Args:
            agent_name: Name of the agent to unbind
            macro: The macro instance
        Returns:
            True if agent was unbound, False otherwise
        """
        if "keybinds" in self.config and agent_name in self.config["keybinds"]:
            del self.config["keybinds"][agent_name]
            self.save_config(macro)
            return True
        return False 