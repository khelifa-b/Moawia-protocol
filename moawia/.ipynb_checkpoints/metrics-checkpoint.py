"""
Utility functions for calculating negotiation metrics
"""

def update_tension(sentiment: float, urgency: float, opponent_posture: str = None) -> float:
    base = 5 + (1 - sentiment) * 5
    if urgency > 0.7:
        base += 2
    if opponent_posture == "Firm":
        base += 1
    return max(0.0, min(10.0, base))

def calculate_dialogue_health(posture_pairs: list) -> float:
    dhi = 10.0
    for self_p, opp_p in posture_pairs:
        if self_p == "Firm" and opp_p == "Firm":
            dhi -= 1.5
        elif self_p == "Flexible" or opp_p == "Flexible":
            dhi += 1.0
        elif self_p == "Neutral" and opp_p == "Neutral":
            dhi += 0.5
    return max(0.0, min(10.0, dhi))