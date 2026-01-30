# Cleanup Old Structure

This document explains how to clean up the old mixed structure now that we have a properly separated frontend and backend.

## What Changed?

### Before (Mixed Structure):
```
noteapp/
├── app/              # Backend code mixed with frontend
│   ├── static/
│   │   └── index.html (593 lines - HTML, CSS, JS all together)
│   └── ...
├── requirements.txt  # At root
├── run.py           # At root
└── test_app.py      # At root
```

### After (Separated Structure):
```
noteapp/
├── frontend/         # Separated frontend
│   ├── index.html   # Clean HTML (100 lines)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
├── backend/         # Separated backend
│   ├── app/
│   ├── requirements.txt
│   ├── run.py
│   └── test_app.py
└── ...
```

## Files to Remove (After Verifying New Structure Works)

Once you've verified the new structure works correctly:

### 1. Old Backend Files (Root Level)
```bash
# These are now in backend/ directory
rm run.py
rm test_app.py  
rm requirements.txt  # Only if you don't use Docker (Dockerfile uses this)
rm noteapp.db  # Old SQLite database
```

### 2. Old App Directory
```bash
# Entire old app directory with mixed structure
rm -rf app/
```

## ⚠️ IMPORTANT: Verify First!

**DO NOT delete files until you've:**

1. **Tested new structure**:
   ```bash
   cd backend
   source venv/bin/activate
   python run.py
   # Should start without errors
   ```

2. **Verified frontend loads**:
   - Open http://localhost:8000
   - Can see the login page
   - CSS styles are loaded
   - JavaScript works

3. **Tested all features**:
   - Register account
   - Login
   - Create note
   - Create task
   - Create calendar event

4. **Committed changes to git**:
   ```bash
   git add frontend/ backend/
   git commit -m "Separate frontend and backend architecture"
   git push
   ```

## Safe Cleanup Commands

Only run these AFTER verifying everything works:

```bash
# From noteapp root directory

# 1. Backup first (optional but recommended)
mkdir _old_structure_backup
cp -r app/ _old_structure_backup/
cp run.py test_app.py requirements.txt noteapp.db _old_structure_backup/ 2>/dev/null

# 2. Remove old files
rm -rf app/
rm run.py test_app.py noteapp.db

# 3. Keep root requirements.txt if using Docker
# Or delete if not needed:
# rm requirements.txt
```

## What to Keep

**Keep these files at root:**
- `.gitignore` - Git ignore rules
- `.env` - Environment variables (NEVER commit)
- `.env.example` - Template for .env
- `Dockerfile` - Container definition
- `docker-compose.yml` - Docker orchestration
- `README.md` - Main documentation
- `SETUP.md` - Setup guide
- `requirements.txt` - Only if using Docker (it copies backend/requirements.txt)

## After Cleanup

Your structure should look like:

```
noteapp/
├── frontend/              ✅ New separated frontend
│   ├── index.html
│   ├── css/
│   └── js/
├── backend/              ✅ New separated backend
│   ├── app/
│   ├── requirements.txt
│   ├── run.py
│   └── test_app.py
├── .git/                 ✅ Keep
├── .gitignore            ✅ Keep
├── .env                  ✅ Keep (NEVER commit)
├── .env.example          ✅ Keep
├── Dockerfile            ✅ Keep
├── docker-compose.yml    ✅ Keep
├── README.md             ✅ Keep
├── SETUP.md              ✅ Keep
├── CLEANUP.md            ✅ This file
└── requirements.txt      ✅ Keep if using Docker
```

## Verification After Cleanup

```bash
# 1. Check git status
git status
# Should show deleted: app/, run.py, test_app.py, etc.

# 2. Test application still works
cd backend
source venv/bin/activate
python run.py
# Open http://localhost:8000

# 3. Commit the cleanup
git add -A
git commit -m "Remove old mixed structure, keep only separated frontend/backend"
git push
```

## Rollback (If Something Breaks)

If you deleted files and need them back:

```bash
# If you made backup:
cp -r _old_structure_backup/* .

# Or from git (if committed before):
git checkout HEAD~1 -- app/ run.py test_app.py
```

## Docker Note

If you're using Docker, the root `requirements.txt` might be used by Dockerfile. Check your Dockerfile:

```dockerfile
# If Dockerfile has this:
COPY requirements.txt .

# Then you need root requirements.txt
# Solution: Update Dockerfile to:
COPY backend/requirements.txt .
```

The new Dockerfile already handles this correctly!

## Questions?

- Is the app working? ✅ Safe to delete old files
- Not sure? ⚠️ Make backup first
- Something broke? 🔄 Restore from backup or git

---

**Pro Tip**: Always commit working state before major deletions. Git is your safety net!
