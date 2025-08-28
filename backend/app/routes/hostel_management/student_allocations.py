from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.hostel_management import StudentAllocation
from app.utils.decorators import admin_required
from app.utils.helpers import success_response, error_response, paginate_query

student_allocations_bp = Blueprint('student_allocations', __name__, url_prefix='/student_allocations')

@student_allocations_bp.route('', methods=['GET'])
@jwt_required()
def get_student_allocations():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = StudentAllocation.query
        paginated = paginate_query(query, page, per_page)
        if not paginated:
            return error_response('Invalid pagination parameters')
        allocations_data = [alloc.__dict__ for alloc in paginated['items']]
        for a in allocations_data:
            a.pop('_sa_instance_state', None)
        return success_response('Student allocations retrieved successfully', {
            'student_allocations': allocations_data,
            'pagination': paginated
        })
    except Exception as e:
        return error_response(f'Failed to retrieve student allocations: {str(e)}', 500)

@student_allocations_bp.route('/<int:allocation_id>', methods=['GET'])
@jwt_required()
def get_student_allocation(allocation_id):
    try:
        allocation = StudentAllocation.query.get(allocation_id)
        if not allocation:
            return error_response('Student allocation not found', 404)
        data = allocation.__dict__
        data.pop('_sa_instance_state', None)
        return success_response('Student allocation retrieved successfully', {'student_allocation': data})
    except Exception as e:
        return error_response(f'Failed to retrieve student allocation: {str(e)}', 500)

@student_allocations_bp.route('', methods=['POST'])
@admin_required
def create_student_allocation(current_user):
    try:
        data = request.get_json()
        required_fields = ['student_id', 'room_id']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'{field} is required')
        allocation = StudentAllocation(
            student_id=data['student_id'],
            room_id=data['room_id'],
            allocation_date=data.get('allocation_date'),
            leave_requested=data.get('leave_requested', False),
            leave_approved=data.get('leave_approved', False)
        )
        db.session.add(allocation)
        db.session.commit()
        return success_response('Student allocation created successfully', {'student_allocation_id': allocation.id}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create student allocation: {str(e)}', 500)

@student_allocations_bp.route('/<int:allocation_id>', methods=['PUT'])
@admin_required
def update_student_allocation(current_user, allocation_id):
    try:
        allocation = StudentAllocation.query.get(allocation_id)
        if not allocation:
            return error_response('Student allocation not found', 404)
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        for field in ['student_id', 'room_id', 'allocation_date', 'leave_requested', 'leave_approved']:
            if field in data:
                setattr(allocation, field, data[field])
        db.session.commit()
        return success_response('Student allocation updated successfully', {'student_allocation': allocation.__dict__})
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update student allocation: {str(e)}', 500)

@student_allocations_bp.route('/<int:allocation_id>', methods=['DELETE'])
@admin_required
def delete_student_allocation(current_user, allocation_id):
    try:
        allocation = StudentAllocation.query.get(allocation_id)
        if not allocation:
            return error_response('Student allocation not found', 404)
        db.session.delete(allocation)
        db.session.commit()
        return success_response('Student allocation deleted successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete student allocation: {str(e)}', 500)
