class FileTool:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.allowed_extensions = ['.py', '.json', '.txt', '.md']
        
    def read(self, path):
        if not any(path.endswith(ext) for ext in self.allowed_extensions):
            return {"error": "File type not allowed"}
        self.safety_manager.record_action()
        with open(path, 'r') as f:
            return f.read()
            
    def write(self, path, content):
        if not any(path.endswith(ext) for ext in self.allowed_extensions):
            return {"error": "File type not allowed"}
        self.safety_manager.record_action()
        with open(path, 'w') as f:
            f.write(content)