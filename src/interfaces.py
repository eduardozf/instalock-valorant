from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class IConfigProvider(ABC):
    @abstractmethod
    def get_config(self, key: str) -> Any:
        pass

    @abstractmethod
    def save_config(self) -> None:
        pass

class IKeyHandler(ABC):
    @abstractmethod
    def handle_key(self, key: Any) -> bool:
        pass

class IMouseController(ABC):
    @abstractmethod
    def move_and_click(self, position: Tuple[int, int], margin: Dict[str, int]) -> None:
        pass

    @abstractmethod
    def get_current_position(self) -> Tuple[int, int]:
        pass

class IMenuController(ABC):
    @abstractmethod
    def show_menu(self, menu_type: str, **kwargs) -> None:
        pass

    @abstractmethod
    def handle_navigation(self, key: Any) -> bool:
        pass

class IMacroState(ABC):
    @abstractmethod
    def enter(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def handle_input(self, key: Any) -> bool:
        pass

class IMacroExecutor(ABC):
    @abstractmethod
    def start_macro(self, agent_position: Tuple[int, int], confirm_position: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def stop_macro(self) -> None:
        pass

class ILanguageProvider(ABC):
    @abstractmethod
    def get_string(self, key: str) -> str:
        pass

    @abstractmethod
    def get_agent_data(self, agent_key: str) -> Dict[str, Any]:
        pass 