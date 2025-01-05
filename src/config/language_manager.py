import json
from typing import Dict, Any
from pynput import keyboard
import threading
import time

from ..ui.menu_manager import MenuManager

class LanguageManager:
    def __init__(self):
        self.languages = self.load_languages()
        self.valorant_agents = list(self.languages["en_US"]["agents"].keys())
        self.selected_index = 0
        self.selected_language = None
        self.keyboard_listener = None
        self.menu_manager = None
        self.selection_done = threading.Event()
    
    def load_languages(self) -> Dict[str, Any]:
        """
        Load language configurations from languages.json file.
        Returns a dictionary with language settings or empty dict if file not found.
        """
        try:
            with open('./src/config/languages.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading languages: {e}")
            return {}
    
    def on_key_press(self, key):
        """Handle key press events during language selection."""
        try:
            if key == keyboard.Key.up or key == keyboard.Key.down:
                if self.menu_manager.handle_navigation(key):
                    self.menu_manager.show_menu("language_selection", languages=self.languages)
            elif key == keyboard.Key.enter:
                self.selected_language = list(self.languages.keys())[self.menu_manager.selected_index]
                self.selection_done.set()
                if self.keyboard_listener:
                    self.keyboard_listener.stop()
                return False
        except Exception as e:
            print(f"⚠️  Error handling key press: {e}")
        return True
    
    def load_or_select_language(self, macro):
        """Load existing language or prompt user to select one."""
        if macro.config_manager.config.get("language") and macro.config_manager.config["language"] in self.languages:
            return macro.config_manager.config["language"]
        
        # Create menu manager with minimal strings needed for language selection
        minimal_strings = {
            "title": "🌐 Select your language / Selecione seu idioma / 选择语言",
            "menu_navigation": "↑/↓: Navigate | Enter: Select",
            "menu_record_agent": "",  # Not used in language selection
            "menu_refresh_settings": "",  # Not used in language selection
            "menu_start_macro": "",  # Not used in language selection
            "recording_new_agent": "",  # Not used in language selection
            "select_agent": "",  # Not used in language selection
            "navigation_help": "",  # Not used in language selection
            "press_delete_unbind": "",  # Not used in language selection
            "agent_bound_to": "",  # Not used in language selection
            "macro_running": "",  # Not used in language selection
            "press_esc_exit": "",  # Not used in language selection
            "macro_ready": ""  # Not used in language selection
        }
        
        self.menu_manager = MenuManager(minimal_strings)
        self.menu_manager.selected_index = self.selected_index
        self.menu_manager.show_menu("language_selection", languages=self.languages)
        
        # Setup keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()
        
        try:
            # Wait for language selection with timeout
            if not self.selection_done.wait(timeout=60):  # 60 seconds timeout
                print("\n⚠️  No language selected within timeout, defaulting to English")
                time.sleep(2)
                return "en_US"
            
            if not self.selected_language:
                print("\n⚠️  No language selected, defaulting to English")
                time.sleep(2)
                return "en_US"
            
            return self.selected_language
            
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            if self.keyboard_listener and self.keyboard_listener.running:
                self.keyboard_listener.stop()
            raise SystemExit(0)
        finally:
            if self.keyboard_listener and self.keyboard_listener.running:
                self.keyboard_listener.stop()

# Create a singleton instance
language_manager = LanguageManager()
LANGUAGES = language_manager.languages
VALORANT_AGENTS = language_manager.valorant_agents 