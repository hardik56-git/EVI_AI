class Critic:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def evaluate_output(self, result):
        self.safety_manager.record_action()
        
        total = len(result.get("results", []))
        verified = sum(1 for r in result.get("results", []) if r.get("verified"))
        
        score = verified / total if total > 0 else 0
        passed = verified == total
        
        return {
            "score": score,
            "passed": passed,
            "verified_count": verified,
            "total_count": total,
            "feedback": f"{'All' if passed else verified}/{total} steps verified successfully"
        }