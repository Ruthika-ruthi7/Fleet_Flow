from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User

def role_required(*allowed_roles):
    """Decorator to check if user has required role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            if not current_user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 403
            
            if current_user.role not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require admin role."""
    return role_required('admin')(f)

def driver_required(f):
    """Decorator to require driver or admin role."""
    return role_required('admin', 'driver', 'conductor')(f)

def student_required(f):
    """Decorator to require student, parent, or admin role."""
    return role_required('admin', 'student', 'parent')(f)

def staff_required(f):
    """Decorator to require staff access (admin, driver, conductor)."""
    return role_required('admin', 'driver', 'conductor', 'staff')(f)
