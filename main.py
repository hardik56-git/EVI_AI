import threading
import signal
import sys
from core.brain import Brain
from core.planner import Planner
from core.executor import Executor
from core.language_generator import LanguageGenerator
from self_improvement.evaluator import Evaluator
from configs.safety_manager import SafetyManager

class EVOAI:
    def __init__(self):
        self.safety_manager = SafetyManager()
        self.brain = Brain(self.safety_manager)
        self.planner = Planner(self.safety_manager)
        self.executor = Executor(self.safety_manager)
        self.evaluator = Evaluator(self.safety_manager)
        self.generator = LanguageGenerator(self.safety_manager)
        self.running = False
        self.emergency_lock = threading.Lock()
        
    def start(self):
        signal.signal(signal.SIGINT, self.emergency_shutdown)
        signal.signal(signal.SIGTERM, self.emergency_shutdown)
        self.running = True
        print("EVO_AI started with safety controls active")
        
    def emergency_shutdown(self, signum, frame):
        print("\n[EMERGENCY] Shutdown initiated! All operations stopped.")
        self.running = False
        with self.emergency_lock:
            sys.exit(0)
            
    def run_cycle(self, goal):
        if not self.running:
            return {"status": "error", "message": "AI not running"}
            
        if self.safety_manager.check_emergency_conditions():
            return {"status": "emergency_shutdown", "message": "Emergency conditions detected"}
            
        plan = self.planner.create_plan(goal)
        if not plan:
            return {"status": "error", "message": "Failed to create plan"}
            
        result = self.executor.execute(plan)
        evaluation = self.evaluator.evaluate(result)
        response = self.generator.generate_response(goal, plan, result, evaluation)
        
        return {"goal": goal, "plan": plan, "result": result, "evaluation": evaluation, "response": response}