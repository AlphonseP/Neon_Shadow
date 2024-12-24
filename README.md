# Neon Shadows

Neon Shadows is a multiplayer social deduction game inspired by classics like Mafia and Werewolf. Set in a dystopian cyberpunk universe, players take on secret roles, engaging in deception, reasoning, and collaboration to fulfill their role-specific objectives.

This project uses AI-driven players to simulate a fully autonomous game environment, leveraging powerful LLMs to create engaging interactions.

---

## Table of Contents

1. [About the Game](#about-the-game)
2. [Features](#features)
3. [Game Roles](#game-roles)
4. [How It Works](#how-it-works)
5. [Getting Started](#getting-started)
6. [Future Enhancements](#future-enhancements)
7. [Contributing](#contributing)
8. [License](#license)

---

## About the Game

In Neon Shadows, players are divided into two factions: **Corporate** and **Resistance**. Each faction has specific objectives, and roles within the factions possess unique abilities. The game alternates between **Day** and **Night** phases, during which players debate, vote, and take covert actions.

AI-driven players use reasoning, memory, and strategic planning to engage in the game, creating an immersive social deduction experience even in single-player mode.

---

## Features

- **AI Integration**: Each player is controlled by an AI capable of reasoning, deception, and collaboration.
- **Dynamic Phases**: Day discussions and voting, followed by covert night actions.
- **Hidden Roles**: Secret objectives keep gameplay engaging and unpredictable.
- **Memory & History**: AI players maintain memories of events to influence future actions and decisions.
- **Expandable**: Flexible design allows for additional roles and game rules.

---

## Game Roles

### 1. **Corporate**
- **Objective**: Sabotage and outnumber the Resistance.
- **Abilities**: Coordinate at night to eliminate a target.
  
### 2. **Netrunner** (Resistance-aligned)
- **Objective**: Uncover Corporate agents.
- **Abilities**: Investigate a player's role during the night.

### 3. **Doctor** (Resistance-aligned)
- **Objective**: Protect allies and thwart Corporate attacks.
- **Abilities**: Heal a player during the night to prevent their elimination.

### 4. **Resistance**
- **Objective**: Identify and exile all Corporate agents.
- **Abilities**: None (basic voting role).

---

## How It Works

1. **Role Assignment**:
   Players are randomly assigned roles at the start of the game.

2. **Day Phase**:
   - Players discuss suspicions and share observations.
   - A vote determines who gets exiled.

3. **Night Phase**:
   - Corporate agents coordinate to eliminate a target.
   - Special roles (Doctor, Netrunner) use their abilities.

4. **Win Conditions**:
   - Resistance wins when all Corporate agents are eliminated.
   - Corporate wins if they outnumber or equal the Resistance.

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- OpenAI API key (for AI player functionality)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/neon-shadows.git
   cd neon-shadows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenAI API key to the environment:
   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

### Run the Game

To start a game with AI players:
```bash
python main.py
```

---

## Future Enhancements

- New roles with unique abilities.
- Multiplayer support with live players.
- Enhanced AI logic and memory mechanisms.
- Improved visualizations and UX for the gameplay.

---

## Contributing

We welcome contributions from the community! Please feel free to submit issues, fork the repository, and create pull requests.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes and open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Embark on a journey of hidden agendas, deceptions, and alliances in **Neon Shadows**. May the best faction win!
