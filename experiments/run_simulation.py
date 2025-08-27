"""
Run negotiation simulation between MOAWIA agent and opponent
"""

from moawia.agent import MOAWIA_Agent
import json

def load_scenario(scenario_file):
    with open(scenario_file, 'r') as f:
        return json.load(f)

def simulate_negotiation(scenario_file, opponent_strategy="tft"):
    agent = MOAWIA_Agent(cultural_profile="neutral")
    scenario = load_scenario(scenario_file)

    log = []
    posture_pairs = []

    for turn in scenario["dialogue"]:
        # Opponent speaks
        opponent_message = turn["opponent"]
        opponent_posture = turn["opponent_posture"]

        # MOAWIA perceives
        agent.perceive(opponent_message, opponent_posture)

        # Decide posture
        my_posture = agent.decide_posture(opponent_posture)
        posture_pairs.append((my_posture, opponent_posture))

        # Generate response
        my_response = agent.generate_response()
        dialogue_health = agent.update_dialogue_health(opponent_posture)

        # Log
        log.append({
            "round": len(log) + 1,
            "opponent": opponent_message,
            "opponent_posture": opponent_posture,
            "moawia_posture": my_posture,
            "response": my_response,
            "tension": round(agent.tension_level, 2),
            "dialogue_health": round(dialogue_health, 2)
        })

    final_dhi = agent.dialogue_health
    agreement = final_dhi >= 6  # Heuristic: if DHI > 6, agreement reached

    return {
        "log": log,
        "final_dhi": final_dhi,
        "agreement_reached": agreement,
        "total_rounds": len(log)
    }

# Example usage
if __name__ == "__main__":
    result = simulate_negotiation("experiments/scenarios/workplace.json")
    print(json.dumps(result, indent=2))