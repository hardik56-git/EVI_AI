import os
from datetime import datetime

class Verifier:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        self.verifications = []
        
    def verify_action(self, action_type, details):
        verified = False
        evidence = None
        
        if action_type == "file_created":
            path = details.get("path")
            if path and os.path.exists(path):
                verified = True
                evidence = {"exists": True, "size": os.path.getsize(path)}
            else:
                evidence = {"exists": False, "path": path}
                
        elif action_type == "task_completed":
            verified = details.get("success", False)
            evidence = {"status": "verified" if verified else "failed"}
            
        elif action_type == "process_ran":
            verified = "result" in details
            evidence = details
            
        self.safety_manager.record_action(success=verified)
        self.verifications.append({
            "type": action_type,
            "verified": verified,
            "evidence": evidence,
            "timestamp": str(datetime.now())
        })
        
        return {"verified": verified, "evidence": evidence}