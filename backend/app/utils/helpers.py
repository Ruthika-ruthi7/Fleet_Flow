import re
import uuid
from datetime import datetime, date
from flask import jsonify

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format."""
    if not phone:
        return True  # Phone is optional
    pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
    return re.match(pattern, phone) is not None

def validate_password(password):
    """Validate password strength."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"

def success_response(message, data=None, status_code=200):
    """Create success response."""
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message, status_code=400):
    """Create error response."""
    return jsonify({'success': False, 'error': message}), status_code

def paginate_query(query, page, per_page=10):
    """Paginate a SQLAlchemy query."""
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 10
        per_page = min(per_page, 100)  # Limit max items per page
        
        paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page,
            'per_page': paginated.per_page,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    except ValueError:
        return None

def generate_bus_number(prefix="BUS"):
    """Generate unique bus number."""
    timestamp = datetime.now().strftime("%y%m")
    random_suffix = str(uuid.uuid4().int)[:4]
    return f"{prefix}{timestamp}{random_suffix}"

def generate_student_id(prefix="STU"):
    """Generate unique student ID."""
    year = datetime.now().year
    random_suffix = str(uuid.uuid4().int)[:6]
    return f"{prefix}{year}{random_suffix}"

def generate_employee_id(prefix="EMP"):
    """Generate unique employee ID."""
    year = datetime.now().year
    random_suffix = str(uuid.uuid4().int)[:4]
    return f"{prefix}{year}{random_suffix}"

def generate_route_code(route_name):
    """Generate route code from route name."""
    # Take first 3 characters of each word, uppercase
    words = route_name.split()
    code = ''.join(word[:3].upper() for word in words[:2])
    random_suffix = str(uuid.uuid4().int)[:3]
    return f"{code}{random_suffix}"

def calculate_age(birth_date):
    """Calculate age from birth date."""
    if not birth_date:
        return None
    
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )

def format_currency(amount):
    """Format amount as currency."""
    if amount is None:
        return "₹0.00"
    return f"₹{float(amount):,.2f}"

def get_academic_year():
    """Get current academic year."""
    now = datetime.now()
    if now.month >= 4:  # Academic year starts in April
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"

def get_current_month_name():
    """Get current month name."""
    return datetime.now().strftime('%B')

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula."""
    from math import radians, cos, sin, asin, sqrt
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def generate_qr_code_data(student_id):
    """Generate QR code data for student."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"BMS_{student_id}_{timestamp}"

def parse_time_string(time_str):
    """Parse time string to time object."""
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        try:
            return datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            return None

def format_time(time_obj):
    """Format time object to string."""
    if time_obj:
        return time_obj.strftime('%H:%M')
    return None

def get_next_working_day():
    """Get next working day (Monday-Saturday)."""
    today = date.today()
    days_ahead = 1
    
    while True:
        next_day = today + timedelta(days=days_ahead)
        if next_day.weekday() < 6:  # Monday=0, Sunday=6
            return next_day
        days_ahead += 1

def sanitize_filename(filename):
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    filename = re.sub(r'[^\w\s-.]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-.')

def get_file_extension(filename):
    """Get file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def is_allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension."""
    return '.' in filename and \
           get_file_extension(filename) in allowed_extensions
