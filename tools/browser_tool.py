class BrowserTool:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.blocked_domains = ['localhost', '127.0.0.1', '0.0.0.0']
        
    def fetch(self, url):
        if any(blocked in url for blocked in self.blocked_domains):
            return {"error": "Local/network access blocked for security"}
        self.safety_manager.record_action()
        return {"url": url, "content": "fetched (simulated)"}