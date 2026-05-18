# TESTING.md - Testing Guide

## 📋 Testing Overview

This application includes comprehensive testing for the backend API and guidelines for frontend testing.

## Backend Testing

### Test Framework: pytest

The backend uses `pytest` with `pytest-flask` for testing Flask applications.

### Running Tests

```bash
# Run all tests
python -m pytest test_app.py -v

# Run with detailed output
python -m pytest test_app.py -vv

# Run specific test
python -m pytest test_app.py::test_health_check -v

# Run with output capturing disabled (see print statements)
python -m pytest test_app.py -v -s

# Run with coverage report
pip install pytest-cov
python -m pytest test_app.py --cov=. --cov-report=html

# Run tests in watch mode (requires pytest-watch)
pip install pytest-watch
ptw test_app.py
```

### Test Structure

```python
# Tests are organized by functionality:
# - Health check tests
# - GET endpoint tests (empty and with data)
# - POST endpoint tests (success and validation)
# - DELETE endpoint tests (success and not found)
# - Error handling tests
```

### Available Tests

#### 1. Health Check Test
```python
def test_health_check(client):
    """Test the health check endpoint"""
    # Verifies API is running and responds correctly
```

#### 2. GET Endpoint Tests
```python
def test_get_data_empty(mock_db, client):
    """Test getting data when database is empty"""

def test_get_data_with_students(mock_db, client):
    """Test getting data with students in database"""
    # Verifies correct formatting and data retrieval
```

#### 3. POST Endpoint Tests
```python
def test_add_data_success(mock_db, client):
    """Test adding a new student"""
    # Verifies student is created with correct data

def test_add_data_missing_name(mock_db, client):
    """Test adding a student without name"""
    # Verifies validation works correctly
```

#### 4. DELETE Endpoint Tests
```python
def test_delete_data_success(mock_db, client):
    """Test deleting a student"""
    # Verifies student is deleted

def test_delete_data_not_found(mock_db, client):
    """Test deleting a non-existent student"""
    # Verifies 404 error is returned
```

#### 5. Error Handling Tests
```python
def test_404_error(client):
    """Test 404 error handling"""
    # Verifies proper error response format
```

### Test Database

Tests use a PostgreSQL service container via Docker Compose:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
      POSTGRES_DB: test_db
```

The database is automatically created and torn down for each test run.

### Mocking

Tests use `unittest.mock` to mock database connections:

```python
from unittest.mock import patch, MagicMock

@patch('app.get_db_connection')
def test_example(mock_db, client):
    # Mock the database connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = [...]
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    # Test code here
```

### Test Coverage Goals

- **Minimum Coverage**: 80%
- **Current Coverage**: All critical paths covered
- **Excluded**: Database connection retries, configuration validation

### Adding New Tests

When adding new endpoints:

1. Create test fixture
2. Test success case
3. Test validation/error cases
4. Test edge cases

Example:

```python
@patch('app.get_db_connection')
def test_new_endpoint_success(mock_db, client):
    """Test new endpoint success case"""
    # Setup mock
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (expected_data)
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    # Make request
    response = client.post('/api/new-endpoint',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 201
    assert response.get_json()['key'] == 'value'
```

## Frontend Testing

### Manual Testing Checklist

#### Add Student Form
- [ ] Name field is required (cannot submit empty)
- [ ] Email field accepts valid email format
- [ ] Course field is optional
- [ ] Submit button successfully adds student
- [ ] Form clears after successful submission
- [ ] Error message displays for invalid data
- [ ] Success message appears briefly

#### Student List Display
- [ ] Students display in a table after loading
- [ ] Student ID is visible
- [ ] Student name is displayed
- [ ] Email is displayed (or "-" if empty)
- [ ] Course is displayed (or "-" if empty)
- [ ] Created date is formatted correctly
- [ ] Delete button is present for each student

#### Delete Functionality
- [ ] Confirmation dialog appears when clicking Delete
- [ ] Student is removed after confirmation
- [ ] Student remains if Delete is cancelled
- [ ] List updates after deletion

#### API Status
- [ ] API status shows "Connecting" on load
- [ ] Status changes to "Online" when API is reachable
- [ ] Status changes to "Offline" when API is unreachable
- [ ] Status updates every 10 seconds

#### Error Handling
- [ ] Error message displays when API fails
- [ ] Network errors are handled gracefully
- [ ] Loading spinner appears during API calls
- [ ] User can retry after errors

### Browser Testing

Test on different browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

### Responsive Design Testing

- [ ] Mobile (320px width)
- [ ] Tablet (768px width)
- [ ] Desktop (1024px+ width)

Use browser DevTools to test responsive design:
- F12 → Device Toolbar (Ctrl+Shift+M)
- Test on common screen sizes

### Accessibility Testing

- [ ] Tab navigation works
- [ ] Form labels are associated with inputs
- [ ] Color contrast is sufficient (WCAG AA)
- [ ] Screen reader compatible

Use tools:
- WAVE: https://wave.webaim.org/
- Axe DevTools: https://www.deque.com/axe/devtools/

### Performance Testing

- [ ] Page loads in < 3 seconds
- [ ] API response time < 500ms
- [ ] No memory leaks (check DevTools Memory)

## Automated Testing (GitHub Actions)

### CI Pipeline Tests

The GitHub Actions CI pipeline runs:

1. **Backend Tests**
   ```yaml
   - Run pytest
   - Generate coverage report
   - Check coverage threshold
   ```

2. **Frontend Linting**
   ```yaml
   - Install dependencies
   - Check build
   - Validate JavaScript syntax
   ```

### Test Results

Test results are visible in:
- GitHub Workflow logs
- Pull Request status checks
- Email notifications (on failure)

## Continuous Integration Strategy

### Pre-Commit Testing

Run tests locally before committing:

```bash
# Backend tests
cd backend
python -m pytest test_app.py -v

# If all pass, commit
git add .
git commit -m "feat: Add new feature"
git push
```

### Code Quality Checks

```bash
# Python linting
pip install flake8
flake8 backend/ --max-line-length=100

# Python formatting
pip install black
black backend/

# JavaScript linting (if needed in future)
npm install --save-dev eslint
npx eslint frontend/src/
```

## Performance Testing

### Load Testing

For production deployment, consider:
- Apache JMeter
- Locust
- K6

Example with k6:

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

export default function() {
  let response = http.get('http://localhost:5000/api/data');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

Run with: `k6 run test.js`

### Database Query Performance

```bash
# View query plans
EXPLAIN ANALYZE SELECT * FROM students WHERE name LIKE '%John%';

# Add indexes for frequently searched columns
CREATE INDEX idx_students_name ON students(name);
```

## Security Testing

### SQL Injection Testing

```bash
# Try injecting SQL
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"John\"; DROP TABLE students;--"}'

