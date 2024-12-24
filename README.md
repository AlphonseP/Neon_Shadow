Neon Shadows

Neon Shadows is a cyberpunk-inspired, AI-driven social deduction game, reminiscent of Mafia/Werewolf-style mechanics. Players are divided into city-aligned Resistance (e.g., Doctor, Netrunner) and hidden Corporate agents intent on sabotage. An LLM (Large Language Model) simulates each player’s dialogue, suspicions, defenses, and secret actions, providing an immersive experience even without human participants.
Key Features

    LLM-Controlled Players
    Each in-game player uses AI prompts to make decisions, provide arguments, and vote—no need for human input unless you want a mixed match.

    Hidden Roles
    Corporate agents must deceive or sow confusion; Resistance roles seek to collaborate or investigate to uncover the threats.

    Day/Night Cycle
        Day: Discussion, accusations, and voting to exile a suspect.
        Night: Corporate kills, Doctor heals, Netrunner investigates, and more.

    Memory & Prompt Engineering
    Each AI player maintains a short memory summary of recent events (accusations, exiles, night actions), ensuring coherence in dialogues over multiple days.

    Modular Codebase
    Key logic split into multiple modules (e.g., player.py, roles.py, day_night.py, ai_brain.py) for clarity and easy extension.

Table of Contents

    Screenshots
    Installation
    Usage
    Project Structure
    Game Flow
    Contributing
    License
    Acknowledgments

Screenshots
<details> <summary>Console Snippet</summary>

=== DAY PHASE (Day 1) ===
AIPlayer2 says: I suspect AIPlayer4 is hiding something. Let's keep a close eye.
AIPlayer4 says: I promise I have nothing to hide! I'm on your side...
...
By majority vote, AIPlayer4 is exiled!

</details>

(Add actual screenshots or images if available.)
Installation

    Clone this repository:

git clone https://github.com/<YourUserName>/neon-shadows.git
cd neon-shadows

Install Dependencies:

    Requires Python 3.8+
    Install required packages:

    pip install -r requirements.txt

(Ensure your requirements.txt includes packages like openai or any other dependencies.)

Set Your OpenAI API Key:

    Commonly, you’d do:

        export OPENAI_API_KEY="sk-..."

        Or provide it in your code (not recommended for production).

Usage

    Run the Game:

    python main.py

    This starts a console-based simulation where each AI “player” performs their day/night actions, logs discussions, and eventually ends once a winning condition is reached (all Corporate exiled, or Corporate tying/outnumbering the Resistance).

    Customizing Roles:
        Open roles.py to adjust or add special abilities (e.g., Street Samurai, Corporate Enforcer, Mad Techno-Shaman, etc.).

    Tweak Prompts:
        See ai_brain.py for functions that craft LLM prompts. Adjust them for more dramatic roleplay or stricter behavior rules.

    Game Configuration:
        Within main.py, you can change the number of AI players, their names, or role distributions.
        Adjust the model (e.g., gpt-3.5-turbo or gpt-4) and temperature parameters to control AI creativity vs. logical consistency.

Project Structure

neon-shadows/
├── ai_brain.py         # LLM prompt-building and response handling
├── day_night.py        # Main day/night cycle flow
├── main.py             # Entry point for running the game loop
├── player.py           # Player class, storing role & memory
├── public_state.py     # Utilities for building “public” vs. “private” info
├── roles.py            # Definitions of roles & their abilities
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── ... (additional modules, test files, etc.)

Game Flow

    Initialization
        main.py sets up a list of players, assigns roles, and starts the game loop.

    Day Phase
        Each AI player receives prompts to “speak” (accuse, defend) and then “vote” for a suspect.
        The group tallies votes; the highest-voted player is exiled.

    Night Phase
        Corporate attempts a kill.
        Doctor can protect someone; Netrunner can investigate a target.

    Win Condition
        If no Corporate remain, Resistance wins.
        If Corporate tie or outnumber the rest, Corporate wins.

Contributing

Contributions are welcome! To propose changes or add new features:

    Fork this repo
    Create a feature branch:

git checkout -b feature/my-new-feature

Commit your changes:

git commit -m "Add some feature"

Push to the branch:

    git push origin feature/my-new-feature

    Open a Pull Request on GitHub

License

    (Choose a license, e.g., MIT)

MIT License

Copyright (c) [Year]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

Acknowledgments

    Inspired by classic social deduction games like Werewolf/Mafia and Town of Salem.
    Prompt engineering strategies drawn from AI roleplay community ideas and iterative refinement.
    Special thanks to all the open-source contributors and early playtesters.

Enjoy playing and tinkering with Neon Shadows! For questions or suggestions, open an Issue or Pull Request in this repo or contact the dev team directly.
