from typing import Any
from ..core.interfaces import (
    IConfigProvider, IKeyHandler, IMouseController,
    IMenuController, IMacroExecutor, ILanguageProvider
)
from ..state.state_manager import StateManager
import time

class MacroManager:
    """
    Coordinates the macro system using dependency injection and state pattern.
    Each component is responsible for its own functionality and state.
    """
    def __init__(
        self,
        config_provider: IConfigProvider,
        key_handler: IKeyHandler,
        mouse_controller: IMouseController,
        menu_controller: IMenuController,
        macro_executor: IMacroExecutor,
        language_provider: ILanguageProvider
    ):
        self.config = config_provider
        self.keys = key_handler
        self.mouse = mouse_controller
        self.menu = menu_controller
        self.executor = macro_executor
        self.language = language_provider
        
        # Store reference to macro instance
        self.macro = self.keys.macro
        
        # Initialize state manager
        self.state_manager = StateManager(
            config=self.config,
            menu=self.menu,
            lang=self.language
        )
    
    def start(self) -> None:
        """Start the macro system."""
        try:
            # Show initial menu
            self.menu.show_menu("main", config=self.config.config)
            
            # Start keyboard listener
            self.keys.start_listening()
            
            # Keep the main thread alive
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop()
                
        except Exception as e:
            print(f"⚠️ Fatal error: {e}")
            self.stop()
    
    def stop(self) -> None:
        """Stop the macro system."""
        self.executor.stop_macro()
        self.keys.stop_listening()
        self.config.save_config(self.macro)
    
    def handle_input(self, key: Any) -> bool:
        """Handle input by delegating to current state."""
        return self.state_manager.handle_input(key) 