# Valorant Instalock Macro 🎯

[English](README.md) | [Português](README_PTBR.md) | [中文](README_CN.md)

A Python script that helps you instalock agents in Valorant. Created for educational purposes only 👀

![Example](example.gif)

> [!WARNING]  
> This tool may violate Valorant's Terms of Service. Use at your own risk. The creator is not responsible for any consequences.

## Features

- Easy agent selection with customizable keybinds
- Multi-language support
- Simple setup process
- Configurable click delays and positions
- Randomized click positions with a configurable margin of error help prevent macro detection

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

   Make sure you're in the project folder (where `instalock.py` is located) and run:

   ```bash
   python instalock.py
   ```

   If you closed the terminal, you'll need to navigate to the project folder again using the steps in **Navigate to Project Folder** above.

3. **First Time Setup**:

   - Select your language
   - Press F1 to start recording a new agent
   - Select an agent using arrow keys and Enter
   - Press the key you want to use for that agent (e.g. DELETE, END, HOME, etc.)
   - Move your mouse to where the agent appears on the selection screen and press Space
   - Move your mouse to the Lock In button and press Space
   - Repeat for other agents if desired

4. **Using the Macro**:
   - Start a game
   - When agent selection begins, _hold_ the key you set for your desired agent
   - Release the key once the agent is locked
   - Close the script by pressing Ctrl+C and win your game! (Seriously, you already instalocked, so please win the game :))

## Tips

- Each agent can have its own keybind
- Press ESC during recording to cancel
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
