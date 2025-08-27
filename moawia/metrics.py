"""
Utility functions for calculating negotiation metrics
"""

def update_tension(current_tension: float, sentiment: float, urgency: float, 
                   opponent_posture: str = None, decay_rate: float = 0.1) -> float:
    """
    Compute updated tension level with decay
    """
    # Base tension from sentiment and urgency
    base = 5 + (1 - sentiment) * 5
    if urgency > 0.7:
        base += 2
    if opponent_posture == "Firm":
        base += 1

    # Apply exponential smoothing with decay
    smoothed = current_tension * (1 - decay_rate) + base * decay_rate
    return max(0.0, min(10.0, smoothed))


def calculate_dialogue_health(posture_pairs: list) -> float:
    """
    Calculate Dialogue Health Index (DHI) from interaction history
    """
    dhi = 10.0
    for self_p, opp_p in posture_pairs:
        if self_p == "Firm" and opp_p == "Firm":
            dhi -= 1.5  # Mutual firmness harms dialogue
        elif self_p == "Flexible" or opp_p == "Flexible":
            dhi += 1.0  # Flexibility preserves dialogue
        elif self_p == "Neutral" and opp_p == "Neutral":
            dhi += 0.5  # Balance supports continuity
        else:
            dhi -= 0.2  # Minor decay for non-cooperative patterns
    return max(0.0, min(10.0, dhi))