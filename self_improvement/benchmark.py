class Benchmark:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def run_benchmark(self, test_name):
        self.safety_manager.record_action()
        return {"test": test_name, "passed": True, "score": 0.92}