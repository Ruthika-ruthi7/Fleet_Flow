import os
from flask.cli import with_appcontext
import click
from app import create_app, db
from app.models import User, Student, Driver, Bus, Route, RouteStop

# Create Flask app
config_name = os.environ.get('FLASK_CONFIG', 'development')
app = create_app(config_name)

@app.cli.command()
@with_appcontext
def create_admin():
    """Create admin user."""
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('Admin user already exists')
        return
    
    admin = User(
        username='admin',
        email='admin@busmanagement.com',
        role='admin',
        first_name='System',
        last_name='Administrator',
        is_active=True
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print('Admin user created successfully')
    print('Username: admin')
    print('Password: admin123')

@app.cli.command()
@with_appcontext
def create_sample_data():
    """Create sample data for testing."""
    from app.utils.helpers import generate_bus_number, generate_student_id, generate_employee_id
    from datetime import date, time
    
    # Create sample driver
    driver_user = User(
        username='driver1',
        email='driver@busmanagement.com',
        role='driver',
        first_name='John',
        last_name='Driver',
        phone='+1234567890',
        is_active=True
    )
    driver_user.set_password('driver123')
    db.session.add(driver_user)
    db.session.flush()
    
    driver = Driver(
        user_id=driver_user.id,
        employee_id=generate_employee_id(),
        driver_type='Driver',
        license_number='DL123456789',
        license_type='Heavy Vehicle',
        license_expiry=date(2025, 12, 31),
        shift_type='Full Day',
        shift_start_time=time(6, 0),
        shift_end_time=time(18, 0)
    )
    db.session.add(driver)
    db.session.flush()
    
    # Create sample bus
    bus = Bus(
        bus_number=generate_bus_number(),
        registration_number='KA01AB1234',
        bus_type='Non-AC',
        capacity=50,
        manufacturer='Tata',
        model='Starbus',
        year_of_manufacture=2020,
        fuel_type='Diesel',
        status='Active',
        driver_id=driver.id
    )
    db.session.add(bus)
    db.session.flush()
    
    # Create sample route
    route = Route(
        route_name='City Center to School',
        route_code='CC2SCH001',
        start_location='City Center',
        end_location='ABC School',
        total_distance=15.5,
        estimated_duration=45,
        start_time=time(7, 0),
        end_time=time(8, 0),
        status='Active'
    )
    db.session.add(route)
    db.session.flush()
    
    # Create sample route stops
    stops = [
        {'name': 'City Center', 'order': 1, 'arrival_time': time(7, 0)},
        {'name': 'Main Market', 'order': 2, 'arrival_time': time(7, 15)},
        {'name': 'Park Avenue', 'order': 3, 'arrival_time': time(7, 30)},
        {'name': 'ABC School', 'order': 4, 'arrival_time': time(7, 45)}
    ]
    
    for stop_data in stops:
        stop = RouteStop(
            route_id=route.id,
            stop_name=stop_data['name'],
            stop_order=stop_data['order'],
            arrival_time=stop_data['arrival_time'],
            departure_time=stop_data['arrival_time'],
            stop_duration=2
        )
        db.session.add(stop)
    
    # Assign bus to route
    bus.route_id = route.id
    
    # Create sample student
    student_user = User(
        username='student1',
        email='student@busmanagement.com',
        role='student',
        first_name='Jane',
        last_name='Student',
        phone='+1234567891',
        is_active=True
    )
    student_user.set_password('student123')
    db.session.add(student_user)
    db.session.flush()
    
    student = Student(
        user_id=student_user.id,
        student_id=generate_student_id(),
        class_name='10th Grade',
        section='A',
        academic_year='2023-24',
        parent_name='Parent Name',
        parent_phone='+1234567892',
        parent_email='parent@example.com',
        route_id=route.id,
        pickup_stop_id=2,  # Main Market
        bus_id=bus.id,
        monthly_fee=2000.00
    )
    student.generate_qr_code()
    db.session.add(student)
    
    db.session.commit()
    print('Sample data created successfully')

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize database."""
    db.create_all()
    print('Database initialized')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
