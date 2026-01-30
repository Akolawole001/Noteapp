# Deploying to Vercel with Environment Variables

This guide shows you how to deploy your Note App to Vercel and securely configure environment variables.

## Prerequisites

- Vercel account (sign up at [vercel.com](https://vercel.com))
- Vercel CLI installed: `npm i -g vercel`
- Git repository pushed to GitHub

## Part 1: Ensure .env is in .gitignore ✅

Your `.gitignore` already has this correctly configured:

```gitignore
# CRITICAL SECURITY - NEVER COMMIT SECRETS
.env
.env.local
.env.*.local
.env.production
.env.development
```

**Verify it's working:**

```bash
# From your project root
git status

# .env should NOT appear in the list
# If it does, run:
git rm --cached .env
git commit -m "Remove .env from git tracking"
```

## Part 2: Create .env.example Template

Create a template file that CAN be committed (without real secrets):

```bash
cat > .env.example << 'EOF'
# Environment Variables Template
# Copy this to .env and fill in your actual values

# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/database_name

# Security - Generate with: python3 -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Settings
DEBUG=False
ALLOWED_ORIGINS=https://your-domain.vercel.app

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
EOF

git add .env.example
git commit -m "Add environment variables template"
git push
```

## Part 3: Deploy to Vercel

### Option A: Using Vercel Dashboard (Recommended for Beginners)

1. **Go to [vercel.com](https://vercel.com) and login**

2. **Click "Add New Project"**

3. **Import your GitHub repository**
   - Select your `Noteapp` repository
   - Vercel will detect it's a Python project

4. **Configure Build Settings**
   ```
   Framework Preset: Other
   Build Command: cd backend && pip install -r requirements.txt
   Output Directory: backend
   Install Command: pip install -r backend/requirements.txt
   ```

5. **Add Environment Variables** (Click "Environment Variables" section)
   
   Add each variable from your `.env` file:
   
   | Name | Value | Environment |
   |------|-------|-------------|
   | `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Production |
   | `SECRET_KEY` | `<your-generated-secret>` | Production |
   | `ALGORITHM` | `HS256` | All |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | All |
   | `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | All |
   | `DEBUG` | `False` | Production |
   | `ALLOWED_ORIGINS` | `https://your-app.vercel.app` | Production |
   | `RATE_LIMIT_PER_MINUTE` | `60` | All |

   **Important Notes:**
   - Mark `SECRET_KEY` and `DATABASE_URL` as **Sensitive** (eye icon)
   - Use Production PostgreSQL (not SQLite) for Vercel
   - Update `ALLOWED_ORIGINS` after deployment with your actual Vercel URL

6. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Get your deployment URL: `https://your-app.vercel.app`

7. **Update ALLOWED_ORIGINS**
   - Go back to Project Settings → Environment Variables
   - Update `ALLOWED_ORIGINS` with your actual Vercel URL
   - Redeploy for changes to take effect

### Option B: Using Vercel CLI

```bash
# 1. Login to Vercel
vercel login

# 2. Link your project
cd /Users/implicity/Kola-Projects/noteapp
vercel link

# 3. Add environment variables
vercel env add DATABASE_URL production
# Paste your PostgreSQL URL when prompted

vercel env add SECRET_KEY production
# Paste your secret key

vercel env add ALGORITHM production
# Enter: HS256

vercel env add ACCESS_TOKEN_EXPIRE_MINUTES production
# Enter: 30

vercel env add REFRESH_TOKEN_EXPIRE_DAYS production
# Enter: 7

vercel env add DEBUG production
# Enter: False

vercel env add ALLOWED_ORIGINS production
# Enter: https://your-domain.vercel.app

vercel env add RATE_LIMIT_PER_MINUTE production
# Enter: 60

# 4. Deploy
vercel --prod
```

## Part 4: Database Setup for Vercel

Vercel deployments need a cloud database (SQLite won't work):

### Option 1: Vercel Postgres (Easiest)

```bash
# Install Vercel Postgres
vercel postgres create

# This automatically adds DATABASE_URL environment variable
```

### Option 2: External PostgreSQL (Neon, Supabase, Railway)

**Neon (Recommended - Free tier):**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new database
3. Copy connection string: `postgresql://user:pass@host.neon.tech/dbname`
4. Add to Vercel environment variables as `DATABASE_URL`

**Supabase:**
1. Sign up at [supabase.com](https://supabase.com)
2. Create project
3. Get connection string from Settings → Database
4. Add to Vercel as `DATABASE_URL`

## Part 5: Configure vercel.json

Create a `vercel.json` file in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/app/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "PYTHONPATH": "backend"
  }
}
```

## Part 6: Security Checklist

Before deploying:

- [ ] `.env` is in `.gitignore` ✅
- [ ] `.env` file is NOT committed to git
- [ ] Created `.env.example` without real secrets
- [ ] Generated new `SECRET_KEY` for production (don't reuse local key)
- [ ] Using PostgreSQL (not SQLite) for production
- [ ] Set `DEBUG=False` in production
- [ ] Updated `ALLOWED_ORIGINS` with Vercel URL
- [ ] All sensitive variables marked as "Sensitive" in Vercel dashboard

## Part 7: Verify Deployment

After deployment:

```bash
# 1. Check environment variables are loaded
vercel env ls

# 2. Check deployment logs
vercel logs

# 3. Test your API
curl https://your-app.vercel.app/api/health

# 4. Test frontend
open https://your-app.vercel.app
```

## Troubleshooting

### .env appears in git status

```bash
# Remove from git tracking
git rm --cached .env
git commit -m "Stop tracking .env file"
git push
```

### Environment variables not loading

1. Check they're set for correct environment (Production/Preview/Development)
2. Redeploy after adding new variables
3. Check variable names match exactly (case-sensitive)

### Database connection fails

1. Verify `DATABASE_URL` format: `postgresql://user:pass@host:5432/dbname`
2. Check database allows connections from Vercel IPs
3. Confirm database is running and accessible

### CORS errors

Update `ALLOWED_ORIGINS`:
```bash
vercel env add ALLOWED_ORIGINS production
# Enter: https://your-actual-domain.vercel.app,https://www.your-actual-domain.vercel.app
```

## Best Practices

1. **Never commit .env** - Already in your `.gitignore` ✅
2. **Use different secrets for production** - Don't reuse local keys
3. **Rotate secrets regularly** - Change `SECRET_KEY` periodically
4. **Use environment-specific configs** - Different values for dev/prod
5. **Document all variables** - Keep `.env.example` updated
6. **Use Vercel's encryption** - Mark sensitive variables
7. **Audit access logs** - Check who can see your environment variables

## Quick Command Reference

```bash
# Verify .env is ignored
git status

# Add environment variable
vercel env add VARIABLE_NAME production

# List all environment variables
vercel env ls

# Remove environment variable
vercel env rm VARIABLE_NAME production

# Deploy to production
vercel --prod

# View logs
vercel logs

# Open project in browser
vercel open
```

## Generate Production Secrets

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET (if needed)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate strong password
python3 -c "import secrets; print(secrets.token_urlsafe(24))"
```

## Resources

- [Vercel Environment Variables Docs](https://vercel.com/docs/concepts/projects/environment-variables)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Neon PostgreSQL](https://neon.tech)
- [Supabase](https://supabase.com)

---

**Remember:** Your `.env` file stays on your local machine and in Vercel's encrypted storage. It should NEVER appear in your git repository!
