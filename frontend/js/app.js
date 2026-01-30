// API Configuration
const API_URL = window.location.origin + '/api';
let accessToken = localStorage.getItem('accessToken');
let currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');

// ===========================
// Authentication Functions
// ===========================

function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('authError').style.display = 'none';
}

function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('authError').style.display = 'none';
}

function showAuthError(message, type = 'error') {
    const errorDiv = document.getElementById('authError');
    errorDiv.textContent = message;
    errorDiv.className = type === 'success' ? 'error success' : 'error';
    errorDiv.style.display = 'block';
}

async function register() {
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;

    if (!email || !password) {
        showAuthError('Please fill in all fields');
        return;
    }

    showSpinner();
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        hideSpinner();
        if (response.ok) {
            showLogin();
            showAuthError('Registration successful! Please login.', 'success');
            document.getElementById('registerEmail').value = '';
            document.getElementById('registerPassword').value = '';
        } else {
            const error = await response.json();
            showAuthError(error.detail || 'Registration failed');
        }
    } catch (error) {
        hideSpinner();
        showAuthError('Network error. Please try again.');
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showAuthError('Please fill in all fields');
        return;
    }

    showSpinner();
    try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });

        hideSpinner();
        if (response.ok) {
            const data = await response.json();
            accessToken = data.access_token;
            currentUser = { email };
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            showApp();
        } else {
            const error = await response.json();
            showAuthError(error.detail || 'Login failed');
        }
    } catch (error) {
        hideSpinner();
        showAuthError('Network error. Please try again.');
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        accessToken = null;
        currentUser = {};
        localStorage.removeItem('accessToken');
        localStorage.removeItem('currentUser');
        document.getElementById('authContainer').style.display = 'flex';
        document.getElementById('appContainer').style.display = 'none';
        document.getElementById('loginEmail').value = '';
        document.getElementById('loginPassword').value = '';
        showLogin();
    }
}

function showApp() {
    document.getElementById('authContainer').style.display = 'none';
    document.getElementById('appContainer').style.display = 'block';
    document.getElementById('userEmail').textContent = currentUser.email || '';
    loadNotes();
    loadTasks();
    loadEvents();
    updateCounts();
}

// ===========================
// API Helper
// ===========================

async function apiCall(endpoint, method = 'GET', body = null) {
    showSpinner();
    try {
        const options = {
            method,
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_URL}${endpoint}`, options);
        
        hideSpinner();
        if (response.status === 401) {
            logout();
            return null;
        }

        if (method === 'DELETE' && response.status === 204) {
            return true;
        }

        if (response.ok) {
            return await response.json();
        }

        const error = await response.json();
        alert(error.detail || 'Operation failed');
        return null;
    } catch (error) {
        hideSpinner();
        alert('Network error. Please check your connection.');
        return null;
    }
}

// ===========================
// Section Navigation
// ===========================

function showSection(section) {
    // Update tabs
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.closest('.tab').classList.add('active');

    // Update sections
    document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
    document.getElementById(`${section}Section`).classList.add('active');

    // Hide all form containers
    hideAllForms();

    // Load data
    if (section === 'notes') loadNotes();
    if (section === 'tasks') loadTasks();
    if (section === 'calendar') loadEvents();
}

// ===========================
// Form Toggle Functions
// ===========================

function toggleNoteForm() {
    const container = document.getElementById('noteFormContainer');
    const isVisible = container.style.display !== 'none';
    hideAllForms();
    if (!isVisible) {
        container.style.display = 'block';
        document.getElementById('noteTitle').focus();
    }
}

function toggleTaskForm() {
    const container = document.getElementById('taskFormContainer');
    const isVisible = container.style.display !== 'none';
    hideAllForms();
    if (!isVisible) {
        container.style.display = 'block';
        document.getElementById('taskTitle').focus();
    }
}

function toggleEventForm() {
    const container = document.getElementById('eventFormContainer');
    const isVisible = container.style.display !== 'none';
    hideAllForms();
    if (!isVisible) {
        container.style.display = 'block';
        document.getElementById('eventTitle').focus();
    }
}

function hideAllForms() {
    document.getElementById('noteFormContainer').style.display = 'none';
    document.getElementById('taskFormContainer').style.display = 'none';
    document.getElementById('eventFormContainer').style.display = 'none';
}

// ===========================
// Notes Functions
// ===========================

async function loadNotes() {
    const notes = await apiCall('/notes');
    const container = document.getElementById('notesList');
    
    if (!notes || notes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-sticky-note"></i>
                <h3>No notes yet</h3>
                <p>Click "New Note" to create your first note</p>
            </div>
        `;
        return;
    }

    container.innerHTML = notes.map(note => `
        <div class="card">
            <h4>${escapeHtml(note.title)}</h4>
            <p>${escapeHtml(note.content || 'No content')}</p>
            <div class="card-meta">
                <small><i class="fas fa-clock"></i> ${formatDate(note.created_at)}</small>
                <div class="card-actions">
                    <button class="btn-delete" onclick="deleteNote(${note.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    updateCounts();
}

async function createNote() {
    const title = document.getElementById('noteTitle').value.trim();
    const content = document.getElementById('noteContent').value.trim();

    if (!title) {
        alert('Please enter a note title');
        return;
    }

    const result = await apiCall('/notes', 'POST', { title, content });
    if (result) {
        document.getElementById('noteTitle').value = '';
        document.getElementById('noteContent').value = '';
        toggleNoteForm();
        loadNotes();
    }
}

async function deleteNote(id) {
    if (confirm('Are you sure you want to delete this note?')) {
        const result = await apiCall(`/notes/${id}`, 'DELETE');
        if (result) {
            loadNotes();
        }
    }
}

// ===========================
// Tasks Functions
// ===========================

async function loadTasks() {
    const tasks = await apiCall('/tasks');
    const container = document.getElementById('tasksList');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-tasks"></i>
                <h3>No tasks yet</h3>
                <p>Click "New Task" to create your first task</p>
            </div>
        `;
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <h4>${escapeHtml(task.title)}</h4>
                <span class="status-badge status-${task.status}">
                    ${getStatusIcon(task.status)} ${formatStatus(task.status)}
                </span>
            </div>
            <p>${escapeHtml(task.description || 'No description')}</p>
            <div class="card-meta">
                <small>
                    <i class="fas fa-calendar"></i> 
                    ${task.due_date ? 'Due: ' + formatDate(task.due_date) : 'No due date'}
                </small>
                <div class="card-actions">
                    <button class="btn-delete" onclick="deleteTask(${task.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    updateCounts();
}

async function createTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const due_date = document.getElementById('taskDueDate').value || null;
    const status = document.getElementById('taskStatus').value;

    if (!title) {
        alert('Please enter a task title');
        return;
    }

    const result = await apiCall('/tasks', 'POST', { title, description, due_date, status });
    if (result) {
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';
        document.getElementById('taskDueDate').value = '';
        document.getElementById('taskStatus').value = 'pending';
        toggleTaskForm();
        loadTasks();
    }
}

