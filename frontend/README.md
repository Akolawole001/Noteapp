# NoteApp Frontend

Clean, modern frontend for the NoteApp application built with vanilla HTML, CSS, and JavaScript.

## 📁 Structure

```
frontend/
├── index.html      # Main HTML structure (50 lines)
├── css/
│   └── styles.css  # All styling (200+ lines)
└── js/
    └── app.js      # Application logic (300+ lines)
```

## ✨ Features

- **Authentication**: Login and registration forms
- **Notes Management**: Create, view, and delete notes
- **Task Management**: Create tasks with status tracking (todo, in-progress, completed)
- **Calendar Events**: Schedule and manage calendar events
- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Clean gradient design with smooth transitions

## 🚀 Quick Start

### Option 1: Serve with Backend

The backend automatically serves the frontend when running. Just start the backend:

```bash
# From project root
docker-compose up

# Or run backend directly
cd backend
python run.py
```

Then open: http://localhost:8000

### Option 2: Serve Independently (Development)

For frontend-only development:

```bash
# Using Python
python -m http.server 8080 --directory frontend

# Using Node.js
npx serve frontend

# Using PHP
php -S localhost:8080 -t frontend
```

Then configure the API URL in `js/app.js` if needed.

## 🎨 Styling

### Color Scheme
- Primary: `#667eea` (Purple)
- Secondary: `#764ba2` (Deep Purple)
- Success: `#28a745` (Green)
- Danger: `#dc3545` (Red)
- Warning: `#ffc107` (Yellow)
- Info: `#17a2b8` (Cyan)

### Typography
- Font: System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto)
- Optimized for readability and cross-platform consistency

## 📝 Code Organization

### HTML (index.html)
- Semantic HTML5 structure
- Minimal inline styles
- External CSS and JS references
- Organized sections:
  - Authentication container
  - Application container with tabs
  - Notes, Tasks, and Calendar sections

### CSS (css/styles.css)
- Reset and base styles
- Layout components (containers, headers, tabs)
- Form elements styling
- Button variants (primary, secondary, danger)
- Status badges
- Responsive utilities

### JavaScript (js/app.js)
- Modular function organization:
  - **Authentication**: Register, login, logout
  - **API Helper**: Centralized API calls with error handling
  - **Notes**: CRUD operations for notes
  - **Tasks**: Task management with status
  - **Calendar**: Event scheduling
- Clean separation of concerns
- Error handling and user feedback

## 🔐 Security Considerations

### Token Storage
- Access tokens stored in localStorage
- Tokens sent in Authorization header
- Automatic logout on 401 responses

### Input Validation
- Client-side validation for required fields
- Server-side validation enforced by backend
- XSS protection through DOM manipulation (not innerHTML)

### Best Practices
- No sensitive data in frontend code
- API endpoints configurable
- HTTPS recommended for production

## 🌐 API Integration

The frontend communicates with the backend API at `/api`:

```javascript
const API_URL = window.location.origin + '/api';
```

### Authentication Flow
1. User registers or logs in
2. Backend returns JWT access token
3. Token stored in localStorage
4. Token included in all API requests
5. Automatic logout on token expiration

### API Call Pattern
```javascript
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        }
    };
    if (body) options.body = JSON.stringify(body);
    return fetch(`${API_URL}${endpoint}`, options);
}
```

## 📱 Responsive Design

The app is responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🔧 Customization

### Changing Colors
Edit `css/styles.css` and update color values:
```css
button {
    background: #667eea; /* Your color here */
}
```

### Adding New Sections
1. Add HTML in `index.html`
2. Add styles in `css/styles.css`
3. Add logic in `js/app.js`

### Modifying API URL
For different backend locations, edit `js/app.js`:
```javascript
const API_URL = 'https://your-backend-api.com/api';
```

## 🚀 Production Deployment

### Option 1: Deploy with Backend
The backend serves the frontend automatically. Deploy backend with frontend folder.

### Option 2: Deploy to CDN
For separate deployment:

**Vercel:**
```bash
cd frontend
vercel --prod
```

**Netlify:**
```bash
cd frontend
netlify deploy --prod
```

**Cloudflare Pages:**
```bash
npx wrangler pages deploy frontend
```

Update `API_URL` in `js/app.js` to point to your backend.

## 🎯 Performance Tips

1. **Minimize HTTP Requests**: All CSS in one file, all JS in one file
2. **Browser Caching**: Set appropriate cache headers
3. **Minification**: Minify CSS and JS for production
4. **CDN Delivery**: Serve static files from CDN

## 🐛 Troubleshooting

### CORS Errors
Ensure backend CORS settings allow your frontend origin.

### Token Expiration
Tokens expire after set time. Implement refresh token logic if needed.

### API Connection Failed
Check that backend is running and API_URL is correct.

## 📚 Learning Resources

- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript.info](https://javascript.info/)
- [CSS Tricks](https://css-tricks.com/)

## 🤝 Contributing

1. Keep HTML semantic and accessible
2. Follow CSS naming conventions
3. Write clean, commented JavaScript
4. Test across browsers
5. Ensure mobile responsiveness

## 📄 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📝 Notes

- This is a vanilla JavaScript implementation (no framework)
- Intentionally simple for learning purposes
- Can be migrated to React/Vue/Angular if needed
- Focus on separation of concerns and clean code
