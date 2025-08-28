from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, date, time
from app import db
from app.models.user import User
from app.models.driver import Driver
from app.models.bus import Bus
from app.utils.decorators import admin_required, staff_required
from app.utils.helpers import (
    success_response, error_response, paginate_query,
    generate_employee_id, validate_email, validate_phone
)

drivers_bp = Blueprint('drivers', __name__)

@drivers_bp.route('', methods=['GET'])
@jwt_required()
def get_drivers():
    """Get all drivers with pagination and filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        driver_type = request.args.get('driver_type')
        status = request.args.get('status')
        shift_type = request.args.get('shift_type')
        search = request.args.get('search', '').strip()
        
        query = Driver.query.filter_by(is_active=True)
        
        if driver_type:
            query = query.filter_by(driver_type=driver_type)
        
        if status:
            query = query.filter_by(status=status)
        
        if shift_type:
            query = query.filter_by(shift_type=shift_type)
        
        if search:
            query = query.join(User).filter(
                (Driver.employee_id.contains(search)) |
                (Driver.license_number.contains(search)) |
                (User.first_name.contains(search)) |
                (User.last_name.contains(search)) |
                (User.email.contains(search))
            )
        
        query = query.order_by(Driver.employee_id)
        paginated = paginate_query(query, page, per_page)
        
        if not paginated:
            return error_response('Invalid pagination parameters')
        
        drivers_data = [driver.to_dict() for driver in paginated['items']]
        
        return success_response('Drivers retrieved successfully', {
            'drivers': drivers_data,
            'pagination': {
                'total': paginated['total'],
                'pages': paginated['pages'],
                'current_page': paginated['current_page'],
                'per_page': paginated['per_page'],
                'has_next': paginated['has_next'],
                'has_prev': paginated['has_prev']
            }
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve drivers: {str(e)}', 500)

@drivers_bp.route('/<int:driver_id>', methods=['GET'])
@jwt_required()
def get_driver(driver_id):
    """Get a specific driver by ID."""
    try:
        driver = Driver.query.filter_by(id=driver_id, is_active=True).first()
        
        if not driver:
            return error_response('Driver not found', 404)
        
        return success_response('Driver retrieved successfully', {
            'driver': driver.to_dict()
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve driver: {str(e)}', 500)

@drivers_bp.route('', methods=['POST'])
@admin_required
def create_driver(current_user):
    """Create a new driver with AI-powered auto-matching."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Required fields
        required_fields = ['first_name', 'last_name', 'email', 'driver_type', 'license_number']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'{field.replace("_", " ").title()} is required')
        
        email = data.get('email').strip().lower()
        
        # Validate email format
        if not validate_email(email):
            return error_response('Invalid email format')
        
        # Validate phone if provided
        phone = data.get('phone')
        if phone and not validate_phone(phone):
            return error_response('Invalid phone number format')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return error_response('Email already exists')
        
        username = data.get('username') or email.split('@')[0]
        if User.query.filter_by(username=username).first():
            username = f"{username}_{datetime.now().strftime('%Y%m%d')}"
        
        # Generate employee ID
        employee_id = generate_employee_id()
        while Driver.query.filter_by(employee_id=employee_id).first():
            employee_id = generate_employee_id()
        
        # Create user account
        user = User(
            username=username,
            email=email,
            role='driver' if data.get('driver_type') == 'Driver' else 'conductor',
            first_name=data.get('first_name').strip(),
            last_name=data.get('last_name').strip(),
            phone=phone,
            address=data.get('address'),
            is_active=True
        )
        
        # Set default password (should be changed on first login)
        default_password = data.get('password', 'driver123')
        user.set_password(default_password)
        
        db.session.add(user)
        db.session.flush()
        
        # Parse dates
        date_of_birth = None
        if data.get('date_of_birth'):
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        license_expiry = None
        if data.get('license_expiry'):
            license_expiry = datetime.strptime(data['license_expiry'], '%Y-%m-%d').date()
        
        joining_date = date.today()
        if data.get('joining_date'):
            joining_date = datetime.strptime(data['joining_date'], '%Y-%m-%d').date()
        
        # Parse shift times
        shift_start_time = None
        shift_end_time = None
        if data.get('shift_start_time'):
            shift_start_time = datetime.strptime(data['shift_start_time'], '%H:%M').time()
        if data.get('shift_end_time'):
            shift_end_time = datetime.strptime(data['shift_end_time'], '%H:%M').time()
        
        # Create driver profile
        driver = Driver(
            user_id=user.id,
            employee_id=employee_id,
            driver_type=data.get('driver_type'),
            license_number=data.get('license_number').strip(),
            license_type=data.get('license_type'),
            license_expiry=license_expiry,
            date_of_birth=date_of_birth,
            gender=data.get('gender'),
            blood_group=data.get('blood_group'),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_phone=data.get('emergency_contact_phone'),
            joining_date=joining_date,
            salary=data.get('salary'),
            shift_type=data.get('shift_type', 'Full Day'),
            shift_start_time=shift_start_time,
            shift_end_time=shift_end_time,
            status='Available'
        )
        
        db.session.add(driver)
        db.session.commit()
        
        return success_response('Driver created successfully', {
            'driver': driver.to_dict(),
            'default_password': default_password
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create driver: {str(e)}', 500)

@drivers_bp.route('/<int:driver_id>', methods=['PUT'])
@admin_required
def update_driver(current_user, driver_id):
    """Update a driver."""
    try:
        driver = Driver.query.filter_by(id=driver_id, is_active=True).first()
        
        if not driver:
            return error_response('Driver not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        # Update user fields
        user = driver.user
        user_fields = ['first_name', 'last_name', 'phone', 'address']
        for field in user_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # Update email if provided
        if 'email' in data:
            new_email = data['email'].strip().lower()
            if not validate_email(new_email):
                return error_response('Invalid email format')
            
            existing_user = User.query.filter(
                User.email == new_email, User.id != user.id
            ).first()
            if existing_user:
                return error_response('Email already exists')
            
            user.email = new_email
        
        # Update driver fields
        driver_fields = [
            'driver_type', 'license_number', 'license_type', 'gender', 
            'blood_group', 'emergency_contact_name', 'emergency_contact_phone',
            'salary', 'shift_type'
        ]
        
        for field in driver_fields:
            if field in data:
                setattr(driver, field, data[field])
        
        # Handle date fields
        if 'date_of_birth' in data and data['date_of_birth']:
            driver.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        if 'license_expiry' in data and data['license_expiry']:
            driver.license_expiry = datetime.strptime(data['license_expiry'], '%Y-%m-%d').date()
        
        if 'joining_date' in data and data['joining_date']:
            driver.joining_date = datetime.strptime(data['joining_date'], '%Y-%m-%d').date()
        
        # Handle shift times
        if 'shift_start_time' in data and data['shift_start_time']:
            driver.shift_start_time = datetime.strptime(data['shift_start_time'], '%H:%M').time()
        
        if 'shift_end_time' in data and data['shift_end_time']:
            driver.shift_end_time = datetime.strptime(data['shift_end_time'], '%H:%M').time()
        
        db.session.commit()
        
        return success_response('Driver updated successfully', {
            'driver': driver.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update driver: {str(e)}', 500)

@drivers_bp.route('/<int:driver_id>/status', methods=['PATCH'])
@admin_required
def update_driver_status(current_user, driver_id):
    """Update driver status."""
    try:
        driver = Driver.query.filter_by(id=driver_id, is_active=True).first()
        
        if not driver:
            return error_response('Driver not found', 404)
        
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return error_response('Status is required')
        
        valid_statuses = ['Available', 'On Trip', 'On Leave', 'Suspended']
        if new_status not in valid_statuses:
            return error_response('Invalid status')
        
        # If setting to Available, remove bus assignment
        if new_status == 'Available':
            driver.current_bus_id = None
        
        driver.status = new_status
        db.session.commit()
        
        return success_response('Driver status updated successfully', {
            'driver': driver.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update driver status: {str(e)}', 500)

@drivers_bp.route('/<int:driver_id>/performance', methods=['GET'])
@jwt_required()
def get_driver_performance(driver_id):
    """Get driver performance metrics."""
    try:
        driver = Driver.query.filter_by(id=driver_id, is_active=True).first()
        
        if not driver:
            return error_response('Driver not found', 404)
        
        # Calculate performance metrics
        from app.models.trip import Trip
        from sqlalchemy import func
        
        # Get trip statistics
        trip_stats = db.session.query(
            func.count(Trip.id).label('total_trips'),
            func.sum(Trip.delay_minutes).label('total_delay'),
            func.avg(Trip.delay_minutes).label('avg_delay'),
            func.sum(Trip.total_distance).label('total_distance')
        ).filter_by(driver_id=driver_id).first()
        
        # Get on-time performance
        on_time_trips = Trip.query.filter_by(
            driver_id=driver_id
        ).filter(Trip.delay_minutes <= 5).count()
        
        total_trips = trip_stats.total_trips or 0
        on_time_percentage = (on_time_trips / total_trips * 100) if total_trips > 0 else 100
        
        # Get recent trips
        recent_trips = Trip.query.filter_by(
            driver_id=driver_id
        ).order_by(Trip.trip_date.desc()).limit(10).all()
        
        performance_data = {
            'driver_info': driver.to_dict(),
            'statistics': {
                'total_trips': total_trips,
                'on_time_trips': on_time_trips,
                'on_time_percentage': round(on_time_percentage, 2),
                'total_delay_minutes': trip_stats.total_delay or 0,
                'average_delay_minutes': round(trip_stats.avg_delay or 0, 2),
                'total_distance_km': trip_stats.total_distance or 0,
                'rating': driver.rating
            },
            'recent_trips': [trip.to_dict() for trip in recent_trips]
        }
        
        return success_response('Driver performance retrieved successfully', performance_data)
        
    except Exception as e:
        return error_response(f'Failed to retrieve driver performance: {str(e)}', 500)

@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
@admin_required
def delete_driver(current_user, driver_id):
    """Delete (deactivate) a driver."""
    try:
        driver = Driver.query.filter_by(id=driver_id, is_active=True).first()
        
        if not driver:
            return error_response('Driver not found', 404)
        
        # Check if driver has active trips
        from app.models.trip import Trip
        active_trips = Trip.query.filter_by(
            driver_id=driver_id,
            status='In Progress'
        ).count()
        
        if active_trips > 0:
            return error_response('Cannot delete driver with active trips')
        
        # Remove bus assignment
        if driver.current_bus_id:
            bus = Bus.query.get(driver.current_bus_id)
            if bus:
                if bus.driver_id == driver_id:
                    bus.driver_id = None
                elif bus.conductor_id == driver_id:
                    bus.conductor_id = None
        
        # Deactivate driver and user
        driver.is_active = False
        driver.status = 'Suspended'
        driver.user.is_active = False
        
        db.session.commit()
        
        return success_response('Driver deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete driver: {str(e)}', 500)

@drivers_bp.route('/available', methods=['GET'])
@admin_required
def get_available_drivers(current_user):
    """Get available drivers for assignment."""
    try:
        driver_type = request.args.get('driver_type')
        shift_type = request.args.get('shift_type')
        
        query = Driver.query.filter_by(
            is_active=True,
            status='Available'
        )
        
        if driver_type:
            query = query.filter_by(driver_type=driver_type)
        
        if shift_type:
            query = query.filter_by(shift_type=shift_type)
        
        drivers = query.order_by(Driver.employee_id).all()
        drivers_data = [driver.to_dict() for driver in drivers]
        
        return success_response('Available drivers retrieved successfully', {
            'drivers': drivers_data
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve available drivers: {str(e)}', 500)
