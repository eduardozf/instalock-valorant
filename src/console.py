import os
import msvcrt
import sys

def clear_console():
    """Clear the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_key(key_str: str) -> str:
    """Format key string for display in the UI."""
    if key_str.startswith("Key."):
        return key_str[4:].upper()
    return key_str.replace("'", "")

def show_language_selection(languages: dict, selected_index: int) -> None:
    """Display the language selection menu."""
    clear_console()
    print("\n" + "="*70)
    print("🌐 Select your language / Selecione seu idioma / 选择语言".center(50))
    print("="*70 + "\n")
    
    languages_list = list(languages.items())
    menu_height = len(languages_list) + 3
    header_lines = 5
    
    for i, (lang_code, lang_data) in enumerate(languages_list):
        print(f"{'➤ ' if i == selected_index else '  '}{lang_data['flag']} {lang_data['name']}")
    
    print("\n↑/↓: Navigate/Navegar/导航 | Enter: Select/Selecionar/选择")
    return menu_height, header_lines

def show_main_menu(strings: dict, config: dict, agents_data: dict) -> None:
    """Display the main menu of the application."""
    clear_console()
    print("\n" + "="*50)
    print(f"{strings['title']}".center(50))
    print("="*50 + "\n")
    
    print(f"{strings['record_new_agent']}")
    print(f"{strings['save_exit']}\n")
    print("-"*50 + "\n")
    
    if len(config["keybinds"]) > 0:
        for agent_name, data in config["keybinds"].items():
            key = format_key(data.get("key", "Not set"))
            agent_data = agents_data[agent_name]
            print(f"{agent_data['emoji']} {agent_data['name']}: hold {key}")
        print("")
        print("-"*50 + "\n")
        print(strings['macro_ready'])

def show_agent_selection(agents_data: dict, agent_selection_index: int, strings: dict) -> None:
    """Display the agent selection menu."""
    clear_console()
    print("\n" + "-"*50)
    print(f"{strings['recording_new_agent']}")
    print("-"*50)
    print(f"{strings['select_agent']}")
    print(f"{strings['navigation_help']}")
    print("-"*50 + "\n")
    
    for i, agent_key in enumerate(agents_data.keys()):
        agent_data = agents_data[agent_key]
        if i == agent_selection_index:
            print(f"➤ {agent_data['emoji']} {agent_data['name']}")
        else:
            print(f"  {agent_data['emoji']} {agent_data['name']}")
    
    return len(agents_data) 