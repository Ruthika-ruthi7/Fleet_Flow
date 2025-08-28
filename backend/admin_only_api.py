#!/usr/bin/env python3
"""
Complete Admin-Only Transport Management System API
Full functionality for admin users with comprehensive data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta, datetime, date
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin-transport-secret-key'
app.config['JWT_SECRET_KEY'] = 'admin-transport-jwt-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)
CORS(app, origins=['http://localhost:3000'])

# Admin user only
ADMIN_USER = {
    'id': 1,
    'username': 'admin',
    'email': 'admin@transport.com',
    'password_hash': generate_password_hash('admin123'),
    'role': 'admin',
    'first_name': 'Transport',
    'last_name': 'Administrator',
    'phone': '+1234567890'
}

# Comprehensive transport data
BUSES = [
    {
        'id': 1, 'bus_number': 'TRP001', 'registration_number': 'KA01AB1234',
        'bus_type': 'AC', 'capacity': 45, 'manufacturer': 'Tata', 'model': 'Starbus',
        'year_of_manufacture': 2020, 'fuel_type': 'Diesel', 'mileage': 8.5,
        'status': 'Active', 'occupancy_percentage': 85.0, 'current_occupancy': 38,
        'driver_name': 'John Smith', 'conductor_name': 'Mike Wilson',
        'route_name': 'City Center → School District', 'route_id': 1,
        'is_insurance_expired': False, 'is_rc_expired': False,
        'days_to_insurance_expiry': 180, 'insurance_number': 'INS001234',
        'rc_number': 'RC001234', 'current_location_lat': 12.9716,
        'current_location_lng': 77.5946, 'last_maintenance': '2024-01-15',
        'current_stop': 'City Center Bus Terminal', 'next_stop': 'Mall Junction',
        'eta_next_stop': 8, 'total_stops_remaining': 6, 'speed': 35
    },
    {
        'id': 2, 'bus_number': 'TRP002', 'registration_number': 'KA01CD5678',
        'bus_type': 'Non-AC', 'capacity': 50, 'manufacturer': 'Ashok Leyland', 'model': 'Viking',
        'year_of_manufacture': 2019, 'fuel_type': 'Diesel', 'mileage': 7.2,
        'status': 'Active', 'occupancy_percentage': 72.0, 'current_occupancy': 36,
        'driver_name': 'Sarah Johnson', 'conductor_name': 'Lisa Brown',
        'route_name': 'Residential Area → College Campus', 'route_id': 2,
        'is_insurance_expired': False, 'is_rc_expired': False,
        'days_to_insurance_expiry': 90, 'insurance_number': 'INS005678',
        'rc_number': 'RC005678', 'current_location_lat': 12.9352,
        'current_location_lng': 77.6245, 'last_maintenance': '2024-02-01',
        'current_stop': 'Sunrise Apartments', 'next_stop': 'Tech University Gate',
        'eta_next_stop': 12, 'total_stops_remaining': 8, 'speed': 28
    },
    {
        'id': 3, 'bus_number': 'TRP003', 'registration_number': 'KA01EF9012',
        'bus_type': 'AC', 'capacity': 40, 'manufacturer': 'Mahindra', 'model': 'Tourister',
        'year_of_manufacture': 2021, 'fuel_type': 'CNG', 'mileage': 12.0,
        'status': 'Maintenance', 'occupancy_percentage': 0.0, 'current_occupancy': 0,
        'driver_name': None, 'conductor_name': None,
        'route_name': None, 'route_id': None,
        'is_insurance_expired': False, 'is_rc_expired': False,
        'days_to_insurance_expiry': 200, 'insurance_number': 'INS009012',
        'rc_number': 'RC009012', 'current_location_lat': None,
        'current_location_lng': None, 'last_maintenance': '2024-01-20',
        'current_stop': 'Maintenance Depot', 'next_stop': None,
        'eta_next_stop': None, 'total_stops_remaining': 0, 'speed': 0
    },
    {
        'id': 4, 'bus_number': 'TRP004', 'registration_number': 'KA01GH3456',
        'bus_type': 'Non-AC', 'capacity': 55, 'manufacturer': 'Eicher', 'model': 'Skyline',
        'year_of_manufacture': 2018, 'fuel_type': 'Diesel', 'mileage': 6.8,
        'status': 'Active', 'occupancy_percentage': 90.0, 'current_occupancy': 50,
        'driver_name': 'Robert Davis', 'conductor_name': 'Anna Wilson',
        'route_name': 'Industrial Area → Tech Park', 'route_id': 3,
        'is_insurance_expired': True, 'is_rc_expired': False,
        'days_to_insurance_expiry': -15, 'insurance_number': 'INS003456',
        'rc_number': 'RC003456', 'current_location_lat': 12.8456,
        'current_location_lng': 77.6632, 'last_maintenance': '2024-01-10',
        'current_stop': 'Industrial Complex Gate', 'next_stop': 'Software Tech Park',
        'eta_next_stop': 15, 'total_stops_remaining': 4, 'speed': 42
    },
    {
        'id': 5, 'bus_number': 'TRP005', 'registration_number': 'KA01IJ7890',
        'bus_type': 'Electric', 'capacity': 35, 'manufacturer': 'BYD', 'model': 'K7M',
        'year_of_manufacture': 2022, 'fuel_type': 'Electric', 'mileage': 0.8,
        'status': 'Active', 'occupancy_percentage': 65.0, 'current_occupancy': 23,
        'driver_name': 'Emily Chen', 'conductor_name': 'David Kumar',
        'route_name': 'Metro Station → Airport', 'route_id': 4,
        'is_insurance_expired': False, 'is_rc_expired': False,
        'days_to_insurance_expiry': 300, 'insurance_number': 'INS007890',
        'rc_number': 'RC007890', 'current_location_lat': 13.1986,
        'current_location_lng': 77.7066, 'last_maintenance': '2024-02-10',
        'current_stop': 'Central Metro Station', 'next_stop': 'International Airport',
        'eta_next_stop': 25, 'total_stops_remaining': 2, 'speed': 55
    }
]

DRIVERS = [
    {
        'id': 1, 'employee_id': 'DRV001', 'full_name': 'John Smith',
        'driver_type': 'Driver', 'license_number': 'DL123456789',
        'license_expiry': '2025-12-31', 'phone': '+1234567891',
        'status': 'Available', 'shift_type': 'Morning', 'rating': 4.8,
        'experience_years': 8, 'assigned_bus': 'TRP001'
    },
    {
        'id': 2, 'employee_id': 'DRV002', 'full_name': 'Sarah Johnson',
        'driver_type': 'Driver', 'license_number': 'DL987654321',
        'license_expiry': '2025-08-15', 'phone': '+1234567892',
        'status': 'On Trip', 'shift_type': 'Evening', 'rating': 4.6,
        'experience_years': 5, 'assigned_bus': 'TRP002'
    },
    {
        'id': 3, 'employee_id': 'CON001', 'full_name': 'Mike Wilson',
        'driver_type': 'Conductor', 'license_number': 'DL456789123',
        'license_expiry': '2024-10-20', 'phone': '+1234567893',
        'status': 'Available', 'shift_type': 'Full Day', 'rating': 4.7,
        'experience_years': 3, 'assigned_bus': 'TRP001'
    },
    {
        'id': 4, 'employee_id': 'DRV003', 'full_name': 'Robert Davis',
        'driver_type': 'Driver', 'license_number': 'DL789123456',
        'license_expiry': '2025-06-30', 'phone': '+1234567894',
        'status': 'On Trip', 'shift_type': 'Morning', 'rating': 4.9,
        'experience_years': 12, 'assigned_bus': 'TRP004'
    },
    {
        'id': 5, 'employee_id': 'DRV004', 'full_name': 'Emily Chen',
        'driver_type': 'Driver', 'license_number': 'DL321654987',
        'license_expiry': '2026-03-15', 'phone': '+1234567895',
        'status': 'Available', 'shift_type': 'Evening', 'rating': 4.5,
        'experience_years': 4, 'assigned_bus': 'TRP005'
    }
]

ROUTES = [
    {
        'id': 1, 'route_name': 'City Center to School District', 'route_code': 'CC-SD-01',
        'start_location': 'City Center Bus Terminal', 'end_location': 'Green Valley School',
        'total_distance': 15.5, 'estimated_duration': 45, 'route_type': 'Urban',
        'status': 'Active', 'stops_count': 8, 'daily_trips': 6
    },
    {
        'id': 2, 'route_name': 'Residential Area to College Campus', 'route_code': 'RA-CC-02',
        'start_location': 'Sunrise Apartments', 'end_location': 'Tech University',
        'total_distance': 22.3, 'estimated_duration': 60, 'route_type': 'Suburban',
        'status': 'Active', 'stops_count': 12, 'daily_trips': 8
    },
    {
        'id': 3, 'route_name': 'Industrial Area to Tech Park', 'route_code': 'IA-TP-03',
        'start_location': 'Industrial Complex Gate', 'end_location': 'Software Tech Park',
        'total_distance': 18.7, 'estimated_duration': 50, 'route_type': 'Express',
        'status': 'Active', 'stops_count': 6, 'daily_trips': 10
    },
    {
        'id': 4, 'route_name': 'Metro Station to Airport', 'route_code': 'MS-AP-04',
        'start_location': 'Central Metro Station', 'end_location': 'International Airport',
        'total_distance': 35.2, 'estimated_duration': 75, 'route_type': 'Express',
        'status': 'Active', 'stops_count': 4, 'daily_trips': 12
    }
]

STUDENTS = [
    {
        'id': 1, 'student_id': 'STU001', 'full_name': 'Alice Brown',
        'class_name': 'Grade 10', 'section': 'A', 'roll_number': '101',
        'parent_name': 'Robert Brown', 'parent_phone': '+1234567896',
        'route_id': 1, 'pickup_stop': 'City Center', 'drop_stop': 'School Gate',
        'base_monthly_fee': 2000, 'scholarship_type': 'Merit', 'scholarship_percentage': 25,
        'final_monthly_fee': 1500, 'status': 'Active', 'attendance_percentage': 95,
        'family_income': 45000, 'academic_score': 92
    },
    {
        'id': 2, 'student_id': 'STU002', 'full_name': 'Bob Davis',
        'class_name': 'Grade 11', 'section': 'B', 'roll_number': '205',
        'parent_name': 'Linda Davis', 'parent_phone': '+1234567897',
        'route_id': 2, 'pickup_stop': 'Sunrise Apartments', 'drop_stop': 'University Gate',
        'base_monthly_fee': 2200, 'scholarship_type': 'Need-based', 'scholarship_percentage': 40,
        'final_monthly_fee': 1320, 'status': 'Active', 'attendance_percentage': 88,
        'family_income': 25000, 'academic_score': 78
    },
    {
        'id': 3, 'student_id': 'STU003', 'full_name': 'Carol Wilson',
        'class_name': 'Grade 9', 'section': 'C', 'roll_number': '315',
        'parent_name': 'James Wilson', 'parent_phone': '+1234567898',
        'route_id': 3, 'pickup_stop': 'Industrial Gate', 'drop_stop': 'Tech Park',
        'base_monthly_fee': 1800, 'scholarship_type': 'Sports', 'scholarship_percentage': 50,
        'final_monthly_fee': 900, 'status': 'Active', 'attendance_percentage': 97,
        'family_income': 35000, 'academic_score': 85
    },
    {
        'id': 4, 'student_id': 'STU004', 'full_name': 'David Kumar',
        'class_name': 'Grade 12', 'section': 'A', 'roll_number': '120',
        'parent_name': 'Raj Kumar', 'parent_phone': '+1234567899',
        'route_id': 4, 'pickup_stop': 'Metro Station', 'drop_stop': 'Airport',
        'base_monthly_fee': 2500, 'scholarship_type': None, 'scholarship_percentage': 0,
        'final_monthly_fee': 2500, 'status': 'Active', 'attendance_percentage': 91,
        'family_income': 75000, 'academic_score': 88
    },
    {
        'id': 5, 'student_id': 'STU005', 'full_name': 'Emma Thompson',
        'class_name': 'Grade 10', 'section': 'B', 'roll_number': '210',
        'parent_name': 'Sarah Thompson', 'parent_phone': '+1234567800',
        'route_id': 1, 'pickup_stop': 'City Center', 'drop_stop': 'School Gate',
        'base_monthly_fee': 2000, 'scholarship_type': 'Sibling', 'scholarship_percentage': 15,
        'final_monthly_fee': 1700, 'status': 'Active', 'attendance_percentage': 93,
        'family_income': 55000, 'academic_score': 89
    }
]

# Scholarship criteria and rules
SCHOLARSHIP_TYPES = [
    {
        'type': 'Merit',
        'description': 'Academic excellence scholarship',
        'criteria': 'Academic score >= 90%',
        'percentage_range': [20, 30],
        'max_income': 60000
    },
    {
        'type': 'Need-based',
        'description': 'Financial assistance for low-income families',
        'criteria': 'Family income < 30,000',
        'percentage_range': [30, 50],
        'max_income': 30000
    },
    {
        'type': 'Sports',
        'description': 'Athletic achievement scholarship',
        'criteria': 'Sports excellence + attendance >= 95%',
        'percentage_range': [25, 50],
        'max_income': 50000
    },
    {
        'type': 'Sibling',
        'description': 'Multiple children from same family',
        'criteria': 'Second child onwards',
        'percentage_range': [10, 20],
        'max_income': 70000
    },
    {
        'type': 'Single Parent',
        'description': 'Support for single-parent families',
        'criteria': 'Single parent household',
        'percentage_range': [20, 35],
        'max_income': 40000
    }
]

# API Endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Transport Management System API'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == 'admin' and check_password_hash(ADMIN_USER['password_hash'], password):
            access_token = create_access_token(identity=ADMIN_USER['id'])
            return jsonify({
                'success': True,
                'data': {
                    'access_token': access_token,
                    'user': {
                        'id': ADMIN_USER['id'],
                        'username': ADMIN_USER['username'],
                        'email': ADMIN_USER['email'],
                        'role': ADMIN_USER['role'],
                        'first_name': ADMIN_USER['first_name'],
                        'last_name': ADMIN_USER['last_name']
                    }
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials. Only admin access available.'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    return jsonify({
        'success': True,
        'data': {
            'profile': {
                'id': ADMIN_USER['id'],
                'username': ADMIN_USER['username'],
                'email': ADMIN_USER['email'],
                'role': ADMIN_USER['role'],
                'first_name': ADMIN_USER['first_name'],
                'last_name': ADMIN_USER['last_name'],
                'phone': ADMIN_USER['phone']
            }
        }
    })

@app.route('/api/buses', methods=['GET'])
@jwt_required()
def get_buses():
    try:
        # Get filters
        status = request.args.get('status', '')
        bus_type = request.args.get('bus_type', '')
        search = request.args.get('search', '')

        filtered_buses = BUSES.copy()

        if status:
            filtered_buses = [b for b in filtered_buses if b['status'] == status]
        if bus_type:
            filtered_buses = [b for b in filtered_buses if b['bus_type'] == bus_type]
        if search:
            search_lower = search.lower()
            filtered_buses = [b for b in filtered_buses if
                            search_lower in b['bus_number'].lower() or
                            search_lower in b['registration_number'].lower()]

        # Ensure all required fields are present
        for bus in filtered_buses:
            if 'current_location_lat' not in bus:
                bus['current_location_lat'] = None
            if 'current_location_lng' not in bus:
                bus['current_location_lng'] = None
            if 'last_maintenance' not in bus:
                bus['last_maintenance'] = '2024-01-15'

        return jsonify({
            'success': True,
            'data': {
                'buses': filtered_buses,
                'pagination': {
                    'total': len(filtered_buses),
                    'pages': 1,
                    'current_page': 1,
                    'per_page': 10,
                    'has_next': False,
                    'has_prev': False
                }
            }
        })
    except Exception as e:
        print(f"Error in get_buses: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/buses', methods=['POST'])
@jwt_required()
def create_bus():
    try:
        data = request.get_json()
        new_id = max([b['id'] for b in BUSES]) + 1
        
        new_bus = {
            'id': new_id,
            'bus_number': data.get('bus_number', f'TRP{new_id:03d}'),
            'registration_number': data.get('registration_number'),
            'bus_type': data.get('bus_type'),
            'capacity': data.get('capacity'),
            'manufacturer': data.get('manufacturer'),
            'model': data.get('model'),
            'year_of_manufacture': data.get('year_of_manufacture'),
            'fuel_type': data.get('fuel_type'),
            'mileage': data.get('mileage'),
            'status': 'Active',
            'occupancy_percentage': 0.0,
            'current_occupancy': 0,
            'driver_name': None,
            'conductor_name': None,
            'route_name': None,
            'route_id': None,
            'is_insurance_expired': False,
            'is_rc_expired': False,
            'days_to_insurance_expiry': 365,
            'insurance_number': data.get('insurance_number'),
            'rc_number': data.get('rc_number'),
            'current_location_lat': None,
            'current_location_lng': None,
            'last_maintenance': datetime.now().strftime('%Y-%m-%d')
        }
        
        BUSES.append(new_bus)
        
        return jsonify({
            'success': True,
            'data': {'bus': new_bus}
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    active_buses = len([b for b in BUSES if b['status'] == 'Active'])
    maintenance_buses = len([b for b in BUSES if b['status'] == 'Maintenance'])
    
    return jsonify({
        'success': True,
        'data': {
            'total_buses': len(BUSES),
            'active_buses': active_buses,
            'maintenance_buses': maintenance_buses,
            'total_drivers': len(DRIVERS),
            'total_students': len(STUDENTS),
            'total_routes': len(ROUTES),
            'daily_trips': sum([r['daily_trips'] for r in ROUTES]),
            'average_occupancy': sum([b['occupancy_percentage'] for b in BUSES if b['status'] == 'Active']) / active_buses if active_buses > 0 else 0,
            'expired_documents': len([b for b in BUSES if b['is_insurance_expired'] or b['is_rc_expired']]),
            'revenue_today': 15000,
            'fuel_consumption': 450
        }
    })

# Additional endpoints for complete functionality
@app.route('/api/drivers', methods=['GET'])
@jwt_required()
def get_drivers():
    return jsonify({'success': True, 'data': {'drivers': DRIVERS}})

@app.route('/api/routes', methods=['GET'])
@jwt_required()
def get_routes():
    return jsonify({'success': True, 'data': {'routes': ROUTES}})

@app.route('/api/students', methods=['GET'])
@jwt_required()
def get_students():
    try:
        # Calculate total savings from scholarships
        total_base_fees = sum([s['base_monthly_fee'] for s in STUDENTS])
        total_final_fees = sum([s['final_monthly_fee'] for s in STUDENTS])
        total_scholarship_savings = total_base_fees - total_final_fees

        return jsonify({
            'success': True,
            'data': {
                'students': STUDENTS,
                'summary': {
                    'total_students': len(STUDENTS),
                    'scholarship_recipients': len([s for s in STUDENTS if s['scholarship_type']]),
                    'total_base_fees': total_base_fees,
                    'total_final_fees': total_final_fees,
                    'total_scholarship_savings': total_scholarship_savings,
                    'average_scholarship_percentage': sum([s['scholarship_percentage'] for s in STUDENTS if s['scholarship_type']]) / len([s for s in STUDENTS if s['scholarship_type']]) if [s for s in STUDENTS if s['scholarship_type']] else 0
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scholarships', methods=['GET'])
@jwt_required()
def get_scholarships():
    return jsonify({'success': True, 'data': {'scholarship_types': SCHOLARSHIP_TYPES}})

@app.route('/api/scholarships/calculate', methods=['POST'])
@jwt_required()
def calculate_scholarship():
    try:
        data = request.get_json()
        family_income = data.get('family_income', 0)
        academic_score = data.get('academic_score', 0)
        attendance_percentage = data.get('attendance_percentage', 0)
        has_sibling = data.get('has_sibling', False)
        is_single_parent = data.get('is_single_parent', False)
        has_sports_achievement = data.get('has_sports_achievement', False)
        base_fee = data.get('base_fee', 2000)

        eligible_scholarships = []

        # Check Merit scholarship
        if academic_score >= 90 and family_income <= 60000:
            percentage = min(30, 20 + (academic_score - 90) * 2)  # 20-30% based on score
            eligible_scholarships.append({
                'type': 'Merit',
                'percentage': percentage,
                'amount': base_fee * percentage / 100,
                'reason': f'Academic score: {academic_score}%'
            })

        # Check Need-based scholarship
        if family_income <= 30000:
            percentage = max(30, min(50, 60 - (family_income / 1000)))  # 30-50% based on income
            eligible_scholarships.append({
                'type': 'Need-based',
                'percentage': percentage,
                'amount': base_fee * percentage / 100,
                'reason': f'Family income: ₹{family_income:,}'
            })

        # Check Sports scholarship
        if has_sports_achievement and attendance_percentage >= 95 and family_income <= 50000:
            percentage = 40 if attendance_percentage >= 98 else 30
            eligible_scholarships.append({
                'type': 'Sports',
                'percentage': percentage,
                'amount': base_fee * percentage / 100,
                'reason': f'Sports achievement + {attendance_percentage}% attendance'
            })

        # Check Sibling scholarship
        if has_sibling and family_income <= 70000:
            percentage = 15
            eligible_scholarships.append({
                'type': 'Sibling',
                'percentage': percentage,
                'amount': base_fee * percentage / 100,
                'reason': 'Multiple children discount'
            })

        # Check Single Parent scholarship
        if is_single_parent and family_income <= 40000:
            percentage = min(35, 20 + (40000 - family_income) / 1000)
            eligible_scholarships.append({
                'type': 'Single Parent',
                'percentage': percentage,
                'amount': base_fee * percentage / 100,
                'reason': 'Single parent household support'
            })

        # Select best scholarship (highest amount)
        best_scholarship = None
        if eligible_scholarships:
            best_scholarship = max(eligible_scholarships, key=lambda x: x['amount'])

        final_fee = base_fee
        if best_scholarship:
            final_fee = base_fee - best_scholarship['amount']

        return jsonify({
            'success': True,
            'data': {
                'base_fee': base_fee,
                'eligible_scholarships': eligible_scholarships,
                'recommended_scholarship': best_scholarship,
                'final_fee': final_fee,
                'total_savings': base_fee - final_fee if best_scholarship else 0
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fees/summary', methods=['GET'])
@jwt_required()
def get_fee_summary():
    try:
        # Calculate comprehensive fee statistics
        total_students = len(STUDENTS)
        scholarship_students = [s for s in STUDENTS if s['scholarship_type']]

        fee_stats = {
            'total_students': total_students,
            'scholarship_recipients': len(scholarship_students),
            'scholarship_percentage': (len(scholarship_students) / total_students * 100) if total_students > 0 else 0,
            'total_base_revenue': sum([s['base_monthly_fee'] for s in STUDENTS]),
            'total_actual_revenue': sum([s['final_monthly_fee'] for s in STUDENTS]),
            'total_scholarship_amount': sum([s['base_monthly_fee'] - s['final_monthly_fee'] for s in STUDENTS]),
            'average_scholarship_percentage': sum([s['scholarship_percentage'] for s in scholarship_students]) / len(scholarship_students) if scholarship_students else 0,
            'scholarship_breakdown': {}
        }

        # Breakdown by scholarship type
        for scholarship_type in ['Merit', 'Need-based', 'Sports', 'Sibling', 'Single Parent']:
            students_with_type = [s for s in STUDENTS if s['scholarship_type'] == scholarship_type]
            if students_with_type:
                fee_stats['scholarship_breakdown'][scholarship_type] = {
                    'count': len(students_with_type),
                    'total_savings': sum([s['base_monthly_fee'] - s['final_monthly_fee'] for s in students_with_type]),
                    'average_percentage': sum([s['scholarship_percentage'] for s in students_with_type]) / len(students_with_type)
                }

        return jsonify({
            'success': True,
            'data': fee_stats
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buses/<int:bus_id>/documents', methods=['GET'])
@jwt_required()
def get_bus_documents(bus_id):
    bus = next((b for b in BUSES if b['id'] == bus_id), None)
    if not bus:
        return jsonify({'success': False, 'error': 'Bus not found'}), 404
    
    documents = [
        {
            'id': 1, 'document_type': 'Insurance', 'document_name': 'Vehicle Insurance',
            'document_number': bus['insurance_number'], 'file_size_mb': 1.2,
            'is_expired': bus['is_insurance_expired'], 'is_expiring_soon': bus['days_to_insurance_expiry'] < 30,
            'days_to_expiry': bus['days_to_insurance_expiry'], 'issue_date': '2023-06-30',
            'expiry_date': '2024-06-30', 'issuing_authority': 'National Insurance Company'
        },
        {
            'id': 2, 'document_type': 'RC', 'document_name': 'Registration Certificate',
            'document_number': bus['rc_number'], 'file_size_mb': 0.8,
            'is_expired': bus['is_rc_expired'], 'is_expiring_soon': False,
            'days_to_expiry': 365, 'issue_date': '2020-01-15',
            'expiry_date': '2025-01-15', 'issuing_authority': 'RTO Karnataka'
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

@app.route('/api/buses/tracking', methods=['GET'])
@jwt_required()
def get_bus_tracking():
    """Get real-time bus tracking information."""
    try:
        tracking_data = []
        for bus in BUSES:
            if bus['status'] == 'Active' and bus['current_location_lat'] and bus['current_location_lng']:
                tracking_data.append({
                    'bus_id': bus['id'],
                    'bus_number': bus['bus_number'],
                    'route_name': bus['route_name'],
                    'current_location': {
                        'lat': bus['current_location_lat'],
                        'lng': bus['current_location_lng']
                    },
                    'current_stop': bus['current_stop'],
                    'next_stop': bus['next_stop'],
                    'eta_next_stop': bus['eta_next_stop'],
                    'total_stops_remaining': bus['total_stops_remaining'],
                    'speed': bus['speed'],
                    'occupancy': bus['current_occupancy'],
                    'capacity': bus['capacity'],
                    'driver_name': bus['driver_name']
                })

        return jsonify({
            'success': True,
            'data': {
                'buses': tracking_data,
                'last_updated': datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/buses/<int:bus_id>/route', methods=['GET'])
@jwt_required()
def get_bus_route(bus_id):
    """Get detailed route information for a specific bus."""
    try:
        bus = next((b for b in BUSES if b['id'] == bus_id), None)
        if not bus:
            return jsonify({'success': False, 'error': 'Bus not found'}), 404

        # Mock route stops with coordinates
        route_stops = []
        if bus['route_id'] == 1:  # City Center to School District
            route_stops = [
                {'name': 'City Center Bus Terminal', 'lat': 12.9716, 'lng': 77.5946, 'eta': 0, 'completed': True},
                {'name': 'Mall Junction', 'lat': 12.9750, 'lng': 77.6000, 'eta': 8, 'completed': False},
                {'name': 'Hospital Stop', 'lat': 12.9800, 'lng': 77.6100, 'eta': 15, 'completed': False},
                {'name': 'College Gate', 'lat': 12.9850, 'lng': 77.6200, 'eta': 22, 'completed': False},
                {'name': 'Market Square', 'lat': 12.9900, 'lng': 77.6300, 'eta': 30, 'completed': False},
                {'name': 'Residential Area', 'lat': 12.9950, 'lng': 77.6400, 'eta': 37, 'completed': False},
                {'name': 'School Junction', 'lat': 13.0000, 'lng': 77.6500, 'eta': 42, 'completed': False},
                {'name': 'Green Valley School', 'lat': 13.0050, 'lng': 77.6600, 'eta': 45, 'completed': False}
            ]
        elif bus['route_id'] == 2:  # Residential Area to College Campus
            route_stops = [
                {'name': 'Sunrise Apartments', 'lat': 12.9352, 'lng': 77.6245, 'eta': 0, 'completed': True},
                {'name': 'Shopping Complex', 'lat': 12.9400, 'lng': 77.6300, 'eta': 12, 'completed': False},
                {'name': 'Bus Stand', 'lat': 12.9450, 'lng': 77.6350, 'eta': 20, 'completed': False},
                {'name': 'Tech University Gate', 'lat': 12.9500, 'lng': 77.6400, 'eta': 60, 'completed': False}
            ]
        elif bus['route_id'] == 3:  # Industrial Area to Tech Park
            route_stops = [
                {'name': 'Industrial Complex Gate', 'lat': 12.8456, 'lng': 77.6632, 'eta': 0, 'completed': True},
                {'name': 'Factory Junction', 'lat': 12.8500, 'lng': 77.6700, 'eta': 15, 'completed': False},
                {'name': 'Software Tech Park', 'lat': 12.8600, 'lng': 77.6800, 'eta': 50, 'completed': False}
            ]
        elif bus['route_id'] == 4:  # Metro Station to Airport
            route_stops = [
                {'name': 'Central Metro Station', 'lat': 13.1986, 'lng': 77.7066, 'eta': 0, 'completed': True},
                {'name': 'Highway Junction', 'lat': 13.2000, 'lng': 77.7100, 'eta': 25, 'completed': False},
                {'name': 'International Airport', 'lat': 13.2100, 'lng': 77.7200, 'eta': 75, 'completed': False}
            ]

        return jsonify({
            'success': True,
            'data': {
                'bus_id': bus_id,
                'bus_number': bus['bus_number'],
                'route_name': bus['route_name'],
                'current_location': {
                    'lat': bus['current_location_lat'],
                    'lng': bus['current_location_lng']
                },
                'route_stops': route_stops,
                'current_stop': bus['current_stop'],
                'next_stop': bus['next_stop'],
                'eta_next_stop': bus['eta_next_stop']
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚌 Starting Complete Transport Management System (Admin Only)")
    print("=" * 60)
    print("📍 Backend: http://localhost:5001")
    print("🎯 Health: http://localhost:5001/api/health")
    print("👤 Admin Login: admin / admin123")
    print("✨ Features: Buses, Drivers, Routes, Students, Documents")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
