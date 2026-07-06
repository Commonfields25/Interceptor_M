"""
api/index.py — Vercel Python Runtime Entrypoint
===============================================
Provides a minimal ASGI/starlette application so the Vercel Python runtime
can locate an entrypoint (`app` object) and complete a build.
"""

from http import HTTPStatus
from typing import Callable, Union
import os

import starlette.exceptions
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route, Mount
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.staticfiles import StaticFiles

async def root_handler(request: Request) -> Union[HTMLResponse, JSONResponse]:
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
    <title>Interceptor_M</title>\n    <meta name="theme-color" content="#0ea5e9">
    <link rel="stylesheet" href="/static/style.css">
    <script defer src="/static/script.js"></script>
    <script>
      window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
</head>
<body>
    <div class="container">
        <h1>🚀 Interceptor_M</h1>
        <span class="status" role="status">OK</span>
        <p><strong>Autonomous Swarm Counter-UAS — Drone Interceptor System</strong></p>
        <p class="text-muted">Engineering the next generation of kinetic interception platforms with physics-driven multi-agent coordination.</p>
        
        <nav class="endpoints" aria-label="Available Endpoints">
            <h2>Available Endpoints</h2>
            <div class="endpoint-card">
                <a href="/" class="endpoint-link" aria-label="Go to API Root Metadata">
                    <div class="endpoint">
                        <strong>GET <code>/</code></strong>
                        <p>Returns this page (HTML) or project metadata (JSON)</p>
                    </div>
                </a>
                <button class="copy-btn" onclick="copyToClipboard('/', this)" title="Copy endpoint URL">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
            </div>
            <div class="endpoint-card">
                <a href="/health" class="endpoint-link" aria-label="Check System Health">
                    <div class="endpoint">
                        <strong>GET <code>/health</code></strong>
                        <p>Health check endpoint for liveness probes</p>
                    </div>
                </a>
                <button class="copy-btn" onclick="copyToClipboard('/health', this)" title="Copy endpoint URL">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
            </div>
            <div class="endpoint-card">
                <a href="/dashboard" class="endpoint-link" aria-label="View Project Dashboard">
                    <div class="endpoint">
                        <strong>GET <code>/dashboard</code></strong>
                        <p>Detailed project dashboard with performance metrics</p>
                    </div>
                </a>
                <button class="copy-btn" onclick="copyToClipboard('/dashboard', this)" title="Copy endpoint URL">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
            </div>
        </nav>
        
        <div class="insights-notice">
            <strong>📊 Performance Monitoring Active</strong>
            <p>Vercel Speed Insights is monitoring page performance metrics including Core Web Vitals (LCP, FID, CLS).</p>
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
    <title>Interceptor_M Dashboard</title>\n    <meta name="theme-color" content="#0ea5e9">
    <link rel="stylesheet" href="/static/style.css">
    <script defer src="/static/script.js"></script>
    <script>
      window.si = window.si || function () {{ (window.siq = window.siq || []).push(arguments); }};
    </script>
    <script defer src="/_vercel/speed-insights/script.js"></script>
</head>
<body>
    <div class="container">
        <h1>🚀 Interceptor_M Dashboard</h1>
        <p><strong>Autonomous Swarm Counter-UAS — Drone Interceptor System</strong></p>

        <div class="info-grid">
            <div class="metric-card">
                <span class="metric-label">Intercept Speed</span>
                <span class="metric-value">300 m/s (Mach 0.88)</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">MTOW</span>
                <span class="metric-value">400 g (Defense Line)</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Max Load Factor</span>
                <span class="metric-value">15.1 g</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Turn Radius</span>
                <span class="metric-value">1,559 m @ 300 m/s</span>
            </div>
        </div>

        <div class="info">
            <h2>System Status</h2>
            <div class="metric">
                <span class="label">Status:</span> ✅ Operational
            </div>
            <div class="metric">
                <span class="label">Speed Insights:</span> ✅ Enabled
            </div>
            <nav style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <a href="/" class="nav-link" aria-label="Back to API Root Metadata">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                    Home
                </a>
                <a href="/health" class="nav-link" aria-label="Check System Health Status">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
                    Health
                </a>
            </nav>
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
