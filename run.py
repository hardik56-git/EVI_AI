#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from main import EVOAI

if __name__ == "__main__":
    ai = EVOAI()
    ai.start()
    
    if "--status" in sys.argv:
        print("System Status:")
        status = ai.safety_manager.get_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
    else:
        print("EVO_AI initialized. Use --status to check system health.")