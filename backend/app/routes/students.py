from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.student import Student
from app.models.user import User
from app.utils.helpers import success_response, error_response

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    """Get all students"""
    try:
        students = Student.query.all()
        students_data = []
        for student in students:
            students_data.append({
                'id': student.id,
                'student_id': student.student_id,
                'name': student.name,
                'email': student.email,
                'phone': student.phone,
                'address': student.address,
                'route_id': student.route_id,
                'created_at': student.created_at.isoformat() if student.created_at else None
            })
        return success_response(students_data)
    except Exception as e:
        return error_response(f"Error fetching students: {str(e)}")

@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    """Get a specific student"""
    try:
        student = Student.query.get_or_404(student_id)
        student_data = {
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name,
            'email': student.email,
            'phone': student.phone,
            'address': student.address,
            'route_id': student.route_id,
            'created_at': student.created_at.isoformat() if student.created_at else None
        }
        return success_response(student_data)
    except Exception as e:
        return error_response(f"Error fetching student: {str(e)}")

@students_bp.route('/', methods=['POST'])
@jwt_required()
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'name', 'email', 'phone']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}")
        
        # Check if student ID already exists
        existing_student = Student.query.filter_by(student_id=data['student_id']).first()
        if existing_student:
            return error_response("Student ID already exists")
        
        # Create new student
        student = Student(
            student_id=data['student_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data.get('address'),
            route_id=data.get('route_id')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return success_response({
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name,
            'message': 'Student created successfully'
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating student: {str(e)}")

@students_bp.route('/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    """Update a student"""
    try:
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            student.name = data['name']
        if 'email' in data:
            student.email = data['email']
        if 'phone' in data:
            student.phone = data['phone']
        if 'address' in data:
            student.address = data['address']
        if 'route_id' in data:
            student.route_id = data['route_id']
        
        db.session.commit()
        
        return success_response({
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name,
            'message': 'Student updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating student: {str(e)}")

@students_bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    """Delete a student"""
    try:
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        
        return success_response({'message': 'Student deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting student: {str(e)}")
