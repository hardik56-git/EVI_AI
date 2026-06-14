class CodeRunner:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.sandbox_timeout = 10
        self.blocked_modules = ['os.system', 'subprocess', 'socket', 'requests']
        
    def run(self, code):
        if not self.safety_manager.can_execute_tool('code_runner'):
            return {"error": "Permission denied - code runner blocked"}
            
        for blocked in self.blocked_modules:
            if blocked in code:
                return {"error": f"Dangerous code pattern blocked: {blocked}"}
                
        self.safety_manager.record_action()
        return {"status": "simulated_run", "output": "code executed safely"}