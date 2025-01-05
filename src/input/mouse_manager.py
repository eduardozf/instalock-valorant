import pyautogui
import random
from typing import Tuple, Dict

class MouseManager:
    def __init__(self):
        self.default_pause = pyautogui.PAUSE
        self.default_failsafe = pyautogui.FAILSAFE
    
    def perform_click(self):
        """Execute selection using F key and pyautogui for optimized speed"""
        try:
            # Disable pyautogui safety nets temporarily
            pyautogui.PAUSE = 0.01
            pyautogui.FAILSAFE = False

            # Execute F + Click without any delays
            pyautogui.press('f')
            pyautogui.click()

            # Restore safety nets
            pyautogui.PAUSE = self.default_pause
            pyautogui.FAILSAFE = self.default_failsafe
            
        except Exception:
            # Fallback to just click if the optimized method fails
            try:
                pyautogui.click()
            except:
                pass
    
    def get_current_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return pyautogui.position()
    
    def move_and_click(self, position: Tuple[int, int], margin_of_error: Dict[str, int]):
        """Move to position with random offset and click."""
        try:
            x = position[0] + random.randrange(margin_of_error[0] + 1)
            y = position[1] + random.randrange(margin_of_error[1] + 1)
            pyautogui.moveTo(x, y)
            self.perform_click()
        except Exception:
            pass
    
    def run_macro_sequence(self, agent_position: Tuple[int, int], confirm_position: Tuple[int, int], margin_of_error: Dict[str, Dict[str, int]]):
        """Run the complete macro sequence."""
        if not agent_position or not confirm_position:
            return False
        
        try:
            # Move to agent position and click
            self.move_and_click(agent_position, margin_of_error["agent"])
            
            # Move to confirm position and click
            self.move_and_click(confirm_position, margin_of_error["confirm"])
            
            return True
        except Exception:
            return False 