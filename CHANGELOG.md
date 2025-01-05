# Changelog

## V2.0.0 (Current)

### Added

- More detailed macro behavior description in all languages
- New menu options:
  - Record New Agent
  - Start Macro Listener
  - Refresh Settings
- Agent unbinding functionality with DELETE key
- Improved navigation with consistent Ctrl+C for cancellation

### Changed

- Changed macro activation from `start_listening()` to `run()`
- Improved error messages and user feedback
- Enhanced navigation instructions across all languages
- More intuitive menu structure and flow
- Solved the most annoying bug that the mouse get stuck on clicking

### Removed

- Removed human-like mouse movement simulation
- Removed a lot of unnecessary settings
- Made the macro more reliable and faster
- Console-based UI components:
  - `console.py` (removed entire file)
  - `key_manager.py` (removed entire file)
  - `language_manager.py` (removed entire file)

### Technical Changes

- Reorganized code structure for better maintainability
- Improved error handling and user feedback mechanisms
- Enhanced configuration management

## V1.0.0 (Initial Release)

- Basic instalock functionality with keyboard shortcuts
- Console-based interface
- Agent selection and key binding system
- Position recording for agent selection and confirmation
- Basic error handling and configuration saving
- Support for multiple languages (English, Portuguese, Chinese)
- Random margin functionality for agent and confirmation clicks to prevent detection
- Human-like mouse movement simulation
- Configurable click delays and positions
- Auto-save configuration system
- Fine-tunable settings for click intervals and hold times
