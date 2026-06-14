class CompilerBuilder:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def build(self, language_spec):
        self.safety_manager.record_action()
        return {"compiler": "built", "spec": language_spec}