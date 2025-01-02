from pynput import keyboard
import time
import threading
import pyautogui

from .language import VALORANT_AGENTS
from .console import clear_console, show_main_menu, show_agent_selection
from .settings import save_config, update_registered_keys

def on_key_press(macro):
    """
    Handle key press events for macro activation and recording.
    """
    try:
        key = macro.keyboard_listener.key
        if key == keyboard.Key.esc and macro.recording_mode:
            macro.cancel_recording()
            return True

        if key in {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                  keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
                  keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r,
                  keyboard.Key.f1, keyboard.Key.space}:
            macro.pressed_keys.add(key)
            
            # Handle F1 key for recording mode
            if key == keyboard.Key.f1:
                macro.recording_mode = True
                macro.recording_state = "agent_select"
                show_agent_selection(macro.agents_data, macro.agent_selection_index, macro.strings)
                return True
            
            # Handle space key during recording
            if key == keyboard.Key.space and macro.recording_mode:
                if macro.recording_state == "position":
                    x, y = pyautogui.position()
                    macro.config["keybinds"][macro.current_agent_name]["position"] = [x, y]
                    print(f"\n{macro.strings['agent_position_recorded'].format([x, y])}")
                elif macro.config["confirmation_button"]["position"] is None:
                    print(f"{macro.strings['move_to_confirm']}")
                    macro.recording_state = "confirm"
                    x, y = pyautogui.position()
                    macro.config["confirmation_button"]["position"] = [x, y]
                    print(f"\n{macro.strings['confirm_position_recorded'].format([x, y])}")
                    
                save_config(macro)
                agent_name = macro.agents_data[macro.current_agent_name]["name"]
                print(f"{macro.strings['agent_configured'].format(agent_name)}")
                macro.recording_mode = False
                macro.recording_state = None
                macro.current_agent_name = None
                time.sleep(1)
                show_main_menu(macro.strings, macro.config, macro.agents_data)
                return True
            return True

        # Handle agent selection during recording
        if macro.recording_mode:
            if key == keyboard.Key.up:
                macro.agent_selection_index = (macro.agent_selection_index - 1) % len(VALORANT_AGENTS)
                show_agent_selection(macro.agents_data, macro.agent_selection_index, macro.strings)
                return True
            elif key == keyboard.Key.down:
                macro.agent_selection_index = (macro.agent_selection_index + 1) % len(VALORANT_AGENTS)
                show_agent_selection(macro.agents_data, macro.agent_selection_index, macro.strings)
                return True
            elif key == keyboard.Key.enter:
                macro.current_agent_name = VALORANT_AGENTS[macro.agent_selection_index]
                agent_emoji = macro.agents_data[macro.current_agent_name]["emoji"]
                agent_name = macro.agents_data[macro.current_agent_name]["name"]
                agent_full_name = f"{agent_emoji} {agent_name}"
                print(f"\n{macro.strings['selected_agent'].format(agent_full_name)}")
                print(f"\n{macro.strings['press_bind_key']}")
                macro.recording_state = "key"
                return True

        # Handle key binding during recording
        if macro.recording_mode and macro.recording_state == "key":
            if isinstance(key, keyboard.Key):
                key_str = f"Key.{key.name}"
            else:
                key_str = str(key)
            
            if "keybinds" not in macro.config:
                macro.config["keybinds"] = {}
            
            macro.config["keybinds"][macro.current_agent_name] = {
                "key": key_str,
                "key_obj": key,
                "position": None
            }
            print(f"\n{macro.strings['key_bound'].format(key_str)}")
            print(f"{macro.strings['move_to_position']}")
            macro.recording_state = "position"
            update_registered_keys(macro)
            return True
        
        # Handle macro activation
        if key in macro.registered_keys:
            for agent_name, data in macro.config["keybinds"].items():
                if data.get("key_obj") == key:
                    macro.key_held = True  # Marca que a tecla está sendo segurada
                    if not macro.macro_active:
                        macro.macro_active = True
                        macro.macro_thread = threading.Thread(
                            target=macro.run_macro,
                            args=(data["position"], macro.config["confirmation_button"]["position"])
                        )
                        macro.macro_thread.start()
                    break
        
    except Exception as e:
        print(f"{macro.strings['fatal_error'].format(e)}")
        return False

    return True  # Important: return True to keep the listener running

def on_key_release(macro):
    try:
        key = macro.keyboard_listener.key
        if key in macro.pressed_keys:
            macro.pressed_keys.discard(key)
        
        if key in macro.registered_keys:
            macro.key_held = False  # Marca que a tecla foi solta
            macro.macro_active = False
            if macro.macro_thread and macro.macro_thread.is_alive():
                macro.macro_thread.join(timeout=0.1)
    except Exception as e:
        print(f"{macro.strings['fatal_error'].format(e)}")