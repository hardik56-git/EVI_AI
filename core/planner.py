class Planner:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def create_plan(self, goal):
        self.safety_manager.record_action()
        
        goal_lower = goal.lower().strip()
        tasks = []
        
        if "create" in goal_lower or "write" in goal_lower:
            tasks = ["analyze_requirements", "design_solution", "implement", "test_output", "verify_result"]
        elif "study" in goal_lower or "learn" in goal_lower or "plan" in goal_lower:
            tasks = ["analyze_subject", "research_resources", "create_schedule", "set_milestones", "review_plan"]
        elif "code" in goal_lower or "program" in goal_lower:
            tasks = ["understand_requirements", "design_architecture", "write_code", "add_tests", "document"]
        else:
            tasks = [f"analyze_{i}" for i in range(5)]
            
        return {"goal": goal, "tasks": tasks, "steps": tasks, "validated": True}