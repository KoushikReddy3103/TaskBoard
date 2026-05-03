# TaskBoard

A lightweight **Trello-style task manager** with a REST API and modern web frontend. Build with Django, Django REST Framework, Celery, and Redis.

## 📋 Features

- **Task Management**: Create, update, and manage tasks with priority and status tracking
- **User Authentication**: JWT-based authentication with login/logout functionality
- **REST API**: Complete REST API for programmatic access to tasks
- **Async Processing**: Celery background tasks for sending email notifications
- **Web UI**: Simple and intuitive web interface for managing tasks
- **Admin Dashboard**: Django admin panel for administrative tasks
- **Dockerized**: Full Docker and Docker Compose support for easy deployment

## 🛠 Tech Stack

- **Backend**: Django 5.2.13
- **API**: Django REST Framework with JWT authentication
- **Task Queue**: Celery with Redis broker
- **Database**: SQLite (development), can be configured for PostgreSQL
- **Frontend**: Django templates with HTML/CSS
- **Containerization**: Docker & Docker Compose
- **Python**: 3.11

## 📁 Project Structure

```
TaskBoard/
├── config/                          # Django project settings
│   ├── config/                      # Main configuration
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # URL routing
│   │   ├── wsgi.py                  # WSGI config
│   │   ├── asgi.py                  # ASGI config
│   │   ├── celery.py                # Celery configuration
│   │   └── __init__.py
│   ├── taskboard/                   # Main app
│   │   ├── models.py                # Task model definition
│   │   ├── views.py                 # REST API views
│   │   ├── views_ui.py              # Web UI views
│   │   ├── views_auth.py            # Authentication views
│   │   ├── serializers.py           # DRF serializers
│   │   ├── forms.py                 # Django forms
│   │   ├── tasks.py                 # Celery async tasks
│   │   ├── admin.py                 # Django admin config
│   │   ├── urls.py                  # API URLs
│   │   ├── urls_ui.py               # UI URLs
│   │   ├── urls_auth.py             # Auth URLs
│   │   ├── migrations/              # Database migrations
│   │   ├── templates/               # HTML templates
│   │   │   ├── taskboard/
│   │   │   │   ├── base.html        # Base template
│   │   │   │   ├── dashboard.html   # Dashboard view
│   │   │   │   ├── create_task.html # Create task form
│   │   │   │   ├── task_detail.html # Task detail view
│   │   │   │   └── registration/
│   │   │   │       └── login.html   # Login template
│   │   ├── static/                  # Static files (CSS, JS)
│   │   └── tests.py                 # API tests
│   └── manage.py                    # Django CLI
├── docker-compose.yml               # Docker Compose configuration
├── Dockerfile                       # Docker image definition
├── requirements.txt                 # Python dependencies
├── setenv                           # Environment setup script
└── README.md                        # This file
```

## 📦 Dependencies

Key Python packages (see `requirements.txt`):
- **django** - Web framework
- **djangorestframework** - REST API framework
- **djangorestframework-simplejwt** - JWT authentication
- **celery** - Async task processing
- **redis** - Message broker for Celery

## 🚀 Getting Started

### Option 1: Run with Docker (Recommended)

#### Prerequisites
- Docker Desktop installed and running
- Git (for cloning the repository)

#### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaskBoard
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

   This will start three services:
   - **Web**: Django development server on http://localhost:8000
   - **Worker**: Celery worker for background tasks
   - **Redis**: Message broker for task queue

3. **Create a superuser** (Open a new terminal)
   ```bash
   docker-compose exec web sh -c "cd config && python manage.py createsuperuser"
   ```

4. **Access the application**
   - **Web UI**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin/

5. **Stop the containers**
   ```bash
   docker-compose down
   ```

### Option 2: Run Locally

#### Prerequisites
- Python 3.11+
- Redis running locally
- Virtual environment manager (venv)

#### Steps

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd TaskBoard
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .taskboard-env
   source .taskboard-env/bin/activate  # On macOS/Linux
   # or
   .taskboard-env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   cd config
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **In another terminal, start Celery worker**
   ```bash
   source .taskboard-env/bin/activate
   cd config
   celery -A config worker --loglevel=info
   ```

8. **Access the application**
   - **Web UI**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin/

## 📚 API Documentation

### Authentication

Get JWT tokens for API access:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Endpoints

#### List Tasks
```bash
GET /api/tasks/
Authorization: Bearer <your_token>
```

#### Create Task
```bash
POST /api/tasks/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Task Title",
  "description": "Task description",
  "priority": 2,
  "due_date": "2026-05-15",
  "status": "todo"
}
```

#### Get Task Details
```bash
GET /api/tasks/{id}/
Authorization: Bearer <your_token>
```

#### Update Task
```bash
PATCH /api/tasks/{id}/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "status": "doing",
  "priority": 1
}
```

#### Delete Task
```bash
DELETE /api/tasks/{id}/
Authorization: Bearer <your_token>
```

## 🌐 Web UI Routes

| Route | Description |
|-------|-------------|
| `/` | Dashboard (list all tasks) |
| `/tasks/new/` | Create new task form |
| `/tasks/<id>/` | Task detail view |
| `/accounts/login/` | Login page |
| `/accounts/logout/` | Logout |
| `/admin/` | Admin dashboard |

## 🔐 Authentication

The application uses **JWT (JSON Web Tokens)** for API authentication and **Session-based authentication** for web UI.

- **Web UI**: Login using username/password via Django's built-in authentication
- **REST API**: Obtain JWT tokens via `/api/token/` endpoint

## 📧 Email Notifications

When a task is created, an async email notification is sent via Celery:
- Uses Redis as message broker
- Celery worker processes the background job
- Emails are sent to console in development (configured via `EMAIL_BACKEND`)

## 🧪 Testing

Run the test suite:
```bash
cd config
python manage.py test
```

Or with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Configuration

### Environment Variables

Key settings in `config/config/settings.py`:

- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Configure for your domain
- `SECRET_KEY`: Generate a new one for production
- `CELERY_BROKER_URL`: Redis connection string
- `DATABASES`: Database configuration

### Database

Default: SQLite (development only)

For production, use PostgreSQL by updating `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskboard',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📝 Task Model

```python
class Task:
    title: CharField(max_length=200)
    description: TextField
    status: Choice['todo', 'doing', 'done']
    priority: PositiveSmallInteger (1-5)
    due_date: DateField (optional)
    owner: ForeignKey(User)
    created_at: DateTime
    updated_at: DateTime
```

## 🐛 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
docker-compose logs web
```

**Static files not serving:**
```bash
docker-compose exec web python manage.py collectstatic
```

### Database Issues

**Reset database:**
```bash
cd config
python manage.py migrate --fake-initial
python manage.py migrate
```

### Celery Issues

**Check Celery worker status:**
```bash
docker-compose logs worker
```

**Clear task queue:**
```bash
docker-compose exec redis redis-cli FLUSHDB
```

## 📋 Development Workflow

1. Make changes to code
2. Django's auto-reload will restart the server
3. For database changes, create migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run tests:
   ```bash
   python manage.py test
   ```
5. Commit and push changes

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Generate a new `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Use a production-grade WSGI server (Gunicorn, uWSGI)
5. Use a production database (PostgreSQL recommended)
6. Set up SSL/HTTPS
7. Configure email backend for real emails
8. Set up monitoring and logging


## 💬 Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Last Updated**: May 3, 2026
**Version**: 1.0.0
