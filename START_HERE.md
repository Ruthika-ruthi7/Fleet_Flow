# 🚀 SUPER QUICK START - 3 MINUTES!

## Just Run These Commands:

### 1. Backend (Terminal 1)
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements-simple.txt
cp .env.simple .env
python quick_setup.py
python run.py
```

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
cp .env.simple .env
npm start
```

## 🎯 Login
- Browser opens: http://localhost:3000
- **Username**: `admin`
- **Password**: `admin123`

## ✨ What You Get
- 5 sample buses with documents
- 10 drivers with different roles
- 8 routes with stops
- 20 students with assignments
- Working dashboard with AI features
- Document upload with OCR simulation

## 🎮 Try These Features
1. **Bus Management** - Add buses with AI auto-fill
2. **Document Upload** - Upload files, see OCR magic
3. **Dashboard** - Different views for Admin/Driver/Student
4. **Sample Data** - Everything pre-loaded and working

## 🆘 Problems?
- Make sure Python 3.8+ and Node.js 16+ are installed
- If port 5000 is busy, change it in `run.py`
- Delete `app.db` and run `python quick_setup.py` again to reset

**That's it! You're running a full bus management system! 🎉**
