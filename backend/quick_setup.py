#!/usr/bin/env python3
"""
Quick Setup Script - Creates SQLite database with sample data
No external dependencies required!
"""

import os
import sys
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.driver import Driver
from app.models.bus import Bus
from app.models.route import Route, RouteStop
from app.models.student import Student
from app.models.document import Document

def create_sample_data():
    """Create comprehensive sample data for the bus management system"""
    
    print("🚀 Creating Bus Management System with Sample Data...")
    
    # Create admin user
    print("👤 Creating admin user...")
    admin_user = User(
        username='admin',
        email='admin@busms.com',
        role='admin',
        first_name='System',
        last_name='Administrator',
        phone='+1234567890',
        address='123 Admin Street, City',
        is_active=True
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    db.session.flush()

    # Create sample routes
    print("🛣️ Creating sample routes...")
    routes_data = [
        {
            'route_name': 'City Center to School',
            'route_code': 'CC-SCH-01',
            'start_location': 'City Center Bus Stand',
            'end_location': 'Green Valley School',
            'total_distance': 15.5,
            'estimated_duration': 45,
            'route_type': 'Urban',
            'start_time': time(7, 0),
            'end_time': time(8, 0),
            'frequency': 2
        },
        {
            'route_name': 'Residential Area to College',
            'route_code': 'RA-COL-02',
            'start_location': 'Sunrise Apartments',
            'end_location': 'Tech University',
            'total_distance': 22.3,
            'estimated_duration': 60,
            'route_type': 'Suburban',
            'start_time': time(6, 30),
            'end_time': time(7, 45),
            'frequency': 3
        },
        {
            'route_name': 'Downtown Express',
            'route_code': 'DT-EXP-03',
            'start_location': 'Downtown Terminal',
            'end_location': 'Business District',
            'total_distance': 12.8,
            'estimated_duration': 35,
            'route_type': 'Express',
            'start_time': time(8, 0),
            'end_time': time(8, 45),
            'frequency': 4
        }
    ]

    routes = []
    for route_data in routes_data:
        route = Route(**route_data)
        db.session.add(route)
        routes.append(route)
    
    db.session.flush()

    # Create sample drivers
    print("👨‍💼 Creating sample drivers...")
    drivers_data = [
        {
            'username': 'driver1', 'email': 'driver1@busms.com', 'role': 'driver',
            'first_name': 'John', 'last_name': 'Smith', 'phone': '+1234567891',
            'employee_id': 'DRV001', 'driver_type': 'Driver', 'license_number': 'DL123456789',
            'license_type': 'Commercial', 'license_expiry': date(2025, 12, 31),
            'date_of_birth': date(1985, 5, 15), 'gender': 'Male', 'blood_group': 'O+',
            'salary': 35000, 'shift_type': 'Morning', 'shift_start_time': time(6, 0), 'shift_end_time': time(14, 0)
        },
        {
            'username': 'driver2', 'email': 'driver2@busms.com', 'role': 'driver',
            'first_name': 'Sarah', 'last_name': 'Johnson', 'phone': '+1234567892',
            'employee_id': 'DRV002', 'driver_type': 'Driver', 'license_number': 'DL987654321',
            'license_type': 'Commercial', 'license_expiry': date(2025, 8, 15),
            'date_of_birth': date(1990, 3, 22), 'gender': 'Female', 'blood_group': 'A+',
            'salary': 38000, 'shift_type': 'Evening', 'shift_start_time': time(14, 0), 'shift_end_time': time(22, 0)
        },
        {
            'username': 'conductor1', 'email': 'conductor1@busms.com', 'role': 'conductor',
            'first_name': 'Mike', 'last_name': 'Wilson', 'phone': '+1234567893',
            'employee_id': 'CON001', 'driver_type': 'Conductor', 'license_number': 'DL456789123',
            'license_type': 'Light Vehicle', 'license_expiry': date(2024, 10, 20),
            'date_of_birth': date(1988, 7, 10), 'gender': 'Male', 'blood_group': 'B+',
            'salary': 25000, 'shift_type': 'Full Day', 'shift_start_time': time(6, 0), 'shift_end_time': time(18, 0)
        }
    ]

    drivers = []
    for driver_data in drivers_data:
        # Create user
        user = User(
            username=driver_data['username'],
            email=driver_data['email'],
            role=driver_data['role'],
            first_name=driver_data['first_name'],
            last_name=driver_data['last_name'],
            phone=driver_data['phone'],
            is_active=True
        )
        user.set_password('driver123')
        db.session.add(user)
        db.session.flush()

        # Create driver profile
        driver = Driver(
            user_id=user.id,
            employee_id=driver_data['employee_id'],
            driver_type=driver_data['driver_type'],
            license_number=driver_data['license_number'],
            license_type=driver_data['license_type'],
            license_expiry=driver_data['license_expiry'],
            date_of_birth=driver_data['date_of_birth'],
            gender=driver_data['gender'],
            blood_group=driver_data['blood_group'],
            salary=driver_data['salary'],
            shift_type=driver_data['shift_type'],
            shift_start_time=driver_data['shift_start_time'],
            shift_end_time=driver_data['shift_end_time'],
            joining_date=date(2023, 1, 15),
            status='Available'
        )
        db.session.add(driver)
        drivers.append(driver)

    db.session.flush()

    # Create sample buses
    print("🚌 Creating sample buses...")
    buses_data = [
        {
            'bus_number': 'BUS001', 'registration_number': 'KA01AB1234',
            'bus_type': 'AC', 'capacity': 45, 'manufacturer': 'Tata',
            'model': 'Starbus', 'year_of_manufacture': 2020, 'fuel_type': 'Diesel',
            'mileage': 8.5, 'insurance_number': 'INS123456789',
            'insurance_expiry': date(2024, 6, 30), 'rc_number': 'RC123456789',
            'rc_expiry': date(2025, 3, 15), 'route_id': routes[0].id, 'driver_id': drivers[0].id
        },
        {
            'bus_number': 'BUS002', 'registration_number': 'KA01CD5678',
            'bus_type': 'Non-AC', 'capacity': 50, 'manufacturer': 'Ashok Leyland',
            'model': 'Viking', 'year_of_manufacture': 2019, 'fuel_type': 'Diesel',
            'mileage': 7.2, 'insurance_number': 'INS987654321',
            'insurance_expiry': date(2024, 9, 15), 'rc_number': 'RC987654321',
            'rc_expiry': date(2025, 1, 20), 'route_id': routes[1].id, 'driver_id': drivers[1].id
        },
        {
            'bus_number': 'BUS003', 'registration_number': 'KA01EF9012',
            'bus_type': 'AC', 'capacity': 40, 'manufacturer': 'Mahindra',
            'model': 'Tourister', 'year_of_manufacture': 2021, 'fuel_type': 'CNG',
            'mileage': 12.0, 'insurance_number': 'INS456789123',
            'insurance_expiry': date(2024, 12, 10), 'rc_number': 'RC456789123',
            'rc_expiry': date(2025, 5, 25), 'route_id': routes[2].id, 'conductor_id': drivers[2].id
        }
    ]

    buses = []
    for bus_data in buses_data:
        bus = Bus(**bus_data, status='Active')
        db.session.add(bus)
        buses.append(bus)

    db.session.flush()

    # Create sample students
    print("👨‍🎓 Creating sample students...")
    students_data = [
        {
            'username': 'student1', 'email': 'student1@school.com', 'role': 'student',
            'first_name': 'Alice', 'last_name': 'Brown', 'phone': '+1234567894',
            'student_id': 'STU001', 'class_name': 'Grade 10', 'section': 'A',
            'roll_number': '101', 'date_of_birth': date(2008, 4, 12),
            'parent_name': 'Robert Brown', 'parent_phone': '+1234567895',
            'route_id': routes[0].id, 'monthly_fee': 2000
        },
        {
            'username': 'student2', 'email': 'student2@school.com', 'role': 'student',
            'first_name': 'Bob', 'last_name': 'Davis', 'phone': '+1234567896',
            'student_id': 'STU002', 'class_name': 'Grade 11', 'section': 'B',
            'roll_number': '205', 'date_of_birth': date(2007, 8, 25),
            'parent_name': 'Linda Davis', 'parent_phone': '+1234567897',
            'route_id': routes[1].id, 'monthly_fee': 2200
        }
    ]

    for student_data in students_data:
        # Create user
        user = User(
            username=student_data['username'],
            email=student_data['email'],
            role=student_data['role'],
            first_name=student_data['first_name'],
            last_name=student_data['last_name'],
            phone=student_data['phone'],
            is_active=True
        )
        user.set_password('student123')
        db.session.add(user)
        db.session.flush()

        # Create student profile
        student = Student(
            user_id=user.id,
            student_id=student_data['student_id'],
            class_name=student_data['class_name'],
            section=student_data['section'],
            roll_number=student_data['roll_number'],
            date_of_birth=student_data['date_of_birth'],
            parent_name=student_data['parent_name'],
            parent_phone=student_data['parent_phone'],
            route_id=student_data['route_id'],
            monthly_fee=student_data['monthly_fee'],
            enrollment_date=date(2023, 6, 1),
            status='Active'
        )
        db.session.add(student)

    # Create sample documents
    print("📄 Creating sample documents...")
    documents_data = [
        {
            'bus_id': buses[0].id, 'document_type': 'Insurance',
            'document_name': 'Vehicle Insurance Certificate',
            'document_number': 'INS123456789', 'file_name': 'insurance_bus001.pdf',
            'file_path': '/uploads/insurance_bus001.pdf', 'file_size': 1024000,
            'file_type': 'application/pdf', 'issue_date': date(2023, 6, 30),
            'expiry_date': date(2024, 6, 30), 'issuing_authority': 'National Insurance Company'
        },
        {
            'bus_id': buses[1].id, 'document_type': 'RC',
            'document_name': 'Registration Certificate',
            'document_number': 'RC987654321', 'file_name': 'rc_bus002.pdf',
            'file_path': '/uploads/rc_bus002.pdf', 'file_size': 856000,
            'file_type': 'application/pdf', 'issue_date': date(2019, 1, 20),
            'expiry_date': date(2025, 1, 20), 'issuing_authority': 'Regional Transport Office'
        }
    ]

    for doc_data in documents_data:
        document = Document(**doc_data)
        db.session.add(document)

    # Commit all changes
    db.session.commit()
    
    print("✅ Sample data created successfully!")
    print("\n🎯 Login Credentials:")
    print("Admin: admin / admin123")
    print("Driver: driver1 / driver123")
    print("Student: student1 / student123")
    print("\n🚀 Start the backend with: python run.py")

def main():
    """Main setup function"""
    app = create_app()
    
    with app.app_context():
        # Create uploads directory
        os.makedirs('uploads', exist_ok=True)
        
        # Drop all tables and recreate (fresh start)
        print("🗄️ Setting up database...")
        db.drop_all()
        db.create_all()
        
        # Create sample data
        create_sample_data()
        
        print("\n🎉 Setup complete! Your bus management system is ready.")
        print("Run 'python run.py' to start the backend server.")

if __name__ == '__main__':
    main()
