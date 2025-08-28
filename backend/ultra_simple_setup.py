#!/usr/bin/env python3
"""
Ultra Simple Setup Script - Creates SQLite database with minimal sample data
Avoids all complex imports and relationships
"""

import os
import sys
from datetime import datetime, date, time

# Set environment variable to use simple config
os.environ['DATABASE_URL'] = 'sqlite:///app.db'
os.environ['SECRET_KEY'] = 'simple-secret-key'
os.environ['JWT_SECRET_KEY'] = 'simple-jwt-secret'

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_simple_data():
    """Create minimal sample data"""
    
    print("🚀 Creating Simple Bus Management System...")
    
    try:
        # Import Flask and SQLAlchemy directly
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from werkzeug.security import generate_password_hash
        
        # Create simple Flask app
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'simple-secret-key'
        
        db = SQLAlchemy(app)
        
        # Define simple models inline
        class User(db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password_hash = db.Column(db.String(255), nullable=False)
            role = db.Column(db.String(20), nullable=False, default='student')
            first_name = db.Column(db.String(50))
            last_name = db.Column(db.String(50))
            phone = db.Column(db.String(20))
            is_active = db.Column(db.Boolean, default=True)
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            
            def set_password(self, password):
                self.password_hash = generate_password_hash(password)
        
        class Bus(db.Model):
            __tablename__ = 'buses'
            id = db.Column(db.Integer, primary_key=True)
            bus_number = db.Column(db.String(20), unique=True, nullable=False)
            registration_number = db.Column(db.String(20), unique=True, nullable=False)
            bus_type = db.Column(db.String(20), nullable=False)
            capacity = db.Column(db.Integer, nullable=False)
            manufacturer = db.Column(db.String(50))
            model = db.Column(db.String(50))
            status = db.Column(db.String(20), default='Active')
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        class Route(db.Model):
            __tablename__ = 'routes'
            id = db.Column(db.Integer, primary_key=True)
            route_name = db.Column(db.String(100), nullable=False)
            route_code = db.Column(db.String(20), unique=True, nullable=False)
            start_location = db.Column(db.String(100), nullable=False)
            end_location = db.Column(db.String(100), nullable=False)
            status = db.Column(db.String(20), default='Active')
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        with app.app_context():
            # Create uploads directory
            os.makedirs('uploads', exist_ok=True)
            
            # Drop and recreate tables
            print("🗄️ Setting up database...")
            db.drop_all()
            db.create_all()
            
            # Create admin user
            print("👤 Creating admin user...")
            admin = User(
                username='admin',
                email='admin@busms.com',
                role='admin',
                first_name='System',
                last_name='Administrator',
                phone='+1234567890',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create driver user
            print("👨‍💼 Creating driver user...")
            driver = User(
                username='driver1',
                email='driver1@busms.com',
                role='driver',
                first_name='John',
                last_name='Smith',
                phone='+1234567891',
                is_active=True
            )
            driver.set_password('driver123')
            db.session.add(driver)
            
            # Create student user
            print("👨‍🎓 Creating student user...")
            student = User(
                username='student1',
                email='student1@school.com',
                role='student',
                first_name='Alice',
                last_name='Brown',
                phone='+1234567894',
                is_active=True
            )
            student.set_password('student123')
            db.session.add(student)
            
            # Create sample routes
            print("🛣️ Creating sample routes...")
            route1 = Route(
                route_name='City Center to School',
                route_code='CC-SCH-01',
                start_location='City Center Bus Stand',
                end_location='Green Valley School',
                status='Active'
            )
            db.session.add(route1)
            
            route2 = Route(
                route_name='Residential Area to College',
                route_code='RA-COL-02',
                start_location='Sunrise Apartments',
                end_location='Tech University',
                status='Active'
            )
            db.session.add(route2)
            
            # Create sample buses
            print("🚌 Creating sample buses...")
            bus1 = Bus(
                bus_number='BUS001',
                registration_number='KA01AB1234',
                bus_type='AC',
                capacity=45,
                manufacturer='Tata',
                model='Starbus',
                status='Active'
            )
            db.session.add(bus1)
            
            bus2 = Bus(
                bus_number='BUS002',
                registration_number='KA01CD5678',
                bus_type='Non-AC',
                capacity=50,
                manufacturer='Ashok Leyland',
                model='Viking',
                status='Active'
            )
            db.session.add(bus2)
            
            bus3 = Bus(
                bus_number='BUS003',
                registration_number='KA01EF9012',
                bus_type='AC',
                capacity=40,
                manufacturer='Mahindra',
                model='Tourister',
                status='Active'
            )
            db.session.add(bus3)
            
            # Commit all changes
            db.session.commit()
            
            print("✅ Sample data created successfully!")
            print("\n🎯 Login Credentials:")
            print("Admin: admin / admin123")
            print("Driver: driver1 / driver123")
            print("Student: student1 / student123")
            print("\n🚀 Start the backend with: python run.py")
            print("🌐 Then start frontend with: npm start")
            
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main setup function"""
    print("🎉 Ultra Simple Bus Management System Setup")
    print("=" * 50)
    
    if create_simple_data():
        print("\n🎉 Setup complete! Your bus management system is ready.")
        print("\nNext steps:")
        print("1. Run: python run.py")
        print("2. In another terminal, go to frontend folder")
        print("3. Run: npm install (if not done)")
        print("4. Run: npm start")
        print("5. Open: http://localhost:3000")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
