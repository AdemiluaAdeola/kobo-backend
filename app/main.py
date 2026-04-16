"""
Kobo FastAPI Application — AI-Powered Finance Coach.

Entry point that wires up all routes, middleware, and serves the landing page.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .core.config import get_settings
from .core.database import init_db

# Import all models so they are registered with Base.metadata
from .models import user, waitlist, transaction, nudge  # noqa: F401

# Import routers
from .api.v1.waitlist import router as waitlist_router
from .api.v1.auth import router as auth_router
from .api.v1.users import router as users_router
from .api.v1.transactions import router as transactions_router
from .api.v1.forecast import router as forecast_router
from .api.v1.chat import router as chat_router
from .api.v1.nudges import router as nudges_router

settings = get_settings()

from fastapi.staticfiles import StaticFiles

# ── Paths ───────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "kobo-frontend" / "dist"
INDEX_HTML = FRONTEND_DIR / "index.html"


# ── Lifespan ────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup."""
    await init_db()
    yield


# ── App ─────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Static Files ────────────────────────────────────────────────
if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register API routers ────────────────────────────────────────
API_PREFIX = "/api/v1"
app.include_router(waitlist_router, prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(transactions_router, prefix=API_PREFIX)
app.include_router(forecast_router, prefix=API_PREFIX)
app.include_router(chat_router, prefix=API_PREFIX)
app.include_router(nudges_router, prefix=API_PREFIX)


# ── Serve Landing Page ──────────────────────────────────────────
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_landing_page(request: Request):
    """Serve the Kobo React landing page at root."""
    if not INDEX_HTML.exists():
        return HTMLResponse(content="<h1>Frontend not built. Run 'npm run build' in kobo-frontend.</h1>")
    return HTMLResponse(content=INDEX_HTML.read_text(encoding="utf-8"))


# ── Health Check ────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}
