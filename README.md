# 🚍 Smart Transportation System  

A full-stack web application for managing and optimizing transportation services.  
The system integrates **React (frontend)** and **Flask (backend)** with a MySQL/Supabase database and provides **live GPS tracking** for buses.  

---

## ✨ Features  
- 🔑 **Role-based Authentication** (Admin & User)  
- 🚌 **Bus Management** (allocation, seat tracking, routes, stops)  
- 🗺️ **Route Optimization** using Google Maps API  
- 📡 **Live GPS Tracking** for real-time bus monitoring  
- 💰 **Fee & Driver Payment Management**  
- ⚡ **AI Integrations**  
  - OCR-based document scanning  
  - Auto form-fill from RTO data  
  - Predictive maintenance alerts  
  - Traffic-based predictions  
- 📊 **Real-time Dashboards** with usage analytics  

---

## 🛠️ Tech Stack  

### Frontend (React)  
- React.js  
- TailwindCSS  
- Node.js & npm  

### Backend (Flask - Python)  
- Flask  
- SQLAlchemy  
- REST APIs  
- MySQL / Supabase  

### Integrations  
- Google Maps API (routes & stops)  
- GPS Tracking API (live bus tracking)  
- OCR & AI modules  

---

## 🚀 Getting Started  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Ruthika-ruthi7/smart-transportation-system.git
cd smart-transportation-system

Setup Frontend (React)
cd frontend
npm install
npm start
App runs on: http://localhost:3000

Setup Backend (Flask)
cd backend
pip install -r requirements.txt
python ultra_simple_app.py
API runs on: http://localhost:5000
Project Structure

smart-transportation-system/
│── frontend/        # React frontend
│   ├── public/      
│   ├── src/         
│   └── package.json
│
│── backend/         # Flask backend
│   ├── ultra_simple_app.py
│   ├── requirements.txt
│   └── models/      
│
│── .gitignore
│── README.md

⚡ Future Enhancements

📱 Mobile App integration

🛰️ Advanced GPS tracking with geofencing

🗓️ Automated scheduling system

📈 AI-powered demand prediction
