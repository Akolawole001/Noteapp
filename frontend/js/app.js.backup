// API Configuration
const API_URL = window.location.origin + '/api';
let accessToken = localStorage.getItem('accessToken');

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

async function register() {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            showLogin();
            showAuthError('Registration successful! Please login.', 'success');
        } else {
            const error = await response.json();
            showAuthError(error.detail || 'Registration failed');
        }
    } catch (error) {
        showAuthError('Network error. Please try again.');
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            accessToken = data.access_token;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', data.refresh_token);
            showApp();
        } else {
            const error = await response.json();
            showAuthError(error.detail || 'Login failed');
        }
    } catch (error) {
        showAuthError('Network error. Please try again.');
    }
}

function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    accessToken = null;
    document.getElementById('authContainer').style.display = 'block';
    document.getElementById('appContainer').style.display = 'none';
}

function showAuthError(message, type = 'error') {
    const errorDiv = document.getElementById('authError');
    errorDiv.textContent = message;
    errorDiv.className = type;
    errorDiv.style.display = 'block';
}

function showApp() {
    document.getElementById('authContainer').style.display = 'none';
    document.getElementById('appContainer').style.display = 'block';
    loadNotes();
    loadTasks();
    loadEvents();
}

// ===========================
// Section Navigation
// ===========================

function showSection(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    
    document.getElementById(`${section}Section`).classList.add('active');
    event.target.classList.add('active');

    if (section === 'notes') loadNotes();
    if (section === 'tasks') loadTasks();
    if (section === 'calendar') loadEvents();
}

// ===========================
// API Helper
// ===========================

async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        }
    };

    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_URL}${endpoint}`, options);
    
    if (response.status === 401) {
        logout();
        return null;
    }

    if (response.status === 204) return true;
    return response.json();
}

// ===========================
// Notes Functions
// ===========================

async function loadNotes() {
    const notes = await apiCall('/notes/');
    const container = document.getElementById('notesList');
    
    if (!notes || notes.length === 0) {
        container.innerHTML = '<div class="empty-state">No notes yet. Create your first note!</div>';
        return;
    }

    container.innerHTML = notes.map(note => `
        <div class="item">
            <div class="item-header">
                <div class="item-title">${note.title}</div>
                <div class="item-actions">
                    <button class="btn-danger" onclick="deleteNote(${note.id})">Delete</button>
                </div>
            </div>
            <div>${note.content || ''}</div>
            <small style="color: #666;">Updated: ${new Date(note.updated_at).toLocaleString()}</small>
        </div>
    `).join('');
}

async function createNote() {
    const title = document.getElementById('noteTitle').value;
    const content = document.getElementById('noteContent').value;

    if (!title) {
        alert('Please enter a title');
        return;
    }

    await apiCall('/notes/', 'POST', { title, content });
    document.getElementById('noteTitle').value = '';
    document.getElementById('noteContent').value = '';
    loadNotes();
}

async function deleteNote(id) {
    if (confirm('Delete this note?')) {
        await apiCall(`/notes/${id}`, 'DELETE');
        loadNotes();
    }
}

// ===========================
// Tasks Functions
// ===========================

async function loadTasks() {
    const tasks = await apiCall('/tasks/');
    const container = document.getElementById('tasksList');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = '<div class="empty-state">No tasks yet. Create your first task!</div>';
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="item">
            <div class="item-header">
                <div>
                    <div class="item-title">${task.title}</div>
                    <span class="status-badge status-${task.status}">${task.status.replace('_', ' ')}</span>
                </div>
                <div class="item-actions">
                    <button class="btn-danger" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            </div>
            <div>${task.description || ''}</div>
            ${task.due_date ? `<small style="color: #666;">Due: ${new Date(task.due_date).toLocaleString()}</small>` : ''}
        </div>
    `).join('');
}

async function createTask() {
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const due_date = document.getElementById('taskDueDate').value || null;
    const status = document.getElementById('taskStatus').value;

    if (!title) {
        alert('Please enter a title');
        return;
    }

    await apiCall('/tasks/', 'POST', { title, description, due_date, status });
    document.getElementById('taskTitle').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('taskDueDate').value = '';
    loadTasks();
}

async function deleteTask(id) {
    if (confirm('Delete this task?')) {
        await apiCall(`/tasks/${id}`, 'DELETE');
        loadTasks();
    }
}

// ===========================
// Calendar Functions
// ===========================

async function loadEvents() {
    const events = await apiCall('/calendar/events');
    const container = document.getElementById('eventsList');
    
    if (!events || events.length === 0) {
        container.innerHTML = '<div class="empty-state">No events yet. Create your first event!</div>';
        return;
    }

    container.innerHTML = events.map(event => `
        <div class="item">
            <div class="item-header">
                <div class="item-title">${event.title}</div>
                <div class="item-actions">
                    <button class="btn-danger" onclick="deleteEvent(${event.id})">Delete</button>
                </div>
            </div>
            <div>${event.description || ''}</div>
            <small style="color: #666;">
                ${new Date(event.start_time).toLocaleString()} - ${new Date(event.end_time).toLocaleString()}
            </small>
        </div>
    `).join('');
}

async function createEvent() {
    const title = document.getElementById('eventTitle').value;
    const description = document.getElementById('eventDescription').value;
    const start_time = document.getElementById('eventStartTime').value;
    const end_time = document.getElementById('eventEndTime').value;

    if (!title || !start_time || !end_time) {
        alert('Please fill in all required fields');
        return;
    }

    await apiCall('/calendar/events', 'POST', { 
        title, 
        description, 
        start_time, 
        end_time 
    });
    
    document.getElementById('eventTitle').value = '';
    document.getElementById('eventDescription').value = '';
    document.getElementById('eventStartTime').value = '';
    document.getElementById('eventEndTime').value = '';
    loadEvents();
}

async function deleteEvent(id) {
    if (confirm('Delete this event?')) {
        await apiCall(`/calendar/events/${id}`, 'DELETE');
        loadEvents();
    }
}

// ===========================
// Initialize App
// ===========================

if (accessToken) {
    showApp();
}
