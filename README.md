# Three-Tier Full-Stack Application with CI/CD Pipeline

A complete full-stack web application demonstrating a modern three-tier architecture with automated testing (CI using GitHub Actions) and automated deployment (CD using Railway).

## 📋 Architecture Overview

### Three-Tier Architecture

```
┌─────────────┐
│  Frontend   │ (React/HTML+JS - Port 3000)
│  (UI Layer) │
└──────┬──────┘
       │ REST API
       ▼
┌─────────────────────┐
│  Backend API        │ (Flask - Port 5000)
│  (Business Logic)   │
└──────┬──────────────┘
       │ SQL Queries
       ▼
┌─────────────────────┐
│  PostgreSQL DB      │ (Port 5432)
│  (Data Layer)       │
└─────────────────────┘
```

### Project Structure

```
fullstack-app/
├── .github/
│   └── workflows/
│       ├── ci.yml           # GitHub Actions CI Pipeline
│       └── cd.yml           # GitHub Actions CD Pipeline
├── frontend/
│   ├── Dockerfile           # Frontend Docker configuration
│   ├── package.json         # Node.js dependencies
│   ├── .env.example         # Environment variables template
│   └── src/
│       ├── index.html       # Main HTML file
│       ├── style.css        # Styling
│       └── script.js        # JavaScript logic
├── backend/
│   ├── Dockerfile           # Backend Docker configuration
│   ├── requirements.txt     # Python dependencies
│   ├── app.py               # Flask API server
│   ├── test_app.py          # Unit tests
│   └── .env.example         # Environment variables template
├── docker-compose.yml       # Docker Compose configuration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- PostgreSQL (optional if using Docker)

### Local Development with Docker Compose

1. **Clone or navigate to the project:**
   ```bash
   cd fullstack-app
   ```

2. **Create environment files:**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Start all services:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API Docs: http://localhost:5000/api/data

5. **Stop services:**
   ```bash
   docker-compose down
   ```

### Local Development (Without Docker)

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

5. **Run the Flask server:**
   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

#### Database Setup

1. **Ensure PostgreSQL is running:**
   ```bash
   # Local PostgreSQL default connection
   postgresql://postgres:password@localhost:5432/fullstack_db
   ```

2. **Create database:**
   ```bash
   createdb fullstack_db
   ```

3. **Update DATABASE_URL in backend/.env**

## 🔌 API Endpoints

### Backend REST API

All endpoints return JSON responses and are located at `/api` prefix.

#### 1. **Health Check**
- **Endpoint:** `GET /health`
- **Description:** Check if the API is running
- **Response:**
  ```json
  {
    "status": "healthy"
  }
  ```

#### 2. **Get All Students** (Read)
- **Endpoint:** `GET /api/data`
- **Description:** Retrieve all students from the database
- **Response:**
  ```json
  {
    "students": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "course": "Computer Science",
        "created_at": "2024-05-18T10:30:00"
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "course": "Data Science",
        "created_at": "2024-05-18T11:15:00"
      }
    ]
  }
  ```

#### 3. **Create New Student** (Create)
- **Endpoint:** `POST /api/data`
- **Description:** Add a new student to the database
- **Request Body:**
  ```json
  {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "course": "Engineering"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 3,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "course": "Engineering",
    "created_at": "2024-05-18T12:00:00"
  }
  ```

#### 4. **Delete Student** (Delete)
- **Endpoint:** `DELETE /api/data/:id`
- **Description:** Remove a student from the database
- **Path Parameters:**
  - `id` (integer): Student ID to delete
- **Response (200 OK):**
  ```json
  {
    "message": "Student deleted successfully"
  }
  ```
- **Response (404 Not Found):**
  ```json
  {
    "error": "Student not found"
  }
  ```

### Example API Calls

Using `curl`:

```bash
# Get all students
curl http://localhost:5000/api/data

# Add a new student
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob Wilson","email":"bob@example.com","course":"Math"}'

# Delete a student
curl -X DELETE http://localhost:5000/api/data/1

# Health check
curl http://localhost:5000/health
```

Using Python `requests`:

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# Get all students
response = requests.get(f"{BASE_URL}/api/data")
print(response.json())

# Add a student
new_student = {
    "name": "Charlie Brown",
    "email": "charlie@example.com",
    "course": "Physics"
}
response = requests.post(f"{BASE_URL}/api/data", json=new_student)
print(response.json())

# Delete a student
response = requests.delete(f"{BASE_URL}/api/data/1")
print(response.json())
```

## 🧪 Testing

### Backend Unit Tests

Run pytest to execute all backend tests:

```bash
cd backend
pip install pytest pytest-flask
python -m pytest test_app.py -v
```

**Test Coverage:**
- ✅ Health check endpoint
- ✅ Get all students (empty and with data)
- ✅ Get students with multiple records
- ✅ Add new student (success)
- ✅ Add student without required name (validation)
- ✅ Delete student (success)
- ✅ Delete non-existent student (404 error)
- ✅ Error handling

