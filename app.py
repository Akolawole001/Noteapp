from pathlib import Path
import sys

# Ensure backend package is importable when deployed from repo root
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))

# Import the FastAPI app instance exposed by backend/app/main.py
# Vercel's Python builder looks for a variable named `app` in top-level modules
from app.main import app  # noqa: E402
