// Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// DOM Elements
const addStudentForm = document.getElementById('addStudentForm');
const studentNameInput = document.getElementById('studentName');
const studentEmailInput = document.getElementById('studentEmail');
const studentCourseInput = document.getElementById('studentCourse');
const formMessage = document.getElementById('formMessage');
const studentsTable = document.getElementById('studentsTable');
const studentsBody = document.getElementById('studentsBody');
const emptyMessage = document.getElementById('emptyMessage');
const errorMessage = document.getElementById('errorMessage');
const loadingSpinner = document.getElementById('loadingSpinner');
const apiStatusSpan = document.getElementById('apiStatus');

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
    checkApiStatus();
    // Check API status every 10 seconds
    setInterval(checkApiStatus, 10000);
});

// Event Listeners
addStudentForm.addEventListener('submit', handleAddStudent);

/**
 * Check API health status
 */
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
        if (response.ok) {
            updateApiStatus('online', 'status-online');
        } else {
            updateApiStatus('offline', 'status-offline');
        }
    } catch (error) {
        updateApiStatus('offline', 'status-offline');
    }
}

function updateApiStatus(status, className) {
    apiStatusSpan.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    apiStatusSpan.className = className;
}

/**
 * Load all students from the API
 */
async function loadStudents() {
    try {
        showLoadingSpinner(true);
        hideErrorMessage();

        const response = await fetch(`${API_BASE_URL}/data`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        const students = data.students || [];

        if (students.length === 0) {
            displayEmptyMessage();
        } else {
            displayStudents(students);
        }
    } catch (error) {
        console.error('Error loading students:', error);
        showErrorMessage(`Failed to load students: ${error.message}`);
        displayEmptyMessage();
    } finally {
        showLoadingSpinner(false);
    }
}

/**
 * Display students in the table
 */
function displayStudents(students) {
    emptyMessage.classList.add('hidden');
    studentsTable.classList.remove('hidden');
    studentsBody.innerHTML = '';

    students.forEach(student => {
        const row = document.createElement('tr');
        const createdDate = formatDate(student.created_at);

        row.innerHTML = `
            <td>${student.id}</td>
            <td>${escapeHtml(student.name)}</td>
            <td>${escapeHtml(student.email || '-')}</td>
            <td>${escapeHtml(student.course || '-')}</td>
            <td>${createdDate}</td>
            <td>
                <button class="btn btn-danger" onclick="handleDeleteStudent(${student.id})">
                    Delete
                </button>
            </td>
        `;
        studentsBody.appendChild(row);
    });
}

/**
 * Display empty message
 */
function displayEmptyMessage() {
    emptyMessage.classList.remove('hidden');
    studentsTable.classList.add('hidden');
    studentsBody.innerHTML = '';
}

/**
 * Handle adding a new student
 */
async function handleAddStudent(e) {
    e.preventDefault();

    const name = studentNameInput.value.trim();
    const email = studentEmailInput.value.trim();
    const course = studentCourseInput.value.trim();

    if (!name) {
        showFormMessage('Please enter a student name', 'error');
        return;
    }

    try {
        showLoadingSpinner(true);
        hideErrorMessage();

        const response = await fetch(`${API_BASE_URL}/data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                email: email || null,
                course: course || null
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `API error: ${response.status}`);
        }

        showFormMessage('Student added successfully!', 'success');
        resetForm();
        loadStudents();
    } catch (error) {
        console.error('Error adding student:', error);
        showFormMessage(`Error: ${error.message}`, 'error');
    } finally {
        showLoadingSpinner(false);
    }
}

/**
 * Handle deleting a student
 */
async function handleDeleteStudent(studentId) {
    if (!confirm('Are you sure you want to delete this student?')) {
        return;
    }

    try {
        showLoadingSpinner(true);
        hideErrorMessage();

        const response = await fetch(`${API_BASE_URL}/data/${studentId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `API error: ${response.status}`);
        }

        showFormMessage('Student deleted successfully!', 'success');
        loadStudents();
    } catch (error) {
        console.error('Error deleting student:', error);
        showErrorMessage(`Failed to delete student: ${error.message}`);
    } finally {
        showLoadingSpinner(false);
    }
}

/**
 * Show form message
 */
function showFormMessage(message, type) {
    formMessage.textContent = message;
    formMessage.className = `message ${type}`;
    
    // Auto-hide success messages after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            formMessage.className = 'message';
        }, 3000);
    }
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideErrorMessage() {
    errorMessage.classList.add('hidden');
}

/**
 * Show/hide loading spinner
 */
function showLoadingSpinner(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

/**
 * Reset the form
 */
function resetForm() {
    addStudentForm.reset();
    studentNameInput.focus();
}

/**
 * Format date to readable format
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return dateString;
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
