# EVO_AI - Self-Improving AI System

## Emergency Stop
If EVO_AI becomes unresponsive or acts unexpectedly:

1. **Immediate**: Ctrl+C to send SIGINT (graceful shutdown)
2. **Force kill**: `taskkill /PID <pid> /F` if needed
3. **Safety limits**: Check `configs/safety.yaml` for automatic shutdown thresholds

## Status Check
Run `python main.py --status` to see:
- Current CPU/Memory usage
- Action count
- Modification count
- Consecutive failures

## Permission Levels
- `read_only`: Safe mode (no code execution)
- `cautious`: Limited tools
- `standard`: Basic toolset (default)
- `experimental`: Full access with confirmation

## Health Monitoring
System checks every 30 seconds. Auto-shutdown triggers on:
- CPU > 90%
- Memory > 85%
- 10 consecutive failures
- 50 self-modifications limit