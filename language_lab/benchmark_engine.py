class BenchmarkEngine:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def benchmark(self, component):
        self.safety_manager.record_action()
        return {"component": component, "score": 0.85}