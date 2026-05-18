import pytest
import json
import os
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

@patch('app.get_db_connection')
def test_get_data_empty(mock_db, client):
    """Test getting data when database is empty"""
    # Mock the database connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = []
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'students' in data
    assert len(data['students']) == 0

@patch('app.get_db_connection')
def test_get_data_with_students(mock_db, client):
    """Test getting data with students in database"""
    from datetime import datetime
    
    # Mock the database connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = [
        (1, 'John Doe', 'john@example.com', 'Computer Science', datetime.now()),
        (2, 'Jane Smith', 'jane@example.com', 'Data Science', datetime.now())
    ]
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['students']) == 2
    assert data['students'][0]['name'] == 'John Doe'
    assert data['students'][1]['name'] == 'Jane Smith'

@patch('app.get_db_connection')
def test_add_data_success(mock_db, client):
    """Test adding a new student"""
    from datetime import datetime
    
    # Mock the database connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1, 'Alice Johnson', 'alice@example.com', 'Engineering', datetime.now())
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    payload = {
        'name': 'Alice Johnson',
        'email': 'alice@example.com',
        'course': 'Engineering'
    }
    
    response = client.post('/api/data', 
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Alice Johnson'
    assert data['email'] == 'alice@example.com'

@patch('app.get_db_connection')
def test_add_data_missing_name(mock_db, client):
    """Test adding a student without name"""
    payload = {
        'email': 'test@example.com',
        'course': 'Engineering'
    }
    
    response = client.post('/api/data',
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 400
    assert 'Name is required' in response.get_json()['error']

@patch('app.get_db_connection')
def test_delete_data_success(mock_db, client):
    """Test deleting a student"""
    # Mock the database connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (1,)  # Student exists
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    response = client.delete('/api/data/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'deleted successfully' in data['message']

@patch('app.get_db_connection')
def test_delete_data_not_found(mock_db, client):
    """Test deleting a non-existent student"""
    # Mock the database connection
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = None  # Student not found
    mock_conn.cursor.return_value = mock_cur
    mock_db.return_value = mock_conn
    
    response = client.delete('/api/data/999')
    assert response.status_code == 404
    assert 'not found' in response.get_json()['error']

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert 'not found' in response.get_json()['error']
