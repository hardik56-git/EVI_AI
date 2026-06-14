import sys
sys.path.insert(0, '.')
from flask import Flask, render_template, request, jsonify
from main import EVOAI

app = Flask(__name__)
ai = EVOAI()
ai.start()  # Start AI when module loads

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>EVO_AI Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: #2d3748; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .header h1 { font-size: 24px; }
        .status-card { background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
        .status-item { text-align: center; padding: 10px; background: #edf2f7; border-radius: 6px; }
        .status-label { font-size: 12px; color: #718096; }
        .status-value { font-size: 20px; font-weight: bold; color: #2d3748; }
        .chat-container { background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 20px; }
        .input-area { display: flex; gap: 10px; margin-top: 15px; }
        #goal { flex: 1; padding: 12px; border: 2px solid #e2e8f0; border-radius: 6px; font-size: 16px; }
        button { padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .btn-execute { background: #4299e1; color: white; }
        .btn-stop { background: #e53e3e; color: white; }
        #result { margin-top: 20px; padding: 15px; background: #f7fafc; border-radius: 6px; font-family: 'Segoe UI', sans-serif; font-size: 14px; min-height: 100px; border: 1px solid #e2e8f0; line-height: 1.6; }
        .output-section { margin-top: 15px; }
        .output-title { font-weight: bold; color: #4a5568; margin-bottom: 8px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>EVO_AI Assistant</h1>
    </div>
    
    <div class="status-card">
        <div class="status-grid">
            <div class="status-item"><div class="status-label">Actions</div><div class="status-value" id="actions">0</div></div>
            <div class="status-item"><div class="status-label">Modifications</div><div class="status-value" id="mods">0</div></div>
            <div class="status-item"><div class="status-label">Failures</div><div class="status-value" id="failures">0</div></div>
            <div class="status-item"><div class="status-label">Memory</div><div class="status-value" id="memory">0%</div></div>
        </div>
    </div>
    
    <div class="chat-container">
        <div class="input-area">
            <input type="text" id="goal" placeholder="Enter your goal or question...">
            <button class="btn-execute" onclick="sendGoal()">Execute</button>
            <button class="btn-stop" onclick="emergencyStop()">EMERGENCY STOP</button>
        </div>
        
        <div class="output-section">
            <div class="output-title">Result:</div>
            <div id="result">Ready for input...</div>
        </div>
    </div>
</div>

<script>
async function fetchStatus() {
    const res = await fetch('/api/status');
    const data = await res.json();
    document.getElementById('actions').textContent = data.actions_performed;
    document.getElementById('mods').textContent = data.modifications_made;
    document.getElementById('failures').textContent = data.consecutive_failures;
    document.getElementById('memory').textContent = data.memory_usage + '%';
}

function formatOutput(data) {
    if (data.status === 'error') return `<span style="color:red">❌ Error: ${data.message}</span>`;
    if (data.response) return data.response.replace(/\n/g, '<br>');
    
    // Fallback for older response format
    let output = `I've processed your request: ${data.goal}<br><br>`;
    output += `Status: ${data.result?.status || 'unknown'}<br>`;
    output += `Score: ${Math.round((data.evaluation?.score || 0) * 100)}%`;
    return output;
}

async function sendGoal() {
    const goal = document.getElementById('goal').value;
    if (!goal) return;
    document.getElementById('result').innerHTML = 'Processing...';
    const res = await fetch('/api/execute', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({goal: goal})
    });
    const data = await res.json();
    document.getElementById('result').innerHTML = formatOutput(data);
}

async function emergencyStop() {
    if (confirm('Are you sure? This will stop EVO_AI immediately!')) {
        await fetch('/api/emergency_stop', {method: 'POST'});
        document.getElementById('result').innerHTML = 'EMERGENCY STOP ACTIVATED';
    }
}

setInterval(fetchStatus, 2000);
fetchStatus();
</script>
</body>
</html>'''

@app.route('/api/status')
def status():
    return jsonify(ai.safety_manager.get_status())

@app.route('/api/execute', methods=['POST'])
def execute():
    goal = request.json.get('goal', '')
    result = ai.run_cycle(goal)
    # Debug: ensure response is included
    if 'response' not in result and goal:
        result['response'] = f"Processed: {goal}. Status: {result.get('result', {}).get('status', 'unknown')}"
    return jsonify(result)

@app.route('/api/emergency_stop', methods=['POST'])
def emergency_stop():
    import os
    os._exit(0)

if __name__ == '__main__':
    ai.start()
    app.run(host='0.0.0.0', port=8080, debug=False)