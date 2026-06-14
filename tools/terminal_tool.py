class TerminalTool:
    ALLOWED_COMMANDS = ['ls', 'pwd', 'date', 'echo', 'whoami']
    
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def execute(self, command):
        if not self.safety_manager.can_execute_tool('terminal_tool'):
            return {"error": "Permission denied - tool blocked by safety manager"}
            
        if any(dangerous in command for dangerous in ['rm', 'dd', 'mkfs', 'chmod 777', '> /dev']):
            return {"error": "Dangerous command blocked"}
            
        self.safety_manager.record_action()
        import subprocess
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
            return {"output": result.stdout, "error": result.stderr}
        except Exception as e:
            return {"error": str(e)}