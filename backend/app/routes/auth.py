from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import datetime
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.driver import Driver
from app.utils.helpers import (
    validate_email, validate_password, 
    success_response, error_response
)


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Example demo login
    if username == "admin" and password == "admin123":
        return jsonify({"message": "Login successful", "token": "fake-jwt-token"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return error_response('User not found or inactive', 404)
        
        new_token = create_access_token(identity=current_user_id)
        
        return success_response('Token refreshed', {
            'access_token': new_token
        })
        
    except Exception as e:
        return error_response(f'Token refresh failed: {str(e)}', 500)

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'{field.replace("_", " ").title()} is required')
        
        username = data.get('username').strip()
        email = data.get('email').strip().lower()
        password = data.get('password')
        role = data.get('role')
        first_name = data.get('first_name').strip()
        last_name = data.get('last_name').strip()
        
        # Validate data
        if not validate_email(email):
            return error_response('Invalid email format')
        
        is_valid, message = validate_password(password)
        if not is_valid:
            return error_response(message)
        
        if role not in ['admin', 'driver', 'conductor', 'student', 'parent', 'staff']:
            return error_response('Invalid role')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return error_response('Username already exists')
        
        if User.query.filter_by(email=email).first():
            return error_response('Email already exists')
        
        # Create user
        user = User(
            username=username,
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone=data.get('phone'),
            address=data.get('address'),
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Create role-specific profile
        if role == 'student':
            from app.utils.helpers import generate_student_id
            student = Student(
                user_id=user.id,
                student_id=generate_student_id(),
                class_name=data.get('class_name'),
                section=data.get('section'),
                academic_year=data.get('academic_year'),
                parent_name=data.get('parent_name'),
                parent_phone=data.get('parent_phone'),
                parent_email=data.get('parent_email')
            )
            student.generate_qr_code()
            db.session.add(student)
            
        elif role in ['driver', 'conductor']:
            from app.utils.helpers import generate_employee_id
            driver = Driver(
                user_id=user.id,
                employee_id=generate_employee_id(),
                driver_type=role.title(),
                license_number=data.get('license_number', ''),
                license_type=data.get('license_type'),
                shift_type=data.get('shift_type', 'Full Day')
            )
            db.session.add(driver)
        
        db.session.commit()
        
        return success_response('User registered successfully', {
            'user': user.to_dict()
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Registration failed: {str(e)}', 500)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return error_response('User not found', 404)
        
        profile_data = None
        if user.role == 'student' and user.student:
            profile_data = user.student.to_dict()
        elif user.role in ['driver', 'conductor'] and user.driver:
            profile_data = user.driver.to_dict()
        
        return success_response('Profile retrieved', {
            'user': user.to_dict(),
            'profile': profile_data
        })
        
    except Exception as e:
        return error_response(f'Failed to get profile: {str(e)}', 500)

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return error_response('User not found', 404)
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return error_response('Current and new passwords are required')
        
        if not user.check_password(current_password):
            return error_response('Current password is incorrect', 400)
        
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return error_response(message)
        
        user.set_password(new_password)
        db.session.commit()
        
        return success_response('Password changed successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Password change failed: {str(e)}', 500)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user."""
    try:
        # In a production app, you would blacklist the token here
        return success_response('Logged out successfully')
        
    except Exception as e:
        return error_response(f'Logout failed: {str(e)}', 500)
