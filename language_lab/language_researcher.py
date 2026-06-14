class LanguageResearcher:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.findings = []
        
    def research(self, topic):
        self.safety_manager.record_action()
        self.findings.append({"topic": topic, "research_completed": True})
        return self.findings[-1]