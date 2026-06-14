# EVO_AI Architecture Redesign

## Current Flow (BROKEN)
```
User Goal → Planner (fake steps) → Executor (fake results) → Evaluator (fake score) → LanguageGenerator (formats lies)
```

## Required Flow (REAL)
```
User Goal
    ↓
Planner → ACTUAL task breakdown
    ↓
Executor → REAL tool calls (FileTool, TerminalTool, etc.)
    ↓
Verifier → CONFIRM each action happened
    ↓
Critic → REAL analysis of results
    ↓
Reflector → STORE lessons in memory
    ↓
MemoryManager → PERSIST verified results
    ↓
ImprovementEngine → TRACK performance
```

## Module Fixes Required

### 1. Brain (core/brain.py)
- Parse goal intent using actual NLP
- Extract entities, actions, requirements
- Risk: HIGH

### 2. Planner (core/planner.py)
- Parse goal into executable subtasks
- Use actual task decomposition logic
- Prioritize based on dependencies
- Risk: HIGH

### 3. Executor (core/executor.py)
- CALL REAL TOOLS (FileTool.create_file, TerminalTool.run, etc.)
- Execute actual operations
- Return VERIFIED results
- Risk: HIGH

### 4. Verifier (NEW: core/verifier.py)
- Check file existence after claim
- Verify process completion
- Confirm outputs match expectations
- Risk: CRITICAL - MISSING

### 5. Critic (core/critic.py)
- Compare expected vs actual results
- Identify errors/gaps
- Generate improvement suggestions
- Risk: HIGH

### 6. Reflector (core/reflector.py)
- Extract patterns from successful runs
- Store lessons in MemoryManager
- Risk: MEDIUM

### 7. MemoryManager (memory/memory_manager.py)
- Connect to ACTUAL workflow
- Store verified experiences
- Risk: MEDIUM - exists but unused

### 8. LanguageGenerator (core/language_generator.py)
- ONLY format ACTUALLY verified results
- NO fake claims
- Risk: LOW

## Implementation Priority

1. **VERIFIER** - Cannot claim actions without this
2. **EXECUTOR** - Must call real tools
3. **PLANNER** - Must create real tasks
4. **CRITIC** - Must analyze real results
5. **MEMORY_INTEGRATION** - Must persist real data
6. **REFLECTOR** - Must learn from real runs