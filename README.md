# NoteApp - Production-Grade Note Taking & To-Do List Application

A secure, internet-accessible note-taking and task management application with calendar integration.

## 🚀 Features

- **Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Notes**: Create, read, update, delete notes with search functionality
- **Tasks**: Manage tasks with due dates and status tracking (todo, in_progress, completed)
- **Calendar**: Schedule events with conflict detection and task linking
- **Security**: Rate limiting, input validation, SQL injection protection, HTTPS ready
- **Production-Ready**: Docker support, PostgreSQL database, proper error handling

## 📋 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database
- **JWT** - Secure token-based authentication
- **Bcrypt** - Password hashing
- **Pydantic** - Data validation

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **Responsive Design** - Mobile-friendly interface

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy (for production)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if running without Docker)

### Quick Start with Docker

1. **Clone the repository**
```bash
cd /Users/implicity/kola-repo/noteapp
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Update `.env` file**
```env
DATABASE_URL=postgresql://noteapp:noteapp123@db:5432/noteapp
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

4. **Start the application**
```bash
docker-compose up -d
```

5. **Access the application**
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

### Local Development (Without Docker)

1. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup PostgreSQL database**
```bash
createdb noteapp
```

4. **Create `.env` file**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run the application**
```bash
python -m app.main
# or
uvicorn app.main:app --reload
```

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
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── notes.py      # Notes CRUD
│   │   ├── tasks.py      # Tasks CRUD
│   │   └── calendar.py   # Calendar events
│   ├── core/             # Core utilities
│   │   ├── config.py     # Configuration
│   │   ├── security.py   # Auth & hashing
│   │   └── dependencies.py # FastAPI dependencies
│   ├── db/               # Database
│   │   └── session.py    # DB session
│   ├── domain/           # Data layer
│   │   ├── models.py     # SQLAlchemy models
│   │   └── schemas.py    # Pydantic schemas
│   ├── static/           # Frontend files
│   │   └── index.html    # Web interface
│   └── main.py           # FastAPI app
├── .env.example          # Environment template
├── .gitignore
├── docker-compose.yml    # Docker setup
├── Dockerfile
├── requirements.txt      # Python dependencies
└── README.md
```

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
