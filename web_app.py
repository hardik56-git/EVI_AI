import sys
sys.path.insert(0, '.')
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from main import EVOAI

app = Flask(__name__)
CORS(app)
ai = EVOAI()
ai.start()

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>EVO_AI Assistant</title>
    <style>
        :root { --primary: #4299e1; --danger: #e53e3e; --dark: #2d3748; --light: #f7fafc; --border: #e2e8f0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, var(--dark), #1a202c); color: white; padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .header h1 { font-size: 28px; font-weight: 600; }
        .header p { opacity: 0.8; margin-top: 5px; }
        .status-bar { display: flex; gap: 15px; margin-bottom: 20px; }
        .status-card { flex: 1; background: white; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .status-card .label { font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 1px; }
        .status-card .value { font-size: 24px; font-weight: 700; color: var(--dark); margin-top: 5px; }
        .chat-container { background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow: hidden; }
        .chat-header { background: var(--light); padding: 12px 20px; border-bottom: 1px solid var(--border); font-weight: 600; color: #4a5568; }
        .chat-messages { min-height: 200px; padding: 20px; max-height: 400px; overflow-y: auto; }
        .message { margin-bottom: 15px; padding: 12px 15px; border-radius: 8px; background: var(--light); line-height: 1.6; }
        .message.ai { border-left: 4px solid var(--primary); }
        .input-area { display: flex; gap: 10px; padding: 15px 20px; background: white; border-top: 1px solid var(--border); }
        #goal { flex: 1; padding: 14px; border: 2px solid var(--border); border-radius: 8px; font-size: 16px; outline: none; transition: border-color 0.2s; }
        #goal:focus { border-color: var(--primary); }
        .btn { padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: opacity 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-danger { background: var(--danger); color: white; }
        .footer { text-align: center; margin-top: 20px; color: #718096; font-size: 12px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>EVO_AI Assistant</h1>
        <p>Self-improving AI with safety controls</p>
    </div>
    
    <div class="status-bar">
        <div class="status-card"><div class="label">Actions</div><div class="value" id="actions">0</div></div>
        <div class="status-card"><div class="label">Failures</div><div class="value" id="failures">0</div></div>
        <div class="status-card"><div class="label">Memory</div><div class="value" id="memory">0%</div></div>
        <div class="status-card"><div class="label">Status</div><div class="value" style="color:#48bb78" id="status">Ready</div></div>
    </div>
    
    <div class="chat-container">
        <div class="chat-header">Chat</div>
        <div class="chat-messages" id="result">
            <div class="message ai">Hello! I'm EVO_AI. Type your request to get started.</div>
        </div>
        <div class="input-area">
            <input type="text" id="goal" placeholder="Ask me to study, code, or help with anything..." onkeyup="if(event.key==='Enter') sendGoal()">
            <button class="btn btn-primary" onclick="sendGoal()">Send</button>
            <button class="btn btn-danger" onclick="emergencyStop()">Stop</button>
        </div>
    </div>
    
    <div class="footer">Press Enter to send | Emergency Stop protects against runaway AI</div>
</div>

<script>
async function fetchStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        document.getElementById('actions').textContent = data.actions_performed;
        document.getElementById('failures').textContent = data.consecutive_failures;
        document.getElementById('memory').textContent = data.memory_usage + '%';
        document.getElementById('status').textContent = 'Ready';
    } catch(e) {
        document.getElementById('status').textContent = 'Offline';
        console.log('Status error:', e);
    }
}

function formatOutput(data) {
    if (data.status === 'error') return `<div class="message" style="color:red">Error: ${data.message}</div>`;
    if (data.response) return `<div class="message ai">${data.response.replace(/\\n/g, '<br>')}</div>`;
    return `<div class="message ai">Task completed (${Math.round((data.evaluation?.score || 0) * 100)}%)</div>`;
}

async function sendGoal() {
    const goal = document.getElementById('goal').value;
    if (!goal.trim()) return;
    
    // Add user message
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML += `<div class="message" style="background:#ebf8ff;text-align:right">You: ${goal}</div>`;
    document.getElementById('goal').value = '';
    
    // Show processing
    resultDiv.innerHTML += `<div class="message ai">EVO_AI is thinking...</div>`;
    resultDiv.scrollTop = resultDiv.scrollHeight;
    
    try {
        const res = await fetch('/api/execute', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({goal: goal})
        });
        const data = await res.json();
        resultDiv.innerHTML = resultDiv.innerHTML.replace('thinking...', 'idle');
        resultDiv.innerHTML += formatOutput(data);
        resultDiv.scrollTop = resultDiv.scrollHeight;
    } catch (error) {
        resultDiv.innerHTML = resultDiv.innerHTML.replace('thinking...', 'error');
        resultDiv.innerHTML += `<div class="message" style="color:red">Connection error: ${error.message}</div>`;
        console.error('Execute error:', error);
    }
}

async function emergencyStop() {
    if (confirm('EMERGENCY STOP - Are you sure?')) {
        await fetch('/api/emergency_stop', {method: 'POST'});
        document.getElementById('result').innerHTML += `<div class="message" style="color:red;font-weight:bold">EVO_AI STOPPED</div>`;
    }
}

// Load status on start
fetchStatus();
setInterval(fetchStatus, 2000);
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
    app.run(host='127.0.0.1', port=5555, debug=False, threaded=True)