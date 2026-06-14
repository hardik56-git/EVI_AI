class Optimizer:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.max_changes_per_run = 5
        
    def optimize(self, component, metrics):
        if not self.safety_manager.record_modification():
            return {"status": "blocked", "reason": "modification_limit_exceeded"}
            
        if self.safety_manager.check_emergency_conditions():
            return {"status": "emergency_shutdown"}
            
        changes_applied = 0
        improvements = []
        
        for metric, value in metrics.items():
            if changes_applied >= self.max_changes_per_run:
                break
            if value < 0.7:
                improvements.append(metric)
                changes_applied += 1
                
        self.safety_manager.record_action()
        return {"status": "optimized", "changes": improvements}