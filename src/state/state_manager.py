from typing import Dict, Type, Any
from core.interfaces import IMacroState, IConfigProvider, IMenuController, ILanguageProvider
from .states import MainMenuState, RecordingState, MacroActiveState

class StateManager:
    def __init__(self, config: IConfigProvider, menu: IMenuController, lang: ILanguageProvider):
        self.config = config
        self.menu = menu
        self.lang = lang
        
        # Initialize states
        self.states: Dict[str, Type[IMacroState]] = {
            "main_menu": MainMenuState,
            "recording": RecordingState,
            "macro_active": MacroActiveState
        }
        
        self.current_state: IMacroState = None
        self.transition_to("main_menu")
    
    def transition_to(self, state_name: str) -> None:
        """Transition to a new state."""
        if self.current_state:
            self.current_state.exit()
            
        state_class = self.states.get(state_name)
        if not state_class:
            raise ValueError(f"Invalid state: {state_name}")
            
        self.current_state = state_class(self.config, self.menu, self.lang)
        self.current_state.enter()
    
    def handle_input(self, key: Any) -> bool:
        """Handle input in current state."""
        if self.current_state:
            if self.current_state.handle_input(key):
                self.transition_to("main_menu")
                return True
        return False 