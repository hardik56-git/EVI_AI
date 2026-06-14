class LanguageDesigner:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def design(self, requirements):
        self.safety_manager.record_action()
        return {"design": requirements, "status": "drafted"}