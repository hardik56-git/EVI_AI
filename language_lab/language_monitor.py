from datetime import datetime

class LanguageMonitor:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.metrics = {"grammar_score": 0.0, "clarity": 0.0}
        
    def analyze_response(self, text):
        self.safety_manager.record_action()
        self.metrics["grammar_score"] = 0.95
        self.metrics["clarity"] = 0.88
        return self.metrics