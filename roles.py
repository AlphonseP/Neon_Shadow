# roles.py

import random
from player import Player  # If needed, though we mainly just need Player attributes


ROLE_GUIDE = {
    "Corporate": {
        "description": "Secret agent trying to sabotage the game. Teams up with other Corporate Agents to eliminate targets at night.",
        "abilities": [
            "At night, coordinate to kill one non-Corporate player."
        ]
    },
    "Netrunner": {
        "description": "Hacker who can investigate one target each night.",
        "abilities": [
            "Hack a target to learn their role/faction (limited uses or chance of failure)."
        ]
    },
    "Doctor": {
        "description": "Protects one target each night from Corporate attack.",
        "abilities": [
            "Heal a target at night. If Corporate tries to kill that target, the kill fails."
        ]
    },
    "Resistance": {
        "description": "Basic city-aligned role with no special powers except voting.",
        "abilities": []
    }
}

def assign_roles(players):
    """
    Assign roles to the given list of Player objects.

    Example logic:
      - If at least 8 players, 2 Corporate; else 1 Corporate
      - 1 Netrunner if possible
      - 1 Doctor if possible
      - The rest are Resistance
    """
    num_players = len(players)

    # Decide how many Corporate Agents
    # (Simple logic: 2 if we have 8+ players, else 1)
    if num_players >= 8:
        corp_count = 2
    else:
        corp_count = 1

    # Shuffle players to randomize who gets roles
    random.shuffle(players)

    # Assign Corporate
    for i in range(corp_count):
        players[i].role = "Corporate"

    # Assign Netrunner (if there's still an unassigned player)
    if corp_count < num_players:
        players[corp_count].role = "Netrunner"

    # Assign Doctor (if we still have unassigned players left)
    if corp_count + 1 < num_players:
        players[corp_count + 1].role = "Doctor"

    # The rest are Resistance
    for i in range(corp_count + 2, num_players):
        players[i].role = "Resistance"

    # (Optional) Shuffle again if you prefer the final order to be random:
    random.shuffle(players)

    # Return the players list (not strictly necessary, since it's modified in-place)
    return players
