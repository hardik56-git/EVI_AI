class Planner:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.max_steps = 50
        
    def create_plan(self, goal):
        steps = [f"step_{i}" for i in range(min(5, self.max_steps))]
        return {"goal": goal, "steps": steps, "validated": True}