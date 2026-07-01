"""
api/index.py — Vercel Python Runtime Entrypoint
===============================================
Provides a minimal ASGI/starlette application so the Vercel Python runtime
can locate an entrypoint (`app` object) and complete a build.

The Interceptor_M project is a drone engineering project (physics simulation,
CAD generation, multi-agent governance). It does not expose a persistent HTTP
API. This stub allows Vercel to build and deploy a placeholder endpoint that
returns a JSON acknowledgement.

For a future API, replace `handler` with a real Starlette / FastAPI app.
"""

from http import HTTPStatus
from typing import Callable

import starlette.exceptions
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


async def root_handler(request: Request) -> JSONResponse:
    """GET / → project metadata."""
    return JSONResponse(
        {
            "name": "Interceptor_M",
            "status": "ok",
            "message": (
                "Interceptor_M is a drone engineering project. "
                "No persistent API is exposed in this Vercel deployment."
            ),
        },
        status_code=HTTPStatus.OK,
    )


async def health_handler(request: Request) -> JSONResponse:
    """GET /health → liveness probe."""
    return JSONResponse({"status": "healthy"}, status_code=HTTPStatus.OK)


routes = [
    Route("/", root_handler),
    Route("/health", health_handler),
]

# ---------------------------------------------------------------------------
# Vercel Python runtime requires an exported `app` ASGI application object.
# ---------------------------------------------------------------------------
app = Starlette(
    debug=False,
    routes=routes,
    exception_handlers={
        starlette.exceptions.HTTPException: starlette.exceptions.HTTPException,
        Exception: starlette.exceptions.ExceptionMiddleware,
    },
)
