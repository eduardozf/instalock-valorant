import random
import time
import win32api
import win32con
import pyautogui

from .settings import DEFAULT_HOLD_TIME

def easeOutQuad(x):
    return 1 - (1 - x) * (1 - x)

def easeInOutQuad(x):
    return 2 * x * x if x < 0.5 else 1 - pow(-2 * x + 2, 2) / 2

def human_mouse_move(start_x, start_y, end_x, end_y, duration):
    """
    Move the mouse in a more human-like way with irregular movements.
    """
    pyautogui.PAUSE = 0  # Remove delay between movements
    
    # Calculate total distance
    distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
    
    # Adjust step based on distance
    step = max(distance / 100, 1)
    steps = int(distance / step)
    
    # Calculate time per step to match total duration
    time_per_step = duration / steps if steps > 0 else duration
    start_time = time.time()
    
    # Generate a smooth curve
    for i in range(steps):
        progress = i / steps
        
        # Apply smooth curve to movement
        if progress <= 0.5:
            ease = 2 * progress * progress
        else:
            progress = progress - 1
            ease = 1 - 2 * progress * progress
            
        current_x = start_x + (end_x - start_x) * ease
        current_y = start_y + (end_y - start_y) * ease
        
        # Add small random variation
        current_x += random.uniform(-2, 2)
        current_y += random.uniform(-2, 2)
        
        pyautogui.moveTo(int(current_x), int(current_y))
        
        # Wait for the appropriate time to maintain duration
        elapsed = time.time() - start_time
        expected_time = (i + 1) * time_per_step
        if expected_time > elapsed:
            time.sleep(expected_time - elapsed)
    
    # Ensure reaching destination
    pyautogui.moveTo(end_x, end_y)
    
    # Make sure total duration is respected
    total_elapsed = time.time() - start_time
    if total_elapsed < duration:
        time.sleep(duration - total_elapsed)
        
    pyautogui.PAUSE = 0.1  # Restore default delay

def perform_click():
    """Execute a click using win32api"""
    try:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(random.uniform(DEFAULT_HOLD_TIME["min"], DEFAULT_HOLD_TIME["max"]))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    except:
        pass  # Ignore click errors to not interrupt the macro 
