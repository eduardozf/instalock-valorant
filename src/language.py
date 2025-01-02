import json
from typing import Dict, Any
import msvcrt
import sys

from .console import clear_console
from .settings import save_config

def load_languages() -> Dict[str, Any]:
    """
    Load language configurations from languages.json file.
    Returns a dictionary with language settings or empty dict if file not found.
    """
    try:
        with open('./src/languages.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Error loading languages: {e}")
        return {}
      
def load_or_select_language(macro):
        if macro.config.get("language") and macro.config["language"] in LANGUAGES:
            return macro.config["language"]
        
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
                    macro.config["language"] = selected_lang
                    save_config(macro)
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

# Load language data and define constants
LANGUAGES = load_languages()
VALORANT_AGENTS = list(LANGUAGES["en_US"]["agents"].keys()) 