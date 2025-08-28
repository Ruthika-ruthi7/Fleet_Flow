#!/usr/bin/env python3
"""
Minimal API for Bus Management System
Simple Flask app with hardcoded data to get the frontend working
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-secret-key'
app.config['JWT_SECRET_KEY'] = 'simple-jwt-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)
CORS(app, origins=['http://localhost:3000'])

# Hardcoded users for demo
USERS = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'email': 'admin@busms.com',
        'password_hash': generate_password_hash('admin123'),
        'role': 'admin',
        'first_name': 'System',
        'last_name': 'Administrator',
        'phone': '+1234567890'
    },
    'driver1': {
        'id': 2,
        'username': 'driver1',
        'email': 'driver1@busms.com',
        'password_hash': generate_password_hash('driver123'),
        'role': 'driver',
        'first_name': 'John',
        'last_name': 'Smith',
        'phone': '+1234567891'
    },
    'student1': {
        'id': 3,
        'username': 'student1',
        'email': 'student1@school.com',
        'password_hash': generate_password_hash('student123'),
        'role': 'student',
        'first_name': 'Alice',
        'last_name': 'Brown',
        'phone': '+1234567894'
    }
}

# Hardcoded buses for demo
BUSES = [
    {
        'id': 1,
        'bus_number': 'BUS001',
        'registration_number': 'KA01AB1234',
        'bus_type': 'AC',
        'capacity': 45,
        'manufacturer': 'Tata',
        'model': 'Starbus',
        'status': 'Active',
        'occupancy_percentage': 75.0,
        'current_occupancy': 34,
        'driver_name': 'John Smith',
        'route_name': 'City Center to School',
        'is_insurance_expired': False,
        'is_rc_expired': False,
        'days_to_insurance_expiry': 180,
        'year_of_manufacture': 2020,
        'fuel_type': 'Diesel',
        'mileage': 8.5
    },
    {
        'id': 2,
        'bus_number': 'BUS002',
        'registration_number': 'KA01CD5678',
        'bus_type': 'Non-AC',
        'capacity': 50,
        'manufacturer': 'Ashok Leyland',
        'model': 'Viking',
        'status': 'Active',
        'occupancy_percentage': 60.0,
        'current_occupancy': 30,
        'driver_name': 'Sarah Johnson',
        'route_name': 'Residential Area to College',
        'is_insurance_expired': False,
        'is_rc_expired': False,
        'days_to_insurance_expiry': 90,
        'year_of_manufacture': 2019,
        'fuel_type': 'Diesel',
        'mileage': 7.2
    },
    {
        'id': 3,
        'bus_number': 'BUS003',
        'registration_number': 'KA01EF9012',
        'bus_type': 'AC',
        'capacity': 40,
        'manufacturer': 'Mahindra',
        'model': 'Tourister',
        'status': 'Maintenance',
        'occupancy_percentage': 0.0,
        'current_occupancy': 0,
        'driver_name': None,
        'route_name': None,
        'is_insurance_expired': False,
        'is_rc_expired': False,
        'days_to_insurance_expiry': 200,
        'year_of_manufacture': 2021,
        'fuel_type': 'CNG',
        'mileage': 12.0
    }
]

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Bus Management System API is running'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        user = USERS.get(username)
        
        if user and check_password_hash(user['password_hash'], password):
            access_token = create_access_token(identity=user['id'])
            
            return jsonify({
                'success': True,
                'data': {
                    'access_token': access_token,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name']
                    }
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile."""
    try:
        user_id = get_jwt_identity()
        user = next((u for u in USERS.values() if u['id'] == user_id), None)
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                'profile': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'phone': user['phone']
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buses', methods=['GET'])
@jwt_required()
def get_buses():
    """Get all buses."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        bus_type = request.args.get('bus_type', '')
        search = request.args.get('search', '')
        
        # Filter buses
        filtered_buses = BUSES.copy()
        
        if status:
            filtered_buses = [b for b in filtered_buses if b['status'] == status]
        if bus_type:
            filtered_buses = [b for b in filtered_buses if b['bus_type'] == bus_type]
        if search:
            search_lower = search.lower()
            filtered_buses = [b for b in filtered_buses if 
                            search_lower in b['bus_number'].lower() or
                            search_lower in b['registration_number'].lower() or
                            search_lower in (b['manufacturer'] or '').lower()]
        
        return jsonify({
            'success': True,
            'data': {
                'buses': filtered_buses,
                'pagination': {
                    'total': len(filtered_buses),
                    'pages': 1,
                    'current_page': page,
                    'per_page': per_page,
                    'has_next': False,
                    'has_prev': False
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics."""
    try:
        stats = {
            'total_buses': len(BUSES),
            'total_drivers': 2,
            'total_students': 1,
            'total_routes': 2,
            'todays_trips': 8,
            'students_transported': 150,
            'on_time_percentage': 95,
            'distance_covered': 245,
            'attendance_percentage': 92,
            'monthly_fee': 2000,
            'bus_status': 'On Route',
            'eta': '15 min'
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buses/<int:bus_id>/documents', methods=['GET'])
@jwt_required()
def get_bus_documents(bus_id):
    """Get documents for a bus."""
    try:
        bus = next((b for b in BUSES if b['id'] == bus_id), None)
        if not bus:
            return jsonify({'success': False, 'error': 'Bus not found'}), 404
        
        documents = [
            {
                'id': 1,
                'document_type': 'Insurance',
                'document_name': 'Vehicle Insurance Certificate',
                'document_number': 'INS123456789',
                'file_size_mb': 1.2,
                'is_expired': False,
                'is_expiring_soon': False,
                'days_to_expiry': 180,
                'issue_date': '2023-06-30',
                'expiry_date': '2024-06-30',
                'issuing_authority': 'National Insurance Company',
                'ocr_data': {
                    'text': 'Vehicle Insurance Certificate - Policy Number: INS123456789'
                },
                'ocr_confidence': 0.95
            }
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'bus_id': bus_id,
                'bus_number': bus['bus_number'],
                'documents': documents
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Minimal Bus Management System API...")
    print("📍 Backend running on: http://localhost:5000")
    print("🎯 API Health Check: http://localhost:5000/api/health")
    print("✨ Ready for frontend connection!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
