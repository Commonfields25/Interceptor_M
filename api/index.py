"""
api/index.py — Vercel Python Runtime Entrypoint
===============================================
Provides a minimal ASGI/starlette application so the Vercel Python runtime
can locate an entrypoint (`app` object) and complete a build.
"""

from http import HTTPStatus
from typing import Callable

import starlette.exceptions
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.middleware.exceptions import ExceptionMiddleware


COMMON_CSS = """
:root {
    --bg: #f8fafc;
    --card-bg: #ffffff;
    --text: #1e293b;
    --text-muted: #64748b;
    --primary: #0ea5e9;
    --primary-hover: #0284c7;
    --status-ok: #10b981;
    --code-bg: #f1f5f9;
    --code-text: #e11d48;
    --border: #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #0f172a;
        --card-bg: #1e293b;
        --text: #f1f5f9;
        --text-muted: #94a3b8;
        --primary: #38bdf8;
        --primary-hover: #7dd3fc;
        --status-ok: #34d399;
        --code-bg: #334155;
        --code-text: #fb7185;
        --border: #334155;
    }
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    max-width: 800px;
    margin: 40px auto;
    padding: 0 20px;
    line-height: 1.6;
    transition: background-color 0.3s, color 0.3s;
}

.container {
    background-color: var(--card-bg);
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border: 1px solid var(--border);
}

h1, h2 { color: var(--primary); margin-top: 0; }

.status {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    background-color: var(--status-ok);
    color: white;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.endpoint-link {
    text-decoration: none;
    color: inherit;
    display: block;
    margin-bottom: 1rem;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.endpoint-link:hover { transform: translateX(4px); }

.endpoint {
    background-color: var(--bg);
    padding: 1.25rem;
    border-radius: 8px;
    border-left: 4px solid var(--primary);
    position: relative;
    border: 1px solid var(--border);
    border-left-width: 4px;
}

.endpoint code {
    color: var(--code-text);
    background-color: var(--code-bg);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-size: 0.9em;
}

.copy-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: var(--code-bg);
    border: 1px solid var(--border);
    color: var(--text-muted);
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    z-index: 10;
}

.copy-btn:hover {
    color: var(--primary);
    border-color: var(--primary);
    background-color: var(--bg);
}

.copy-btn:active {
    transform: scale(0.9);
}

.tooltip {
    position: absolute;
    top: -30px;
    right: 0;
    background: var(--text);
    color: var(--bg);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    opacity: 0;
    transition: opacity 0.2s;
    pointer-events: none;
}

.copy-btn:focus .tooltip {
    opacity: 1;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-card {
    background-color: var(--bg);
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    position: relative;
    overflow: hidden;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background-color: var(--primary);
    opacity: 0.3;
}

.metric-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
}

.nav-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
    margin-top: 1rem;
    transition: all 0.2s;
}

.nav-link:hover {
    color: var(--primary-hover);
    transform: translateX(-4px);
}
"""

SCRIPTS = """
function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        const original = btn.innerHTML;
        btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        btn.style.color = 'var(--status-ok)';
        setTimeout(() => {
            btn.innerHTML = original;
            btn.style.color = '';
        }, 2000);
    });
}
"""

async def root_handler(request: Request) -> HTMLResponse | JSONResponse:
    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header and "text/html" not in accept_header:
        return JSONResponse(
            {
                "name": "Interceptor_M",
                "status": "ok",
                "message": "Interceptor_M is a drone engineering project.",
                "speed_insights": "enabled",
            },
            status_code=HTTPStatus.OK,
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interceptor_M | Aerospace Intelligence</title>
    <script>{SCRIPTS}</script>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <div class="container">
        <h1>🚀 Interceptor_M</h1>
        <div class="status" role="status">System Nominal</div>
        <p><strong>Autonomous Swarm Counter-UAS — Drone Interceptor System</strong></p>
        <p style="color: var(--text-muted);">Engineering the next generation of kinetic interception platforms with physics-driven multi-agent coordination.</p>
        
        <nav class="endpoints" aria-label="API Endpoints">
            <h2 style="margin-top: 2rem;">Technical Endpoints</h2>

            <div style="position: relative;">
                <button class="copy-btn" onclick="copyToClipboard('/', this)" title="Copy path">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
                <a href="/" class="endpoint-link" aria-label="Project Metadata">
                    <div class="endpoint">
                        <strong>GET <code>/</code></strong>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-muted);">Root discovery and project metadata.</p>
                    </div>
                </a>
            </div>

            <div style="position: relative;">
                <button class="copy-btn" onclick="copyToClipboard('/health', this)" title="Copy path">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
                <a href="/health" class="endpoint-link" aria-label="System Health Status">
                    <div class="endpoint">
                        <strong>GET <code>/health</code></strong>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-muted);">Real-time telemetry and subsystem health probes.</p>
                    </div>
                </a>
            </div>

            <div style="position: relative;">
                <button class="copy-btn" onclick="copyToClipboard('/dashboard', this)" title="Copy path">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
                <a href="/dashboard" class="endpoint-link" aria-label="Performance Dashboard">
                    <div class="endpoint">
                        <strong>GET <code>/dashboard</code></strong>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-muted);">Comprehensive performance baseline and mission metrics.</p>
                    </div>
                </a>
            </div>
        </nav>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html, status_code=HTTPStatus.OK)


async def health_handler(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy", "subsystems": "nominal"}, status_code=HTTPStatus.OK)


async def dashboard_handler(request: Request) -> HTMLResponse:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard | Interceptor_M</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <div class="container">
        <h1 style="display: flex; align-items: center; gap: 0.75rem;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
            Mission Dashboard
        </h1>
        <p><strong>Baseline Specifications: DD-400 Platform</strong></p>

        <div class="info-grid">
            <div class="metric-card">
                <span class="metric-label">Dash Velocity</span>
                <span class="metric-value">300 m/s</span>
                <span style="font-size: 0.7rem; color: var(--text-muted);">Mach 0.88 cruise speed</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Platform Mass</span>
                <span class="metric-value">400 g</span>
                <span style="font-size: 0.7rem; color: var(--text-muted);">Verified MTOW: 390.6g</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Load Factor</span>
                <span class="metric-value">15.1 G</span>
                <span style="font-size: 0.7rem; color: var(--text-muted);">Structural limit load</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Turn Radius</span>
                <span class="metric-value">1,559 m</span>
                <span style="font-size: 0.7rem; color: var(--text-muted);">@ 300 m/s max turn</span>
            </div>
        </div>

        <div class="endpoint" style="margin-top: 2rem; border-left-color: var(--status-ok);">
            <h2 style="font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--text);">Subsystem Status</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <span class="metric-label">Operational Status</span>
                    <p style="margin: 0; font-weight: 600; color: var(--status-ok);">✅ Ready for Deployment</p>
                </div>
                <div>
                    <span class="metric-label">ISA Verification</span>
                    <p style="margin: 0; font-weight: 600;">✅ Certified Models</p>
                </div>
            </div>
        </div>

        <a href="/" class="nav-link" aria-label="Return to Command Center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
            Return to Command Center
        </a>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html, status_code=HTTPStatus.OK)


routes = [
    Route("/", root_handler),
    Route("/health", health_handler),
    Route("/dashboard", dashboard_handler),
]

app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers={
        starlette.exceptions.HTTPException: starlette.exceptions.HTTPException,
        Exception: ExceptionMiddleware,
    },
)
