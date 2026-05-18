# DEVELOPMENT.md - Development Guide

## 🛠️ Local Development Setup

This guide helps you set up a local development environment for the fullstack application.

## Development Stack

- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Backend**: Python 3.11 + Flask
- **Database**: PostgreSQL
- **Testing**: pytest (Backend), Manual testing (Frontend)
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git

## Prerequisites

Before starting, ensure you have:

- Git installed
- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional but recommended)
- PostgreSQL (only if not using Docker)
- Code editor (VS Code recommended)

## Development with Docker Compose (Recommended)

### 1. Initial Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd fullstack-app

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

### 3. Development Workflow

#### Hot Reload

Frontend and Backend both support automatic reload:

```bash
# Frontend - Changes to src/ are auto-detected
docker-compose exec frontend npm start

# Backend - Changes to app.py are auto-detected
docker-compose exec backend flask run
```

#### Running Tests

```bash
# Run all backend tests
docker-compose exec backend python -m pytest test_app.py -v

# Run specific test
docker-compose exec backend python -m pytest test_app.py::test_health_check -v

# Run with coverage
docker-compose exec backend python -m pytest --cov=. test_app.py
```

#### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U fullstack_user -d fullstack_db

# Common psql commands
\dt                    # List all tables
\d students            # Describe students table
SELECT * FROM students; # Query students
\q                     # Quit
```

#### Backend Shell

```bash
# Get Python shell
docker-compose exec backend python

# Get bash shell
docker-compose exec backend bash
```

### 4. Stop Services

```bash
# Stop all services but keep volumes
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and volumes
docker-compose down -v
```

## Development Without Docker

### Backend Development Setup

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fullstack_db
FLASK_ENV=development
PORT=5000
```

#### 4. Create Database

```bash
# Start PostgreSQL (ensure it's running)
# Create database
createdb -h localhost -U postgres fullstack_db

# Or using psql
psql -U postgres -c "CREATE DATABASE fullstack_db;"
```

#### 5. Run Backend

```bash
# From backend directory with venv activated
python app.py
```

The API will be available at `http://localhost:5000`

#### 6. Run Tests

```bash
# Run all tests
python -m pytest test_app.py -v

# Run with output
python -m pytest test_app.py -v -s

# Run specific test
python -m pytest test_app.py::test_add_data_success -v
```

### Frontend Development Setup

#### 1. Navigate to Frontend

```bash
cd frontend
```

#### 2. Install Dependencies

```bash
npm install
```

#### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

#### 4. Start Development Server

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

#### 5. Build for Production

```bash
npm run build
```

## Code Structure

### Backend Structure

```
backend/
├── app.py              # Main Flask application
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
├── Dockerfile          # Production Docker image
├── Dockerfile.dev      # Development Docker image
├── railway.json        # Railway configuration
├── .env.example        # Environment variables template
└── venv/              # Virtual environment (local dev only)
```

### Frontend Structure

```
frontend/
├── src/
│   ├── index.html      # Main HTML file
│   ├── style.css       # Global styles
│   ├── script.js       # JavaScript logic
│   └── images/         # Static images (if needed)
├── package.json        # Node dependencies
├── Dockerfile          # Production Docker image
├── railway.json        # Railway configuration
├── .env.example        # Environment variables template
└── node_modules/       # Dependencies (generated)
```

## API Development

### Adding New Endpoints

1. Edit `backend/app.py`
2. Add new route:
   ```python
   @app.route('/api/new-endpoint', methods=['GET', 'POST'])
   def new_endpoint():
       """Endpoint description"""
       try:
           # Your logic here
           return jsonify({'result': 'success'}), 200
       except Exception as e:
           return jsonify({'error': str(e)}), 500
   ```
3. Test with curl or Postman
4. Add unit tests in `test_app.py`

### Testing New Endpoints

```bash
# Using curl
curl -X POST http://localhost:5000/api/new-endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Using Python requests
import requests
response = requests.post('http://localhost:5000/api/new-endpoint',
                        json={'key': 'value'})
print(response.json())
```

