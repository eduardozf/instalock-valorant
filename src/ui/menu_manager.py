import os
from typing import List, Tuple, Dict, Any, Callable
from pynput import keyboard

from core.interfaces import IMenuController

def clear_console():
    """Clear the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_key(key_str: str) -> str:
    """Format key string for display in the UI."""
    if key_str.startswith("Key."):
        return key_str[4:].upper()
    return key_str.replace("'", "")

class MenuManager(IMenuController):
    def __init__(self, strings: Dict[str, str]):
        self.strings = strings
        self.selected_index = 0
        self.current_menu = "main"

    def show_menu(self, menu_type: str, **kwargs) -> None:
        """Show the specified menu type with given arguments."""
        if menu_type == "main":
            return self.show_main_menu(kwargs.get("config", {}))
        elif menu_type == "macro_status":
            return self.show_macro_status(kwargs.get("config", {}), kwargs.get("agents", {}))
        elif menu_type == "agent_selection":
            return self.show_agent_selection(kwargs.get("agents", {}), kwargs.get("config", {}))
        elif menu_type == "language_selection":
            return self.show_language_selection(kwargs.get("languages", {}))

    def handle_navigation(self, key: Any) -> bool:
        """Handle navigation input for the current menu."""
        if isinstance(key, keyboard.Key):
            if key in [keyboard.Key.up, keyboard.Key.down]:
                old_index = self.selected_index
                if key == keyboard.Key.up:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_options)
                else:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_options)
                return old_index != self.selected_index
            elif key == keyboard.Key.enter:
                return True
        return False

    def handle_menu_navigation(self, key: keyboard.Key, macro) -> None:
        """Handle menu navigation with arrow keys."""
        if self.current_menu == "main":
            menu_options = self.show_main_menu(macro.config_manager.config)
            
            if key == keyboard.Key.up or key == keyboard.Key.down:
                needs_redraw = self.handle_navigation(key)
                if needs_redraw:
                    self.show_main_menu(macro.config_manager.config)
            elif key == keyboard.Key.enter:
                self.handle_main_menu_selection(macro)
        elif key == keyboard.Key.esc and self.current_menu in ["macro", "description"]:
            self.current_menu = "main"
            self.show_main_menu(macro.config_manager.config)
        elif key == keyboard.Key.enter and self.current_menu == "description":
            self.current_menu = "main"
            self.show_main_menu(macro.config_manager.config)

    def handle_main_menu_selection(self, macro) -> None:
        """Handle main menu option selection."""
        menu_options = [
            ("🎯", self.strings["menu_record_agent"]),
            ("🔄", self.strings["menu_refresh_settings"])
        ]
        
        if macro.config_manager.config and macro.config_manager.config.get("keybinds") and len(macro.config_manager.config["keybinds"]) > 0:
            menu_options.insert(1, ("🎮", self.strings["menu_start_macro"]))
        
        selected_option = menu_options[self.selected_index][1]
        
        if selected_option == self.strings["menu_record_agent"]:
            macro.recording_mode = True
            macro.recording_state = "agent_select"
            self.show_agent_selection(macro.agents_data, macro.config_manager.config)
        elif selected_option == self.strings["menu_start_macro"]:
            self.current_menu = "macro"
            self.show_macro_status(macro.config_manager.config, macro.agents_data)
        elif selected_option == self.strings["menu_refresh_settings"]:
            macro.config_manager.config = macro.config_manager.load_config()
            macro.config_manager.update_registered_keys(macro)
            self.show_main_menu(macro.config_manager.config)

    def show_main_menu(self, config: dict) -> List[Tuple[str, str]]:
        """Display the main menu with selectable options."""
        clear_console()
        print("\n" + "="*50)
        print(f"{self.strings['title']}".center(50))
        print("="*50 + "\n")
        
        menu_options = [
            ("🎯", self.strings["menu_record_agent"]),
            ("🔄", self.strings["menu_refresh_settings"])
        ]
        
        if config and config.get("keybinds") and len(config["keybinds"]) > 0:
            menu_options.insert(1, ("🎮", self.strings["menu_start_macro"]))
        
        for i, (emoji, text) in enumerate(menu_options):
            print(f"{'➤ ' if i == self.selected_index else '  '}{emoji} {text}")
        
        print(f"\n{self.strings['menu_navigation']}")
        print("-"*50 + "\n")
        
        self.menu_options = menu_options
        return menu_options

    def show_macro_status(self, config: dict, agents_data: dict) -> None:
        """Display the macro status with configured agents."""
        clear_console()
        print("\n" + "="*50)
        print(f"{self.strings['title']}".center(50))
        print("="*50 + "\n")
        
        print(f"{self.strings['macro_running']}")
        print(f"{self.strings['press_esc_exit']}\n")
        print("-"*50 + "\n")
        
        if len(config["keybinds"]) > 0:
            for agent_name, data in config["keybinds"].items():
                key = format_key(data.get("key", "Not set"))
                agent_data = agents_data[agent_name]
                print(f"{agent_data['emoji']} {agent_data['name']}: hold {key}")
            print("")
            print("-"*50)
            print(f"\n{self.strings['macro_ready']}")

    def show_agent_selection(self, agents_data: dict, config: dict) -> List[Tuple[str, Dict[str, Any]]]:
        """Display the agent selection menu."""
        clear_console()
        print("\n" + "-"*70)
        print(f"{self.strings['recording_new_agent']}")
        print("-"*70)
        print(f"{self.strings['select_agent']}")
        print(f"{self.strings['navigation_help']}{self.strings['press_delete_unbind']}")
        print("-"*70 + "\n")
        
        agents_list = list(agents_data.items())
        
        for i, (agent_key, agent_data) in enumerate(agents_list):
            bound_key = ""
            if "keybinds" in config and agent_key in config["keybinds"]:
                key = format_key(config["keybinds"][agent_key].get("key", ""))
                bound_key = f" {self.strings['agent_bound_to'].format(key=key)}"
                
            if i == self.selected_index:
                print(f"➤ {agent_data['emoji']} {agent_data['name']}{bound_key}")
            else:
                print(f"  {agent_data['emoji']} {agent_data['name']}{bound_key}")
        
        self.menu_options = agents_list
        return agents_list

    def show_language_selection(self, languages: Dict[str, Dict[str, Any]]) -> List[Tuple[str, Dict[str, Any]]]:
        """Display the language selection menu."""
        clear_console()
        print("\n" + "="*70)
        print("🌐 Select your language / Selecione seu idioma / 选择语言".center(50))
        print("="*70 + "\n")
        
        languages_list = list(languages.items())
        
        for i, (lang_code, lang_data) in enumerate(languages_list):
            print(f"{'➤ ' if i == self.selected_index else '  '}{lang_data['flag']} {lang_data['name']}")
        
        print("\n↑/↓: Navigate/Navegar/导航 | Enter: Select/Selecionar/选择")
        
        self.menu_options = languages_list
        return languages_list 