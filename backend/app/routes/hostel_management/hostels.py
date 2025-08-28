from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.hostel_management import Hostel
from app.utils.decorators import admin_required
from app.utils.helpers import success_response, error_response, paginate_query

hostels_bp = Blueprint('hostels', __name__, url_prefix='/hostels')

@hostels_bp.route('', methods=['GET'])
@jwt_required()
def get_hostels():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = Hostel.query
        paginated = paginate_query(query, page, per_page)
        if not paginated:
            return error_response('Invalid pagination parameters')
        hostels_data = [hostel.__dict__ for hostel in paginated['items']]
        for h in hostels_data:
            h.pop('_sa_instance_state', None)
        return success_response('Hostels retrieved successfully', {
            'hostels': hostels_data,
            'pagination': paginated
        })
    except Exception as e:
        return error_response(f'Failed to retrieve hostels: {str(e)}', 500)

@hostels_bp.route('/<int:hostel_id>', methods=['GET'])
@jwt_required()
def get_hostel(hostel_id):
    try:
        hostel = Hostel.query.get(hostel_id)
        if not hostel:
            return error_response('Hostel not found', 404)
        data = hostel.__dict__
        data.pop('_sa_instance_state', None)
        return success_response('Hostel retrieved successfully', {'hostel': data})
    except Exception as e:
        return error_response(f'Failed to retrieve hostel: {str(e)}', 500)

@hostels_bp.route('', methods=['POST'])
@admin_required
def create_hostel(current_user):
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return error_response('Hostel name is required')
        hostel = Hostel(
            name=data['name'],
            warden=data.get('warden'),
            capacity=data.get('capacity')
        )
        db.session.add(hostel)
        db.session.commit()
        return success_response('Hostel created successfully', {'hostel_id': hostel.id}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create hostel: {str(e)}', 500)

@hostels_bp.route('/<int:hostel_id>', methods=['PUT'])
@admin_required
def update_hostel(current_user, hostel_id):
    try:
        hostel = Hostel.query.get(hostel_id)
        if not hostel:
            return error_response('Hostel not found', 404)
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        for field in ['name', 'warden', 'capacity']:
            if field in data:
                setattr(hostel, field, data[field])
        db.session.commit()
        return success_response('Hostel updated successfully', {'hostel': hostel.__dict__})
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update hostel: {str(e)}', 500)

@hostels_bp.route('/<int:hostel_id>', methods=['DELETE'])
@admin_required
def delete_hostel(current_user, hostel_id):
    try:
        hostel = Hostel.query.get(hostel_id)
        if not hostel:
            return error_response('Hostel not found', 404)
        db.session.delete(hostel)
        db.session.commit()
        return success_response('Hostel deleted successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete hostel: {str(e)}', 500)
