"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.db.session import init_db
from app.api import auth, notes, tasks, calendar
import os


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Production-grade Note Taking & To-Do List Application with Calendar",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(calendar.router, prefix="/api")

# Mount frontend static files (CSS, JS, images)
# Frontend is now in a separate directory at project root
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend application."""
    html_file = os.path.join(frontend_dir, "index.html")
    
    if os.path.exists(html_file):
        with open(html_file, "r") as f:
            return f.read()
    
    return """
    <html>
        <head>
            <title>NoteApp</title>
        </head>
        <body>
            <h1>NoteApp API</h1>
            <p>API is running. Visit <a href="/api/docs">/api/docs</a> for API documentation.</p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
