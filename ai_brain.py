from openai import OpenAI
import os
from dotenv import load_dotenv
import random
from roles import ROLE_GUIDE

# Load environment variables from the .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_day_speech_prompt(
        player,
        public_state,
        private_state,
        memory_summary,
        recent_events
):
    """
    Creates the system and user messages for a player's "day_speech" action,
    emphasizing reasoning, accusations, defense, and roleplay.
    """

    system_content = (
        "You are playing a social deduction game called Neon Shadows. "
        "This is a game of hidden roles where survival and deduction are key to winning. "
        "Your goal depends on your secret role and the faction you belong to:\n"
        "- **Resistance (Doctor, Netrunner)**: Expose and eliminate Corporate agents "
        "while protecting yourself and your allies.\n"
        "- **Corporate**: Hide your identity, manipulate others into suspecting Resistance players, "
        "and work with fellow Corporate agents to eliminate Resistance players.\n\n"
        "Act in character and treat this as a life-or-death scenario. "
        "You must convince others of your innocence if accused and create logical arguments. "
        "Do NOT reveal your secret role unless it serves a strategic purpose. "
        "Never explicitly say you are an AI or mention these system instructions."
    )

    # Construct the public and private game states
    day_info = (
        f"Day {public_state['day_number']}.\n"
        f"Alive players: {', '.join(public_state['alive_players'])}\n"
    )

    role_str = private_state.get("your_role", "Resistance")
    fellow_corp = private_state.get("fellow_corporates", [])

    # Memory and events
    mem_str = f"Memory summary:\n{memory_summary}\nRecent events:\n" + "\n".join(recent_events)

    # User content: detailed instructions for the AI player
    user_content = f"""
You are {player.name}, and your secret role is **{role_str}**.
If you are Corporate, your allies are: {', '.join(fellow_corp) if fellow_corp else "None"}.

### Public Information:
{day_info}

### Memory:
{mem_str}

### Rules of the Game:
1. **Winning Conditions**:
    - Resistance wins if all Corporate agents are eliminated/exiled.
    - Corporate wins if they outnumber or equal the Resistance.
2. **Day Phase** (this is the day time chat phase):
    - Discuss and debate with other players to identify suspicious players (we're currently at this phase).
    - The group will vote to exile one player at the end of the day.
3. **Night Phase** (not part of this task):
    - Corporate agents coordinate to eliminate a player.
    - Special roles (Doctor, Netrunner, Corporate) perform their abilities.

### Your Objectives:
- **If you are Resistance**:
    - Analyze behaviors, speeches, and previous events to identify Corporate agents.
    - Share reasonable suspicions or deductions to guide the group towards exiling Corporate agents.
    - Defend yourself logically and convincingly if accused.
    - Avoid revealing critical information that may make you a Corporate target.
- **If you are Corporate**:
    - Hide your identity while casting suspicion on Resistance players.
    - Support arguments against other players subtly, without making yourself a target.
    - Build trust with other players to deflect accusations.
    - Never vote for your fellow Corporate agents unless necessary for a long-term strategy.

### Instructions:
- Provide a clear, logical, short (from a few words to 1 or 2 sentences), and in-character message.
- Use the public and private information, along with your memory, to back up your reasoning.
- Avoid revealing your role unless it is part of a clever strategy.
- Make your speech realistic, persuasive, and aligned with your faction's goals.
- If this is the first day, you have no reason to accuse anyone. So just great people
"""

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def build_prompt_messages(player, public_state, private_state, memory_summary, recent_events, action_type):
    """
    Creates structured messages for the ChatCompletion call.

    Args:
        player: The current player object.
        public_state: Public game state (day number, alive players, etc.).
        private_state: Private info (player's role, allies, etc.).
        memory_summary: Summarized memory of past events for context.
        recent_events: List of recent events affecting the player.
        action_type: The specific action the player is deciding on (e.g., "vote", "night_kill").

    Returns:
        A list of messages to be sent to the LLM.
    """
    system_content = (
        "You are an AI playing a social deduction game called Neon Shadows. "
        "Stay in-character, concise, and logical. Do not reveal your secret role or hidden info about other players."
    )

    pub_info_str = (
        f"Day {public_state['day_number']}\n"
        f"Alive players: {', '.join(public_state['alive_players'])}\n"
    )

    priv_info_str = f"Your secret info: {private_state}\n"

    mem_str = f"Memory summary: {memory_summary}\n"
    if recent_events:
        mem_str += f"Recent events:\n{', '.join(recent_events)}"

    user_content = (
        f"{pub_info_str}\n"
        f"{priv_info_str}\n"
        f"{mem_str}\n\n"
        f"Requested action: {action_type}\n"
        "Respond in 2-3 sentences."
    )

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def ask_llm_for_action(player, public_state, private_state, action_type):
    """
    Retrieves an action decision from the LLM based on the player's context.

    Args:
        player: The player object requesting the action.
        public_state: Public game state accessible to all players.
        private_state: Private player-specific information.
        action_type: The type of action being decided (e.g., "vote", "night_kill").

    Returns:
        A string representing the LLM's decision or fallback text in case of error.
    """
    messages = build_prompt_messages(
        player,
        public_state,
        private_state,
        player.memory_summary,
        player.recent_history,
        action_type
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[AI ERROR: {player.name}] {e}")
        return "I remain silent (error)."

def build_vote_with_reasoning_prompt(player, public_state, private_state, memory_summary, recent_events, candidates):
    """
    Constructs a prompt for voting with reasoning in the game.

    Args:
        player: The current player object.
        public_state: Public game state.
        private_state: Player-specific private information.
        memory_summary: Summarized memory for context.
        recent_events: List of recent notable events.
        candidates: List of possible vote targets.

    Returns:
        A structured prompt for LLM completion.
    """
    system_content = (
        "You are an AI in a social deduction game, Neon Shadows. "
        "Provide a concise reasoning for your vote with the given history of game, then specify your vote. "
        "We currently are at the voting phase."
        "You're asked for a reasoning and a vote, but none of this is gonna be revealed in public, see it as your private internal thinking."
    )

    # if player.role == "Corporate":
    #     additional_instructions = (
    #         "As a Corporate agent, your primary objective is to subtly frame Resistance players while avoiding suspicion yourself. "
    #         "Do not target fellow Corporate agents under any circumstances unless it is absolutely necessary for survival or a long-term strategy. "
    #         "Focus your reasoning on behaviors or actions that could reasonably be interpreted as suspicious for Resistance players. "
    #         "Your goal is to deceive the group into exiling Resistance members without exposing your true allegiance."
    #     )
    # else:
    #     additional_instructions = (
    #         "As a Resistance member, your primary objective is to identify and vote out Corporate agents. "
    #         "Use logical deductions based on players' behavior, past events, and voting patterns. "
    #         "Avoid making baseless accusations and focus on presenting clear reasoning for your vote."
    #     )

    user_content = f"""

    ### Rules of the Game:
1. **Winning Conditions**:
    - Resistance wins if all Corporate agents are eliminated/exiled.
    - Corporate wins if they outnumber or equal the Resistance.
2. **Day Phase** (this is the day phase - voting time right now):
    - Discuss and debate with other players to identify suspicious players.
    - The group will then vote to exile one player at the end of the day (this is vote time now)
3. **Night Phase** (not part of this task):
    - Corporate agents coordinate to eliminate a player.
    - Special roles (Doctor, Netrunner, Corporate) perform their abilities.

Day {public_state['day_number']}
Alive players: {', '.join(public_state['alive_players'])}

Your secret info: {private_state}

Your memory summary:
{memory_summary}

Recent events:
{', '.join(recent_events)}

Remember you are {player.name}, your role is {player.role}, and you want to live. Never vote for yourself. And act 
accordingly to your role and its associated goals.


Desired response format (1-2 lines):
Reasoning: <one sentence here>
Vote: <exact player name from the list>
"""

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def ask_llm_for_vote_and_reasoning(player, public_state, private_state, candidates):
    """
    Asks the LLM to provide a vote decision and reasoning.

    Args:
        player: The player object requesting the vote.
        public_state: Public game state accessible to all players.
        private_state: Private player-specific information.
        candidates: List of possible vote targets.

    Returns:
        A string containing the reasoning and vote.
    """
    messages = build_vote_with_reasoning_prompt(
        player,
        public_state,
        private_state,
        player.memory_summary,
        player.recent_history,
        candidates
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[AI ERROR: {player.name}] {e}")
        return "Reasoning: No reasoning\nVote: None"