async function deleteTask(id) {
    if (confirm('Are you sure you want to delete this task?')) {
        const result = await apiCall(`/tasks/${id}`, 'DELETE');
        if (result) {
            loadTasks();
        }
    }
}

// ===========================
// Calendar Functions
// ===========================

async function loadEvents() {
    const events = await apiCall('/calendar');
    const container = document.getElementById('eventsList');
    
    if (!events || events.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-alt"></i>
                <h3>No events yet</h3>
                <p>Click "New Event" to create your first event</p>
            </div>
        `;
        return;
    }

    container.innerHTML = events.map(event => `
        <div class="card">
            <h4>${escapeHtml(event.title)}</h4>
            <p>${escapeHtml(event.description || 'No description')}</p>
            <div class="card-meta">
                <small>
                    <i class="fas fa-clock"></i> 
                    ${formatDate(event.start_time)} - ${formatTime(event.end_time)}
                </small>
                <div class="card-actions">
                    <button class="btn-delete" onclick="deleteEvent(${event.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    updateCounts();
}

async function createEvent() {
    const title = document.getElementById('eventTitle').value.trim();
    const description = document.getElementById('eventDescription').value.trim();
    const start_time = document.getElementById('eventStartTime').value;
    const end_time = document.getElementById('eventEndTime').value;

    if (!title || !start_time || !end_time) {
        alert('Please fill in all required fields');
        return;
    }

    if (new Date(end_time) <= new Date(start_time)) {
        alert('End time must be after start time');
        return;
    }

    const result = await apiCall('/calendar', 'POST', { 
        title, 
        description, 
        start_time, 
        end_time 
    });
    
    if (result) {
        document.getElementById('eventTitle').value = '';
        document.getElementById('eventDescription').value = '';
        document.getElementById('eventStartTime').value = '';
        document.getElementById('eventEndTime').value = '';
        toggleEventForm();
        loadEvents();
    }
}

async function deleteEvent(id) {
    if (confirm('Are you sure you want to delete this event?')) {
        const result = await apiCall(`/calendar/${id}`, 'DELETE');
        if (result) {
            loadEvents();
        }
    }
}

// ===========================
// UI Helper Functions
// ===========================

function updateCounts() {
    apiCall('/notes').then(notes => {
        document.getElementById('noteCount').textContent = notes ? notes.length : 0;
    });
    apiCall('/tasks').then(tasks => {
        document.getElementById('taskCount').textContent = tasks ? tasks.length : 0;
    });
    apiCall('/calendar').then(events => {
        document.getElementById('eventCount').textContent = events ? events.length : 0;
    });
}

function showSpinner() {
    document.getElementById('loadingSpinner').style.display = 'flex';
}

function hideSpinner() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', options);
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

function formatStatus(status) {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function getStatusIcon(status) {
    const icons = {
        'pending': '📋',
        'in_progress': '🔄',
        'completed': '✅'
    };
    return icons[status] || '📋';
}

// ===========================
// Initialize App
// ===========================

// Check if already logged in
if (accessToken) {
    showApp();
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit forms
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeSection = document.querySelector('.section.active');
        if (activeSection.id === 'notesSection' && document.getElementById('noteFormContainer').style.display !== 'none') {
            createNote();
        } else if (activeSection.id === 'tasksSection' && document.getElementById('taskFormContainer').style.display !== 'none') {
            createTask();
        } else if (activeSection.id === 'calendarSection' && document.getElementById('eventFormContainer').style.display !== 'none') {
            createEvent();
        }
    }
    
    // Escape to close forms
    if (e.key === 'Escape') {
        hideAllForms();
    }
});
