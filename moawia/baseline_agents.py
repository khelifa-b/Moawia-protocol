"""
Baseline negotiation agents for comparison:
- Harvard Model (Principled Negotiation)
- Tit-for-Tat (Game Theory)
"""

class HarvardAgent:
    def __init__(self):
        self.posture = "Neutral"
        self.opponent_firm_streak = 0

    def perceive(self, opponent_posture: str):
        if opponent_posture == "Firm":
            self.opponent_firm_streak += 1
        else:
            self.opponent_firm_streak = 0

    def decide_posture(self):
        if self.opponent_firm_streak >= 2:
            self.posture = "Firm"
        else:
            self.posture = "Neutral"
        return self.posture

    def generate_response(self):
        responses = {
            "Firm": "We need to stick to the agreed criteria.",
            "Neutral": "Let’s focus on shared interests.",
            "Flexible": "That’s a constructive suggestion."
        }
        return responses[self.posture]


class TitForTatAgent:
    def __init__(self):
        self.posture = "Flexible"  # Starts cooperative
        self.last_opponent_posture = "Flexible"

    def perceive(self, opponent_posture: str):
        self.last_opponent_posture = opponent_posture

    def decide_posture(self):
        self.posture = self.last_opponent_posture
        return self.posture

    def generate_response(self):
        responses = {
            "Firm": "I’ll respond in kind.",
            "Flexible": "I appreciate the cooperation.",
            "Neutral": "Let’s keep this balanced."
        }
        return responses[self.posture]