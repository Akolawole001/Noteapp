# NoteApp Setup Guide

Complete guide to set up and run the NoteApp with separated frontend and backend.

## 📋 Prerequisites

- Python 3.11+ installed
- PostgreSQL 15+ (or use Docker for database)
- Git

## 🚀 Quick Setup (5 Minutes)

### Step 1: Clone and Navigate

```bash
git clone <your-repo-url>
cd noteapp
```

### Step 2: Set Up Environment Variables

The `.env` file contains **CRITICAL SECRETS** - never commit it!

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database (PostgreSQL recommended for production)
DATABASE_URL=postgresql://noteapp:noteapp123@localhost:5432/noteapp

# Security Keys (GENERATE NEW ONES - DON'T USE THESE)
SECRET_KEY=your-32-char-secret-key-change-this-now
JWT_SECRET=your-jwt-secret-key-change-this-too
ALGORITHM=HS256

# Token Expiration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS (allowed frontend origins)
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000

# App Settings
DEBUG=True
```

**Generate secure keys:**
```bash
# Run this twice, use outputs for SECRET_KEY and JWT_SECRET
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Set Up Database

**Option A: PostgreSQL (Recommended)**

```bash
# Install PostgreSQL (macOS)
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb noteapp

# Create user
psql postgres
CREATE USER noteapp WITH PASSWORD 'noteapp123';
GRANT ALL PRIVILEGES ON DATABASE noteapp TO noteapp;
\q
```

**Option B: Docker PostgreSQL (Easier)**

```bash
docker run -d \
  --name noteapp-db \
  -e POSTGRES_USER=noteapp \
  -e POSTGRES_PASSWORD=noteapp123 \
  -e POSTGRES_DB=noteapp \
  -p 5432:5432 \
  postgres:15-alpine
```

**Option C: SQLite (Not recommended for production)**

Change `.env`:
```env
DATABASE_URL=sqlite:///./noteapp.db
```

### Step 4: Set Up Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Run the Application

**From backend directory with venv activated:**

```bash
python run.py
```

Or directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Access the Application

Open your browser:

- **Frontend**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/api/docs
- **API Docs (ReDoc)**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

### Step 7: Create Your First Account

1. Go to http://localhost:8000
2. Click "Register"
3. Enter email and password (min 8 chars, 1 upper, 1 lower, 1 digit)
4. Click "Register"
5. Login with your credentials
6. Start creating notes, tasks, and events!

## 🐳 Docker Setup (Alternative)

If you have Docker installed:

```bash
# Build and start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

Access at http://localhost:8000

## 🔍 Verification Checklist

After setup, verify everything works:

- [ ] Backend starts without errors
- [ ] Can access http://localhost:8000
- [ ] API docs load at http://localhost:8000/api/docs
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Can register a new account
- [ ] Can login with account
- [ ] Can create a note
- [ ] Can create a task
- [ ] Can create a calendar event

## 🐛 Troubleshooting

### "Module not found" errors

```bash
# Make sure you're in backend directory with venv activated
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Connection refused" database errors

**Check if PostgreSQL is running:**
```bash
# macOS
brew services list | grep postgresql

# Docker
docker ps | grep noteapp-db
```

**Check DATABASE_URL in .env:**
```env
# Should match your setup
DATABASE_URL=postgresql://noteapp:noteapp123@localhost:5432/noteapp
```

### "Validation error" on startup

Missing environment variables in `.env`:

```bash
# Check .env has required variables
cat .env

# Required:
# - DATABASE_URL
# - SECRET_KEY
# - JWT_SECRET
```

### Frontend loads but API calls fail

**Check CORS settings in .env:**
```env
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000
```

**Check backend is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","app":"NoteApp","version":"1.0.0"}
```

### Port already in use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

## 📱 Development Workflow

### Making Changes

**Backend changes:**
1. Edit files in `backend/app/`
2. Server auto-reloads (if using `--reload`)
3. Test at http://localhost:8000/api/docs

**Frontend changes:**
1. Edit files in `frontend/`
2. Refresh browser to see changes
3. No build step needed (vanilla JS)

### Running Tests

```bash
cd backend
pytest
pytest --cov=app tests/
```

### Adding Dependencies

```bash
cd backend
source venv/bin/activate
pip install <package-name>
pip freeze > requirements.txt
```

## 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guides for:
- Railway
- Render
- Fly.io
- AWS
- Google Cloud
- Self-hosted

## 🔒 Security Reminder

**BEFORE pushing to GitHub:**

```bash
# 1. Verify .env is in .gitignore
cat .gitignore | grep .env

# 2. Verify .env is NOT staged
git status

# 3. If .env appears in git status, DO NOT COMMIT
# Remove it:
git rm --cached .env

# 4. Check no secrets in code
grep -r "SECRET_KEY\|JWT_SECRET\|password" --include="*.py" backend/app/
# Should only find variable names, not actual values
```

## 📚 Next Steps

- Read [backend/README.md](backend/README.md) for backend details
- Read [frontend/README.md](frontend/README.md) for frontend details
- Explore API at http://localhost:8000/api/docs
- Check out the codebase structure
- Make it your own!

## 🤝 Need Help?

- Check the main [README.md](README.md)
- Review error messages carefully
- Check logs: `docker-compose logs -f api` (if using Docker)
- Ensure all prerequisites are installed
- Verify .env configuration

## 📝 Common Commands Reference

```bash
# Backend
cd backend
source venv/bin/activate
python run.py

# Database
createdb noteapp
psql noteapp
docker ps | grep postgres

# Docker
docker-compose up -d
docker-compose down
docker-compose logs -f api

# Testing
cd backend && pytest
cd backend && pytest --cov=app

# Cleanup
deactivate  # Exit virtual environment
docker-compose down -v  # Remove Docker volumes
rm -rf backend/venv  # Remove virtual environment
```

---

**Remember**: 
- ⚠️ NEVER commit `.env` file
- 🔒 Use strong, unique SECRET_KEY and JWT_SECRET
- 📝 Keep this guide updated when making changes
- 🧪 Test after setup to verify everything works
