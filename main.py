import random
from player import Player
from roles import ROLE_GUIDE
from day_night import day_phase, night_phase

def assign_roles(players):
    """
    Simple role assignment logic:
      - If >= 8 players: 2 Corporate, else 1
      - Then 1 Netrunner, 1 Doctor, rest are Resistance
    """
    n = len(players)
    corp_count = 2 if n >= 8 else 1
    random.shuffle(players)

    # Assign Corporate
    for i in range(corp_count):
        players[i].role = "Corporate"

    # Assign Netrunner
    if corp_count < n:
        players[corp_count].role = "Netrunner"

    # Assign Doctor
    if corp_count + 1 < n:
        players[corp_count+1].role = "Doctor"

    # Remaining are Resistance
    for i in range(corp_count+2, n):
        players[i].role = "Resistance"

    random.shuffle(players)  # shuffle final order

def check_win_condition(players):
    """
    If no Corporate left -> Resistance wins.
    If Corporate >= other players, Corporate wins.
    """
    alive_players = [p for p in players if p.alive]
    if not alive_players:
        return True  # no one alive = game end

    corp = [p for p in alive_players if p.role == "Corporate"]
    if not corp:
        print("\n*** RESISTANCE WINS! ***")
        return True

    others = len(alive_players) - len(corp)
    if len(corp) >= others:
        print("\n*** CORPORATE WINS! ***")
        return True

    return False

def main():
    print("Welcome to Neon Shadows (hidden roles fix).")

    # Create players
    default_names = ["Luna", "Sol", "Nova", "Orion", "Zephyr", "Aurora"]
    players = [Player(name) for name in default_names]

    # Assign roles
    assign_roles(players)

    # (Optional) Print initial roles for your debugging only
    # They won't go into any LLM prompt, so it's safe:
    print("\nInitial Setup (for debugging only):")
    for p in players:
        print(p)

    day_number = 1
    while True:

        alive_count = sum(p.alive for p in players)
        if alive_count <= 1:
            break

        # Day
        day_phase(players, day_number)
        if check_win_condition(players):
            break

        # Night
        night_phase(players, day_number)
        if check_win_condition(players):
            break

        day_number += 1

    # Show final status
    print("\nGame Over. Final statuses:")
    for p in players:
        status = "Alive" if p.alive else "Dead"
        print(f"{p.name} ({p.role}) - {status}")


if __name__ == "__main__":
    main()