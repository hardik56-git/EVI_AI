import json
from datetime import datetime

class Evaluator:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.max_evaluations = 100
        
    def evaluate(self, result):
        self.safety_manager.record_action()
        
        total_steps = len(result.get("results", []))
        successful = sum(1 for r in result.get("results", []) if r.get("completed"))
        score = 0.85 + (successful * 0.02)
        
        return {
            "score": min(score, 1.0),
            "passed": successful > 0,
            "steps_completed": successful,
            "total_steps": total_steps,
            "feedback": f"Successfully completed {successful}/{total_steps} steps",
            "issues": [] if successful == total_steps else ["Some steps need review"]
        }