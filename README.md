# NoteApp - Production-Grade Note Taking & To-Do List Application

A secure, production-ready note-taking and task management application with calendar integration. Built with separated frontend and backend architecture for scalability and maintainability.

## 🏗️ Architecture

This project follows industry best practices with **separated frontend and backend**:

```
noteapp/
├── frontend/           # Vanilla JavaScript SPA
│   ├── index.html     # Clean HTML structure
│   ├── css/           # Separated styles
│   │   └── styles.css
│   └── js/            # Separated logic
│       └── app.js
├── backend/           # FastAPI REST API
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── core/      # Configuration
│   │   ├── db/        # Database layer
│   │   └── domain/    # Models & schemas
│   └── requirements.txt
├── docker-compose.yml # Orchestration
├── Dockerfile        # Container definition
└── .env.example      # Configuration template
```

## ✨ Features

- **Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Notes**: Create, read, update, delete notes with timestamps
- **Tasks**: Manage tasks with due dates and status tracking (todo, in_progress, completed)
- **Calendar**: Schedule events with start/end times
- **Security**: 
  - Rate limiting
  - Input validation (Pydantic schemas)
  - SQL injection protection (SQLAlchemy ORM)
  - Password hashing (bcrypt)
  - CORS configuration
  - Environment-based secrets
- **Production-Ready**: 
  - Docker support
  - PostgreSQL database
  - Proper error handling
  - Health check endpoint
  - API documentation (auto-generated)
  - Separated concerns

## 📋 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework with automatic API docs
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production-grade relational database
- **JWT (python-jose)** - Secure token-based authentication
- **Bcrypt (passlib)** - Password hashing
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend
- **Vanilla JavaScript** - No framework overhead, pure performance
- **Modern CSS** - Clean, responsive design with CSS Grid/Flexbox
- **HTML5** - Semantic markup

### Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration
- **PostgreSQL 15** - Database with Alpine Linux for minimal footprint

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd noteapp
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Update `.env` file** (⚠️ NEVER commit this file)
```env
DATABASE_URL=postgresql://noteapp:noteapp123@db:5432/noteapp
SECRET_KEY=your-super-secret-key-min-32-characters-change-this
JWT_SECRET=your-jwt-secret-key-change-this-too
DEBUG=True
CORS_ORIGINS=http://localhost:8000,http://localhost:3000
```

Generate secure keys:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

4. **Start the application**
```bash
docker-compose up -d
```

5. **Access the application**
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/api/redoc (ReDoc)
- **Health Check**: http://localhost:8000/health

### First Time Setup

1. Register a new account at http://localhost:8000
2. Login with your credentials
3. Start creating notes, tasks, and events!

## 📚 API Documentation

### Authentication Endpoints

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePass123
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhb...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhb...",
  "token_type": "bearer"
}
```

### Notes Endpoints

All notes endpoints require authentication header:
```
Authorization: Bearer <access_token>
```

#### Get Notes
```http
GET /api/notes/?skip=0&limit=10&search=optional
```

#### Create Note
```http
POST /api/notes/
Content-Type: application/json

{
  "title": "My Note",
  "content": "Note content here"
}
```

#### Update Note
```http
PUT /api/notes/{note_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### Delete Note
```http
DELETE /api/notes/{note_id}
```

### Tasks Endpoints

#### Get Tasks
```http
GET /api/tasks/?status=todo
```

#### Create Task
```http
POST /api/tasks/
Content-Type: application/json

{
  "title": "My Task",
  "description": "Task details",
  "due_date": "2026-01-30T10:00:00",
  "status": "todo"
}
```

#### Update Task
```http
PUT /api/tasks/{task_id}
Content-Type: application/json

{
  "status": "completed"
}
```

### Calendar Endpoints

#### Get Events
```http
GET /api/calendar/events?start_date=2026-01-01T00:00:00&end_date=2026-12-31T23:59:59
```

#### Create Event
```http
POST /api/calendar/events
Content-Type: application/json

{
  "title": "Meeting",
  "description": "Team sync",
  "start_time": "2026-01-25T14:00:00",
  "end_time": "2026-01-25T15:00:00",
  "linked_task_id": null
}
```

## 🔒 Security Features

### Authentication
- JWT access tokens (30 min expiry)
- JWT refresh tokens (7 day expiry)
- Bcrypt password hashing with salt
- OAuth2 password flow

### Data Protection
- SQL injection prevention (ORM only, no raw queries)
- XSS protection (input sanitization)
- CSRF protection (token-based auth, no cookies)
- Password strength validation
- Input length limits

### Authorization
- Every resource tied to user ID
- Ownership checks on all operations
- No data leakage between users

## 🚀 Deployment

### Deploy to Railway (Free Tier)

1. **Fork/Push to GitHub**

2. **Create Railway account**: https://railway.app

3. **Create new project**
   - Connect GitHub repository
   - Add PostgreSQL service
   - Add environment variables from `.env`

4. **Railway will auto-deploy**

### Deploy to Render (Free Tier)

1. **Create Render account**: https://render.com

2. **Create PostgreSQL database**
   - Copy connection string

3. **Create Web Service**
   - Connect GitHub repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Add environment variables

### Deploy to Your Own Server

1. **Setup server** (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install docker docker-compose nginx certbot python3-certbot-nginx
```

2. **Clone repository**
```bash
git clone <your-repo-url>
cd noteapp
```

3. **Setup environment**
```bash
cp .env.example .env
# Edit .env with production values
```

4. **Start with Docker Compose**
```bash
docker-compose up -d
```

5. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. **Setup SSL with Let's Encrypt**
```bash
sudo certbot --nginx -d yourdomain.com
```

## 📊 Database Schema

### Users
- `id`: Integer (PK)
- `email`: String (unique)
- `password_hash`: String
- `created_at`: DateTime

### Notes
- `id`: Integer (PK)
- `user_id`: Integer (FK)
- `title`: String
- `content`: Text
- `created_at`: DateTime
- `updated_at`: DateTime

### Tasks
- `id`: Integer (PK)
- `user_id`: Integer (FK)
- `title`: String
- `description`: Text
- `due_date`: DateTime
- `status`: Enum (todo, in_progress, completed)
- `created_at`: DateTime
- `updated_at`: DateTime

### Calendar Events
- `id`: Integer (PK)
- `user_id`: Integer (FK)
- `title`: String
- `description`: Text
- `start_time`: DateTime
- `end_time`: DateTime
- `linked_task_id`: Integer (FK, nullable)
- `created_at`: DateTime
- `updated_at`: DateTime

## 🧪 Testing

Create test file `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "test@example.com",
    "password": "TestPass123"
})
print(f"Register: {response.status_code}")

