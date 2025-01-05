from typing import Dict, Any
from pynput import keyboard

from .interfaces import IMacroState, IConfigProvider, IMenuController, ILanguageProvider

class MacroState(IMacroState):
    def __init__(self, config: IConfigProvider, menu: IMenuController, lang: ILanguageProvider):
        self.config = config
        self.menu = menu
        self.lang = lang
    
    def enter(self) -> None:
        pass
    
    def exit(self) -> None:
        pass
    
    def handle_input(self, key: Any) -> bool:
        return False

class MainMenuState(MacroState):
    def enter(self) -> None:
        self.menu.show_main_menu(self.config.config)
    
    def handle_input(self, key: Any) -> bool:
        if isinstance(key, keyboard.Key):
            if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.enter]:
                return self.menu.handle_menu_navigation(key, self.config)
        return False

class RecordingState(MacroState):
    def enter(self) -> None:
        self.menu.show_agent_selection(
            self.lang.languages["en_US"]["agents"],
            self.config.config
        )
    
    def handle_input(self, key: Any) -> bool:
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.esc:
                return True
            elif key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.enter]:
                return self.menu.handle_menu_navigation(key, self.config)
            elif key == keyboard.Key.delete:
                # Handle agent unbinding
                return True
        return False

class MacroActiveState(MacroState):
    def enter(self) -> None:
        self.menu.show_macro_status(
            self.config.config,
            self.lang.languages["en_US"]["agents"]
        )
    
    def handle_input(self, key: Any) -> bool:
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.esc:
                return True
        return False 