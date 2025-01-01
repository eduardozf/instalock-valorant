import time
import threading
import signal
import sys
import json
import os
import atexit
import win32gui
import win32con
import win32api
import win32process
from pynput import keyboard, mouse
import pyautogui
import ctypes
import msvcrt
import random

def load_languages():
    """
    Load language configurations from languages.json file.
    Returns a dictionary with language settings or empty dict if file not found.
    """
    try:
        with open('languages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Error loading languages: {e}")
        return {}

# Load language data and define constants
LANGUAGES = load_languages()
VALORANT_AGENTS = list(LANGUAGES["en_US"]["agents"].keys())

def clear_console():
    """Clear the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_key(key_str):
    """Format key string for display in the UI."""
    if key_str.startswith("Key."):
        return key_str[4:].upper()
    return key_str.replace("'", "")

class InstalockMacro:
    """
    Main class handling the instalock macro functionality.
    Manages key bindings, agent selection, and macro execution.
    """
    def __init__(self):
        clear_console()
        self.save_file = "config.json"
        
        # Initialize default language settings
        self.language = "en_US"
        self.strings = LANGUAGES["en_US"]["strings"]
        self.agents_data = LANGUAGES["en_US"]["agents"]
        
        # Load configuration and language preferences
        self.config = self.load_config()
        selected_language = self.load_or_select_language()
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
        self.update_registered_keys()

    def _setup_listeners(self):
        """Setup keyboard and mouse listeners with signal handlers."""
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def load_or_select_language(self):
        if self.config.get("language") and self.config["language"] in LANGUAGES:
            return self.config["language"]
        
        clear_console()
        print("\n" + "="*70)
        print("🌐 Select your language / Selecione seu idioma / 选择语言".center(50))
        print("="*70 + "\n")
        
        languages = list(LANGUAGES.items())
        selected_index = 0
        menu_height = len(languages) + 3
        header_lines = 5
        
        # Print initial menu
        for i, (lang_code, lang_data) in enumerate(languages):
            print(f"{'➤ ' if i == selected_index else '  '}{lang_data['flag']} {lang_data['name']}")
        
        print("\n↑/↓: Navigate/Navegar/导航 | Enter: Select/Selecionar/选择")
        
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                old_index = selected_index
                
                if key == b'H':  # Up arrow
                    selected_index = (selected_index - 1) % len(languages)
                elif key == b'P':  # Down arrow
                    selected_index = (selected_index + 1) % len(languages)
                elif key == b'\r':  # Enter
                    selected_lang = languages[selected_index][0]
                    self.config["language"] = selected_lang
                    self.save_config()
                    # Move cursor to bottom of menu before returning
                    print(f"\033[{menu_height - selected_index}B", end='')
                    return selected_lang
                
                if old_index != selected_index:
                    # Move cursor to old selection and clear the arrow
                    print(f"\033[{header_lines + old_index + 1};1H  ", end='')
                    # Move cursor to new selection and draw the arrow
                    print(f"\033[{header_lines + selected_index + 1};1H➤ ", end='')
                    # Move cursor back to navigation help line
                    print(f"\033[{header_lines + len(languages) + 2};1H", end='')
                    sys.stdout.flush()

    def show_main_menu(self):
        clear_console()
        print("\n" + "="*50)
        print(f"{self.strings['title']}".center(50))
        print("="*50 + "\n")
        
        print(f"{self.strings['record_new_agent']}")
        print(f"{self.strings['save_exit']}\n")
        print("-"*50 + "\n")
        
        if len(self.config["keybinds"]) > 0:
            for agent_name, data in self.config["keybinds"].items():
                key = format_key(data.get("key", "Not set"))
                agent_data = self.agents_data[agent_name]
                print(f"{agent_data['emoji']} {agent_data['name']}: hold {key}")
            print("")
            print("-"*50 + "\n")
            print(self.strings['macro_ready'])
        

    def cancel_recording(self):
        if self.recording_mode:
            print(f"\n{self.strings['recording_cancelled']}")
            self.recording_mode = False
            self.recording_state = None
            self.current_agent_name = None
            self.agent_selection_index = 0
            time.sleep(1)
            self.show_main_menu()

    def select_agent(self):
        clear_console()
        print("\n" + "-"*50)
        print(f"{self.strings['recording_new_agent']}")
        print("-"*50)
        print(f"{self.strings['select_agent']}")
        print(f"{self.strings['navigation_help']}")
        print("-"*50 + "\n")
        
        for i, agent_key in enumerate(VALORANT_AGENTS):
            agent_data = self.agents_data[agent_key]
            if i == self.agent_selection_index:
                print(f"➤ {agent_data['emoji']} {agent_data['name']}")
            else:
                print(f"  {agent_data['emoji']} {agent_data['name']}")
        
        self._last_display_count = len(VALORANT_AGENTS)

    def show_agent_selection(self):
        if hasattr(self, '_last_display_count'):
            for _ in range(self._last_display_count):
                print('\033[F\033[K', end='')
        
        for i, agent_key in enumerate(VALORANT_AGENTS):
            agent_data = self.agents_data[agent_key]
            if i == self.agent_selection_index:
                print(f"➤ {agent_data['emoji']} {agent_data['name']}")
            else:
                print(f"  {agent_data['emoji']} {agent_data['name']}")
        
        self._last_display_count = len(VALORANT_AGENTS)

    def update_registered_keys(self):
        self.registered_keys.clear()
        if "keybinds" in self.config:
            for agent_data in self.config["keybinds"].values():
                if "key_obj" in agent_data:
                    self.registered_keys.add(agent_data["key_obj"])

    def load_config(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    
                    # Ensure delays exist with default values
                    if "delays" not in data:
                        data["delays"] = { "click_interval": 0.05, "loop_interval": 0.05 }
                    
                    # Convert key strings to key objects for keybinds
                    if "keybinds" in data:
                        for agent in data["keybinds"].values():
                            if "key" in agent:
                                key_str = agent["key"]
                                try:
                                    if key_str.startswith("Key."):
                                        agent["key_obj"] = getattr(keyboard.Key, key_str[4:])
                                    else:
                                        agent["key_obj"] = keyboard.KeyCode.from_char(key_str.replace("'", ""))
                                except:
                                    continue
                        print(self.strings["agents_loaded"].format(len(data["keybinds"])))
                    return data
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
        return {
            "language": None,
            "confirmation_button": {"position": None},
            "margin_of_error": { "agent": [20, 20], "confirm": [60, 20] },
            "delays": { "click_interval": 0.03, "loop_interval": 0.05 },
            "keybinds": {}
        }

    def save_config(self):
        try:
            serializable_data = {
                "language": self.language,
                "confirmation_button": {
                    "position": self.config["confirmation_button"]["position"]
                },
                "margin_of_error": self.config.get("margin_of_error", { "agent": [20, 20], "confirm": [60, 20] }),
                "delays": self.config.get("delays", { "click_interval": 0.03, "loop_interval": 0.05}),
                "keybinds": {}
            }
            
            for agent_name, data in self.config["keybinds"].items():
                serializable_data["keybinds"][agent_name] = {
                    "key": data.get("key", None),
                    "position": data.get("position", None)
                }

            with open(self.save_file, "w") as f:
                json.dump(serializable_data, f, indent=2)
            print(f"{self.strings['settings_saved']}")
            self.update_registered_keys()
        except Exception as e:
            print(f"⚠️ Error saving config: {e}")  # Generic error message independent of language strings

    def signal_handler(self, signum, frame):
        clear_console()
        print("\n" + "-"*50)
        print(f"{self.strings['saving_closing']}")
        self.save_config()
        self.running = False
        self.macro_active = False
        if self.macro_thread and self.macro_thread.is_alive():
            self.macro_thread.join(timeout=0.5)
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        print(f"{self.strings['goodbye']}")
        print("-"*50 + "\n")
        sys.stdout.flush()

    def start_listening(self):
        self.show_main_menu()
        
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.signal_handler(None, None)

    def on_mouse_click(self, x, y, button, pressed):
        pass

    def on_key_press(self, key):
        """
        Handle key press events for macro activation and recording.
        
        Args:
            key: The key that was pressed
        """
        try:
            if key == keyboard.Key.esc and self.recording_mode:
                self.cancel_recording()
                return

            if key in {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                      keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
                      keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r,
                      keyboard.Key.f1, keyboard.Key.space}:
                self.pressed_keys.add(key)
                
                # Handle F1 key for recording mode
                if key == keyboard.Key.f1:
                    self.recording_mode = True
                    self.recording_state = "agent_select"
                    self.select_agent()
                    return
                
                # Handle space key during recording
                if key == keyboard.Key.space and self.recording_mode:
                    if self.recording_state == "position":
                        x, y = pyautogui.position()
                        self.config["keybinds"][self.current_agent_name]["position"] = [x, y]
                        print(f"\n{self.strings['agent_position_recorded'].format([x, y])}")
                    elif self.config["confirmation_button"]["position"] is None:
                        print(f"{self.strings['move_to_confirm']}")
                        self.recording_state = "confirm"
                        x, y = pyautogui.position()
                        self.config["confirmation_button"]["position"] = [x, y]
                        print(f"\n{self.strings['confirm_position_recorded'].format([x, y])}")
                        
                    self.save_config()
                    agent_name = self.agents_data[self.current_agent_name]["name"]
                    print(f"{self.strings['agent_configured'].format(agent_name)}")
                    self.recording_mode = False
                    self.recording_state = None
                    self.current_agent_name = None
                    time.sleep(1)
                    self.show_main_menu()
                    return
                return

            # Handle agent selection during recording
            if self.recording_mode and self.recording_state == "agent_select":
                if key == keyboard.Key.up:
                    self.agent_selection_index = (self.agent_selection_index - 1) % len(VALORANT_AGENTS)
                    self.show_agent_selection()
                elif key == keyboard.Key.down:
                    self.agent_selection_index = (self.agent_selection_index + 1) % len(VALORANT_AGENTS)
                    self.show_agent_selection()
                elif key == keyboard.Key.enter:
                    self.current_agent_name = VALORANT_AGENTS[self.agent_selection_index]
                    agent_emoji = self.agents_data[self.current_agent_name]["emoji"]
                    agent_name = self.agents_data[self.current_agent_name]["name"]
                    agent_full_name = f"{agent_emoji} {agent_name}"
                    print(f"\n{self.strings['selected_agent'].format(agent_full_name)}")
                    print(f"\n{self.strings['press_bind_key']}")
                    self.recording_state = "key"
                return
            
            # Handle key binding during recording
            if self.recording_mode and self.recording_state == "key":
                if isinstance(key, keyboard.Key):
                    key_str = f"Key.{key.name}"
                else:
                    key_str = str(key)
                
                if "keybinds" not in self.config:
                    self.config["keybinds"] = {}
                
                self.config["keybinds"][self.current_agent_name] = {
                    "key": key_str,
                    "key_obj": key,
                    "position": None
                }
                print(f"\n{self.strings['key_bound'].format(key_str)}")
                print(f"{self.strings['move_to_position']}")
                self.recording_state = "position"
                self.update_registered_keys()
                return
            
            # Handle macro activation
            if key in self.registered_keys and not self.macro_active:
                for agent_name, data in self.config["keybinds"].items():
                    if data.get("key_obj") == key:
                        self.macro_active = True
                        self.macro_thread = threading.Thread(
                            target=self.run_macro,
                            args=(data["position"], self.config["confirmation_button"]["position"])
                        )
                        self.macro_thread.start()
                        break
            
        except Exception as e:
            print(f"{self.strings['fatal_error'].format(e)}")

    def on_key_release(self, key):
        try:
            if key in self.pressed_keys:
                self.pressed_keys.discard(key)
            
            if key in self.registered_keys:
                for agent_name, data in self.config["keybinds"].items():
                    if data.get("key_obj") == key:
                        self.macro_active = False
                        if self.macro_thread and self.macro_thread.is_alive():
                            self.macro_thread.join()
                        break
        except Exception as e:
            print(f"{self.strings['fatal_error'].format(e)}")

    def run_macro(self, agent_position, confirm_position):
        """
        Execute the instalock macro functionality.
        
        Args:
            agent_position (list): [x, y] coordinates for agent selection
            confirm_position (list): [x, y] coordinates for confirmation button
        """
        if not agent_position or not confirm_position:
            print(f"{self.strings['position_not_set']}")
            self.macro_active = False
            return

        # Get configuration values with defaults
        click_interval = self.config.get("delays", {}).get("click_interval", 0.03)
        loop_interval = self.config.get("delays", {}).get("loop_interval", 0.05)
        margin_of_error = self.config.get("margin_of_error", { "agent": [20, 20], "confirm": [60, 20] })

        while self.macro_active and self.running:
            # Add randomization to click positions to avoid detection
            agent_x = agent_position[0] + random.randint(0, margin_of_error["agent"][0])
            agent_y = agent_position[1] + random.randint(0, margin_of_error["agent"][1])
            confirm_x = confirm_position[0] + random.randint(0, margin_of_error["confirm"][0])
            confirm_y = confirm_position[1] + random.randint(0, margin_of_error["confirm"][1])

            # Execute click sequence
            pyautogui.click(agent_x, agent_y)
            time.sleep(click_interval)
            pyautogui.click(confirm_x, confirm_y)
            time.sleep(loop_interval)

def main():
    try:
        macro = InstalockMacro()
        macro.start_listening()
    except Exception as e:
        print(f"\n⚠️ Fatal error: {e}")  # Generic error message
        sys.exit(1)

if __name__ == "__main__":
    main() 