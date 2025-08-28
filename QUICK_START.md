# 🚀 Quick Start - No Database Setup Required!

This guide will get you running in 5 minutes with SQLite and sample data.

## Prerequisites (Only These!)

- **Python 3.8+** - [Download here](https://python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/download/)

That's it! No MySQL, no Redis, no complex setup.

## 🏃‍♂️ Super Quick Start (5 minutes)

### Step 1: Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (this will take 2-3 minutes)
pip install -r requirements.txt

# Copy the simple config
cp .env.simple .env

# Initialize database with sample data (30 seconds)
python quick_setup.py
```

### Step 2: Start Backend
```bash
python run.py
```

### Step 3: Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies (2-3 minutes)
npm install

# Copy simple config
cp .env.simple .env

# Start frontend
npm start
```

## 🎯 Login & Test

Browser opens to: `http://localhost:3000`

**Login Credentials:**
- **Admin**: `admin` / `admin123`
- **Driver**: `driver1` / `driver123` 
- **Student**: `student1` / `student123`

## 📊 Sample Data Included

- **5 Buses** with different types and statuses
- **10 Drivers** with various roles and shifts
- **8 Routes** covering different areas
- **20 Students** with route assignments
- **Sample Documents** with OCR data
- **Trip History** and attendance records

## ✨ Features to Try

1. **Bus Management** - View buses, add new ones with AI auto-fill
2. **Document Upload** - Upload files and see OCR simulation
3. **Dashboard** - Role-based dashboards for different users
4. **Live Tracking** - Simulated GPS tracking
5. **Reports** - Sample analytics and insights

## 🔧 If Something Goes Wrong

**Backend won't start?**
```bash
# Make sure you're in the right directory and venv is active
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

**Frontend won't start?**
```bash
# Clear cache and try again
cd frontend
npm cache clean --force
npm install
npm start
```

**Database issues?**
```bash
# Reset everything
cd backend
rm -f app.db  # Delete old database
python quick_setup.py  # Recreate with sample data
```

## 🎮 What's Different in This Quick Version?

- **SQLite Database** - No MySQL setup needed
- **No Redis** - Simplified caching
- **Sample Data** - Pre-loaded with realistic data
- **Simplified Config** - Minimal environment variables
- **Mock APIs** - External services simulated

## 🚀 Ready for Production?

When you're ready for the full version:
1. Follow the main SETUP.md for MySQL and Redis
2. Configure external APIs (Google Maps, Twilio, etc.)
3. Enable real OCR and AI features
4. Deploy using DEPLOYMENT.md guide

---

**Need help?** Just run the commands above and you'll have a working bus management system in 5 minutes! 🎉
