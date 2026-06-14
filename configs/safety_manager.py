import yaml
import time
import psutil
import threading
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SafetyManager:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(BASE_DIR, "configs", "safety.yaml")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.action_count = 0
        self.modification_count = 0
        self.last_action_time = time.time()
        self.consecutive_failures = 0
        self.lock = threading.Lock()
        
    def check_emergency_conditions(self):
        with self.lock:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            
            if cpu > self.config['emergency_shutdown']['trigger_conditions'][1]['max_resource_usage_cpu']:
                print(f"[EMERGENCY] CPU usage {cpu}% exceeded limit")
                return True
                
            if memory > self.config['emergency_shutdown']['trigger_conditions'][2]['max_resource_usage_memory']:
                print(f"[EMERGENCY] Memory usage {memory}% exceeded limit")
                return True
                
            if self.consecutive_failures > self.config['emergency_shutdown']['trigger_conditions'][0]['max_consecutive_failures']:
                print(f"[EMERGENCY] Consecutive failures: {self.consecutive_failures}")
                return True
                
            return False
            
    def record_action(self, success=True):
        with self.lock:
            self.action_count += 1
            if not success:
                self.consecutive_failures += 1
            else:
                self.consecutive_failures = 0
            self.last_action_time = time.time()
            
    def record_modification(self):
        with self.lock:
            self.modification_count += 1
            if self.modification_count > self.config['emergency_shutdown']['trigger_conditions'][3]['max_self_modifications']:
                return False
            return True
            
    def can_execute_tool(self, tool_name, permission_level="standard"):
        level_config = self.config['permission_levels'].get(permission_level, {})
        if tool_name in level_config.get('denied', []):
            return level_config.get('requires_confirmation', False)
        return True
        
    def get_status(self):
        with self.lock:
            return {
                "actions_performed": self.action_count,
                "modifications_made": self.modification_count,
                "consecutive_failures": self.consecutive_failures,
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent
            }