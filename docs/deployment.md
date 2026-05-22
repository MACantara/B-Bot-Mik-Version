# Deployment Guide

Instructions for setting up and deploying B-Bot to local and production environments.

## Prerequisites

- Python 3.10 or higher
- Supabase account (for PostgreSQL database)
- Git (for version control)
- Vercel account (for production deployment)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd B-Bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file from the example:

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 6. Generate Secret Key

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Use the output as your `SECRET_KEY`.

### 7. Set Up Supabase Database

#### Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Create a new project
4. Wait for the project to be ready

#### Get Supabase Credentials

1. Navigate to your project dashboard
2. Go to Settings → API
3. Copy the **Project URL**
4. Copy the **anon/public** key (starts with `eyJhbGci...`)

#### Create Database Tables

1. Navigate to the SQL Editor in Supabase
2. Open the `supabase_setup.sql` file from the project root
3. Copy the SQL script
4. Paste it into the SQL Editor
5. Click "Run" to execute

The script creates:
- `users` table (user accounts)
- `save_states` table (game saves)

### 8. Run Development Server

```bash
python wsgi.py
```

The application will be available at `http://localhost:5000`

### 9. Test the Application

1. Open `http://localhost:5000` in your browser
2. Register a new account
3. Log in
4. Try running a simple script:
```python
bot.move()
bot.turn_left()
bot.move()
```

## Production Deployment (Vercel)

### 1. Prepare for Deployment

#### Update `.gitignore`

Ensure `.env` is in `.gitignore`:

```
.env
venv/
__pycache__/
*.pyc
```

#### Commit Changes

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy to Vercel

#### Import Project

1. Go to [vercel.com](https://vercel.com)
2. Log in or sign up
3. Click "Add New Project"
4. Import your GitHub repository
5. Select the `B-Bot` repository

#### Configure Project

**Framework Preset:** Flask

**Build Command:**
```
pip install -r requirements.txt
```

**Output Directory:** `./`

**Environment Variables:**

Add the following in Vercel dashboard:

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon/public key
- `SECRET_KEY` - Your JWT secret key
- `ALGORITHM` - `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`
- `REFRESH_TOKEN_EXPIRE_DAYS` - `7`

#### Deploy

Click "Deploy" and wait for the build to complete.

### 3. Verify Deployment

1. Visit the deployed URL
2. Test registration and login
3. Test script execution
4. Test save/load functionality

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Supabase project URL | `https://xyz.supabase.co` |
| `SUPABASE_KEY` | Supabase anon/public key | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `SECRET_KEY` | JWT secret key | `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |

## Troubleshooting

### Local Development Issues

#### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

#### Database Connection Error

**Error:** `Connection refused` or `Invalid API key`

**Solution:**
- Verify `.env` file exists
- Check Supabase credentials
- Ensure Supabase project is active

#### Script Timeout

**Error:** Script execution times out

**Solution:**
- Optimize script to reduce iterations
- Check for infinite loops
- Verify multiprocessing is working

### Deployment Issues

#### Build Failure

**Error:** Build fails on Vercel

**Solution:**
- Check `requirements.txt` is present
- Verify Python version compatibility
- Check build logs for specific errors

#### Environment Variables Missing

**Error:** Application crashes on startup

**Solution:**
- Verify all environment variables are set in Vercel
- Check variable names match exactly
- Restart deployment after adding variables

#### Database Connection in Production

**Error:** Cannot connect to Supabase

**Solution:**
- Verify Supabase URL is correct
- Check Supabase project is not paused
- Ensure network allows outbound connections

#### CORS Errors

**Error:** CORS policy blocked request

**Solution:**
- Verify CORS is configured in Flask
- Check frontend is making requests to correct URL
- Ensure origin is allowed in CORS settings

## Performance Optimization

### Database Optimization

- Add indexes to frequently queried columns
- Use connection pooling
- Implement caching for frequently accessed data

### Script Execution Optimization

- Monitor timeout failures
- Implement request queuing for high load
- Consider script caching for repeated executions

### Frontend Optimization

- Minify JavaScript and CSS
- Enable gzip compression
- Use CDN for static assets

## Monitoring

### Application Monitoring

Consider adding:
- Error tracking (Sentry, Rollbar)
- Performance monitoring (New Relic, Datadog)
- Uptime monitoring (UptimeRobot, Pingdom)

### Database Monitoring

- Monitor query performance
- Track connection pool usage
- Set up alerts for slow queries

### Security Monitoring

- Log authentication attempts
- Monitor for suspicious script execution
- Track rate limit violations

## Backup and Recovery

### Database Backups

Supabase provides automatic backups:
- Daily backups retained for 7 days
- Point-in-time recovery available
- Manual backups can be created

### Application Backups

- Version control (Git)
- Environment variable backup
- Configuration file backup

### Recovery Procedures

1. **Database Recovery:**
   - Use Supabase dashboard to restore from backup
   - Use point-in-time recovery if needed

2. **Application Recovery:**
   - Re-deploy from Git
   - Restore environment variables
   - Restart services

## Scaling Considerations

### Horizontal Scaling

- Deploy multiple instances behind a load balancer
- Use session storage for JWT tokens (stateless)
- Implement database connection pooling

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching

### Cost Optimization

- Monitor resource usage
- Optimize script execution time
- Implement rate limiting

## Security Hardening

### Production Security Checklist

- [ ] Use strong secret keys
- [ ] Enable HTTPS only
- [ ] Implement rate limiting
- [ ] Set up CORS properly
- [ ] Monitor for security vulnerabilities
- [ ] Keep dependencies updated
- [ ] Enable security headers
- [ ] Implement logging and monitoring

### HTTPS Configuration

Vercel automatically provides HTTPS. Ensure:
- All API calls use HTTPS
- Redirect HTTP to HTTPS
- Use secure cookies

### Security Headers

Add security headers in Flask:

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Review and apply security patches
- Monitor database storage
- Check logs for errors
- Test backup and recovery procedures

### Dependency Updates

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all
pip install --upgrade -r requirements.txt
```

### Database Maintenance

- Vacuum and analyze tables regularly
- Archive old save states
- Monitor storage usage
- Optimize slow queries

## Support

For deployment issues:
- Check the [Troubleshooting](#troubleshooting) section
- Review Vercel deployment logs
- Check Supabase dashboard for database issues
- Review application logs

## Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Vercel Python Guide](https://vercel.com/docs/frameworks/flask)
- [Supabase Documentation](https://supabase.com/docs)
- [RestrictedPython Documentation](https://restrictedpython.readthedocs.io/)
