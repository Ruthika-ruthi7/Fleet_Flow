# Bus Management System - Deployment Guide

This guide covers deploying the Bus Management System to production environments.

## Deployment Options

### Option 1: Vercel (Frontend) + Railway (Backend)

#### Frontend Deployment (Vercel)

1. **Prepare for Deployment**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel

   # Deploy
   vercel

   # Follow prompts and configure environment variables
   ```

3. **Environment Variables in Vercel**
   - `REACT_APP_API_URL`: Your backend API URL
   - `REACT_APP_MAPS_API_KEY`: Google Maps API key

#### Backend Deployment (Railway)

1. **Prepare Backend**
   ```bash
   cd backend
   # Ensure requirements.txt is up to date
   pip freeze > requirements.txt
   ```

2. **Create railway.json**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "gunicorn -w 4 -b 0.0.0.0:$PORT run:app",
       "healthcheckPath": "/api/health"
     }
   }
   ```

3. **Deploy to Railway**
   - Connect your GitHub repository to Railway
   - Configure environment variables
   - Deploy automatically on push

### Option 2: Render (Full Stack)

#### Backend on Render

1. **Create Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`

2. **Database Setup**
   - Create PostgreSQL database on Render
   - Update DATABASE_URL in environment variables

#### Frontend on Render

1. **Create Static Site**
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`

## Environment Variables

### Backend Production Variables

```env
# Flask Configuration
FLASK_CONFIG=production
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret

# Database (Railway PostgreSQL example)
DATABASE_URL=postgresql://username:password@host:port/database

# Redis (Railway Redis example)
REDIS_URL=redis://username:password@host:port

# External APIs
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
OPENAI_API_KEY=your-openai-api-key

# CORS (add your frontend domain)
CORS_ORIGINS=https://your-frontend-domain.vercel.app

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Frontend Production Variables

```env
REACT_APP_API_URL=https://your-backend-domain.railway.app/api
REACT_APP_MAPS_API_KEY=your-google-maps-api-key
REACT_APP_WEBSOCKET_URL=https://your-backend-domain.railway.app
```

## Database Migration for Production

### PostgreSQL Setup (Recommended for Production)

1. **Update requirements.txt**
   ```
   psycopg2-binary==2.9.7
   ```

2. **Update Database URL**
   ```env
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

3. **Run Migrations**
   ```bash
   flask db upgrade
   flask create-admin
   ```

## Security Considerations

### 1. Environment Variables
- Never commit .env files to version control
- Use strong, unique secrets for production
- Rotate API keys regularly

### 2. Database Security
- Use SSL connections for database
- Implement proper backup strategies
- Restrict database access by IP

### 3. API Security
- Enable HTTPS only
- Implement rate limiting
- Use proper CORS configuration
- Validate all inputs

### 4. File Upload Security
- Limit file sizes and types
- Scan uploaded files for malware
- Store files in secure cloud storage

## Performance Optimization

### Backend Optimization

1. **Gunicorn Configuration**
   ```bash
   gunicorn -w 4 -k gevent -b 0.0.0.0:$PORT run:app
   ```

2. **Redis Caching**
   ```python
   # Cache frequently accessed data
   @cache.memoize(timeout=300)
   def get_bus_stats():
       # Expensive database query
       pass
   ```

3. **Database Optimization**
   - Add proper indexes
   - Use connection pooling
   - Implement query optimization

### Frontend Optimization

1. **Build Optimization**
   ```bash
   npm run build
   # Automatically optimizes bundle size
   ```

2. **Code Splitting**
   ```javascript
   // Lazy load components
   const BusManagement = lazy(() => import('./pages/BusManagement'));
   ```

3. **CDN Configuration**
   - Use Vercel's global CDN
   - Optimize images and assets
   - Enable compression

## Monitoring and Logging

### 1. Application Monitoring
- Use services like Sentry for error tracking
- Implement health check endpoints
- Monitor API response times

### 2. Database Monitoring
- Track query performance
- Monitor connection counts
- Set up backup alerts

### 3. Infrastructure Monitoring
- Monitor server resources
- Set up uptime monitoring
- Configure alert notifications

## Backup Strategy

### 1. Database Backups
```bash
# Automated daily backups
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### 2. File Backups
- Use cloud storage with versioning
- Implement automated backup schedules
- Test restore procedures regularly

## SSL/HTTPS Configuration

### 1. Automatic HTTPS
- Vercel and Railway provide automatic HTTPS
- Ensure all API calls use HTTPS
- Redirect HTTP to HTTPS

### 2. Custom Domain Setup
```bash
# Add custom domain in platform settings
# Configure DNS records
# Enable automatic SSL certificate
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway-app/railway@v1
        with:
          token: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
```

## Health Checks

### Backend Health Check
```python
@app.route('/api/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
```

### Database Health Check
```python
@app.route('/api/health/db')
def db_health_check():
    try:
        db.session.execute('SELECT 1')
        return {'database': 'healthy'}
    except Exception as e:
        return {'database': 'unhealthy', 'error': str(e)}, 500
```

## Scaling Considerations

### 1. Horizontal Scaling
- Use load balancers
- Implement stateless architecture
- Use Redis for session storage

### 2. Database Scaling
- Implement read replicas
- Use connection pooling
- Consider database sharding for large datasets

### 3. File Storage Scaling
- Use cloud storage (AWS S3, Google Cloud Storage)
- Implement CDN for file delivery
- Use image optimization services

## Troubleshooting Production Issues

### 1. Common Issues
- Check environment variables
- Verify database connections
- Review application logs
- Test API endpoints

### 2. Debugging Tools
- Use platform-specific logging
- Implement structured logging
- Set up error tracking

### 3. Performance Issues
- Monitor database queries
- Check memory usage
- Analyze API response times
- Review caching strategies

## Post-Deployment Checklist

- [ ] All environment variables configured
- [ ] Database migrations completed
- [ ] Admin user created
- [ ] SSL certificates active
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] DNS records configured
- [ ] Error tracking enabled
- [ ] Performance monitoring active

## Support and Maintenance

### 1. Regular Updates
- Keep dependencies updated
- Apply security patches
- Monitor for vulnerabilities

### 2. Performance Monitoring
- Regular performance reviews
- Database optimization
- Code profiling

### 3. User Feedback
- Implement feedback collection
- Monitor user analytics
- Plan feature improvements

For additional support or questions about deployment, please refer to the platform-specific documentation or contact the development team.
