"""
Lightweight NLP Processor (No External Dependencies)
"""

import re

POSITIVE_WORDS = [
    'good', 'great', 'excellent', 'happy', 'pleased', 'satisfied', 'agree',
    'accept', 'fine', 'ok', 'okay', 'thank', 'thanks', 'appreciate', 'love',
    'like', 'support', 'understand', 'agreeable', 'positive', 'benefit'
]

NEGATIVE_WORDS = [
    'bad', 'terrible', 'awful', 'angry', 'frustrated', 'upset', 'disagree',
    'no', 'not', 'never', 'waste', 'useless', 'unacceptable', 'problem',
    'issue', 'concern', 'overload', 'stress', 'impossible', 'can’t', "cannot",
    'critical', 'urgent', 'emergency', 'delay', 'failure', 'risk'
]

URGENCY_KEYWORDS = [
    'urgent', 'now', 'immediately', 'asap', 'deadline', 'must', 'critical',
    'emergency', 'today', 'right now', 'final', 'last chance', 'imperative'
]

class NLPProcessor:
    def analyze(self, text: str):
        text_lower = text.lower()
        words = re.findall(r'\b[a-zA-Z]+\b', text_lower)
        
        if not words:
            return {"sentiment": 0.0, "urgency": 0.0}
        
        # Sentiment score
        pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
        sentiment = (pos_count - neg_count) / len(words)
        sentiment = max(-1.0, min(1.0, sentiment))

        # Urgency score
        urgency_score = sum(1 for w in words if w in URGENCY_KEYWORDS) * 0.3
        urgency_score += text.count("!") * 0.2
        urgency_score += text.count("???") * 0.3
        urgency_score = min(1.0, urgency_score)

        return {
            "sentiment": round(sentiment, 2),
            "urgency": round(urgency_score, 2)
        }