from ai_brain import ask_llm_for_action, ask_llm_for_vote_and_reasoning, build_day_speech_prompt
from public_state import get_public_game_state, get_private_player_info
from openai import OpenAI
from dotenv import load_dotenv
import random
import os

# Load environment variables from the .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def day_phase(players, day_number):
    alive_players = [p for p in players if p.alive]
    if len(alive_players) <= 1:
        return

    pub_state = get_public_game_state(players, day_number)

    # 1) Discussion / day_speech
    for p in alive_players:
        priv_state = get_private_player_info(p, players)
        prompt_msgs = build_day_speech_prompt(
            p,
            pub_state,
            priv_state,
            p.memory_summary,
            p.recent_history
        )

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo"
            messages=prompt_msgs,
            max_tokens=250,
            temperature=0.9
        )
        speech = response.choices[0].message.content.strip()

        print(f"{p.name} says: {speech}")

        # store in memory for all alive players
        event_str = f"{p.name} said: {speech}"
        for other in alive_players:
            other.add_event_to_memory(event_str)

    # 2) Voting with unified reasoning
    votes = {}
    reasoning_map = {}
    candidate_names = [ply.name for ply in alive_players]

    for p in alive_players:
        priv_state = get_private_player_info(p, players)
        llm_text = ask_llm_for_vote_and_reasoning(
            p, pub_state, priv_state, candidate_names
        )

        reasoning, chosen = parse_vote_with_reasoning(llm_text, candidate_names)
        reasoning_map[p.name] = reasoning
        votes[p.name] = chosen
        print(f"[DEBUG] {p.name} Reasoning: {reasoning}")
        print(f"{p.name} votes to exile: {chosen}")

    # 3) Tally and exile
    if votes:
        tally = {}
        for v in votes.values():
            tally[v] = tally.get(v, 0) + 1
        max_count = max(tally.values())
        top_candidates = [nm for nm, count in tally.items() if count == max_count]
        exiled = random.choice(top_candidates)

        for p in alive_players:
            if p.name == exiled:
                p.alive = False
                print(f"** {p.name} is exiled by majority vote! **")
                for other in players:
                    if other.alive:
                        other.add_event_to_memory(f"{p.name} was exiled by vote.")
                break

def night_phase(players, day_number):
    alive_players = [p for p in players if p.alive]
    if len(alive_players) <= 1:
        return

    print(f"\n=== NIGHT PHASE (Day {day_number}) ===")

    # Corporate kill example
    corporates = [p for p in alive_players if p.role == "Corporate"]
    if not corporates:
        # No corporate left
        return

    # Decide which corporate picks the victim
    killer = random.choice(corporates)
    # Potential victims: non-corporate
    targets = [p for p in alive_players if p.role != "Corporate"]
    if not targets:
        return

    # Get the LLM's kill choice
    pub_state = get_public_game_state(players, day_number)
    priv_info = get_private_player_info(killer, players)
    kill_text = ask_llm_for_action(killer, pub_state, priv_info, "night_kill")

    victim_name = parse_vote(kill_text, [t.name for t in targets])
    for t in targets:
        if t.name == victim_name:
            t.alive = False
            print(f"** Corporate kills {t.name} (chosen by {killer.name})! **")
            # Memory update
            for other in players:
                if other.alive:
                    other.add_event_to_memory(f"{t.name} was killed by Corporate last night.")
            break


def parse_vote(ai_text, possible_targets):
    """
    Looks for a name in ai_text that matches possible_targets.
    If none found, returns a random target.
    """
    for cand in possible_targets:
        if cand in ai_text:
            return cand
    return random.choice(possible_targets)

def parse_vote_with_reasoning(llm_text, candidates):
    """
    Extract 'Reasoning:' line and 'Vote:' line from the LLM text.
    Return (reasoning_str, chosen_candidate).
    If something is missing or invalid, fallback to random.
    """
    lines = [ln.strip() for ln in llm_text.split('\n') if ln.strip()]
    reasoning = ""
    vote_target = None

    for ln in lines:
        if ln.startswith("Reasoning:"):
            # e.g. "Reasoning: I find AIPlayer2 suspicious..."
            reasoning = ln[len("Reasoning:"):].strip()
        elif ln.startswith("Vote:"):
            # e.g. "Vote: AIPlayer2"
            potential_vote = ln[len("Vote:"):].strip()
            if potential_vote in candidates:
                vote_target = potential_vote

    # Fallback if no valid vote
    if vote_target is None and candidates:
        vote_target = random.choice(candidates)

    return reasoning, vote_target