## Frontend Development

### Adding New Features

1. Edit `frontend/src/script.js` for logic
2. Edit `frontend/src/index.html` for HTML
3. Edit `frontend/src/style.css` for styling
4. Test in browser at http://localhost:3000

### Debugging Frontend

- Open browser DevTools (F12)
- Check Console for JavaScript errors
- Check Network tab for API calls
- Check Application tab for local storage

### Common Frontend Issues

**API 404 Errors:**
```javascript
// Wrong API URL
const API_BASE_URL = '/api';  // ❌ Relative path

// Correct API URL
const API_BASE_URL = 'http://localhost:5000/api';  // ✅ Full URL
```

**CORS Errors:**
```javascript
// Frontend CORS headers are set in backend (Flask-CORS)
// No need to configure on frontend
```

## Database Development

### Schema Changes

1. Edit table structure in `backend/app.py` (init_db function)
2. Drop and recreate tables:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```
3. Run migrations (if using Alembic)

### Running Queries

```bash
# Interactive query
docker-compose exec postgres psql -U fullstack_user -d fullstack_db -c "SELECT * FROM students;"

# Or use Python
python
>>> import psycopg2
>>> conn = psycopg2.connect("postgresql://user:pass@localhost/db")
>>> cur = conn.cursor()
>>> cur.execute("SELECT * FROM students;")
```

## Git Workflow

### Branching Strategy

```bash
# Main branch - production ready
git checkout main

# Development branch - active development
git checkout develop

# Feature branch - new features
git checkout -b feature/feature-name

# Bug fix branch
git checkout -b bugfix/bug-name
```

### Committing Changes

```bash
# Check status
git status

# Stage changes
git add .
git add filename  # Specific file

# Commit with message
git commit -m "feat: Add new endpoint"
git commit -m "fix: Fix database connection"
git commit -m "docs: Update README"

# Push to remote
git push origin feature/feature-name
```

### Creating Pull Requests

1. Push your branch to GitHub
2. Open GitHub and create a Pull Request
3. Add description and link issues
4. Wait for CI/CD checks to pass
5. Request review
6. Merge when approved

## Debugging

### Backend Debugging

```python
# Add logging
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
logger.error("Error message")

# Add breakpoints
import pdb
pdb.set_trace()

# Use Python debugger
python -m pdb app.py
```

### Frontend Debugging

```javascript
// Console logging
console.log('Value:', value);
console.error('Error:', error);

// Browser debugger
debugger;  // Code execution will pause here

// Check variable types
console.log(typeof value);
console.log(value instanceof Array);
```

## Performance Optimization

### Backend

- Add database indexes for frequent queries
- Use connection pooling
- Cache frequently accessed data
- Minimize database round trips

### Frontend

- Minimize HTTP requests
- Compress images
- Use lazy loading for large lists
- Implement pagination

## Security Considerations

### Backend

- Validate all inputs
- Use parameterized queries (already done with psycopg2)
- Add rate limiting for APIs
- Use HTTPS in production (handled by Railway)
- Keep dependencies updated

### Frontend

- Escape user input (already done in script.js)
- Don't store sensitive data in localStorage
- Use Content Security Policy headers
- Keep dependencies updated

## Useful Tools

### For Python Development

- **pytest**: Unit testing
- **black**: Code formatter
- **flake8**: Linter
- **mypy**: Type checker

```bash
pip install black flake8 mypy

# Format code
black backend/

# Check code style
flake8 backend/

# Type checking
mypy backend/app.py
```

### For Frontend Development

- **prettier**: Code formatter
- **eslint**: JavaScript linter

```bash
npm install --save-dev prettier eslint

# Format code
npx prettier --write src/

# Lint code
npx eslint src/
```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JavaScript MDN Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Docker Documentation](https://docs.docker.com/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Happy developing!** 🚀
