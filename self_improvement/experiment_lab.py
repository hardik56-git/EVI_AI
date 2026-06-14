import threading
import time

class ExperimentLab:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.max_experiments = 10
        self._experiments_run = 0
        self.lock = threading.Lock()
        
    def run_experiment(self, hypothesis):
        with self.lock:
            if self._experiments_run >= self.max_experiments:
                return {"status": "limit_reached", "message": "Max experiments reached"}
            self._experiments_run += 1
            
        if self.safety_manager.check_emergency_conditions():
            return {"status": "emergency_shutdown"}
            
        self.safety_manager.record_action()
        return {"hypothesis": hypothesis, "result": "tested", "success": True}