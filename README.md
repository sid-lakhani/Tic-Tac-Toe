# Tic Tac Toe Game

A simple Tic Tac Toe game built using Pygame.

## Description

This is a basic implementation of the classic Tic Tac Toe game created with Python and Pygame. It features a graphical user interface where two players can take turns to play the game.

## Features

- Two-player gameplay
- Graphical user interface (GUI)
- Win detection and game-over condition

## Usage

### For Windows:
1. Download the executable file: [tictactoe.exe](https://github.com/sid-lakhani/Tic-Tac-Toe/releases/download/tic-tac-toe/tictactoe.exe)
2. Run the downloaded executable to start the game.

### For Linux / macOS (Running from source):
Since there is no pre-built executable for Linux, you can easily run the game directly from the source code.

1. **Install System Dependencies (Linux only):**
   To ensure `pygame` compiles and runs flawlessly without missing font or audio modules, install the required SDL libraries first.
   - For **Arch Linux**: `sudo pacman -S sdl2 sdl2_image sdl2_ttf sdl2_mixer`
   - For **Ubuntu/Debian**: `sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev`

2. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/sid-lakhani/tic-tac-toe.git
   cd tic-tac-toe
   ```

3. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For bash/zsh
   # source venv/bin/activate.fish  # For Fish shell
   ```

4. Install the Python dependencies:
   ```bash
   pip install --no-cache-dir pygame
   ```
   *(Note: `--no-cache-dir` guarantees a fresh, rock-solid build with the newly installed SDL libraries)*

5. Run the game:
   ```bash
   python3 tictactoe.py
   ```

## Development

If you want to contribute or make modifications to the game, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/sid-lakhani/tic-tac-toe.git

2. Install the necessary dependencies:

   ```bash
   pip install pygame
   
3. Make your changes to the code.

4. Test your changes locally:

   ```bash
   python tictactoe.py

5. If everything works as expected, create a pull request to submit your changes.
