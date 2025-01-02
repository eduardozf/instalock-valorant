import json
import os
import time
from typing import Dict, Any
from pynput import keyboard

# Default values
DEFAULT_LANGUAGE = None
DEFAULT_DELAYS = {"click_interval": 0.05, "loop_interval": 0.05}
DEFAULT_MARGIN_OF_ERROR = {"agent": [20, 20], "confirm": [60, 20]}
DEFAULT_CLICK_TRIES = 3
DEFAULT_CLICK_INTERVAL = {"min": 0.01, "max": 0.03}
DEFAULT_HOLD_TIME = {"min": 0.01, "max": 0.03}
DEFAULT_MOUSE_MOVE_DURATION = 0.07
DEFAULT_CYCLE_INTERVAL = 0.002

# All config keys and their default values
DEFAULT_CONFIG = {
    "language": DEFAULT_LANGUAGE,
    "confirmation_button": {"position": None},
    "margin_of_error": DEFAULT_MARGIN_OF_ERROR,
    "delays": DEFAULT_DELAYS,
    "mouse_move_duration": DEFAULT_MOUSE_MOVE_DURATION,
    "click_tries": DEFAULT_CLICK_TRIES,
    "click_interval": DEFAULT_CLICK_INTERVAL,
    "cycle_interval": DEFAULT_CYCLE_INTERVAL,
    "keybinds": {}
}

# Change the save_file path to be relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
save_file = os.path.join(SCRIPT_DIR, "config.json")

def load_config(macro) -> Dict[str, Any]:
    """Load configuration from file or create with default configuration"""
    
    try:
        if not os.path.exists(save_file):
            # Create the config file with default values
            with open(save_file, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
            return DEFAULT_CONFIG
            
        with open(save_file, "r") as f:
            data = json.load(f)
            # Ensure all default keys exist
            for key, default_value in DEFAULT_CONFIG.items():
                data.setdefault(key, default_value)
            
            # Convert key strings to key objects for keybinds
            for agent in data.get("keybinds", {}).values():
                key_str = agent.get("key")
                try:
                    if not key_str:
                        continue
                        
                    agent["key_obj"] = (
                        getattr(keyboard.Key, key_str[4:])
                        if key_str.startswith("Key.")
                        else keyboard.KeyCode.from_char(key_str.replace("'", ""))
                    )
                except:
                    continue
                    
            if hasattr(macro, 'strings'):
                print(macro.strings["agents_loaded"].format(len(data["keybinds"])))
            return data
            
    except Exception as e:
        print(f"⚠️  Error loading config: {e}")
        return DEFAULT_CONFIG

def update_registered_keys(macro):
    macro.registered_keys.clear()
    if "keybinds" in macro.config:
        for agent_data in macro.config["keybinds"].values():
            if "key_obj" in agent_data:
                macro.registered_keys.add(agent_data["key_obj"])
                
def get_config(config, key):
    """Get a config value with fallback to defaults"""
    if config is None:
        return DEFAULT_CONFIG[key]
    return config.get(key, DEFAULT_CONFIG[key])

def save_config(macro):
    """Save configuration to file, excluding non-serializable objects"""
    try:
        serializable_data = {
            "language": macro.language,
            "confirmation_button": {
                "position": macro.config["confirmation_button"]["position"]
            },
            "margin_of_error": macro.config.get("margin_of_error", DEFAULT_MARGIN_OF_ERROR),
            "delays": macro.config.get("delays", DEFAULT_DELAYS),
            "mouse_move_duration": macro.config.get("mouse_move_duration", DEFAULT_MOUSE_MOVE_DURATION),
            "click_tries": macro.config.get("click_tries", DEFAULT_CLICK_TRIES),
            "click_interval": macro.config.get("click_interval", DEFAULT_CLICK_INTERVAL),
            "cycle_interval": macro.config.get("cycle_interval", DEFAULT_CYCLE_INTERVAL),
            "keybinds": {}
        }
        
        # Only save serializable key data
        for agent_name, data in macro.config["keybinds"].items():
            serializable_data["keybinds"][agent_name] = {
                "key": data.get("key", None),
                "position": data.get("position", None)
            }

        with open(save_file, "w") as f:
            json.dump(serializable_data, f, indent=2)
        print(f"{macro.strings['settings_saved']}")
        update_registered_keys(macro)
    except Exception as e:
        print(f"⚠️ Error saving config: {e}")