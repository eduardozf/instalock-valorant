from pynput import keyboard
import threading
import time
import pyautogui

class KeyManager:
    def __init__(self, macro):
        self.macro = macro
        self.pressed_keys = set()
        self.registered_keys = set()
        self.key_held = False
        self.setup_listeners()
        
    def setup_listeners(self):
        """Setup keyboard listeners with handlers."""
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
    
    def start_listening(self):
        """Start the keyboard listener."""
        self.keyboard_listener.start()
    
    def stop_listening(self):
        """Stop the keyboard listener."""
        self.keyboard_listener.stop()
    
    def handle_menu_key(self, key: keyboard.Key) -> bool:
        """Handle menu navigation keys."""
        if not self.macro.recording_mode and key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.enter, keyboard.Key.esc]:
            if self.macro.menu_manager.current_menu == "main":
                menu_options = self.macro.menu_manager.show_main_menu(self.macro.config_manager.config)
                
                if key == keyboard.Key.up:
                    self.macro.menu_manager.selected_index = (self.macro.menu_manager.selected_index - 1) % len(menu_options)
                    self.macro.menu_manager.show_main_menu(self.macro.config_manager.config)
                elif key == keyboard.Key.down:
                    self.macro.menu_manager.selected_index = (self.macro.menu_manager.selected_index + 1) % len(menu_options)
                    self.macro.menu_manager.show_main_menu(self.macro.config_manager.config)
                elif key == keyboard.Key.enter:
                    self.macro.menu_manager.handle_main_menu_selection(self.macro)
            return True
        return False
    
    def handle_recording_key(self, key: keyboard.Key) -> bool:
        """Handle keys during recording mode."""
        if key == keyboard.Key.esc and self.macro.recording_mode:
            self.macro.recording_mode = False
            self.macro.recording_state = None
            self.macro.current_agent_name = None
            print(f"\n{self.macro.strings['recording_cancelled']}")
            time.sleep(1)
            self.macro.menu_manager.show_main_menu(self.macro.config_manager.config)
            return True
            
        if key == keyboard.Key.delete and self.macro.recording_mode and self.macro.recording_state == "agent_select":
            agent_name = list(self.macro.agents_data.keys())[self.macro.menu_manager.selected_index]
            if self.macro.config_manager.unbind_agent(agent_name, self.macro):
                print(f"\n{self.macro.strings['agent_unbound']}")
                self.macro.menu_manager.show_agent_selection(self.macro.agents_data, self.macro.config_manager.config)
            return True
            
        return False
    
    def handle_special_keys(self, key: keyboard.Key) -> bool:
        """Handle special keys like Ctrl, Shift, Alt, F1, Space."""
        special_keys = {
            keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
            keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
            keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r,
            keyboard.Key.f1, keyboard.Key.space
        }
        
        if key in special_keys:
            self.pressed_keys.add(key)
            
            if key == keyboard.Key.f1 and self.macro.menu_manager.current_menu == "main":
                self.macro.recording_mode = True
                self.macro.recording_state = "agent_select"
                self.macro.menu_manager.show_agent_selection(self.macro.agents_data, self.macro.config_manager.config)
                return True
            
            if key == keyboard.Key.space and self.macro.recording_mode:
                return self.handle_space_key()
                
            return True
        return False
    
    def handle_space_key(self) -> bool:
        """Handle space key during recording."""
        if self.macro.recording_state == "position":
            x, y = pyautogui.position()
            self.macro.config_manager.config["keybinds"][self.macro.current_agent_name]["position"] = [x, y]
            print(f"\n{self.macro.strings['agent_position_recorded'].format([x, y])}")
        elif self.macro.config_manager.config["confirmation_button"]["position"] is None:
            print(f"{self.macro.strings['move_to_confirm']}")
            self.macro.recording_state = "confirm"
            x, y = pyautogui.position()
            self.macro.config_manager.config["confirmation_button"]["position"] = [x, y]
            print(f"\n{self.macro.strings['confirm_position_recorded'].format([x, y])}")
            
        self.macro.config_manager.save_config(self.macro)
        agent_name = self.macro.agents_data[self.macro.current_agent_name]["name"]
        print(f"{self.macro.strings['agent_configured'].format(agent_name)}")
        self.macro.recording_mode = False
        self.macro.recording_state = None
        self.macro.current_agent_name = None
        time.sleep(1)
        self.macro.menu_manager.show_main_menu(self.macro.config_manager.config)
        return True
    
    def handle_agent_selection(self, key: keyboard.Key) -> bool:
        """Handle key events during agent selection."""
        if not self.macro.recording_mode or self.macro.recording_state != "agent_select":
            return False
            
        if key == keyboard.Key.up:
            self.macro.menu_manager.selected_index = (self.macro.menu_manager.selected_index - 1) % len(self.macro.agents_data)
            self.macro.menu_manager.show_agent_selection(self.macro.agents_data, self.macro.config_manager.config)
            return True
        elif key == keyboard.Key.down:
            self.macro.menu_manager.selected_index = (self.macro.menu_manager.selected_index + 1) % len(self.macro.agents_data)
            self.macro.menu_manager.show_agent_selection(self.macro.agents_data, self.macro.config_manager.config)
            return True
        elif key == keyboard.Key.enter:
            agent_keys = list(self.macro.agents_data.keys())
            self.macro.current_agent_name = agent_keys[self.macro.menu_manager.selected_index]
            agent_emoji = self.macro.agents_data[self.macro.current_agent_name]["emoji"]
            agent_name = self.macro.agents_data[self.macro.current_agent_name]["name"]
            agent_full_name = f"{agent_emoji} {agent_name}"
            print(f"\n{self.macro.strings['selected_agent'].format(agent_full_name)}")
            print(f"\n{self.macro.strings['press_bind_key']}")
            self.macro.recording_state = "key"
            return True
            
        return False
    
    def handle_key_binding(self, key: keyboard.Key) -> bool:
        """Handle key binding during recording."""
        if not self.macro.recording_mode or self.macro.recording_state != "key":
            return False
            
        if isinstance(key, keyboard.Key):
            key_str = f"Key.{key.name}"
        else:
            key_str = str(key)
        
        if "keybinds" not in self.macro.config_manager.config:
            self.macro.config_manager.config["keybinds"] = {}
        
        self.macro.config_manager.config["keybinds"][self.macro.current_agent_name] = {
            "key": key_str,
            "key_obj": key,
            "position": None
        }
        print(f"\n{self.macro.strings['key_bound'].format(key_str)}")
        print(f"{self.macro.strings['move_to_position']}")
        self.macro.recording_state = "position"
        self.macro.config_manager.update_registered_keys(self.macro)
        return True
    
    def handle_macro_activation(self, key: keyboard.Key) -> bool:
        """Handle macro activation when in macro menu."""
        if self.macro.menu_manager.current_menu == "macro" and key in self.registered_keys:
            for agent_name, data in self.macro.config_manager.config["keybinds"].items():
                if data.get("key_obj") == key:
                    self.key_held = True
                    if not self.macro.macro_active:
                        self.macro.macro_active = True
                        self.macro.macro_thread = threading.Thread(
                            target=self.macro.execute_macro,
                            args=(data["position"], self.macro.config_manager.config["confirmation_button"]["position"])
                        )
                        self.macro.macro_thread.start()
                    break
            return True
        return False
    
    def on_key_press(self, key):
        """Handle key press events."""
        try:
            self.keyboard_listener.key = key
            
            if (self.handle_menu_key(key) or
                self.handle_recording_key(key) or
                self.handle_special_keys(key) or
                self.handle_agent_selection(key) or
                self.handle_key_binding(key) or
                self.handle_macro_activation(key)):
                return True
                
        except Exception as e:
            print(f"{self.macro.strings['fatal_error'].format(e)}")
            return False
            
        return True
    
    def on_key_release(self, key):
        """Handle key release events."""
        try:
            self.keyboard_listener.key = key
            if key in self.pressed_keys:
                self.pressed_keys.discard(key)
            
            if key in self.registered_keys:
                self.key_held = False
                self.macro.macro_active = False
                if self.macro.macro_thread and self.macro.macro_thread.is_alive():
                    self.macro.macro_thread.join(timeout=0.1)
        except Exception as e:
            print(f"{self.macro.strings['fatal_error'].format(e)}") 