# Login
response = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "test@example.com",
    "password": "TestPass123"
})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"Login: {response.status_code}")

# Create Note
response = requests.post(f"{BASE_URL}/notes/", 
    headers=headers,
    json={"title": "Test Note", "content": "Hello World"}
)
print(f"Create Note: {response.status_code}")

# Get Notes
response = requests.get(f"{BASE_URL}/notes/", headers=headers)
print(f"Get Notes: {response.json()}")
```

Run tests:
```bash
python test_api.py
```

## 📝 Project Structure

```
noteapp/
├── frontend/             # Frontend Application (Separated)
│   ├── index.html       # Clean HTML structure (50 lines)
│   ├── css/
│   │   └── styles.css   # All styling (200+ lines)
│   └── js/
│       └── app.js       # Application logic (300+ lines)
│   └── README.md        # Frontend documentation
├── backend/             # Backend API (Separated)
│   ├── app/
│   │   ├── api/         # API route handlers
│   │   │   ├── auth.py  # Authentication endpoints
│   │   │   ├── notes.py # Notes CRUD operations
│   │   │   ├── tasks.py # Tasks CRUD operations
│   │   │   └── calendar.py # Calendar events
│   │   ├── core/        # Core utilities
│   │   │   ├── config.py    # App configuration
│   │   │   ├── security.py  # Auth & password hashing
│   │   │   └── dependencies.py # FastAPI dependencies
│   │   ├── db/          # Database layer
│   │   │   └── session.py   # DB session management
│   │   ├── domain/      # Data models
│   │   │   ├── models.py    # SQLAlchemy ORM models
│   │   │   └── schemas.py   # Pydantic validation schemas
│   │   └── main.py      # FastAPI application entry point
│   ├── requirements.txt # Python dependencies
│   ├── run.py          # Development server runner
│   └── README.md       # Backend documentation
├── .env                # Environment variables (NEVER COMMIT)
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules (CRITICAL for security)
├── docker-compose.yml  # Docker orchestration
├── Dockerfile          # Container definition
├── requirements.txt    # Root requirements (for Docker)
└── README.md          # This file
```

## 🎨 Why Separated Frontend & Backend?

This project follows **industry best practices** by separating frontend and backend:

### Benefits:

1. **Independent Development**
   - Frontend and backend teams can work simultaneously
   - Different deployment schedules
   - Easier to update one without affecting the other

2. **Better Security**
   - Backend code not exposed in frontend
   - Clear separation of concerns
   - API can be locked down separately

3. **Scalability**
   - Frontend can be served from CDN (Vercel, Netlify, Cloudflare)
   - Backend can scale independently
   - Different hosting strategies for different needs

4. **Maintainability**
   - Easier to locate and fix bugs
   - Clear file organization
   - Each part has focused responsibility

5. **Flexibility**
   - Can build mobile app using same backend
   - Can rebuild frontend in React/Vue/Angular
   - Multiple frontends can use same API

### File Separation Details:

**Before (Mixed - 593 lines):**
- index.html contained HTML, CSS, and JavaScript all together
- Hard to maintain and debug
- Browser couldn't cache CSS/JS separately

**After (Separated - Clean):**
- `index.html`: 100 lines (HTML structure only)
- `css/styles.css`: 200 lines (All styling)
- `js/app.js`: 300 lines (All logic)
- Each file has ONE responsibility
- Browser caches files independently
- Much easier to maintain

## 🔒 Security Best Practices

### Critical Rules (NEVER BREAK THESE):

1. **NEVER commit `.env` file**
   - Contains database passwords, secret keys
   - One leaked .env = complete compromise
   - Always in .gitignore

2. **Use strong SECRET_KEY and JWT_SECRET**
   ```bash
   # Generate secure keys
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Environment-specific configs**
   - Development: DEBUG=True, local database
   - Production: DEBUG=False, managed database, HTTPS

4. **Regular updates**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

### Security Checklist:

- ✅ Passwords hashed with bcrypt (not plain text)
- ✅ JWT tokens for authentication (not sessions)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation (Pydantic schemas)
- ✅ CORS configuration (controlled origins)
- ✅ Secrets in environment variables (not code)
- ✅ .gitignore prevents committing secrets
- ✅ HTTPS ready (use reverse proxy in production)

## 🎯 Roadmap

- [ ] Email verification
- [ ] Password reset
- [ ] Shared notes/tasks
- [ ] Rich text editor
- [ ] File attachments
- [ ] Mobile app
- [ ] Export data (JSON/CSV)
- [ ] Dark mode
- [ ] Notifications
- [ ] Tags and categories

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

For support, email support@noteapp.com or open an issue on GitHub.

---

**Built with ❤️ using FastAPI and modern web technologies**
