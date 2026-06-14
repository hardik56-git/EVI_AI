class GoalManager:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.goals = []
        
    def add_goal(self, goal):
        if self.safety_manager.check_emergency_conditions():
            return False
        self.goals.append(goal)
        return True
        
    def get_priority_goal(self):
        return self.goals[0] if self.goals else None