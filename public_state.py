def get_public_game_state(players, day_number):
    """
    Info that everyone in the game can see:
      - Day number
      - Which players are alive (names only, no roles)
      - Possibly who died or was exiled recently
    """
    alive_names = [p.name for p in players if p.alive]

    return {
        "day_number": day_number,
        "alive_players": alive_names,
        # For further expansions, you might store public events:
        # "recent_exile": "PlayerX",
        # "recent_kill": "PlayerY"
    }


def get_private_player_info(current_player, players):
    """
    Info only 'current_player' should see:
      - Their own role
      - If Corporate, who else is Corporate
      - If Netrunner, any investigate results, etc.
    """
    private_data = {
        "your_role": current_player.role
    }

    if current_player.role == "Corporate":
        # Let them know who their fellow Corporate are
        fellow_corp = [
            p.name for p in players
            if p.role == "Corporate" and p != current_player
        ]
        private_data["fellow_corporates"] = fellow_corp

    # Add more logic if you have Netrunner investigations, etc.
    return private_data