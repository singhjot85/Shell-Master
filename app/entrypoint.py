"""FastAPI entrypoint for the jqtools web UI."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.services.jq_formatter_service import JQFormatterService


BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
STATIC_DIR = BASE_DIR / "assets" / "static"

app = FastAPI(title="jqtools UI")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
formatter_service = JQFormatterService()


class FormatRequest(BaseModel):
    """Request payload for jq formatting."""

    source: str = Field(default="", description="Raw jq source to format.")


@app.get("/")
async def index(request: Request):
    """Render the landing page."""

    context = {
        "title": "jqtools",
        "active_page": "home",
        "hero_title": "Compiler-first jq tooling",
        "hero_description": "Format, inspect, and extend jq workflows through a clean web interface.",
        "tool_cards": [
            {
                "title": "JQ Formatter",
                "description": "Paste jq source, format it with the compiler-backed formatter, and inspect errors quickly.",
                "href": "/jq-formatter",
                "tag": "Ready",
            },
            {
                "title": "Debugger",
                "description": "Planned next: token and AST views powered by the same compiler service.",
                "href": "#",
                "tag": "Planned",
            },
        ],
    }
    return templates.TemplateResponse(request, "index.html", {"context": context})


@app.get("/jq-formatter")
async def jq_formatter_page(request: Request):
    """Render the jq formatter page."""

    context = {
        "title": "JQ Formatter",
        "active_page": "formatter",
        "sample_input": '.people[] | select(.active == true) | {name: .name, emails: [.email, "unknown"]}',
    }
    return templates.TemplateResponse(request, "jq_formatter.html", {"context": context})


@app.post("/api/jq/format")
async def format_jq(payload: FormatRequest):
    """Format jq through the core formatting service."""

    result = formatter_service.format_jq(payload.source)
    status_code = 200 if result.ok else 400
    return JSONResponse(
        status_code=status_code,
        content={
            "ok": result.ok,
            "source": result.source,
            "formatted": result.formatted,
            "error": result.error,
        },
    )
