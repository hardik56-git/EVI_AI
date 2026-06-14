import sys
sys.path.insert(0, '.')
from main import EVOAI

def main():
    ai = EVOAI()
    ai.start()
    print("=" * 60)
    print("EVO_AI CLI Mode - Type 'quit' to exit, 'status' for system info")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if user_input.lower() == 'status':
                status = ai.safety_manager.get_status()
                print(f"Actions: {status['actions_performed']}")
                print(f"Failures: {status['consecutive_failures']}")
                print(f"CPU: {status['cpu_usage']}%")
                print(f"Memory: {status['memory_usage']}%")
                continue
            
            result = ai.run_cycle(user_input)
            if result.get('response'):
                print(result['response'])
            else:
                print(f"Status: {result.get('status', 'unknown')}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()