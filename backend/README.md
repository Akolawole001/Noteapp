# NoteApp Backend

Production-grade FastAPI backend for the NoteApp note-taking, task management, and calendar application.

## 🏗️ Architecture

This backend follows a clean, layered architecture:

```
backend/
├── app/
│   ├── api/           # API endpoints (routes)
│   │   ├── auth.py    # Authentication endpoints
│   │   ├── notes.py   # Notes CRUD operations
│   │   ├── tasks.py   # Tasks management
│   │   └── calendar.py # Calendar events
│   ├── core/          # Core configuration
│   │   ├── config.py  # App settings
│   │   ├── security.py # Security utilities
│   │   └── dependencies.py # FastAPI dependencies
│   ├── db/            # Database layer
│   │   └── session.py # Database session management
│   ├── domain/        # Business logic & models
│   │   ├── models.py  # SQLAlchemy models
│   │   └── schemas.py # Pydantic schemas
│   └── main.py        # Application entry point
├── requirements.txt   # Python dependencies
└── run.py            # Development runner
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **CORS Configuration**: Controlled cross-origin requests
- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Environment Variables**: Secrets managed via .env file

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- pip or poetry

### Local Development

1. **Create virtual environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create `.env` file in project root:
```env
DATABASE_URL=postgresql://noteapp:noteapp123@localhost:5432/noteapp
SECRET_KEY=your-super-secret-key-min-32-characters
JWT_SECRET=your-jwt-secret-key-for-tokens
DEBUG=True
```

⚠️ **NEVER commit .env file to git!**

4. **Run the development server**:
```bash
# From backend directory
python run.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Access the API**:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/api/docs
- Alternative docs: http://localhost:8000/api/redoc

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (returns JWT token)
- `POST /api/auth/refresh` - Refresh access token

### Notes
- `GET /api/notes/` - Get all user notes
- `POST /api/notes/` - Create new note
- `GET /api/notes/{id}` - Get specific note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note

### Tasks
- `GET /api/tasks/` - Get all user tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Calendar
- `GET /api/calendar/events` - Get all events
- `POST /api/calendar/events` - Create new event
- `GET /api/calendar/events/{id}` - Get specific event
- `PUT /api/calendar/events/{id}` - Update event
- `DELETE /api/calendar/events/{id}` - Delete event

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 🐳 Docker Deployment

See main project README for Docker deployment instructions.

## 📦 Dependencies

Main dependencies:
- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **python-jose**: JWT token handling
- **passlib**: Password hashing
- **psycopg2-binary**: PostgreSQL adapter
- **uvicorn**: ASGI server

## 🔧 Configuration

Configuration is managed through environment variables in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for sessions (32+ characters)
- `JWT_SECRET`: Secret for JWT token signing
- `DEBUG`: Enable/disable debug mode
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

## 📝 Database Models

### User
- id (Primary Key)
- email (Unique)
- hashed_password
- created_at
- updated_at

### Note
- id (Primary Key)
- user_id (Foreign Key → User)
- title
- content
- created_at
- updated_at

### Task
- id (Primary Key)
- user_id (Foreign Key → User)
- title
- description
- status (todo, in_progress, completed)
- due_date
- created_at
- updated_at

### CalendarEvent
- id (Primary Key)
- user_id (Foreign Key → User)
- title
- description
- start_time
- end_time
- created_at
- updated_at

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Add tests for new features
3. Update documentation
4. Keep security in mind

## 📄 License

This project is for educational purposes.
