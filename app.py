from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from concurrent.futures import ThreadPoolExecutor
import os
import asyncio

from multi_agent import run_research

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=3)

# HTML as a string — no Jinja2 needed
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Agent Research Assistant</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
        .container { max-width: 900px; margin-top: 3rem; }
        .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; }
        .form-control { background-color: #0d1117; border: 1px solid #30363d; color: #e6edf3; }
        .form-control:focus { background-color: #0d1117; border-color: #58a6ff; color: #e6edf3; box-shadow: none; }
        .btn-primary { background-color: #238636; border-color: #238636; }
        .btn-primary:hover { background-color: #2ea043; border-color: #2ea043; }
        #report { white-space: pre-wrap; line-height: 1.8; font-size: 16px; color: #e6edf3; }
        .spinner-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(13,17,23,0.9); z-index: 9999; text-align: center; padding-top: 20%; }
        .agent-status { color: #58a6ff; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>

<div class="spinner-overlay" id="spinner">
    <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
    <p class="mt-3 text-white">Agents are researching...</p>
    <p class="agent-status" id="agentStatus"></p>
</div>

<div class="container">
    <div class="text-center mb-5">
        <h1 class="fw-bold" style="color: #e6edf3;">Multi-Agent Research Assistant</h1>
        <p style="color: #8b949e;">5 AI agents work together: Researcher - Analyst - Writer - Critic - Editor</p>
    </div>

    <div class="card p-4 mb-4">
        <form id="researchForm">
            <div class="mb-3">
                <label class="form-label fw-semibold" style="color: #e6edf3;">Research Topic</label>
                <input type="text" id="topic" class="form-control form-control-lg" 
                       placeholder="e.g. How is AI transforming cybersecurity in 2025?" required>
            </div>
            <button type="submit" class="btn btn-primary btn-lg w-100">
                Generate Research Report
            </button>
        </form>
    </div>

    <div id="resultSection" style="display: none;">
        <div class="card p-4">
            <h5 class="mb-3" style="color: #7ee787;">Research Report</h5>
            <div id="report"></div>
        </div>
    </div>
</div>

<script>
    const form = document.getElementById('researchForm');
    const spinner = document.getElementById('spinner');
    const resultSection = document.getElementById('resultSection');
    const reportDiv = document.getElementById('report');
    const agentStatus = document.getElementById('agentStatus');
    const topicInput = document.getElementById('topic');

    const statusMessages = [
        "Agent 1: Researcher gathering information...",
        "Agent 2: Analyst extracting key insights...",
        "Agent 3: Writer drafting the report...",
        "Agent 4: Critic reviewing the report...",
        "Agent 5: Editor finalizing the report..."
    ];

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const topic = topicInput.value.trim();
        if (!topic) return;

        spinner.style.display = 'block';
        resultSection.style.display = 'none';
        
        let statusIndex = 0;
        const statusInterval = setInterval(() => {
            agentStatus.textContent = statusMessages[statusIndex % statusMessages.length];
            statusIndex++;
        }, 5000);

        try {
            const response = await fetch('/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ topic: topic })
            });

            const data = await response.json();
            
            clearInterval(statusInterval);
            spinner.style.display = 'none';
            resultSection.style.display = 'block';
            reportDiv.innerHTML = data.report.replace(/\\n/g, '<br>');
            
        } catch (error) {
            clearInterval(statusInterval);
            spinner.style.display = 'none';
            reportDiv.innerHTML = '<p class="text-danger">Error generating report. Please try again.</p>';
            resultSection.style.display = 'block';
        }
    });
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=HTML_PAGE)

@app.post("/research")
async def research(topic: str = Form(...)):
    loop = asyncio.get_running_loop()
    report = await loop.run_in_executor(executor, run_research, topic)
    return {"report": report}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))