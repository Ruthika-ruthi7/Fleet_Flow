# Bus Management System - Setup Guide

This guide will help you set up the Bus Management System locally for development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (3.8 or higher) - [Download](https://python.org/)
- **MySQL** (8.0 or higher) - [Download](https://mysql.com/)
- **Redis** (6.0 or higher) - [Download](https://redis.io/)
- **Git** - [Download](https://git-scm.com/)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bus-management-system
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your database credentials and API keys
```

### 3. Database Setup

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE bus_management_dev;
EXIT;

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Create admin user
flask create-admin

# (Optional) Create sample data
flask create-sample-data
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env file with your API URL and other settings

# Start development server
npm start
```

### 5. Start Backend Server

```bash
cd ../backend

# Make sure virtual environment is activated
# Start Flask development server
python run.py
```

## Environment Configuration

### Backend (.env)

```env
# Required
DATABASE_URL=mysql+pymysql://root:password@localhost/bus_management_dev
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Optional (for full functionality)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
OPENAI_API_KEY=your-openai-api-key
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_MAPS_API_KEY=your-google-maps-api-key
```

## Default Login Credentials

After running `flask create-admin`, you can login with:

- **Username**: admin
- **Password**: admin123

Additional sample users (if you ran `flask create-sample-data`):

- **Driver**: driver1 / driver123
- **Student**: student1 / student123

## API Keys Setup (Optional)

For full functionality, you'll need these API keys:

### Google Maps API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Maps JavaScript API and Directions API
4. Create credentials (API Key)
5. Add the key to your .env files

### Twilio (for SMS notifications)
1. Sign up at [Twilio](https://twilio.com/)
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Add credentials to backend .env

### OpenAI (for AI features)
1. Sign up at [OpenAI](https://openai.com/)
2. Get your API key
3. Add to backend .env

## Development Workflow

### Running the Application

1. **Start Redis** (required for background tasks):
   ```bash
   redis-server
   ```

2. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate  # Windows: venv\Scripts\activate
   python run.py
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   npm start
   ```

4. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Database Migrations

When you make changes to models:

```bash
cd backend
flask db migrate -m "Description of changes"
flask db upgrade
```

### Adding New Dependencies

**Backend**:
```bash
cd backend
pip install package-name
pip freeze > requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install package-name
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in .env
   - Verify database exists

2. **Port Already in Use**
   - Backend: Change port in run.py
   - Frontend: Set PORT=3001 in frontend/.env

3. **Module Not Found**
   - Backend: Ensure virtual environment is activated
   - Frontend: Run `npm install`

4. **CORS Errors**
   - Check CORS_ORIGINS in backend .env
   - Ensure frontend URL is included

### Reset Database

If you need to reset the database:

```bash
cd backend
flask db downgrade base
flask db upgrade
flask create-admin
```

## Next Steps

1. **Explore the Application**: Login and explore different features
2. **Read Documentation**: Check API.md for API documentation
3. **Customize**: Modify the code to fit your specific needs
4. **Deploy**: See DEPLOYMENT.md for production deployment

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in terminal
3. Ensure all prerequisites are installed correctly
4. Verify environment configuration

For additional help, please refer to the project documentation or create an issue in the repository.
