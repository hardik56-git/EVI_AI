import os
import sys
from datetime import datetime
from core.brain import Brain
from core.planner import Planner
from core.executor import Executor
from core.verifier import Verifier
from core.critic import Critic
from core.reflector import Reflector
from core.language_generator import LanguageGenerator
from memory.memory_manager import MemoryManager
from configs.safety_manager import SafetyManager

class EVOAI:
    def __init__(self):
        self.safety_manager = SafetyManager()
        self.verifier = Verifier(self.safety_manager)
        self.memory = MemoryManager()
        self.brain = Brain(self.safety_manager)
        self.planner = Planner(self.safety_manager)
        self.executor = Executor(self.safety_manager)
        self.critic = Critic(self.safety_manager)
        self.reflector = Reflector(self.safety_manager)
        self.generator = LanguageGenerator(self.safety_manager)
        self.running = True
        
    def run_cycle(self, goal):
        if not self.running:
            return {"status": "error", "message": "AI not running"}
            
        # 1. PLANNER - Create real plan
        plan = self.planner.create_plan(goal)
        if not plan:
            return {"status": "error", "message": "Failed to create plan"}
        
        # 2. EXECUTOR - Execute real actions
        result = self.executor.execute(plan)
        
        # 3. VERIFIER - Verify each claimed action
        verified_results = []
        for step_result in result.get("results", []):
            if step_result.get("verified") and "file" in step_result:
                verification = self.verifier.verify_action("file_created", {"path": step_result["file"]})
                step_result["verification"] = verification
            verified_results.append(step_result)
        result["results"] = verified_results
        
        # 4. CRITIC - Real critique
        critique = self.critic.evaluate_output(result)
        
        # 5. MEMORY - Actually store
        self.memory.remember(goal, result, long_term=True)
        
        # 6. REFLECTOR - Learn from result
        self.reflector.reflect(result)
        
        # 7. LANGUAGE GENERATOR - Only format verified results
        response = self.generator.generate_response(goal, plan, result, critique)
        
        return {"goal": goal, "plan": plan, "result": result, "evaluation": critique, "response": response}