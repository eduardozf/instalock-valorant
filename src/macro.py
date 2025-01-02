import threading
import time
import random
import signal
import sys
try:
    from pynput import keyboard, mouse
    import pyautogui
    import win32api
    import win32con
except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Please ensure all required packages are installed using 'pip install -r requirements.txt'")
    exit(1)

from .keys import on_key_press, on_key_release
from .console import clear_console, show_main_menu, show_agent_selection
from .mouse import human_mouse_move, perform_click
from .settings import load_config, update_registered_keys, get_config, save_config
from .language import load_or_select_language, LANGUAGES, VALORANT_AGENTS

class InstalockMacro:
    """
    Main class handling the instalock macro functionality.
    Manages key bindings, agent selection, and macro execution.
    """
    def __init__(self):
        clear_console()
        
        # First load configuration
        self.config = load_config(self)
        
        # Then initialize language settings using the loaded config
        self.language = get_config(self.config, "language")
        if self.language is None:
            self.language = "en_US"
        self.strings = LANGUAGES[self.language]["strings"]
        self.agents_data = LANGUAGES[self.language]["agents"]
        
        # Load or select language
        selected_language = load_or_select_language(self)
        if selected_language != self.language:
            self.language = selected_language
            self.strings = LANGUAGES[self.language]["strings"]
            self.agents_data = LANGUAGES[self.language]["agents"]
        
        # Initialize state variables
        self._initialize_state()
        self._setup_listeners()

    def _initialize_state(self):
        """Initialize all state variables for the macro."""
        self.current_macro_key = None
        self.macro_active = False
        self.macro_thread = None
        self.running = True
        self.recording_mode = False
        self.recording_state = None
        self.current_agent_name = None
        self.agent_selection_index = 0
        self.pressed_keys = set()
        self.registered_keys = set()
        self.key_held = False
        update_registered_keys(self)

    def _setup_listeners(self):
        """Setup keyboard and mouse listeners with signal handlers."""
        def on_press(key):
            self.keyboard_listener.key = key
            return on_key_press(self)
        
        def on_release(key):
            self.keyboard_listener.key = key
            return on_key_release(self)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.keyboard_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )

    def signal_handler(self, signum, frame):
        print("\n" + "-"*50)
        print(f"{self.strings['saving_closing']}")
        save_config(self)
        self.running = False
        self.macro_active = False
        if self.macro_thread and self.macro_thread.is_alive():
            self.macro_thread.join(timeout=0.5)
        self.keyboard_listener.stop()
        print(f"{self.strings['goodbye']}")
        print("-"*50 + "\n")
        sys.stdout.flush()

    def start_listening(self):
        show_main_menu(self.strings, self.config, self.agents_data)
        
        self.keyboard_listener.start()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.signal_handler(None, None)
    
    def run_macro(self, agent_position, confirm_position):
        if not agent_position or not confirm_position:
            print(f"{self.strings['position_not_set']}")
            self.macro_active = False
            return

        margin_of_error = get_config(self.config, "margin_of_error")
        first_move = True

        while self.macro_active and self.running and self.key_held:
            try:
                # Generate random positions once per cycle
                agent_x = agent_position[0] + random.randint(0, margin_of_error["agent"][0])
                agent_y = agent_position[1] + random.randint(0, margin_of_error["agent"][1])
                
                current_x, current_y = pyautogui.position()
                
                if first_move:
                    human_mouse_move(current_x, current_y, agent_x, agent_y, 0.2)
                    first_move = False
                else:
                    human_mouse_move(current_x, current_y, agent_x, agent_y, get_config(self.config, "mouse_move_duration"))
                
                if not (self.macro_active and self.key_held):
                    break
                
                for _ in range(get_config(self.config, "click_tries")):
                    if not (self.macro_active and self.key_held):
                        break
                    perform_click()
                    time.sleep(random.uniform(get_config(self.config, "click_interval")["min"], get_config(self.config, "click_interval")["max"]))

                confirm_x = confirm_position[0] + random.randint(0, margin_of_error["confirm"][0])
                confirm_y = confirm_position[1] + random.randint(0, margin_of_error["confirm"][1])
                
                current_x, current_y = pyautogui.position()
                human_mouse_move(current_x, current_y, confirm_x, confirm_y, get_config(self.config, "mouse_move_duration"))
                
                if not (self.macro_active and self.key_held):
                    break
                
                for _ in range(get_config(self.config, "click_tries")):
                    if not (self.macro_active and self.key_held):
                        break
                    perform_click()
                    time.sleep(random.uniform(get_config(self.config, "click_interval")["min"], get_config(self.config, "click_interval")["max"]))

                time.sleep(get_config(self.config, "cycle_interval"))
                
            except Exception as e:
                print(f"Error in macro: {e}")
                continue 
    def select_agent(self):
        clear_console()
        print("\n" + "-"*50)
        print(f"{self.strings['recording_new_agent']}")
        print("-"*50)
        print(f"{self.strings['select_agent']}")
        print(f"{self.strings['navigation_help']}")
        print("-"*50 + "\n")
        
        show_agent_selection(self.agents_data, self.agent_selection_index, self.strings)