import signal
import sys

class SignalManager:
    def __init__(self, macro):
        self.macro = macro
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
    
    def handle_signal(self, signum, frame):
        """Handle application shutdown gracefully."""
        print("\n" + "-"*50)
        print(f"{self.macro.strings['saving_closing']}")
        self.macro.config_manager.save_config(self.macro)
        self.macro.running = False
        self.macro.macro_active = False
        if self.macro.macro_thread and self.macro.macro_thread.is_alive():
            self.macro.macro_thread.join(timeout=0.5)
        self.macro.key_manager.stop_listening()
        print(f"{self.macro.strings['goodbye']}")
        print("-"*50 + "\n")
        sys.stdout.flush() 