# Should be safe (parameterized queries)
```

### XSS Testing

```bash
# Try injecting JavaScript
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"<script>alert(\"XSS\")</script>"}'

# Frontend should escape and render as text
```

### CORS Testing

```bash
# Test CORS headers
curl -i -X OPTIONS http://localhost:5000/api/data \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

## Test Data Management

### Sample Data for Testing

```python
SAMPLE_STUDENTS = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "course": "Computer Science"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "course": "Data Science"
    },
    {
        "id": 3,
        "name": "Bob Wilson",
        "email": "bob@example.com",
        "course": "Engineering"
    }
]
```

### Reset Database for Testing

```bash
# Drop and recreate
docker-compose down -v
docker-compose up -d

# Or programmatically
psql -U fullstack_user -d fullstack_db -c "DELETE FROM students;"
```

## Debugging Tests

### Verbose Output

```bash
# Show detailed test output
python -m pytest test_app.py -vv

# Show print statements
python -m pytest test_app.py -v -s

# Show local variables on failures
python -m pytest test_app.py --tb=long
```

### Interactive Debugging

```bash
# Enter pdb on failure
python -m pytest test_app.py --pdb

# Enter pdb on first failure
python -m pytest test_app.py -x --pdb
```

### Test Fixtures

```python
@pytest.fixture(scope="function")
def test_data():
    """Setup test data"""
    data = {"key": "value"}
    yield data
    # Cleanup
```

## Reporting

### Coverage Report

```bash
python -m pytest test_app.py --cov=. --cov-report=html
open htmlcov/index.html
```

### Test Results Summary

```bash
# Run with summary
python -m pytest test_app.py -v --tb=short

# Generate JUnit XML report (for CI)
python -m pytest test_app.py --junit-xml=results.xml
```

## Best Practices

### ✅ Do's

- Write descriptive test names
- Test one thing per test
- Use fixtures for setup/teardown
- Mock external dependencies
- Test both success and failure cases
- Keep tests isolated and independent
- Run tests before committing

### ❌ Don'ts

- Don't test internal implementation details
- Don't use hardcoded data (use fixtures)
- Don't create dependencies between tests
- Don't ignore failing tests
- Don't test third-party libraries
- Don't write tests that randomly pass/fail

## Continuous Testing

### Pre-Push Hook

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash
echo "Running tests before push..."
cd backend
python -m pytest test_app.py -v
if [ $? -ne 0 ]; then
    echo "Tests failed! Push cancelled."
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-push
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)
- [Testing Best Practices](https://testingpython.com/)
- [OWASP Security Testing](https://owasp.org/www-project-web-security-testing-guide/)

---

**Happy testing!** ✅
