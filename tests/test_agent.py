"""
Unit tests for the MOAWIA Negotiation Agent
Validates core logic, posture decisions, and metric calculations
"""

import unittest
from moawia.agent import MOAWIA_Agent
from moawia.nlp_processor import NLPProcessor
from moawia.metrics import update_tension, calculate_dialogue_health


class TestNLPProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = NLPProcessor()

    def test_sentiment_positive(self):
        text = "That sounds great! I'm happy to help."
        result = self.nlp.analyze(text)
        self.assertGreater(result["sentiment"], 0.5)

    def test_sentiment_negative(self):
        text = "This is unacceptable. We are behind schedule!"
        result = self.nlp.analyze(text)
        self.assertLess(result["sentiment"], 0.0)

    def test_urgency_detection(self):
        text = "URGENT: Deadline moved to today! Must be done now!!!"
        result = self.nlp.analyze(text)
        self.assertGreater(result["urgency"], 0.8)

    def test_low_urgency(self):
        text = "We might consider this option later."
        result = self.nlp.analyze(text)
        self.assertLess(result["urgency"], 0.2)


class TestTensionCalculation(unittest.TestCase):
    def test_high_tension(self):
        tension = update_tension(sentiment=-0.8, urgency=0.9, opponent_posture="Firm")
        self.assertGreaterEqual(tension, 8.0)

    def test_low_tension(self):
        tension = update_tension(sentiment=0.9, urgency=0.1, opponent_posture="Neutral")
        self.assertLessEqual(tension, 3.0)

    def test_neutral_tension(self):
        tension = update_tension(sentiment=0.0, urgency=0.5, opponent_posture="Neutral")
        self.assertGreaterEqual(tension, 4.0)
        self.assertLessEqual(tension, 6.0)


class TestMOAWIAAgentPostureLogic(unittest.TestCase):
    def setUp(self):
        self.agent = MOAWIA_Agent()

    def test_opponent_firm_high_tension_leads_to_flexible(self):
        self.agent.tension_level = 7.0
        posture = self.agent.decide_posture("Firm")
        self.assertEqual(posture, "Flexible", 
                         "Should de-escalate when tension is high")

    def test_opponent_firm_low_tension_leads_to_firm(self):
        self.agent.tension_level = 4.0
        posture = self.agent.decide_posture("Firm")
        self.assertEqual(posture, "Firm",
                         "Should hold ground when tension is manageable")

    def test_opponent_flexible_leads_to_firm(self):
        self.agent.tension_level = 5.0
        posture = self.agent.decide_posture("Flexible")
        self.assertEqual(posture, "Firm",
                         "Should reclaim advantage when opponent softens")

    def test_opponent_neutral_leads_to_neutral(self):
        posture = self.agent.decide_posture("Neutral")
        self.assertEqual(posture, "Neutral",
                         "Should maintain balance in neutral context")

    def test_dialogue_health_override(self):
        self.agent.dialogue_health = 3.0  # Low DHI
        self.agent.tension_level = 5.0
        self.agent.decide_posture("Firm")
        # After decision, posture should be Flexible due to low DHI
        self.assertEqual(self.agent.posture, "Flexible",
                         "Low dialogue health should force de-escalation")


class TestDialogueHealth(unittest.TestCase):
    def test_mutual_firm_reduces_dhi(self):
        pairs = [("Firm", "Firm")]
        dhi = calculate_dialogue_health(pairs)
        self.assertLess(dhi, 10.0)

    def test_flexible_moves_increase_dhi(self):
        pairs = [("Flexible", "Neutral"), ("Neutral", "Flexible")]
        dhi = calculate_dialogue_health(pairs)
        self.assertGreater(dhi, 10.0)

    def test_balanced_neutral_maintains_dhi(self):
        pairs = [("Neutral", "Neutral"), ("Neutral", "Neutral")]
        dhi = calculate_dialogue_health(pairs)
        self.assertAlmostEqual(dhi, 11.0)  # +0.5 per round


class TestCulturalAdaptation(unittest.TestCase):
    def test_high_context_firm_response(self):
        agent = MOAWIA_Agent(cultural_profile="high-context")
        agent.posture = "Firm"
        response = agent.generate_response()
        self.assertIn("Perhaps", response) or self.assertIn("reconsider", response)

    def test_low_context_firm_response(self):
        agent = MOAWIA_Agent(cultural_profile="low-context")
        agent.posture = "Firm"
        response = agent.generate_response()
        self.assertIn("disagree", response.lower()) or self.assertIn("here’s why", response.lower())

    def test_high_context_flexible_response(self):
        agent = MOAWIA_Agent(cultural_profile="high-context")
        agent.posture = "Flexible"
        response = agent.generate_response()
        self.assertIn("wisely", response) or self.assertIn("quietly", response)


class TestAgentMemoryAndReset(unittest.TestCase):
    def setUp(self):
        self.agent = MOAWIA_Agent()

    def test_perceive_updates_memory(self):
        self.agent.perceive("We need this done now!", opponent_posture="Firm")
        self.assertEqual(len(self.agent.memory), 1)
        entry = self.agent.memory[0]
        self.assertIn("urgency", entry)
        self.assertIn("sentiment", entry)

    def test_reset_clears_state(self):
        self.agent.perceive("Test message")
        self.agent.reset()
        self.assertEqual(self.agent.posture, "Neutral")
        self.assertEqual(self.agent.tension_level, 0.0)
        self.assertEqual(self.agent.dialogue_health, 10.0)
        self.assertEqual(len(self.agent.memory), 0)


if __name__ == "__main__":
    unittest.main()