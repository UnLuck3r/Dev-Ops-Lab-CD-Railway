# QUICK_REFERENCE.md - Developer Quick Reference

## 🚀 Quick Commands

### Docker (Recommended for Development)

```bash
# First time setup
make setup              # Create .env files
make build              # Build images
make up                 # Start all services

# Daily usage
make logs               # View logs
make test               # Run tests
make down               # Stop services
make ps                 # Show running containers

# Cleanup
make clean              # Remove all containers and volumes
```

### Without Docker

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py           # Start Flask server on port 5000
```

#### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm start               # Start on port 3000
```

#### Tests
```bash
cd backend
python -m pytest test_app.py -v
```

## 📍 Key URLs

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | http://localhost:3000 | User interface |
| Backend | http://localhost:5000 | API server |
| API Health | http://localhost:5000/health | Status check |
| API Docs | http://localhost:5000/api/data | Example endpoint |

## 🔌 API Endpoints

### Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check if API is running |
| GET | `/api/data` | Get all students |
| POST | `/api/data` | Add new student |
| DELETE | `/api/data/:id` | Delete student by ID |

### Example Requests

```bash
# Get all students
curl http://localhost:5000/api/data

# Add student
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@test.com","course":"CS"}'

# Delete student
curl -X DELETE http://localhost:5000/api/data/1
```

## 🗄️ Database

### Access Database

```bash
# Using docker-compose
docker-compose exec postgres psql -U fullstack_user -d fullstack_db

# Useful commands
\dt                          # List tables
\d students                  # Describe students table
SELECT * FROM students;      # Query all students
\q                          # Quit
```

### Database Credentials

- **User**: fullstack_user
- **Password**: fullstack_password
- **Database**: fullstack_db
- **Host**: localhost:5432

## 🧪 Testing

```bash
# All tests
python -m pytest test_app.py -v

# Specific test
python -m pytest test_app.py::test_health_check -v

# With coverage
python -m pytest test_app.py --cov=. --cov-report=html

# Watch mode
ptw test_app.py
```

## 📝 File Locations

### Important Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Main Flask API |
| `backend/test_app.py` | Backend tests |
| `frontend/src/index.html` | Frontend UI |
| `frontend/src/script.js` | Frontend logic |
| `frontend/src/style.css` | Frontend styling |
| `docker-compose.yml` | Container config |
| `.env.example` | Environment template |
| `.github/workflows/ci.yml` | CI pipeline |
| `.github/workflows/cd.yml` | CD pipeline |

## 🐛 Debugging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Common Issues

**Port 5000/3000 in use:**
```bash
# Kill process on port
lsof -i :5000
kill -9 <PID>

# Or change port in docker-compose.yml
```

**Database connection error:**
```bash
# Check if postgres is running
docker-compose ps

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

**Tests failing:**
```bash
# Run with verbose output
python -m pytest test_app.py -vv

# Run with print statements
python -m pytest test_app.py -vv -s

# Run with debugging
python -m pytest test_app.py -vv --pdb
```

## 🔑 Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/db
FLASK_ENV=development
PORT=5000
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## 📊 Project Structure at a Glance

```
fullstack-app/
├── backend/          # Flask API
│   ├── app.py       # (400 lines) Main application
│   └── test_app.py  # (250 lines) Unit tests
├── frontend/        # User interface
│   └── src/
│       ├── index.html    # (150 lines) HTML
│       ├── script.js     # (300 lines) JavaScript
│       └── style.css     # (350 lines) CSS
├── .github/
│   └── workflows/
│       ├── ci.yml       # Automated testing
│       └── cd.yml       # Automated deployment
└── docs/
    ├── README.md         # Main documentation
    ├── DEVELOPMENT.md    # Dev setup guide
    ├── DEPLOYMENT.md     # Railway deployment
    └── TESTING.md        # Testing guide
```

## 🚢 Deployment

### To Railway

```bash
# Login
railway login

# Initialize
railway init

# Deploy backend
cd backend && railway up

# Deploy frontend
cd frontend && railway up

# View logs
railway logs

# Set environment variables
railway variable add DATABASE_URL="..."
railway variable add REACT_APP_API_URL="..."
```

### GitHub Actions

1. Push to `main` branch → CI pipeline runs
2. If CI passes → CD pipeline deploys to Railway
3. Requires `RAILWAY_TOKEN` in GitHub Secrets

## 💾 Data Model

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

## 🎯 Development Workflow

### 1. Setup
```bash
git clone <repo>
cd fullstack-app
make setup && make build && make up
```

### 2. Code Changes
- Edit backend: `backend/app.py` → auto-reload
- Edit frontend: `frontend/src/*` → auto-reload

### 3. Testing
```bash
make test                    # Run tests
docker-compose logs -f       # View logs
```

### 4. Commit & Push
```bash
git add .
git commit -m "feat: description"
git push origin main
```

### 5. Review & Deploy
- GitHub Actions CI runs
- Review workflow results
- CD deploys if all checks pass

## 📱 Frontend Features

- ✅ Display student list
- ✅ Add new student form
- ✅ Delete student button
- ✅ API status indicator
- ✅ Loading spinner
- ✅ Error messages
- ✅ Responsive design
- ✅ Form validation

## ⚙️ Backend Features

- ✅ REST API endpoints
- ✅ PostgreSQL integration
- ✅ Input validation
- ✅ Error handling
- ✅ CORS support
- ✅ Database connection pooling
- ✅ Health check endpoint
- ✅ JSON responses
- ✅ Comprehensive tests

## 🔐 Security Notes

- SQL injection protected (parameterized queries)
- XSS prevented (HTML escaping)
- CORS enabled for same-origin
- Input validation on backend
- Environment variables for secrets
- HTTPS ready for production

## 📞 Getting Help

- **Documentation**: See README.md
- **Development Issues**: See DEVELOPMENT.md
- **Testing Issues**: See TESTING.md
- **Deployment Issues**: See DEPLOYMENT.md
- **Project Overview**: See PROJECT_MANIFEST.md

## ✅ Pre-Deployment Checklist

- [ ] All tests passing: `make test`
- [ ] No console errors in browser
- [ ] API responding correctly
- [ ] Database connection working
- [ ] Environment variables set
- [ ] Docker images built
- [ ] Git commits pushed
- [ ] GitHub Actions CI passed

## 🎯 Common Workflows

### Adding a New API Endpoint

1. Add function to `backend/app.py`
2. Add route decorator
3. Add test to `backend/test_app.py`
4. Run tests: `make test`
5. Update frontend to call new endpoint
6. Test in browser
7. Commit and push

### Adding a New Frontend Page

1. Update `frontend/src/index.html`
2. Add CSS to `frontend/src/style.css`
3. Add JavaScript to `frontend/src/script.js`
4. Test in browser at http://localhost:3000
5. Verify API integration
6. Commit and push

### Debugging Database Issues

1. Connect to database: `docker-compose exec postgres psql -U fullstack_user -d fullstack_db`
2. Check table structure: `\d students`
3. Run test query: `SELECT * FROM students;`
4. Check logs: `docker-compose logs postgres`
5. Restart if needed: `docker-compose restart postgres`

## 📈 Performance Tips

- Use PostgreSQL indexes for frequently searched columns
- Implement API response caching
- Compress frontend assets
- Use connection pooling for database
- Monitor application logs regularly
- Profile slow endpoints
- Optimize database queries

---

**For detailed information, refer to the complete documentation files!** 📚
