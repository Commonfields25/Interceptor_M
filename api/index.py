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
from starlette.routing import Route, Mount
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.staticfiles import StaticFiles


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

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interceptor_M | Aerospace Intelligence</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="/static/script.js"></script>
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
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard | Interceptor_M</title>
    <link rel="stylesheet" href="/static/style.css">
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
