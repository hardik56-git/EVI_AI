from datetime import datetime

class SkillTracker:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.skills = {}
        
    def track(self, skill_name, progress):
        self.safety_manager.record_action()
        self.skills[skill_name] = {
            "progress": progress,
            "last_updated": str(datetime.now())
        }
        return self.skills[skill_name]