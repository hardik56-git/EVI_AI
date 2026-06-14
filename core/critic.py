class Critic:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def evaluate_output(self, output):
        self.safety_manager.record_action()
        return {"quality": "good", "feedback": "Output meets standards"}