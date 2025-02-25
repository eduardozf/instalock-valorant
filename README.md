# Valorant Instalock Macro 🎯

[English](README.md) | [Português](README_PTBR.md) | [中文](README_CN.md)

A Python script that helps you instalock agents in Valorant. Created for educational purposes only 👀

<div style="display: grid; grid-column: 3;">
    <img src="examples/main_menu.png" alt="Main Menu" style="width: auto; height: 320px; object-fit: contain;"/>
    <img src="examples/record_agent.png" alt="Record Agent" style="width: auto; height: 320px; object-fit: contain;"/>
    <img src="examples/instalock_mode.png" alt="Instalock Mode" style="width: auto; height: 320px; object-fit: contain;"/>
</div>

> [!WARNING]  
> This tool may violate Valorant's Terms of Service. Use at your own risk. The creator is not responsible for any consequences.

## Features

- Easy agent selection with customizable keybinds
- Multi-language support (English, Portuguese, Chinese)
- Simple setup process
- Configurable click delays and positions
- Randomized click positions with a configurable margin of error help prevent macro detection
- Enhanced error handling and stability
- Intuitive menu-based interface with options to:
  - Record new agents
  - Start macro listener
  - Refresh settings
  - Unbind agents

## Prerequisites

1. **Install Python**:

   - Download Python from [python.org](https://python.org/downloads/)
   - During installation, **make sure to check** "Add Python to PATH"
   - After installation, restart your terminal/command prompt (CMD)

2. **Verify Python Installation**:
   ```bash
   python --version
   ```
   If you see a version number, Python is installed correctly!

## Installation

1. **Download the Project**:

   **Option A - Using Git**:

   ```bash
   git clone https://github.com/yourusername/valorant-instalock
   cd valorant-instalock
   ```

   **Option B - Without Git**:

   - Go to the repository page
   - Click the green "Code" button
   - Select "Download ZIP"
   - Extract the ZIP file to a folder (e.g., to Desktop)
   - Remember the folder location (e.g., `C:\Users\YourUser\Desktop\valorant-instalock-main`)

2. **Navigate to Project Folder**:

   **Option A - Windows 11 (Easiest way)**:

   - Go to the extracted folder
   - Right-click on an empty space inside the folder
   - Select "Open in Terminal"

   **Option B - Using Command Prompt**:

   - Open Command Prompt (CMD)
   - Navigate to the project folder using the `cd` command:

   ```bash
   # If you extracted to Desktop:
   cd C:\Users\YourUser\Desktop\valorant-instalock-main

   # Or if you know the full path, use it directly:
   cd "path_to_your_extracted_folder"
   ```

3. **Install Requirements**:

   Make sure you're in the project folder (where `requirements.txt` is located) and run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Game Settings**:

   - Recommended: Set Valorant to "Windowed Fullscreen" mode (Just to make it easier to see the agents position)
   - Recommended: Use in Custom Games only

2. **Running the Script**:

   Make sure you're in the project folder and run:

   ```bash
   python -m src
   ```

   If you closed the terminal, you'll need to navigate to the project folder again using the steps in **Navigate to Project Folder** above.

3. **Using the Menu**:

   - Use arrow keys to navigate the menu
   - Press Enter to select an option
   - Press DELETE to unbind an agent
   - Press Ctrl+C to cancel or exit

4. **Recording an Agent**:

   - Select "Record New Agent" from the menu
   - Select an agent using arrow keys and Enter
   - Press the key you want to use for that agent (e.g. DELETE, END, HOME, etc.)
   - Move your mouse to where the agent appears on the selection screen and press Space
   - Move your mouse to the Lock In button and press Space

5. **Using the Macro**:
   - Select "Start Macro Listener" from the menu
   - When agent selection begins, _hold_ the key you set for your desired agent
   - Release the key once the agent is locked
   - Press Esc to get back to main menu so the macro doesn't get in your way

## Tips

- Each agent can have its own keybind
- Press Ctrl+C during any operation to cancel
- Use DELETE key to unbind agents
- The script saves your configuration automatically
- **Configuration File** (`config.json`):
  - Located in the project folder
  - Easy reset: Simply delete `config.json` and restart the script
  - Fully customizable:
    - Manually edit keybindings
    - Add or remove agent configurations
    - Adjust click delays in the "delays" section
    - Fine-tune detection avoidance with "margin_of_error" settings

## Contributing

Feel free to submit issues and pull requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Educational Purpose

This project was created solely for educational purposes to demonstrate:

- Python automation capabilities
- GUI interaction
- Multi-language support
- Configuration management
- Event handling

Remember: Using macros in competitive games may result in account penalties. Use responsibly!
