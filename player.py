class Player:
    def __init__(self, name, role=None, is_ai=True):
        self.name = name
        self.role = role or "Resistance"
        self.alive = True
        self.is_ai = is_ai

        # Memory logs (to keep track of game events or conversations)
        self.memory_summary = ""      # A summarized backlog
        self.recent_history = []      # Recent lines of info

        # Usage counters for abilities
        self.used_protect = 0
        self.used_hack = 0
        self.used_disrupt = 0
        self.used_kill = False

    def __str__(self):
        status = "Alive" if self.alive else "Dead"
        return f"{self.name} ({self.role}) - {status}"

    def add_event_to_memory(self, event_str):
        """
        Append short event to recent_history.
        If it grows too large, optionally merge into memory_summary.
        """
        self.recent_history.append(event_str)
        if len(self.recent_history) > 5:
            chunk = " ".join(self.recent_history)
            self.memory_summary += f"\n[Summary chunk]\n{chunk}\n"
            self.recent_history = []