### Frontend Testing

Frontend uses manual and browser testing. For automated testing in production:

```bash
cd frontend
npm test
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### CI Pipeline (`.github/workflows/ci.yml`)

Runs on every push to `main` or `develop` branches:

1. **Test Backend**
   - Set up Python 3.11
   - Install dependencies from `requirements.txt`
   - Run pytest tests
   - Uses PostgreSQL service container for database tests

2. **Lint Frontend**
   - Set up Node.js 18
   - Install dependencies from `package.json`
   - Run build check
   - Validates JavaScript syntax

3. **Build Docker Images**
   - Build backend Docker image (on main branch only)
   - Build frontend Docker image (on main branch only)

#### CD Pipeline (`.github/workflows/cd.yml`)

Runs on successful CI and push to `main` branch only:

1. **Deploy Backend to Railway**
   - Uses Railway CLI
   - Requires `RAILWAY_TOKEN` secret

2. **Deploy Frontend to Railway**
   - Uses Railway CLI
   - Requires `RAILWAY_TOKEN` secret

3. **Notify Deployment Status**
   - Reports deployment success/failure

### Setting Up GitHub Actions Secrets

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `RAILWAY_TOKEN`: Your Railway CLI authentication token

## 🚢 Deployment to Railway

### Prerequisites

1. Create Railway account at https://railway.app
2. Install Railway CLI: `npm i -g @railway/cli`
3. Generate Railway token from account settings

### Manual Deployment Steps

#### Backend Deployment

1. **Login to Railway:**
   ```bash
   railway login
   ```

2. **Create a new project on Railway:**
   ```bash
   railway init
   ```

3. **Create PostgreSQL database:**
   - Go to Railway dashboard
   - Click "New" → "Database" → "PostgreSQL"
   - Copy the `DATABASE_URL`

4. **Deploy backend:**
   ```bash
   cd backend
   railway up
   ```

5. **Set environment variables in Railway:**
   - Go to backend service settings
   - Add `DATABASE_URL` with the PostgreSQL connection string
   - Add `FLASK_ENV=production`

#### Frontend Deployment

1. **Deploy frontend:**
   ```bash
   cd frontend
   railway up
   ```

2. **Set environment variables in Railway:**
   - Go to frontend service settings
   - Add `REACT_APP_API_URL` with your backend Railway URL (e.g., `https://backend-service.railway.app/api`)
   - Add `PORT=3000`

### Environment Variables

**Backend (.env or Railway):**
```
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=production
PORT=5000
```

**Frontend (.env or Railway):**
```
REACT_APP_API_URL=https://your-backend-url/api
PORT=3000
```

## 📊 Database Schema

### students Table

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    course VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table Columns

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-incrementing |
| name | VARCHAR(255) | Student's full name (required) |
| email | VARCHAR(255) | Student's email address |
| course | VARCHAR(255) | Course name/major |
| created_at | TIMESTAMP | Record creation timestamp |

## 🛠️ Development Tools & Technologies

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with modern features
- **JavaScript (ES6+)** - Interactivity and API calls
- **Fetch API** - HTTP requests to backend

### Backend
- **Python 3.11** - Programming language
- **Flask 2.3** - Web framework
- **psycopg2** - PostgreSQL adapter
- **pytest** - Testing framework
- **flask-cors** - CORS support
- **gunicorn** - Production server

### Database
- **PostgreSQL 15** - Relational database

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD automation
- **Railway** - Cloud deployment platform

## 📝 Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Error: could not translate host name "postgres" to address
```
Solution: Ensure Docker Compose is running and all services are healthy
```bash
docker-compose ps
docker-compose logs postgres
```

**2. CORS Issues (Frontend cannot reach Backend)**
```
Access to XMLHttpRequest at 'http://backend:5000/api/data' blocked by CORS policy
```
Solution: Verify `REACT_APP_API_URL` environment variable
```bash
# Frontend .env
REACT_APP_API_URL=http://localhost:5000/api
```

**3. Port Already in Use**
```
Error: Address already in use
```
Solution: Kill the process using the port or change the port in docker-compose.yml

**4. Tests Failing Locally**
```bash
# Clear cache and reinstall
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest test_app.py -v
```

**5. Frontend not connecting to Backend**
- Check backend is running: `curl http://localhost:5000/health`
- Verify API URL in frontend console
- Check browser DevTools Network tab for actual requests

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Railway Documentation](https://docs.railway.app/)

## 📖 Learning Outcomes

After completing this project, you will understand:

✅ Three-tier application architecture  
✅ REST API design principles  
✅ Database design and relationships  
✅ Docker containerization  
✅ CI/CD pipeline automation  
✅ Cloud deployment strategies  
✅ Environment variable management  
✅ Testing best practices  
✅ Frontend-Backend integration  

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 Author

DevOps Labs - Educational Project

---

**Happy Coding!** 🎉
