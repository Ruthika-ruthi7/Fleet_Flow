#!/usr/bin/env python3
"""
Ultra Simple Flask App - No SQLAlchemy, just basic endpoints
"""

import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# In-memory data storage (for demo purposes)
buses_data = [
    {
        'id': 1,
        'bus_number': 'BUS001',
        'registration_number': 'KA01AB1234',
        'bus_type': 'AC',
        'capacity': 50,
        'manufacturer': 'Tata',
        'model': 'Starbus',
        'status': 'Active',
        'occupancy_percentage': 75.0,
        'current_occupancy': 38,
        'driver_name': 'John Smith',
        'route_name': 'City Center to School',
        'is_insurance_expired': False,
        'is_rc_expired': False,
        'days_to_insurance_expiry': 180,
        'year_of_manufacture': 2020,
        'fuel_type': 'Diesel',
        'mileage': 8.5,
        'current_location': None,
        'last_location_update': None
    },
    {
        'id': 2,
        'bus_number': 'BUS002',
        'registration_number': 'KA01CD5678',
        'bus_type': 'Non-AC',
        'capacity': 45,
        'manufacturer': 'Ashok Leyland',
        'model': 'Viking',
        'status': 'Active',
        'occupancy_percentage': 60.0,
        'current_occupancy': 27,
        'driver_name': 'Sarah Johnson',
        'route_name': 'Suburb to College',
        'is_insurance_expired': False,
        'is_rc_expired': False,
        'days_to_insurance_expiry': 90,
        'year_of_manufacture': 2019,
        'fuel_type': 'Diesel',
        'mileage': 7.8,
        'current_location': None,
        'last_location_update': None
    },
    {
        'id': 3,
        'bus_number': 'BUS003',
        'registration_number': 'KA01EF9012',
        'bus_type': 'AC',
        'capacity': 55,
        'manufacturer': 'Volvo',
        'model': 'B7R',
        'status': 'Maintenance',
        'occupancy_percentage': 0.0,
        'current_occupancy': 0,
        'driver_name': 'Mike Wilson',
        'route_name': 'Downtown Express',
        'is_insurance_expired': False,
        'is_rc_expired': True,
        'days_to_insurance_expiry': 45,
        'year_of_manufacture': 2021,
        'fuel_type': 'Diesel',
        'mileage': 9.2,
        'current_location': None,
        'last_location_update': None
    }
]

users_data = [
    {
        'id': 1,
        'username': 'admin',
        'password': 'admin123',
        'email': 'admin@busmanagement.com',
        'role': 'admin',
        'first_name': 'System',
        'last_name': 'Administrator',
        'phone': '+1234567890'
    },
    {
        'id': 2,
        'username': 'driver1',
        'password': 'driver123',
        'email': 'driver@busmanagement.com',
        'role': 'driver',
        'first_name': 'John',
        'last_name': 'Smith',
        'phone': '+1234567891'
    },
    {
        'id': 3,
        'username': 'student1',
        'password': 'student123',
        'email': 'student@busmanagement.com',
        'role': 'student',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'phone': '+1234567892'
    }
]

routes_data = [
    {
        'id': 1,
        'route_name': 'City Center to School',
        'route_code': 'CC2SCH001',
        'start_location': 'City Center',
        'end_location': 'ABC School',
        'status': 'Active'
    },
    {
        'id': 2,
        'route_name': 'Suburb to College',
        'route_code': 'SUB2COL002',
        'start_location': 'Suburb Area',
        'end_location': 'XYZ College',
        'status': 'Active'
    }
]

