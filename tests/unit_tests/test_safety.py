import unittest
import sys
sys.path.insert(0, '..')
from configs.safety_manager import SafetyManager

class TestSafetyManager(unittest.TestCase):
    def test_emergency_conditions(self):
        sm = SafetyManager()
        result = sm.check_emergency_conditions()
        self.assertFalse(result)
        
    def test_action_recording(self):
        sm = SafetyManager()
        sm.record_action()
        status = sm.get_status()
        self.assertEqual(status["actions_performed"], 1)

if __name__ == '__main__':
    unittest.main()