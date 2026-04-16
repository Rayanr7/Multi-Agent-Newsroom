from orchestrator.logger import log_event

class StateMachine:
    def __init__(self):
        self.state = "IDLE"
        self.history = []

    def transition(self, new_state):
        from datetime import datetime

        old_state = self.state

        log = {
            "type": "STATE_TRANSITION",   # 🔥 important
            "from": old_state,
            "to": new_state,
            "timestamp": datetime.utcnow().isoformat()
        }

        # ✅ Save in memory
        self.history.append(log)

        # ✅ Save to logs.json (VERY IMPORTANT)
        log_event(log)

        # ✅ Update state
        self.state = new_state

        # ✅ Print for terminal
        print(f"{old_state} → {new_state}")