drivers_data = [
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

# Current logged in user (for demo)
current_user = None

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Bus Management System API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test_endpoint():
    """Test endpoint for debugging frontend connection."""
    print(f"Test endpoint called with method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    if request.method == 'POST':
        print(f"Body: {request.get_json()}")

    return jsonify({
        'success': True,
        'message': 'Test endpoint working',
        'method': request.method,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Login endpoint."""
    global current_user

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'success': True})

    try:
        print(f"Login attempt - Method: {request.method}")
        print(f"Headers: {dict(request.headers)}")

        data = request.get_json()
        print(f"Login data received: {data}")

        username = data.get('username') if data else None
        password = data.get('password') if data else None

        if not username or not password:
            print("Missing username or password")
            return jsonify({'error': 'Username and password required'}), 400
        
        # Find user
        user = None
        for u in users_data:
            if u['username'] == username and u['password'] == password:
                user = u
                break
        
        if user:
            current_user = user
            # Generate simple tokens (in real app, use JWT)
            timestamp = datetime.now().timestamp()
            access_token = f"token_{user['id']}_{timestamp}"
            refresh_token = f"refresh_{user['id']}_{timestamp}"

            return jsonify({
                'success': True,
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'role': user['role'],
                        'first_name': user['first_name'],
                        'last_name': user['last_name']
                    },
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
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Get user profile."""
    try:
        if not current_user:
            return jsonify({'error': 'Not authenticated'}), 401
        
        return jsonify({
            'success': True,
            'data': {
                'profile': {
                    'id': current_user['id'],
                    'username': current_user['username'],
                    'email': current_user['email'],
                    'role': current_user['role'],
                    'first_name': current_user['first_name'],
                    'last_name': current_user['last_name'],
                    'phone': current_user['phone']
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/buses', methods=['GET'])
def get_buses():
    """Get all buses."""
    try:
        # Get query parameters
        status = request.args.get('status', '')
        bus_type = request.args.get('bus_type', '')
        search = request.args.get('search', '')

        # Filter buses
        filtered_buses = buses_data.copy()
        
        if status:
            filtered_buses = [b for b in filtered_buses if b['status'].lower() == status.lower()]
        if bus_type:
            filtered_buses = [b for b in filtered_buses if b['bus_type'].lower() == bus_type.lower()]
        if search:
            search_lower = search.lower()
            filtered_buses = [b for b in filtered_buses if 
                            search_lower in b['bus_number'].lower() or 
                            search_lower in b['registration_number'].lower() or 
                            search_lower in b['manufacturer'].lower()]

        return jsonify({
            'success': True,
            'data': {
                'buses': filtered_buses,
                'pagination': {
                    'total': len(filtered_buses),
                    'pages': 1,
                    'current_page': 1,
                    'per_page': len(filtered_buses),
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
def create_bus():
    """Create a new bus."""
    try:
        data = request.get_json()
        
        # Generate new ID
        new_id = max([b['id'] for b in buses_data]) + 1 if buses_data else 1
        
        # Generate bus number if not provided
        bus_number = data.get('bus_number') or f"BUS{new_id:03d}"
        
        new_bus = {
            'id': new_id,
            'bus_number': bus_number,
            'registration_number': data.get('registration_number'),
            'bus_type': data.get('bus_type'),
            'capacity': data.get('capacity'),
            'manufacturer': data.get('manufacturer'),
            'model': data.get('model'),
            'status': 'Active',
            'occupancy_percentage': 0.0,
            'current_occupancy': 0,
            'driver_name': 'Unassigned',
            'route_name': 'Unassigned',
            'is_insurance_expired': False,
            'is_rc_expired': False,
            'days_to_insurance_expiry': 365,
            'year_of_manufacture': data.get('year_of_manufacture', 2023),
            'fuel_type': data.get('fuel_type', 'Diesel'),
            'mileage': 8.0,
            'current_location': None,
            'last_location_update': None
        }
        
        buses_data.append(new_bus)
        
        return jsonify({
            'success': True,
            'data': {
                'bus': new_bus
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics."""
    try:
        # Calculate statistics from data
        total_buses = len(buses_data)
        active_buses = len([b for b in buses_data if b['status'] == 'Active'])
        total_drivers = len(drivers_data)
        total_routes = len(routes_data)

        stats = {
            'total_buses': total_buses,
            'total_drivers': total_drivers,
            'total_students': len([u for u in users_data if u['role'] == 'student']),
            'total_routes': total_routes,
            'active_buses': active_buses,
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
def get_bus_documents(bus_id):
    """Get documents for a bus."""
    try:
        bus = None
        for b in buses_data:
            if b['id'] == bus_id:
                bus = b
                break

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
                'bus_number': bus['bus_number'],
                'documents': documents
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    """Get available drivers."""
    try:
        return jsonify({
            'success': True,
            'data': {
                'drivers': drivers_data
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Get all routes."""
    try:
        return jsonify({
            'success': True,
            'data': {
                'routes': routes_data
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Additional endpoints for frontend compatibility
@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students."""
    try:
        students = [
            {
                'id': 1,
                'student_id': 'STU001',
                'name': 'Jane Doe',
                'email': 'jane@example.com',
                'phone': '+1234567892',
                'address': '123 Main St',
                'route_id': 1,
                'class_name': '10th Grade',
                'section': 'A'
            },
            {
                'id': 2,
                'student_id': 'STU002',
                'name': 'John Smith',
                'email': 'john@example.com',
                'phone': '+1234567893',
                'address': '456 Oak Ave',
                'route_id': 2,
                'class_name': '11th Grade',
                'section': 'B'
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'students': students
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Get all trips."""
    try:
        trips = [
            {
                'id': 1,
                'bus_id': 1,
                'route_id': 1,
                'driver_id': 1,
                'start_time': '2024-01-15T07:00:00',
                'end_time': '2024-01-15T08:00:00',
                'status': 'completed',
                'trip_type': 'morning'
            },
            {
                'id': 2,
                'bus_id': 2,
                'route_id': 2,
                'driver_id': 2,
                'start_time': '2024-01-15T15:00:00',
                'end_time': None,
                'status': 'in_progress',
                'trip_type': 'evening'
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'trips': trips
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/maintenance', methods=['GET'])
def get_maintenance():
    """Get all maintenance records."""
    try:
        # Get query parameters for filtering
        bus_id = request.args.get('bus_id')
        status = request.args.get('status')
        maintenance_type = request.args.get('maintenance_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Generate comprehensive maintenance data
        maintenance_records = []

        # Sample maintenance data for different buses and types
        maintenance_types = [
            'Regular Service', 'Oil Change', 'Brake Service', 'Engine Repair',
            'Transmission Service', 'AC Service', 'Tire Replacement', 'Battery Replacement',
            'Electrical Repair', 'Body Work', 'Interior Cleaning', 'Safety Inspection'
        ]

        statuses = ['completed', 'in_progress', 'scheduled', 'cancelled', 'pending_approval']

        from datetime import datetime, timedelta
        import random

        # Generate maintenance records for the last 6 months
        today = datetime.now()

        for record_id in range(1, 101):  # 100 maintenance records
            days_ago = random.randint(0, 180)  # Last 6 months
            maintenance_date = today - timedelta(days=days_ago)

            bus_id_val = random.randint(1, 5)  # 5 buses
            maintenance_type_val = random.choice(maintenance_types)
            status_val = random.choice(statuses)

            # Adjust status based on date (future dates should be scheduled)
            if maintenance_date > today:
                status_val = 'scheduled'
            elif days_ago < 7 and status_val in ['scheduled']:
                status_val = random.choice(['in_progress', 'completed'])

            # Generate realistic costs based on maintenance type
            base_costs = {
                'Regular Service': 5000,
                'Oil Change': 2000,
                'Brake Service': 8000,
                'Engine Repair': 25000,
                'Transmission Service': 15000,
                'AC Service': 6000,
                'Tire Replacement': 12000,
                'Battery Replacement': 4000,
                'Electrical Repair': 7000,
                'Body Work': 18000,
                'Interior Cleaning': 1500,
                'Safety Inspection': 1000
            }

            base_cost = base_costs.get(maintenance_type_val, 5000)
            actual_cost = base_cost + random.randint(-1000, 3000)

            # Generate next maintenance date
            next_maintenance_days = {
                'Regular Service': 90,
                'Oil Change': 30,
                'Brake Service': 180,
                'Engine Repair': 365,
                'Transmission Service': 365,
                'AC Service': 180,
                'Tire Replacement': 365,
                'Battery Replacement': 730,
                'Electrical Repair': 180,
                'Body Work': 365,
                'Interior Cleaning': 30,
                'Safety Inspection': 365
            }

            next_maintenance = maintenance_date + timedelta(days=next_maintenance_days.get(maintenance_type_val, 90))

            # Generate mechanic and vendor info
            mechanics = ['Rajesh Kumar', 'Amit Singh', 'Suresh Patel', 'Vikram Sharma', 'Ravi Gupta']
            vendors = ['City Auto Service', 'Express Motors', 'Prime Auto Care', 'Quick Fix Garage', 'Elite Motors']

            maintenance_records.append({
                'id': record_id,
                'bus_id': bus_id_val,
                'bus_number': f'BUS{bus_id_val:03d}',
                'bus_registration': f'KA01AB{1234 + bus_id_val}',
                'maintenance_type': maintenance_type_val,
                'category': 'Preventive' if maintenance_type_val in ['Regular Service', 'Oil Change', 'Safety Inspection'] else 'Corrective',
                'priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
                'description': f'{maintenance_type_val} for {f"BUS{bus_id_val:03d}"}',
                'detailed_description': f'Comprehensive {maintenance_type_val.lower()} including inspection of all related components and systems.',
                'cost': actual_cost,
                'estimated_cost': base_cost,
                'labor_cost': actual_cost * 0.4,
                'parts_cost': actual_cost * 0.6,
                'maintenance_date': maintenance_date.strftime('%Y-%m-%d'),
                'scheduled_date': maintenance_date.strftime('%Y-%m-%d'),
                'completion_date': maintenance_date.strftime('%Y-%m-%d') if status_val == 'completed' else None,
                'next_maintenance_date': next_maintenance.strftime('%Y-%m-%d'),
                'status': status_val,
                'mechanic_name': random.choice(mechanics),
                'vendor_name': random.choice(vendors),
                'vendor_contact': f'+91 {random.randint(7000000000, 9999999999)}',
                'work_order_number': f'WO{record_id:04d}',
                'invoice_number': f'INV{record_id:04d}' if status_val == 'completed' else None,
                'warranty_period': random.choice([30, 60, 90, 180]) if status_val == 'completed' else None,
                'parts_replaced': [
                    {'name': 'Engine Oil', 'quantity': 5, 'unit': 'liters'},
                    {'name': 'Oil Filter', 'quantity': 1, 'unit': 'piece'},
                    {'name': 'Air Filter', 'quantity': 1, 'unit': 'piece'}
                ] if maintenance_type_val == 'Oil Change' else [],
                'odometer_reading': random.randint(50000, 150000),
                'estimated_hours': random.randint(2, 8),
                'actual_hours': random.randint(2, 10) if status_val == 'completed' else None,
                'quality_rating': random.randint(3, 5) if status_val == 'completed' else None,
                'notes': f'Maintenance completed successfully. All systems functioning normally.' if status_val == 'completed' else 'Scheduled maintenance as per service plan.',
                'created_at': (maintenance_date - timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d'),
                'updated_at': maintenance_date.strftime('%Y-%m-%d'),
                'approved_by': 'Fleet Manager' if status_val != 'pending_approval' else None,
                'technician_notes': 'All checks completed as per standard procedure.' if status_val == 'completed' else None,
                'customer_feedback': random.choice(['Excellent', 'Good', 'Satisfactory']) if status_val == 'completed' and random.random() > 0.3 else None
            })

        # Apply filters
        filtered_maintenance = maintenance_records
        if bus_id:
            filtered_maintenance = [m for m in filtered_maintenance if m['bus_id'] == int(bus_id)]
        if status:
            filtered_maintenance = [m for m in filtered_maintenance if m['status'] == status]
        if maintenance_type:
            filtered_maintenance = [m for m in filtered_maintenance if m['maintenance_type'] == maintenance_type]
        if start_date:
            filtered_maintenance = [m for m in filtered_maintenance if m['maintenance_date'] >= start_date]
        if end_date:
            filtered_maintenance = [m for m in filtered_maintenance if m['maintenance_date'] <= end_date]

        # Sort by maintenance date (most recent first)
        filtered_maintenance.sort(key=lambda x: x['maintenance_date'], reverse=True)

        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        paginated_maintenance = filtered_maintenance[start_idx:end_idx]

        # Calculate summary statistics
        total_cost = sum([m['cost'] for m in filtered_maintenance])
        completed_count = len([m for m in filtered_maintenance if m['status'] == 'completed'])
        pending_count = len([m for m in filtered_maintenance if m['status'] in ['scheduled', 'in_progress', 'pending_approval']])

        return jsonify({
            'success': True,
            'data': {
                'maintenance': paginated_maintenance,
                'pagination': {
                    'total': len(filtered_maintenance),
                    'pages': (len(filtered_maintenance) + per_page - 1) // per_page,
                    'current_page': page,
                    'per_page': per_page,
                    'has_next': end_idx < len(filtered_maintenance),
                    'has_prev': page > 1
                },
                'summary': {
                    'total_records': len(filtered_maintenance),
                    'total_cost': total_cost,
                    'completed_count': completed_count,
                    'pending_count': pending_count,
                    'average_cost': round(total_cost / len(filtered_maintenance), 2) if filtered_maintenance else 0,
                    'maintenance_types': list(set([m['maintenance_type'] for m in filtered_maintenance])),
                    'buses_serviced': list(set([m['bus_number'] for m in filtered_maintenance]))
                }
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """Get all attendance records."""
    try:
        # Get query parameters for filtering
        date = request.args.get('date')
        student_id = request.args.get('student_id')
        route_id = request.args.get('route_id')
        status = request.args.get('status')

        # Generate comprehensive attendance data
        attendance = []

        # Sample data for the last 7 days
        from datetime import datetime, timedelta
        today = datetime.now()

        for day_offset in range(7):
            current_date = today - timedelta(days=day_offset)
            date_str = current_date.strftime('%Y-%m-%d')

            # Morning trip attendance
            for student_idx in range(1, 51):  # 50 students
                attendance_status = 'present' if (student_idx + day_offset) % 10 != 0 else 'absent'
                if (student_idx + day_offset) % 15 == 0:
                    attendance_status = 'late'

                attendance.append({
                    'id': len(attendance) + 1,
                    'student_id': student_idx,
                    'student_name': f'Student {student_idx:02d}',
                    'student_roll': f'STU{student_idx:03d}',
                    'class': f'Grade {10 + (student_idx % 3)}',
                    'route_id': 1 + (student_idx % 3),
                    'route_name': ['City Center Route', 'Suburb Route', 'Downtown Route'][student_idx % 3],
                    'trip_id': day_offset * 2 + 1,
                    'trip_type': 'morning',
                    'bus_number': f'BUS{1 + (student_idx % 3):03d}',
                    'driver_name': ['John Smith', 'Sarah Johnson', 'Mike Wilson'][student_idx % 3],
                    'status': attendance_status,
                    'timestamp': f'{date_str}T07:{15 + (student_idx % 30):02d}:00',
                    'boarding_location': ['Main Market', 'Park Avenue', 'City Center', 'School Gate'][student_idx % 4],
                    'boarding_time': f'{date_str}T07:{15 + (student_idx % 30):02d}:00',
                    'drop_location': 'ABC School',
                    'drop_time': f'{date_str}T08:{15 + (student_idx % 30):02d}:00' if attendance_status != 'absent' else None,
                    'attendance_method': 'qr_scan' if student_idx % 3 == 0 else 'manual',
                    'temperature': 98.6 + (student_idx % 3) * 0.2 if attendance_status == 'present' else None,
                    'parent_notified': attendance_status == 'absent',
                    'notes': 'Late due to traffic' if attendance_status == 'late' else None
                })

            # Evening trip attendance (only for present students)
            for student_idx in range(1, 51):
                if (student_idx + day_offset) % 10 != 0:  # Only students who were present in morning
                    attendance_status = 'present' if (student_idx + day_offset) % 12 != 0 else 'absent'

                    attendance.append({
                        'id': len(attendance) + 1,
                        'student_id': student_idx,
                        'student_name': f'Student {student_idx:02d}',
                        'student_roll': f'STU{student_idx:03d}',
                        'class': f'Grade {10 + (student_idx % 3)}',
                        'route_id': 1 + (student_idx % 3),
                        'route_name': ['City Center Route', 'Suburb Route', 'Downtown Route'][student_idx % 3],
                        'trip_id': day_offset * 2 + 2,
                        'trip_type': 'evening',
                        'bus_number': f'BUS{1 + (student_idx % 3):03d}',
                        'driver_name': ['John Smith', 'Sarah Johnson', 'Mike Wilson'][student_idx % 3],
                        'status': attendance_status,
                        'timestamp': f'{date_str}T15:{15 + (student_idx % 30):02d}:00',
                        'boarding_location': 'ABC School',
                        'boarding_time': f'{date_str}T15:{15 + (student_idx % 30):02d}:00',
                        'drop_location': ['Main Market', 'Park Avenue', 'City Center', 'School Gate'][student_idx % 4],
                        'drop_time': f'{date_str}T16:{15 + (student_idx % 30):02d}:00' if attendance_status != 'absent' else None,
                        'attendance_method': 'qr_scan' if student_idx % 3 == 0 else 'manual',
                        'temperature': None,  # Temperature not checked in evening
                        'parent_notified': attendance_status == 'absent',
                        'notes': None
                    })

        # Apply filters
        filtered_attendance = attendance
        if date:
            filtered_attendance = [a for a in filtered_attendance if a['timestamp'].startswith(date)]
        if student_id:
            filtered_attendance = [a for a in filtered_attendance if a['student_id'] == int(student_id)]
        if route_id:
            filtered_attendance = [a for a in filtered_attendance if a['route_id'] == int(route_id)]
        if status:
            filtered_attendance = [a for a in filtered_attendance if a['status'] == status]

        # Sort by timestamp (most recent first)
        filtered_attendance.sort(key=lambda x: x['timestamp'], reverse=True)

        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        paginated_attendance = filtered_attendance[start_idx:end_idx]

        return jsonify({
            'success': True,
            'data': {
                'attendance': paginated_attendance,
                'pagination': {
                    'total': len(filtered_attendance),
                    'pages': (len(filtered_attendance) + per_page - 1) // per_page,
                    'current_page': page,
                    'per_page': per_page,
                    'has_next': end_idx < len(filtered_attendance),
                    'has_prev': page > 1
                },
                'summary': {
                    'total_records': len(filtered_attendance),
                    'present_count': len([a for a in filtered_attendance if a['status'] == 'present']),
                    'absent_count': len([a for a in filtered_attendance if a['status'] == 'absent']),
                    'late_count': len([a for a in filtered_attendance if a['status'] == 'late']),
                    'attendance_rate': round(len([a for a in filtered_attendance if a['status'] in ['present', 'late']]) / len(filtered_attendance) * 100, 2) if filtered_attendance else 0
                }
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fees', methods=['GET'])
def get_fees():
    """Get all fee records."""
    try:
        fees = [
            {
                'id': 1,
                'student_id': 1,
                'amount': 2000.0,
                'month': 1,
                'year': 2024,
                'status': 'paid',
                'due_date': '2024-01-31',
                'paid_date': '2024-01-15'
            },
            {
                'id': 2,
                'student_id': 2,
                'amount': 2000.0,
                'month': 1,
                'year': 2024,
                'status': 'pending',
                'due_date': '2024-01-31',
                'paid_date': None
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'fees': fees
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Additional endpoints for specific modules

# Trip Management endpoints
@app.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip_by_id(trip_id):
    """Get a specific trip by ID."""
    try:
        # Mock trip data
        trip = {
            'id': trip_id,
            'bus_id': 1,
            'route_id': 1,
            'driver_id': 1,
            'start_time': '2024-01-15T07:00:00',
            'end_time': '2024-01-15T08:00:00',
            'status': 'completed',
            'trip_type': 'morning'
        }

        return jsonify({
            'success': True,
            'data': {
                'trip': trip
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trips', methods=['POST'])
def create_trip():
    """Create a new trip."""
    try:
        data = request.get_json()

        new_trip = {
            'id': 999,  # Mock ID
            'bus_id': data.get('bus_id'),
            'route_id': data.get('route_id'),
            'driver_id': data.get('driver_id'),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'status': 'scheduled',
            'trip_type': data.get('trip_type', 'morning')
        }

        return jsonify({
            'success': True,
            'data': {
                'trip': new_trip
            }
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trips/<int:trip_id>/start', methods=['POST'])
def start_trip(trip_id):
    """Start a trip."""
    try:
        return jsonify({
            'success': True,
            'data': {
                'trip_id': trip_id,
                'status': 'in_progress',
                'start_time': datetime.now().isoformat(),
                'message': 'Trip started successfully'
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trips/<int:trip_id>/end', methods=['POST'])
def end_trip(trip_id):
    """End a trip."""
    try:
        return jsonify({
            'success': True,
            'data': {
                'trip_id': trip_id,
                'status': 'completed',
                'end_time': datetime.now().isoformat(),
                'message': 'Trip completed successfully'
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Maintenance Management endpoints
@app.route('/api/maintenance/<int:maintenance_id>', methods=['GET'])
def get_maintenance_by_id(maintenance_id):
    """Get a specific maintenance record by ID."""
    try:
        maintenance = {
            'id': maintenance_id,
            'bus_id': 1,
            'maintenance_type': 'Regular Service',
            'description': 'Oil change and general inspection',
            'cost': 5000.0,
            'maintenance_date': '2024-01-10',
            'status': 'completed'
        }

        return jsonify({
            'success': True,
            'data': {
                'maintenance': maintenance
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/maintenance', methods=['POST'])
def create_maintenance():
    """Create a new maintenance record."""
    try:
        data = request.get_json()

        new_maintenance = {
            'id': 999,  # Mock ID
            'bus_id': data.get('bus_id'),
            'maintenance_type': data.get('maintenance_type'),
            'description': data.get('description'),
            'cost': data.get('cost'),
            'maintenance_date': data.get('maintenance_date'),
            'status': 'scheduled'
        }

        return jsonify({
            'success': True,
            'data': {
                'maintenance': new_maintenance
            }
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/maintenance/schedule', methods=['POST'])
def schedule_maintenance():
    """Schedule maintenance."""
    try:
        data = request.get_json()

        return jsonify({
            'success': True,
            'data': {
                'message': 'Maintenance scheduled successfully',
                'scheduled_date': data.get('scheduled_date'),
                'bus_id': data.get('bus_id')
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Attendance Management endpoints
@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """Mark attendance for a student."""
    try:
        data = request.get_json()

        return jsonify({
            'success': True,
            'data': {
                'message': 'Attendance marked successfully',
                'student_id': data.get('student_id'),
                'status': data.get('status'),
                'timestamp': datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/scan-qr', methods=['POST'])
def scan_qr_attendance():
    """Scan QR code for attendance."""
    try:
        data = request.get_json()

        return jsonify({
            'success': True,
            'data': {
                'message': 'QR code scanned successfully',
                'student_id': 1,
                'student_name': 'Jane Doe',
                'status': 'present',
                'timestamp': datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/bulk', methods=['GET'])
def get_bulk_attendance():
    """Get bulk attendance data."""
    try:
        bulk_attendance = [
            {
                'date': '2024-01-15',
                'total_students': 50,
                'present': 45,
                'absent': 5,
                'attendance_rate': 90.0
            },
            {
                'date': '2024-01-14',
                'total_students': 50,
                'present': 48,
                'absent': 2,
                'attendance_rate': 96.0
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'bulk_attendance': bulk_attendance
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/attendance/report', methods=['GET'])
def get_attendance_report():
    """Get attendance report."""
    try:
        report = {
            'summary': {
                'total_students': 100,
                'average_attendance': 92.5,
                'total_days': 30,
                'best_day': '2024-01-10',
                'worst_day': '2024-01-05'
            },
            'daily_stats': [
                {
                    'date': '2024-01-15',
                    'present': 95,
                    'absent': 5,
                    'rate': 95.0
                },
                {
                    'date': '2024-01-14',
                    'present': 90,
                    'absent': 10,
                    'rate': 90.0
                }
            ]
        }

        return jsonify({
            'success': True,
            'data': report
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Reports endpoints
@app.route('/api/reports/attendance', methods=['GET'])
def get_attendance_reports():
    """Get attendance reports."""
    try:
        reports = {
            'monthly_summary': {
                'total_students': 100,
                'average_attendance': 92.5,
                'total_school_days': 22,
                'highest_attendance_day': '2024-01-15',
                'lowest_attendance_day': '2024-01-08'
            },
            'class_wise': [
                {
                    'class': '10th Grade A',
                    'total_students': 30,
                    'average_attendance': 95.0
                },
                {
                    'class': '10th Grade B',
                    'total_students': 25,
                    'average_attendance': 88.0
                }
            ],
            'route_wise': [
                {
                    'route': 'City Center to School',
                    'total_students': 40,
                    'average_attendance': 93.0
                },
                {
                    'route': 'Suburb to College',
                    'total_students': 35,
                    'average_attendance': 91.0
                }
            ]
        }

        return jsonify({
            'success': True,
            'data': reports
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/buses', methods=['GET'])
def get_bus_reports():
    """Get bus reports."""
    try:
        reports = {
            'utilization': [
                {
                    'bus_number': 'BUS001',
                    'total_trips': 44,
                    'average_occupancy': 75.0,
                    'fuel_efficiency': 8.5
                },
                {
                    'bus_number': 'BUS002',
                    'total_trips': 40,
                    'average_occupancy': 60.0,
                    'fuel_efficiency': 7.8
                }
            ],
            'maintenance_summary': {
                'total_maintenance_cost': 50000,
                'scheduled_maintenance': 5,
                'emergency_repairs': 2,
                'average_downtime': 2.5
            }
        }

        return jsonify({
            'success': True,
            'data': reports
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/financial', methods=['GET'])
def get_financial_reports():
    """Get financial reports."""
    try:
        reports = {
            'fee_collection': {
                'total_fees_due': 200000,
                'total_collected': 180000,
                'collection_rate': 90.0,
                'pending_amount': 20000,
                'overdue_amount': 15000,
                'advance_payments': 5000
            },
            'expenses': {
                'fuel_cost': 50000,
                'maintenance_cost': 30000,
                'driver_salary': 80000,
                'insurance': 25000,
                'permits_licenses': 5000,
                'total_expenses': 190000
            },
            'monthly_breakdown': [
                {
                    'month': 'January 2024',
                    'income': 180000,
                    'expenses': 160000,
                    'profit': 20000,
                    'profit_margin': 11.1
                },
                {
                    'month': 'December 2023',
                    'income': 175000,
                    'expenses': 155000,
                    'profit': 20000,
                    'profit_margin': 11.4
                }
            ],
            'yearly_summary': {
                'total_income': 2100000,
                'total_expenses': 1890000,
                'net_profit': 210000,
                'average_monthly_profit': 17500,
                'best_month': 'September 2023',
                'worst_month': 'June 2023'
            }
        }

        return jsonify({
            'success': True,
            'data': reports
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/performance', methods=['GET'])
def get_performance_reports():
    """Get performance analysis reports."""
    try:
        reports = {
            'driver_performance': [
                {
                    'driver_id': 1,
                    'driver_name': 'John Smith',
                    'total_trips': 220,
                    'on_time_percentage': 95.5,
                    'fuel_efficiency': 8.5,
                    'safety_score': 98,
                    'student_feedback': 4.8,
                    'incidents': 0
                },
                {
                    'driver_id': 2,
                    'driver_name': 'Sarah Johnson',
                    'total_trips': 200,
                    'on_time_percentage': 92.0,
                    'fuel_efficiency': 7.8,
                    'safety_score': 96,
                    'student_feedback': 4.6,
                    'incidents': 1
                }
            ],
            'route_efficiency': [
                {
                    'route_id': 1,
                    'route_name': 'City Center to School',
                    'average_trip_time': 45,
                    'scheduled_time': 50,
                    'efficiency_score': 90,
                    'fuel_consumption': 12.5,
                    'student_capacity_utilization': 85,
                    'delay_frequency': 5
                },
                {
                    'route_id': 2,
                    'route_name': 'Suburb to College',
                    'average_trip_time': 38,
                    'scheduled_time': 40,
                    'efficiency_score': 95,
                    'fuel_consumption': 10.2,
                    'student_capacity_utilization': 78,
                    'delay_frequency': 3
                }
            ],
            'bus_utilization': [
                {
                    'bus_id': 1,
                    'bus_number': 'BUS001',
                    'total_distance': 15500,
                    'total_trips': 220,
                    'average_occupancy': 75,
                    'fuel_efficiency': 8.5,
                    'maintenance_cost': 25000,
                    'downtime_hours': 48,
                    'revenue_per_km': 12.5
                },
                {
                    'bus_id': 2,
                    'bus_number': 'BUS002',
                    'total_distance': 14200,
                    'total_trips': 200,
                    'average_occupancy': 68,
                    'fuel_efficiency': 7.8,
                    'maintenance_cost': 22000,
                    'downtime_hours': 36,
                    'revenue_per_km': 11.8
                }
            ]
        }

        return jsonify({
            'success': True,
            'data': reports
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/analytics', methods=['GET'])
def get_analytics_reports():
    """Get advanced analytics and insights."""
    try:
        reports = {
            'trends': {
                'attendance_trend': {
                    'current_month': 92.5,
                    'previous_month': 89.2,
                    'trend': 'increasing',
                    'change_percentage': 3.7
                },
                'fuel_efficiency_trend': {
                    'current_month': 8.2,
                    'previous_month': 7.9,
                    'trend': 'improving',
                    'change_percentage': 3.8
                },
                'on_time_performance': {
                    'current_month': 94.5,
                    'previous_month': 91.8,
                    'trend': 'improving',
                    'change_percentage': 2.9
                }
            },
            'predictions': {
                'next_month_attendance': 94.2,
                'maintenance_alerts': [
                    {
                        'bus_id': 3,
                        'bus_number': 'BUS003',
                        'predicted_maintenance_date': '2024-02-15',
                        'type': 'Engine Service',
                        'confidence': 85
                    }
                ],
                'fuel_cost_forecast': {
                    'next_month': 52000,
                    'confidence': 78,
                    'factors': ['fuel_price_increase', 'route_expansion']
                }
            },
            'insights': [
                {
                    'category': 'efficiency',
                    'title': 'Route Optimization Opportunity',
                    'description': 'Route 2 shows 15% better fuel efficiency. Consider applying similar optimization to Route 1.',
                    'impact': 'high',
                    'potential_savings': 8500
                },
                {
                    'category': 'maintenance',
                    'title': 'Preventive Maintenance Success',
                    'description': 'Buses with regular maintenance show 25% less downtime.',
                    'impact': 'medium',
                    'potential_savings': 12000
                },
                {
                    'category': 'attendance',
                    'title': 'Weather Impact Analysis',
                    'description': 'Attendance drops by 8% during rainy days. Consider weather-based notifications.',
                    'impact': 'low',
                    'potential_improvement': '5% attendance increase'
                }
            ],
            'benchmarks': {
                'industry_average_attendance': 88.5,
                'our_attendance': 92.5,
                'industry_fuel_efficiency': 7.2,
                'our_fuel_efficiency': 8.2,
                'industry_on_time': 89.0,
                'our_on_time': 94.5
            }
        }

        return jsonify({
            'success': True,
            'data': reports
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reports/safety', methods=['GET'])
def get_safety_reports():
    """Get safety analysis reports."""
    try:
        reports = {
            'incident_summary': {
                'total_incidents': 3,
                'minor_incidents': 2,
                'major_incidents': 1,
                'incidents_per_1000_trips': 1.2,
                'days_since_last_incident': 45
            },
            'safety_metrics': {
                'average_safety_score': 96.8,
                'driver_safety_training_completion': 100,
                'vehicle_safety_inspections_passed': 98.5,
                'emergency_drill_participation': 95.0
            },
            'incident_details': [
                {
                    'date': '2024-01-10',
                    'type': 'Minor Accident',
                    'bus_number': 'BUS002',
                    'driver': 'Sarah Johnson',
                    'description': 'Minor fender bender in parking lot',
                    'injuries': 0,
                    'cost': 2500,
                    'status': 'resolved'
                },
                {
                    'date': '2023-12-15',
                    'type': 'Breakdown',
                    'bus_number': 'BUS003',
                    'driver': 'Mike Wilson',
                    'description': 'Engine overheating',
                    'injuries': 0,
                    'cost': 5000,
                    'status': 'resolved'
                }
            ],
            'safety_recommendations': [
                'Increase frequency of vehicle inspections',
                'Implement advanced driver assistance systems',
                'Conduct monthly safety training sessions',
                'Install GPS tracking for all vehicles'
            ]
        }

        return jsonify({
            'success': True,
            'data': reports
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Additional CRUD endpoints for students, drivers, routes
@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student."""
    try:
        data = request.get_json()

        new_student = {
            'id': 999,  # Mock ID
            'student_id': data.get('student_id', 'STU999'),
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'address': data.get('address'),
            'route_id': data.get('route_id'),
            'class_name': data.get('class_name'),
            'section': data.get('section')
        }

        return jsonify({
            'success': True,
            'data': {
                'student': new_student
            }
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    """Get a specific student by ID."""
    try:
        student = {
            'id': student_id,
            'student_id': f'STU{student_id:03d}',
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '+1234567892',
            'address': '123 Main St',
            'route_id': 1,
            'class_name': '10th Grade',
            'section': 'A'
        }

        return jsonify({
            'success': True,
            'data': {
                'student': student
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/drivers', methods=['POST'])
def create_driver():
    """Create a new driver."""
    try:
        data = request.get_json()

        new_driver = {
            'id': 999,  # Mock ID
            'full_name': data.get('full_name'),
            'employee_id': data.get('employee_id', 'DRV999'),
            'driver_type': data.get('driver_type', 'Driver'),
            'status': 'Available',
            'phone': data.get('phone'),
            'license_number': data.get('license_number')
        }

        return jsonify({
            'success': True,
            'data': {
                'driver': new_driver
            }
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/routes', methods=['POST'])
def create_route():
    """Create a new route."""
    try:
        data = request.get_json()

        new_route = {
            'id': 999,  # Mock ID
            'route_name': data.get('route_name'),
            'route_code': data.get('route_code', 'RT999'),
            'start_location': data.get('start_location'),
            'end_location': data.get('end_location'),
            'status': 'Active'
        }

        return jsonify({
            'success': True,
            'data': {
                'route': new_route
            }
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Tracking endpoints
@app.route('/api/tracking/live', methods=['GET'])
def get_all_live_locations():
    """Get all live bus locations."""
    try:
        locations = [
            {
                'bus_id': 1,
                'bus_number': 'BUS001',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'speed': 25.5,
                'heading': 45.0,
                'timestamp': datetime.now().isoformat()
            },
            {
                'bus_id': 2,
                'bus_number': 'BUS002',
                'latitude': 12.9716,
                'longitude': 77.5946,
                'speed': 30.0,
                'heading': 90.0,
                'timestamp': datetime.now().isoformat()
            }
        ]

        return jsonify({
            'success': True,
            'data': {
                'locations': locations
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tracking/live/<int:bus_id>', methods=['GET'])
def get_live_location(bus_id):
    """Get live location for a specific bus."""
    try:
        location = {
            'bus_id': bus_id,
            'bus_number': f'BUS{bus_id:03d}',
            'latitude': 12.9716,
            'longitude': 77.5946,
            'speed': 25.5,
            'heading': 45.0,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify({
            'success': True,
            'data': location
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Ultra Simple Bus Management System...")
    print("📍 Backend running on: http://localhost:5000")
    print("🎯 API Health Check: http://localhost:5000/api/health")
    print("📚 Available endpoints:")
    print("   - GET  /api/health")
    print("   - POST /api/auth/login")
    print("   - GET  /api/auth/profile")
    print("   - GET  /api/buses")
    print("   - POST /api/buses")
    print("   - GET  /api/dashboard/stats")
    print("   - GET  /api/buses/<id>/documents")
    print("   - GET  /api/drivers")
    print("   - GET  /api/routes")
    print("   - GET  /api/students")
    print("   - GET  /api/trips")
    print("   - GET  /api/maintenance")
    print("   - GET  /api/attendance")
    print("   - GET  /api/fees")
    print("\n✨ Ready for frontend connection!")
    print("🔑 Demo login: admin / admin123")
    print("🌐 CORS enabled for: http://localhost:3000")

    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
