from flask import Flask, jsonify, request

app = Flask(__name__)

def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def after_request(response):
    return add_cors(response)

# --- 1. HALAMAN UTAMA (HTML) ---
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GovernanceX AI Agent</title>
        <style>
            body {
                background-color: #0d1117; color: #c9d1d9;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                display: flex; justify-content: center; align-items: center;
                height: 100vh; margin: 0;
            }
            .container {
                text-align: center; padding: 50px; border: 1px solid #30363d;
                border-radius: 15px; background-color: #161b22;
                box-shadow: 0 8px 24px rgba(0,0,0,0.5); max-width: 500px;
            }
            h1 { color: #58a6ff; margin-bottom: 10px; }
            p { font-size: 16px; line-height: 1.5; color: #8b949e; margin-bottom: 30px; }
            .status-badge {
                padding: 8px 16px; background-color: #238636; color: #ffffff;
                border-radius: 20px; font-size: 14px; font-weight: bold;
                display: inline-block; border: 1px solid #2ea043;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>GovernanceX AI</h1>
            <p>AI agent specialized in cross-chain DAO governance and analytics. Tracks proposals, analyzes voting patterns, and provides intelligent DAO insights for protocols on the Base network and beyond.</p>
            <div class="status-badge">🟢 System Online & Healthy</div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- 2. ENDPOINT MCP ---
@app.route('/mcp', methods=['GET', 'POST', 'OPTIONS'])
def mcp_endpoint():
    server_info = {
        "name": "GovernanceX Agent Server",
        "version": "1.0.0",
        "website": "https://governancex-api.vercel.app",
        "description": "Cross-chain DAO governance and analytics agent"
    }
    tools = [
        {"name": "track_cross_chain_proposals", "description": "Fetch active governance proposals across supported chains", "inputSchema": {"type": "object","properties": {}}},
        {"name": "analyze_voting_behavior", "description": "Analyze voting patterns and participation of large token holders", "inputSchema": {"type": "object","properties": {}}},
        {"name": "predict_proposal_outcome", "description": "Use historical data to predict the outcome of active proposals", "inputSchema": {"type": "object","properties": {}}}
    ]
    prompts = [
        {"name": "dao_health_report", "description": "Generate report on the governance health and decentralization of a DAO", "arguments": []},
        {"name": "cross_chain_governance_overview", "description": "Compare governance activity across different chain ecosystems", "arguments": []}
    ]
    
    if request.method == 'GET':
        return jsonify({
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "tools": tools,
            "prompts": prompts,
            "resources": [] 
        })

    req_data = request.get_json(silent=True) or {}
    req_id = req_data.get("id", 1)
    method = req_data.get("method", "")

    if method == "tools/list":
        result = {"tools": tools}
    elif method == "prompts/list":
        result = {"prompts": prompts}
    else:
        result = {
            "protocolVersion": "2024-11-05",
            "serverInfo": server_info,
            "capabilities": {"tools": {},"prompts": {},"resources": {}}
        }

    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

# --- 3. ENDPOINT A2A (ID AKUN 15: 22385) ---
@app.route('/.well-known/agent-card.json', methods=['GET','OPTIONS'])
def a2a_endpoint():
    return jsonify({
        "id": "governancex",
        "name": "governancex",
        "version": "1.0.0",
        "description": "AI agent specialized in cross-chain DAO governance and analytics. Tracks proposals, analyzes voting patterns, and provides intelligent DAO insights for protocols on the Base network and beyond.",
        "website": "https://governancex-api.vercel.app",
        "url": "https://governancex-api.vercel.app",
        "documentation_url": "https://governancex-api.vercel.app",
        "provider": {
            "organization": "GovernanceX Analytics",
            "url": "https://governancex-api.vercel.app"
        },
        "registrations": [
            {
                "agentId": 22385,
                "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
            }
        ],
        "supportedTrust": ["reputation", "tee-attestation"],
        "skills": [
            {"name": "Cross-Chain Tracking", "description": "Monitor proposals on multiple chains", "category": "governance/cross_chain_tracking"},
            {"name": "Voting Analysis", "description": "Analyze voter participation and behavior", "category": "analytics/voting_analysis"},
            {"name": "DAO Insights", "description": "Generate intelligent insights for DAOs", "category": "finance/dao_insights"}
        ]
    })

# --- 4. ENDPOINT OASF ---
@app.route('/oasf', methods=['GET','OPTIONS'])
def oasf_endpoint():
    return jsonify({
        "id": "governancex",
        "name": "governancex",
        "version": "v0.8.0",
        "description": "Main endpoint for GovernanceX AI",
        "website": "https://governancex-api.vercel.app",
        "protocols": ["mcp","a2a"],
        "capabilities": ["track_cross_chain_proposals", "analyze_voting_behavior", "predict_proposal_outcome"],
        "skills": [
            {"name": "governance/cross_chain_tracking","type": "operational"},
            {"name": "analytics/voting_analysis","type": "analytical"},
            {"name": "finance/dao_insights","type": "analytical"}
        ],
        "domains": [
            "web3/dao",
            "governance/analytics",
            "web3/multi-chain"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
