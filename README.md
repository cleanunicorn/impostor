# Impostor Game

Impostor is a Python-based party game simulation similar to Mafia/Werewolf where players assume the roles of crew members and impostors. The game features role assignments, discussions, voting phases, and impostor actions powered by a flow-based architecture.

## Demo

![Demo](./demo.gif)

## Features

- **Role Assignment:** Players are assigned roles using the [`AssignRoles`](nodes/AssignRoles.py) node.
- **Discussion Phase:** Live discussion simulated by [`Discuss`](nodes/Discuss.py) where players can debate.
- **Voting Phase:** Players vote to eliminate a suspect via the [`Vote`](nodes/Vote.py) node.
- **Impostor Action:** Impostors select a crew member to kill using the [`ImpostorAction`](nodes/ImpostorAction.py) node.
- **Game Status Check:** The game status is continuously checked by [`CheckGameStatus`](nodes/CheckGameStatus.py) and concludes with [`EndGame`](nodes/EndGame.py).
- **LLM Integration:** Utilizes the [`call_llm`](utils/call_llm.py) module to integrate with the OpenAI API for generating dynamic content.

## Requirements

- Python 3.12 or newer (see [.python-version](.python-version))
- Dependencies as specified in [pyproject.toml](pyproject.toml)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/cleanunicorn/impostor.git
    ```
2. **Navigate to the project directory:**
    ```sh
    cd impostor
    ```
3. **Create and activate a virtual environment:**
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```
4. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    *Alternatively, use `pip install .` if the project supports it via [pyproject.toml](http://_vscodecontentref_/0).*

## Setup and Running the Game with `uv`

The project now uses the `uv` command-line tool to manage setup and execution. Once your virtual environment is active and dependencies are installed, you can use the following commands:

1. **Set up the project:**
    ```sh
    uv setup
    ```
2. **Launch the game:**
    ```sh
    uv start --players 6 --add-human --impostors 1
    ```
    - `--players`: Number of players in the game.
    - `--add-human`: Include at least one human player.
    - `--impostors`: Number of impostors.

## Configuration

1. **Setup environment variables:**
    - Copy the example environment file:
        ```sh
        cp .env.example .env
        ```
    - Update [.env](http://_vscodecontentref_/1) with your OpenAI API credentials and adjust model settings if needed.

## Game Flow

The game is constructed as a flow using [Pocketflow](https://github.com/microsoft/pocketflow). The flow proceeds as:

1. **Assign Roles:** Generates a list of players and randomly assigns impostors.
2. **Check Game Status:** Evaluates the current game state.
   - If impostors outnumber or equal crew members, the game ends.
3. **Impostor Action:** Living impostors decide on a crew member to kill.
4. **Discussion:** Players converse to debate suspicions using.
5. **Voting:** Players vote to eliminate a suspected impostor through.
6. **Game Status Check:** The cycle repeats until a win condition is met, or stops the game.
