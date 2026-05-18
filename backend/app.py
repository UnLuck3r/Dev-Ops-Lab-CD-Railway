import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/fullstack_db')

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Create students table
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    course VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            conn.commit()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

# Initialize database on startup
@app.before_request
def before_first_request():
    """Called before the first request"""
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

# GET all students
@app.route('/api/data', methods=['GET'])
def get_data():
    """Retrieve all students from the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor()
        cur.execute('SELECT id, name, email, course, created_at FROM students ORDER BY created_at DESC;')
        data = cur.fetchall()
        cur.close()
        conn.close()
        
        # Format the response
        students = []
        for row in data:
            students.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'course': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        
        return jsonify({'students': students}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST - Add a new student
@app.route('/api/data', methods=['POST'])
def add_data():
    """Add a new student to the database"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        name = data.get('name')
        email = data.get('email', '')
        course = data.get('course', '')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO students (name, email, course) VALUES (%s, %s, %s) RETURNING id, name, email, course, created_at;',
            (name, email, course)
        )
        new_student = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'id': new_student[0],
            'name': new_student[1],
            'email': new_student[2],
            'course': new_student[3],
            'created_at': new_student[4].isoformat() if new_student[4] else None
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Remove a student
@app.route('/api/data/<int:student_id>', methods=['DELETE'])
def delete_data(student_id):
    """Delete a student from the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor()
        
        # Check if student exists
        cur.execute('SELECT id FROM students WHERE id = %s;', (student_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'Student not found'}), 404
        
        # Delete the student
        cur.execute('DELETE FROM students WHERE id = %s;', (student_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
