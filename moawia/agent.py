"""
MOAWIA Negotiation Agent
Implements: "If they pull, I loosen; if they loosen, I tighten"
"""

from .nlp_processor import NLPProcessor
from .metrics import update_tension, calculate_dialogue_health
import random

class MOAWIA_Agent:
    def __init__(self):
        self.posture = "Neutral"
        self.tension_level = 0.0
        self.dialogue_health = 10.0
        self.memory = []
        self.last_opponent_posture = "Neutral"  # ← New: store opponent's posture
        self.flexible_responses = [
            "I understand your concern. Maybe we can adjust?",
            "That’s a valid point. How about a compromise?",
            "I hear you. Let’s explore another option."
        ]
        self.firm_responses = [
            "Let’s stay focused on the main point.",
            "We need to address this directly.",
            "This is non-negotiable at this stage."
        ]
        self.neutral_responses = [
            "That’s a fair point. Let’s see how we can move forward.",
            "We’re making progress—let’s keep going.",
            "Let’s evaluate the options together."
        ]
    
    def perceive(self, message: str, opponent_posture: str):
        sentiment = 0.0
        urgency = 0.0
        if any(word in message.lower() for word in ['urgent', 'now', 'must', 'critical']):
            urgency = 0.8
        if 'overloaded' in message.lower() or 'cannot' in message.lower():
            sentiment = -0.5
        elif 'maybe' in message.lower() or 'adjust' in message.lower():
            sentiment = 0.4
        
        self.tension_level = 5 + (1 - sentiment) * 5
        if urgency > 0.7:
            self.tension_level += 2
        if opponent_posture == "Firm":
            self.tension_level += 1
        self.tension_level = max(0.0, min(10.0, self.tension_level))
        
        self.memory.append({
            "sentiment": sentiment,
            "urgency": urgency,
            "tension": self.tension_level
        })
        self.last_opponent_posture = opponent_posture  # ← Store for later use

    def decide_posture(self):  # ✅ Now takes only self
        opponent_posture = self.last_opponent_posture
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
        import random
        if self.posture == "Flexible":
            return random.choice(self.flexible_responses)
        elif self.posture == "Firm":
            return random.choice(self.firm_responses)
        else:
            return random.choice(self.neutral_responses)

    def update_dialogue_health(self, opponent_posture: str):
        if opponent_posture == "Firm" and self.posture == "Firm":
            self.dialogue_health -= 1.5
        elif opponent_posture == "Flexible" or self.posture == "Flexible":
            self.dialogue_health += 0.8
        elif opponent_posture == "Neutral" and self.posture == "Neutral":
            self.dialogue_health += 0.5
        else:
            self.dialogue_health -= 0.2
        self.dialogue_health = max(0.0, min(10.0, self.dialogue_health))
        return self.dialogue_health

    def reset(self):
        """Reset agent state for new negotiation"""
        self.posture = "Neutral"
        self.tension_level = 0.0
        self.dialogue_health = 10.0
        self.memory = []