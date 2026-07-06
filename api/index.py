"""
api/index.py — Vercel Python Runtime Entrypoint
===============================================
Provides a minimal ASGI/starlette application so the Vercel Python runtime
can locate an entrypoint (`app` object) and complete a build.
"""

from http import HTTPStatus
from typing import Callable
import os

import starlette.exceptions
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.middleware.exceptions import ExceptionMiddleware

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
    <title>Interceptor_M</title>
    <script>
      window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #0070f3; margin-bottom: 0.5rem; }
        .status {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #00d97e;
            color: white;
            border-radius: 4px;
            font-size: 0.875rem;
            margin-bottom: 1rem;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 217, 126, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(0, 217, 126, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 217, 126, 0); }
        }
        p { color: #666; }
        .endpoints {
            margin-top: 2rem;
        }
        .endpoint-link {
            text-decoration: none;
            color: inherit;
            display: block;
            margin: 0.5rem 0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .endpoint-link:hover, .endpoint-link:focus {
            transform: translateY(-2px);
            outline: none;
        }
        .endpoint-link:focus .endpoint {
            box-shadow: 0 0 0 2px #0070f3;
        }
        .endpoint {
            background: #f9f9f9;
            padding: 1rem;
            border-radius: 4px;
            border-left: 3px solid #0070f3;
            transition: background 0.2s ease;
        }
        .endpoint-link:hover .endpoint {
            background: #f0f7ff;
        }
        .endpoint code {
            color: #e74c3c;
            background: #fff;
            padding: 0.2rem 0.4rem;
            border-radius: 30px;
        }
        .insights-notice {
            margin-top: 2rem;
            padding: 1rem;
            background: #e3f2fd;
            border-left: 3px solid #2196f3;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Interceptor_M</h1>
        <span class="status" role="status">OK</span>
        <p><strong>Autonomous Swarm Counter-UAS — Drone Interceptor System</strong></p>
        <p style="color: var(--text-muted);">Engineering the next generation of kinetic interception platforms with physics-driven multi-agent coordination.</p>
        
        <nav class="endpoints" aria-label="Available Endpoints">
            <h2>Available Endpoints</h2>
            <a href="/" class="endpoint-link" aria-label="Go to API Root Metadata">
                <div class="endpoint">
                    <strong>GET <code>/</code></strong>
                    <p>Returns this page (HTML) or project metadata (JSON)</p>
                </div>
            </a>
            <a href="/health" class="endpoint-link" aria-label="Check System Health">
                <div class="endpoint">
                    <strong>GET <code>/health</code></strong>
                    <p>Health check endpoint for liveness probes</p>
                </div>
            </a>
            <a href="/dashboard" class="endpoint-link" aria-label="View Project Dashboard">
                <div class="endpoint">
                    <strong>GET <code>/dashboard</code></strong>
                    <p>Detailed project dashboard with performance metrics</p>
                </div>
            </a>
        </nav>
        
        <div class="insights-notice">
            <strong>📊 Performance Monitoring Active</strong>
            <p style="margin: 0.5rem 0 0 0;">Vercel Speed Insights is monitoring page performance metrics including Core Web Vitals (LCP, FID, CLS).</p>
        </div>
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
    <title>Interceptor_M Dashboard</title>
    <script>
      window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
        }
        h1 { color: #0070f3; }
        .info { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .metric { margin: 10px 0; }
        .label { font-weight: 600; }
        .nav-link {
            display: inline-block;
            margin-top: 1rem;
            color: #0070f3;
            text-decoration: none;
            font-weight: 500;
            transition: text-decoration 0.2s;
        }
        .nav-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>🚀 Interceptor_M</h1>
    <p><strong>Autonomous Swarm Counter-UAS — Drone Interceptor System</strong></p>
    
    <div class="info">
        <h2>Performance Baseline (DD-400)</h2>
        <div class="metric"><span class="label">Intercept Speed:</span> 300 m/s (Mach 0.88)</div>
        <div class="metric"><span class="label">MTOW:</span> 400 g (Defense Line)</div>
        <div class="metric"><span class="label">Max Load Factor:</span> 15.1 g</div>
        <div class="metric"><span class="label">Turn Radius:</span> 1,559 m @ 300 m/s</div>
    </div>
    
    <div class="info">
        <h2>System Status</h2>
        <div class="metric"><span class="label">Status:</span> ✅ Operational</div>
        <div class="metric"><span class="label">Speed Insights:</span> ✅ Enabled</div>
        <div class="metric">
            <span class="label">API Endpoint:</span>
            <a href="/" class="nav-link" aria-label="Back to API Root Metadata">Home (/)</a>
        </div>
        <div class="metric">
            <span class="label">Health Check:</span>
            <a href="/health" class="nav-link" aria-label="Check System Health Status">/health</a>
        </div>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html, status_code=HTTPStatus.OK)


routes = [
    Route("/", root_handler),
    Route("/health", health_handler),
    Route("/dashboard", dashboard_handler),
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
]

app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers={
        starlette.exceptions.HTTPException: starlette.exceptions.HTTPException,
        Exception: ExceptionMiddleware,
    },
)
