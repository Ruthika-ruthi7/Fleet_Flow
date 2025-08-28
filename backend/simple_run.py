#!/usr/bin/env python3
"""
Simple Run Script - Starts the Flask app without complex model imports
"""

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from datetime import timedelta

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'simple-secret-key'
app.config['JWT_SECRET_KEY'] = 'simple-jwt-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:3000'])

# Simple User model
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

# Simple Bus model
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

# Simple Route model
class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    route_code = db.Column(db.String(20), unique=True, nullable=False)
    start_location = db.Column(db.String(100), nullable=False)
    end_location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Active')

# API Routes
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
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'success': True,
                'data': {
                    'access_token': access_token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                'profile': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': user.phone
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

        # Get buses from database
        query = Bus.query

        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if bus_type:
            query = query.filter_by(bus_type=bus_type)
        if search:
            query = query.filter(
                (Bus.bus_number.contains(search)) |
                (Bus.registration_number.contains(search)) |
                (Bus.manufacturer.contains(search))
            )

        buses = query.all()
        buses_data = []

        for bus in buses:
            buses_data.append({
                'id': bus.id,
                'bus_number': bus.bus_number,
                'registration_number': bus.registration_number,
                'bus_type': bus.bus_type,
                'capacity': bus.capacity,
                'manufacturer': bus.manufacturer,
                'model': bus.model,
                'status': bus.status,
                'occupancy_percentage': 75.0,  # Mock data
                'current_occupancy': int(bus.capacity * 0.75),
                'driver_name': 'John Smith',  # Mock data
                'route_name': 'City Center to School',  # Mock data
                'is_insurance_expired': False,
                'is_rc_expired': False,
                'days_to_insurance_expiry': 180,
                'year_of_manufacture': 2020,
                'fuel_type': 'Diesel',
                'mileage': 8.5,
                'current_location': None,
                'last_location_update': None
            })

        return jsonify({
            'success': True,
            'data': {
                'buses': buses_data,
                'pagination': {
                    'total': len(buses_data),
                    'pages': 1,
                    'current_page': page,
                    'per_page': per_page,
                    'has_next': False,
                    'has_prev': False
                }
            }
        })

    except Exception as e:
        print(f"Error in get_buses: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/buses', methods=['POST'])
@jwt_required()
def create_bus():
    """Create a new bus."""
    try:
        data = request.get_json()
        
        # Generate bus number if not provided
        bus_number = data.get('bus_number') or f"BUS{Bus.query.count() + 1:03d}"
        
        bus = Bus(
            bus_number=bus_number,
            registration_number=data.get('registration_number'),
            bus_type=data.get('bus_type'),
            capacity=data.get('capacity'),
            manufacturer=data.get('manufacturer'),
            model=data.get('model'),
            status='Active'
        )
        
        db.session.add(bus)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'bus': {
                    'id': bus.id,
                    'bus_number': bus.bus_number,
                    'registration_number': bus.registration_number,
                    'bus_type': bus.bus_type,
                    'capacity': bus.capacity,
                    'manufacturer': bus.manufacturer,
                    'model': bus.model,
                    'status': bus.status
                }
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Mock statistics
        stats = {
            'total_buses': Bus.query.count(),
            'total_drivers': User.query.filter_by(role='driver').count(),
            'total_students': User.query.filter_by(role='student').count(),
            'total_routes': Route.query.count(),
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
        return jsonify({'error': str(e)}), 500

@app.route('/api/buses/<int:bus_id>/documents', methods=['GET'])
@jwt_required()
def get_bus_documents(bus_id):
    """Get documents for a bus."""
    try:
        bus = Bus.query.get(bus_id)
        if not bus:
            return jsonify({'success': False, 'error': 'Bus not found'}), 404

        # Mock documents
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
                    'text': 'Vehicle Insurance Certificate - Policy Number: INS123456789',
                    'confidence': 0.95
                },
                'ocr_confidence': 0.95
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'bus_id': bus_id,
                'bus_number': bus.bus_number,
                'documents': documents
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Add missing endpoints that frontend might call
@app.route('/api/drivers', methods=['GET'])
@jwt_required()
def get_drivers():
    """Get available drivers."""
    try:
        drivers = [
            {
                'id': 1,
                'full_name': 'John Smith',
                'employee_id': 'DRV001',
                'driver_type': 'Driver',
                'status': 'Available'
            },
            {
                'id': 2,
                'full_name': 'Sarah Johnson',
                'employee_id': 'DRV002',
                'driver_type': 'Driver',
                'status': 'Available'
            },
            {
                'id': 3,
                'full_name': 'Mike Wilson',
                'employee_id': 'CON001',
                'driver_type': 'Conductor',
                'status': 'Available'
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'drivers': drivers
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/routes', methods=['GET'])
@jwt_required()
def get_routes():
    """Get all routes."""
    try:
        routes = Route.query.all()
        routes_data = []

        for route in routes:
            routes_data.append({
                'id': route.id,
                'route_name': route.route_name,
                'route_code': route.route_code,
                'start_location': route.start_location,
                'end_location': route.end_location,
                'status': route.status
            })

        return jsonify({
            'success': True,
            'data': {
                'routes': routes_data
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting Bus Management System...")
    print("📍 Backend running on: http://localhost:5000")
    print("🎯 API Health Check: http://localhost:5000/api/health")
    print("📚 Available endpoints:")
    print("   - POST /api/auth/login")
    print("   - GET  /api/auth/profile")
    print("   - GET  /api/buses")
    print("   - POST /api/buses")
    print("   - GET  /api/dashboard/stats")
    print("   - GET  /api/buses/<id>/documents")
    print("\n✨ Ready for frontend connection!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
