# Tic Tac Toe

A premium, highly-polished implementation of the classic Tic Tac Toe game built with Python and Pygame. It features a complete modular architecture, an unbeatable AI, and dynamic graphical themes.

## Features

- **Game Modes**: 
  - **1 Player**: Test your skills against an unbeatable Minimax AI.
  - **2 Player**: Play locally with a friend.
- **Dynamic Themes**: 
  - **Whiteboard**: Dry-erase marker style
  - **Blackboard**: Chalk style
  - **Paper**: Ballpoint pen style
- **Interface & Mechanics**: 
  - Smooth scale-in animations and screen-shake effects
  - Audio SFX integration for clicks and wins
  - Integrated pause menu (press `ESC`)
  - Authentic hand-drawn aesthetic

## Usage

### For Windows:
You don't need to install Python! Just download the standalone executable:
1. Go to the [Releases](https://github.com/sid-lakhani/Tic-Tac-Toe/releases) tab.
2. Download the latest `TicTacToe.exe`.
3. Run it directly! (It is automatically built and bundled via GitHub Actions).

### For Linux / macOS (Running from source):
1. **Install System Dependencies (Linux only):**
   To ensure `pygame` compiles and runs flawlessly without missing font or audio modules, install the required SDL libraries first.
   - For **Arch Linux**: `sudo pacman -S sdl2 sdl2_image sdl2_ttf sdl2_mixer`
   - For **Ubuntu/Debian**: `sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev`

2. **Clone the repository:**
   ```bash
   git clone https://github.com/sid-lakhani/Tic-Tac-Toe.git
   cd Tic-Tac-Toe
   ```

3. **Set up a virtual environment (Optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
   python3 main.py
   ```

## Development & Architecture

This project is built using a clean, scalable MVC-style architecture.

- `main.py`: The entry point.
- `src/engine.py`: The orchestrator handling the main game loop, event polling, state management (`MENU`, `PLAYING`, `PAUSED`), and haptics.
- `src/renderer.py`: Encapsulates all Pygame drawing logic, alpha-blending, animations, and typography.
- `src/logic.py`: Contains the pure state of the game (the board, win detection, current player).
- `src/ai.py`: Implements the Minimax algorithm for the unbeatable AI opponent.
- `themes/manager.py`: Handles dynamic loading of assets and custom Google Fonts on the fly.

### Automating Windows Builds
The Windows `.exe` is automatically built by GitHub Actions every time a new Release is published on GitHub. Check `.github/workflows/release.yml` for the CI/CD configuration.
