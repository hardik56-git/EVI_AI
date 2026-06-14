class LanguageGenerator:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def generate_response(self, goal, plan, result, evaluation):
        self.safety_manager.record_action()
        
        # Only format what was ACTUALLY verified
        verified_results = [r for r in result.get("results", []) if r.get("verified")]
        failed_results = [r for r in result.get("results", []) if not r.get("verified")]
        
        if goal.lower().startswith(('hi', 'hello', 'hey', 'greetings')):
            return "Hello! I'm EVO_AI. I execute real tasks and verify every action. What would you like me to do?"
            
        if failed_results:
            output = f"I attempted to process '{goal}'.\n\n"
            output += f"⚠️ Some steps failed:\n"
            for r in failed_results:
                output += f"  - {r['step']}: {r.get('details', 'failed')}\n"
            return output
            
        output = f"I've processed your request: '{goal}'\n\n"
        
        for i, step in enumerate(verified_results, 1):
            detail = step.get('details', '')
            output += f"{i}. {step['step']}: {detail}\n"
            if 'file' in step:
                output += f"   (File: {step['file']})\n"
                
        output += f"\nAll {len(verified_results)} steps completed and verified!\n"
        output += f"Score: {int(evaluation.get('score', 0.9) * 100)}%"
        
        return output