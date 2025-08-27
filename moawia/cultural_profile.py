"""
Cultural Profile Definitions
Based on Hofstede's dimensions
"""

CULTURAL_PROFILES = {
    "high-context": {
        "power_distance": 0.8,
        "uncertainty_avoidance": 0.7,
        "communication_style": "indirect",
        "decision_speed": "slow"
    },
    "low-context": {
        "power_distance": 0.3,
        "uncertainty_avoidance": 0.4,
        "communication_style": "direct",
        "decision_speed": "fast"
    },
    "neutral": {
        "power_distance": 0.5,
        "uncertainty_avoidance": 0.5,
        "communication_style": "balanced",
        "decision_speed": "moderate"
    }
}