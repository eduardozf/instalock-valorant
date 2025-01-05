from .macro_manager import MacroManager
from .macro_executor import MacroExecutor
from ..config.config_manager import ConfigManager
from ..input.key_manager import KeyManager
from ..input.mouse_manager import MouseManager
from ..ui.menu_manager import MenuManager
from ..config.language_manager import LanguageManager

class InstalockMacro:
    """
    Main class for the Instalock Valorant macro.
    Acts as a dependency injector and entry point.
    """
    def __init__(self):
        # Create components
        self.config_manager = ConfigManager()
        self.language_manager = LanguageManager()
        
        # Load or select language
        self.selected_language = self.language_manager.load_or_select_language(self)
        self.strings = self.language_manager.languages[self.selected_language]["strings"]
        
        # Save selected language to config
        self.config_manager.config["language"] = self.selected_language
        
        # Initialize recording state
        self.recording_mode = False
        self.recording_state = None
        self.current_agent_name = None
        self.macro_active = False
        self.macro_thread = None
        self.agents_data = self.language_manager.languages[self.selected_language]["agents"]
        
        # Initialize other components
        self.menu_manager = MenuManager(self.strings)
        self.mouse_manager = MouseManager()
        self.macro_executor = MacroExecutor(self.mouse_manager, self.config_manager)
        self.key_manager = KeyManager(self)
        
        # Create and configure macro manager
        self.manager = MacroManager(
            config_provider=self.config_manager,
            key_handler=self.key_manager,
            mouse_controller=self.mouse_manager,
            menu_controller=self.menu_manager,
            macro_executor=self.macro_executor,
            language_provider=self.language_manager
        )
        
        # Save config after all components are initialized
        self.config_manager.save_config(self)

    def run(self):
        """Start the macro application."""
        self.manager.start()

    def execute_macro(self, agent_position, confirm_position):
        """Execute the macro sequence by moving to agent position and confirm position."""
        if not agent_position or not confirm_position:
            print(f"{self.strings['position_not_set']}")
            return
        
        while self.macro_active:
            try:
                self.macro_executor.execute_macro(agent_position, confirm_position)
                if not self.macro_active:  # Check if we should stop
                    break
            except Exception as e:
                print(f"{self.strings['fatal_error'].format(e)}")
                break