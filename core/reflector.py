class Reflector:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.insights = []
        
    def reflect(self, execution_result):
        self.safety_manager.record_action()
        insight = f"Learned from: {execution_result.get('status', 'unknown')}"
        self.insights.append(insight)
        return {"insights": self.insights[-5:]}