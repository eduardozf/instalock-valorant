from typing import Tuple

class MacroExecutor:
    """
    Handles the execution of the macro functionality.
    Responsible for moving the mouse and clicking at specified positions.
    """
    def __init__(self, mouse_manager, config_manager):
        self.mouse_manager = mouse_manager
        self.config_manager = config_manager
        self.running = True
        self.active = False
        self.thread = None

    def execute_macro(self, agent_position: Tuple[int, int], confirm_position: Tuple[int, int]) -> None:
        """
        Execute the macro sequence by moving to agent position and confirm position.
        
        Args:
            agent_position: The (x, y) coordinates of the agent button
            confirm_position: The (x, y) coordinates of the confirm button
        """
        if not agent_position or not confirm_position:
            return

        try:
            # Get margin of error settings from config
            margin_of_error = self.config_manager.get_config("margin_of_error")

            # Run the macro sequence
            self.mouse_manager.run_macro_sequence(
                agent_position,
                confirm_position,
                margin_of_error
            )
        except Exception as e:
            print(f"⚠️  Error executing macro: {e}")
            
    def stop_macro(self) -> None:
        """Stop the macro execution."""
        self.running = False
        self.active = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=0.1) 