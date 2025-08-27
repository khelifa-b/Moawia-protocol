# moawia/agent.py

"""
MOAWIA Negotiation Agent
Implements: "If they pull, I loosen; if they loosen, I tighten"
"""

# ✅ Critical: Import NLPProcessor locally
from .nlp_processor import NLPProcessor
from .metrics import update_tension

class MOAWIA_Agent:
    def __init__(self, cultural_profile="neutral", long_term_weight=0.7):
        self.posture = "Neutral"
        self.tension_level = 0.0
        self.dialogue_health = 10.0
        self.long_term_weight = long_term_weight
        self.cultural_profile = cultural_profile
        self.memory = []
        self.nlp = NLPProcessor()  # ✅ Now works

    def perceive(self, message: str, opponent_posture: str = None):
        analysis = self.nlp.analyze(message)
        self.tension_level = update_tension(
            sentiment=analysis["sentiment"],
            urgency=analysis["urgency"],
            opponent_posture=opponent_posture
        )
        self.memory.append({
            "message": message,
            "sentiment": analysis["sentiment"],
            "urgency": analysis["urgency"],
            "tension": self.tension_level
        })

    def decide_posture(self, opponent_posture: str):
        if opponent_posture == "Firm" and self.tension_level > 6:
            self.posture = "Flexible"
        elif opponent_posture == "Firm" and self.tension_level <= 6:
            self.posture = "Firm"
        elif opponent_posture == "Flexible":
            self.posture = "Firm"
        elif opponent_posture == "Neutral":
            self.posture = "Neutral"
        else:
            self.posture = "Neutral"

        if self.dialogue_health < 4.0:
            self.posture = "Flexible"

        return self.posture

    def generate_response(self):
        base_responses = {
            "Firm": "Let’s stay focused on the main point.",
            "Flexible": "I understand your concern. Maybe we can adjust?",
            "Neutral": "That’s a fair point. Let’s see how we can move forward."
        }

        if self.cultural_profile == "high-context":
            if self.posture == "Firm":
                return "Perhaps we should reconsider the broader implications…"
            elif self.posture == "Flexible":
                return "It might be wise to explore another approach quietly."
        elif self.cultural_profile == "low-context":
            if self.posture == "Firm":
                return "I disagree. Here’s why: [clear argument]"
            elif self.posture == "Flexible":
                return "I accept your point. Let’s change direction."

        return base_responses[self.posture]

    def update_dialogue_health(self, opponent_posture: str):
        if opponent_posture == "Firm" and self.posture == "Firm":
            self.dialogue_health -= 1.5
        elif opponent_posture == "Flexible" or self.posture == "Flexible":
            self.dialogue_health += 1.0
        elif opponent_posture == "Neutral" and self.posture == "Neutral":
            self.dialogue_health += 0.5

        self.dialogue_health = max(0.0, min(10.0, self.dialogue_health))
        return self.dialogue_health

    def reset(self):
        self.posture = "Neutral"
        self.tension_level = 0.0
        self.dialogue_health = 10.0
        self.memory = []