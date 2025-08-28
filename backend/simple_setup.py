#!/usr/bin/env python3
"""
Simple Setup Script - Creates SQLite database with sample data
Avoids complex imports and circular dependencies
"""

import os
import sys
from datetime import datetime, date, time

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_sample_data():
    """Create comprehensive sample data for the bus management system"""
    
    print("🚀 Creating Bus Management System with Sample Data...")
    
    # Import here to avoid circular imports
    from app import create_app, db
    
    app = create_app('development')
    
    with app.app_context():
        # Create uploads directory
        os.makedirs('uploads', exist_ok=True)
        
        # Drop all tables and recreate (fresh start)
        print("🗄️ Setting up database...")
        db.drop_all()
        db.create_all()
        
        # Import models after database is created
        from app.models.user import User
        from app.models.driver import Driver
        from app.models.bus import Bus
        from app.models.route import Route, RouteStop
        from app.models.student import Student
        from app.models.document import Document
        
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
        route1 = Route(
            route_name='City Center to School',
            route_code='CC-SCH-01',
            start_location='City Center Bus Stand',
            end_location='Green Valley School',
            total_distance=15.5,
            estimated_duration=45,
            route_type='Urban',
            start_time=time(7, 0),
            end_time=time(8, 0),
            frequency=2,
            status='Active'
        )
        db.session.add(route1)
        
        route2 = Route(
            route_name='Residential Area to College',
            route_code='RA-COL-02',
            start_location='Sunrise Apartments',
            end_location='Tech University',
            total_distance=22.3,
            estimated_duration=60,
            route_type='Suburban',
            start_time=time(6, 30),
            end_time=time(7, 45),
            frequency=3,
            status='Active'
        )
        db.session.add(route2)
        
        db.session.flush()

        # Create sample drivers
        print("👨‍💼 Creating sample drivers...")
        
        # Driver 1
        driver1_user = User(
            username='driver1',
            email='driver1@busms.com',
            role='driver',
            first_name='John',
            last_name='Smith',
            phone='+1234567891',
            is_active=True
        )
        driver1_user.set_password('driver123')
        db.session.add(driver1_user)
        db.session.flush()

        driver1 = Driver(
            user_id=driver1_user.id,
            employee_id='DRV001',
            driver_type='Driver',
            license_number='DL123456789',
            license_type='Commercial',
            license_expiry=date(2025, 12, 31),
            date_of_birth=date(1985, 5, 15),
            gender='Male',
            blood_group='O+',
            salary=35000,
            shift_type='Morning',
            shift_start_time=time(6, 0),
            shift_end_time=time(14, 0),
            joining_date=date(2023, 1, 15),
            status='Available'
        )
        db.session.add(driver1)
        
        # Driver 2
        driver2_user = User(
            username='driver2',
            email='driver2@busms.com',
            role='driver',
            first_name='Sarah',
            last_name='Johnson',
            phone='+1234567892',
            is_active=True
        )
        driver2_user.set_password('driver123')
        db.session.add(driver2_user)
        db.session.flush()

        driver2 = Driver(
            user_id=driver2_user.id,
            employee_id='DRV002',
            driver_type='Driver',
            license_number='DL987654321',
            license_type='Commercial',
            license_expiry=date(2025, 8, 15),
            date_of_birth=date(1990, 3, 22),
            gender='Female',
            blood_group='A+',
            salary=38000,
            shift_type='Evening',
            shift_start_time=time(14, 0),
            shift_end_time=time(22, 0),
            joining_date=date(2023, 2, 1),
            status='Available'
        )
        db.session.add(driver2)
        
        db.session.flush()

        # Create sample buses
        print("🚌 Creating sample buses...")
        
        bus1 = Bus(
            bus_number='BUS001',
            registration_number='KA01AB1234',
            bus_type='AC',
            capacity=45,
            manufacturer='Tata',
            model='Starbus',
            year_of_manufacture=2020,
            fuel_type='Diesel',
            mileage=8.5,
            insurance_number='INS123456789',
            insurance_expiry=date(2024, 6, 30),
            rc_number='RC123456789',
            rc_expiry=date(2025, 3, 15),
            route_id=route1.id,
            driver_id=driver1.id,
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
            year_of_manufacture=2019,
            fuel_type='Diesel',
            mileage=7.2,
            insurance_number='INS987654321',
            insurance_expiry=date(2024, 9, 15),
            rc_number='RC987654321',
            rc_expiry=date(2025, 1, 20),
            route_id=route2.id,
            driver_id=driver2.id,
            status='Active'
        )
        db.session.add(bus2)
        
        db.session.flush()

        # Create sample students
        print("👨‍🎓 Creating sample students...")
        
        student1_user = User(
            username='student1',
            email='student1@school.com',
            role='student',
            first_name='Alice',
            last_name='Brown',
            phone='+1234567894',
            is_active=True
        )
        student1_user.set_password('student123')
        db.session.add(student1_user)
        db.session.flush()

        student1 = Student(
            user_id=student1_user.id,
            student_id='STU001',
            class_name='Grade 10',
            section='A',
            roll_number='101',
            date_of_birth=date(2008, 4, 12),
            parent_name='Robert Brown',
            parent_phone='+1234567895',
            route_id=route1.id,
            monthly_fee=2000,
            enrollment_date=date(2023, 6, 1),
            status='Active'
        )
        db.session.add(student1)
        
        student2_user = User(
            username='student2',
            email='student2@school.com',
            role='student',
            first_name='Bob',
            last_name='Davis',
            phone='+1234567896',
            is_active=True
        )
        student2_user.set_password('student123')
        db.session.add(student2_user)
        db.session.flush()

        student2 = Student(
            user_id=student2_user.id,
            student_id='STU002',
            class_name='Grade 11',
            section='B',
            roll_number='205',
            date_of_birth=date(2007, 8, 25),
            parent_name='Linda Davis',
            parent_phone='+1234567897',
            route_id=route2.id,
            monthly_fee=2200,
            enrollment_date=date(2023, 6, 1),
            status='Active'
        )
        db.session.add(student2)

        # Create sample documents
        print("📄 Creating sample documents...")
        
        doc1 = Document(
            bus_id=bus1.id,
            document_type='Insurance',
            document_name='Vehicle Insurance Certificate',
            document_number='INS123456789',
            file_name='insurance_bus001.pdf',
            file_path='/uploads/insurance_bus001.pdf',
            file_size=1024000,
            file_type='application/pdf',
            issue_date=date(2023, 6, 30),
            expiry_date=date(2024, 6, 30),
            issuing_authority='National Insurance Company'
        )
        db.session.add(doc1)
        
        doc2 = Document(
            bus_id=bus2.id,
            document_type='RC',
            document_name='Registration Certificate',
            document_number='RC987654321',
            file_name='rc_bus002.pdf',
            file_path='/uploads/rc_bus002.pdf',
            file_size=856000,
            file_type='application/pdf',
            issue_date=date(2019, 1, 20),
            expiry_date=date(2025, 1, 20),
            issuing_authority='Regional Transport Office'
        )
        db.session.add(doc2)

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
    try:
        create_sample_data()
        print("\n🎉 Setup complete! Your bus management system is ready.")
        print("Run 'python run.py' to start the backend server.")
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
