from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from app import db
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.trip import Trip
from app.utils.helpers import success_response, error_response

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['GET'])
@jwt_required()
def get_attendance_records():
    """Get all attendance records"""
    try:
        # Get query parameters for filtering
        student_id = request.args.get('student_id')
        trip_id = request.args.get('trip_id')
        date_str = request.args.get('date')
        
        query = Attendance.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if trip_id:
            query = query.filter_by(trip_id=trip_id)
        if date_str:
            try:
                filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                query = query.filter(db.func.date(Attendance.timestamp) == filter_date)
            except ValueError:
                return error_response("Invalid date format. Use YYYY-MM-DD")
        
        attendance_records = query.all()
        records_data = []
        for record in attendance_records:
            records_data.append({
                'id': record.id,
                'student_id': record.student_id,
                'trip_id': record.trip_id,
                'status': record.status,
                'timestamp': record.timestamp.isoformat() if record.timestamp else None,
                'location': record.location,
                'created_at': record.created_at.isoformat() if record.created_at else None
            })
        return success_response(records_data)
    except Exception as e:
        return error_response(f"Error fetching attendance records: {str(e)}")

@attendance_bp.route('/<int:attendance_id>', methods=['GET'])
@jwt_required()
def get_attendance_record(attendance_id):
    """Get a specific attendance record"""
    try:
        record = Attendance.query.get_or_404(attendance_id)
        record_data = {
            'id': record.id,
            'student_id': record.student_id,
            'trip_id': record.trip_id,
            'status': record.status,
            'timestamp': record.timestamp.isoformat() if record.timestamp else None,
            'location': record.location,
            'created_at': record.created_at.isoformat() if record.created_at else None
        }
        return success_response(record_data)
    except Exception as e:
        return error_response(f"Error fetching attendance record: {str(e)}")

@attendance_bp.route('/', methods=['POST'])
@jwt_required()
def create_attendance_record():
    """Create a new attendance record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'trip_id', 'status']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}")
        
        # Validate status
        valid_statuses = ['present', 'absent', 'boarded', 'alighted']
        if data['status'] not in valid_statuses:
            return error_response(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        # Create new attendance record
        record = Attendance(
            student_id=data['student_id'],
            trip_id=data['trip_id'],
            status=data['status'],
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.utcnow(),
            location=data.get('location')
        )
        
        db.session.add(record)
        db.session.commit()
        
        return success_response({
            'id': record.id,
            'student_id': record.student_id,
            'trip_id': record.trip_id,
            'status': record.status,
            'message': 'Attendance record created successfully'
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating attendance record: {str(e)}")

@attendance_bp.route('/<int:attendance_id>', methods=['PUT'])
@jwt_required()
def update_attendance_record(attendance_id):
    """Update an attendance record"""
    try:
        record = Attendance.query.get_or_404(attendance_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'status' in data:
            valid_statuses = ['present', 'absent', 'boarded', 'alighted']
            if data['status'] not in valid_statuses:
                return error_response(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            record.status = data['status']
        
        if 'timestamp' in data:
            record.timestamp = datetime.fromisoformat(data['timestamp'])
        
        if 'location' in data:
            record.location = data['location']
        
        db.session.commit()
        
        return success_response({
            'id': record.id,
            'status': record.status,
            'message': 'Attendance record updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating attendance record: {str(e)}")

@attendance_bp.route('/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
def delete_attendance_record(attendance_id):
    """Delete an attendance record"""
    try:
        record = Attendance.query.get_or_404(attendance_id)
        db.session.delete(record)
        db.session.commit()
        
        return success_response({'message': 'Attendance record deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting attendance record: {str(e)}")

@attendance_bp.route('/student/<int:student_id>/summary', methods=['GET'])
@jwt_required()
def get_student_attendance_summary(student_id):
    """Get attendance summary for a specific student"""
    try:
        # Get date range from query parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        query = Attendance.query.filter_by(student_id=student_id)
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Attendance.timestamp) >= start_date)
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Attendance.timestamp) <= end_date)
        
        records = query.all()
        
        # Calculate summary
        total_records = len(records)
        present_count = len([r for r in records if r.status in ['present', 'boarded']])
        absent_count = len([r for r in records if r.status == 'absent'])
        
        attendance_percentage = (present_count / total_records * 100) if total_records > 0 else 0
        
        summary_data = {
            'student_id': student_id,
            'total_records': total_records,
            'present_count': present_count,
            'absent_count': absent_count,
            'attendance_percentage': round(attendance_percentage, 2)
        }
        
        return success_response(summary_data)
    except Exception as e:
        return error_response(f"Error fetching attendance summary: {str(e)}")

@attendance_bp.route('/trip/<int:trip_id>/summary', methods=['GET'])
@jwt_required()
def get_trip_attendance_summary(trip_id):
    """Get attendance summary for a specific trip"""
    try:
        records = Attendance.query.filter_by(trip_id=trip_id).all()
        
        # Calculate summary
        total_students = len(records)
        present_count = len([r for r in records if r.status in ['present', 'boarded']])
        absent_count = len([r for r in records if r.status == 'absent'])
        
        summary_data = {
            'trip_id': trip_id,
            'total_students': total_students,
            'present_count': present_count,
            'absent_count': absent_count,
            'attendance_rate': round((present_count / total_students * 100), 2) if total_students > 0 else 0
        }
        
        return success_response(summary_data)
    except Exception as e:
        return error_response(f"Error fetching trip attendance summary: {str(e)}")
