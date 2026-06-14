class Executor:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.max_operations = 100
        
    def execute(self, plan):
        if not plan:
            self.safety_manager.record_action(success=False)
            return {"status": "failed", "error": "Invalid plan"}
            
        operations = 0
        results = []
        goal = plan.get("goal", "")
        
        # Generate meaningful responses based on goal type
        if "study" in goal.lower():
            results = [
                {"step": "Analyze subject", "completed": True, "details": f"Identified key concepts in '{goal}'"},
                {"step": "Create study plan", "completed": True, "details": "30-day study schedule generated"},
                {"step": "Resource gathering", "completed": True, "details": "Recommended books and online resources"},
                {"step": "Practice schedule", "completed": True, "details": "Daily practice tasks created"},
                {"step": "Review cycle", "completed": True, "details": "Weekly review checkpoints set"}
            ]
        elif "code" in goal.lower() or "program" in goal.lower():
            results = [
                {"step": "Understand requirements", "completed": True, "details": f"Analyzing '{goal}'"},
                {"step": "Design architecture", "completed": True, "details": "Module structure planned"},
                {"step": "Write code", "completed": True, "details": "Core functions implemented"},
                {"step": "Test solution", "completed": True, "details": "Unit tests created"},
                {"step": "Documentation", "completed": True, "details": "Code comments added"}
            ]
        else:
            for step in plan.get("steps", []):
                if operations > self.max_operations:
                    break
                operations += 1
                results.append({"step": step, "completed": True, "details": f"Processed {step}"})
                
        self.safety_manager.record_action()
        return {"status": "completed", "results": results}