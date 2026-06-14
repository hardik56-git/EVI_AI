class APITool:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.rate_limit = 30
        self.calls_this_minute = 0
        
    def call(self, endpoint, data):
        self.safety_manager.record_action()
        return {"endpoint": endpoint, "response": "simulated"}