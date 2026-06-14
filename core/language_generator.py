class LanguageGenerator:
    def __init__(self, safety_manager):
        self.safety_manager = safety_manager
        
    def generate_response(self, goal, plan, result, evaluation):
        self.safety_manager.record_action()
        
        if goal.lower().startswith(('hi', 'hello', 'hey')):
            return "Hello! I'm EVO_AI, your self-improvement assistant. How can I help you today?"
            
        if "study" in goal.lower():
            return self._study_plan_response(goal, result)
            
        if "code" in goal.lower() or "program" in goal.lower() or "write" in goal.lower():
            return self._coding_response(goal, result)
            
        if "help" in goal.lower() or "what" in goal.lower() or "can you" in goal.lower():
            return self._help_response()
            
        return self._default_response(goal, result, evaluation)
        
    def _study_plan_response(self, goal, result):
        output = f"I've analyzed your request: '{goal}'. Here's my plan:\n\n"
        for i, step in enumerate(result.get("results", []), 1):
            output += f"{i}. {step['step']}: {step.get('details', 'Completed')}\n"
        output += f"\nAll steps completed successfully! Would you like me to dive deeper into any specific area?"
        return output
        
    def _coding_response(self, goal, result):
        output = f"I can help you with '{goal}'. My approach:\n\n"
        for i, step in enumerate(result.get("results", []), 1):
            output += f"{i}. {step['step']} - {step.get('details', 'Ready to proceed')}\n"
        output += f"\nLet me know which programming language you prefer, and I'll generate the code structure!"
        return output
        
    def _help_response(self):
        return """I can help you with:
* Study planning and learning schedules  
* Writing and debugging code
* Research and analysis tasks
* Problem-solving and optimization

Just type your request and I'll create a plan to accomplish it.
Example: 'create a study plan for machine learning' or 'write a Python web scraper'"""
        
    def _default_response(self, goal, result, evaluation):
        output = f"I've processed your request: '{goal}'.\n\n"
        output += f"The task was {result['status']}.\n"
        output += f"{evaluation.get('feedback', '')}\n"
        output += f"(Score: {int(evaluation['score']*100)}%)"
        return output