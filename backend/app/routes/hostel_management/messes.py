from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.hostel_management import Mess
from app.utils.decorators import admin_required
from app.utils.helpers import success_response, error_response, paginate_query

messes_bp = Blueprint('messes', __name__, url_prefix='/messes')

@messes_bp.route('', methods=['GET'])
@jwt_required()
def get_messes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = Mess.query
        paginated = paginate_query(query, page, per_page)
        if not paginated:
            return error_response('Invalid pagination parameters')
        messes_data = [mess.__dict__ for mess in paginated['items']]
        for m in messes_data:
            m.pop('_sa_instance_state', None)
        return success_response('Messes retrieved successfully', {
            'messes': messes_data,
            'pagination': paginated
        })
    except Exception as e:
        return error_response(f'Failed to retrieve messes: {str(e)}', 500)

@messes_bp.route('/<int:mess_id>', methods=['GET'])
@jwt_required()
def get_mess(mess_id):
    try:
        mess = Mess.query.get(mess_id)
        if not mess:
            return error_response('Mess not found', 404)
        data = mess.__dict__
        data.pop('_sa_instance_state', None)
        return success_response('Mess retrieved successfully', {'mess': data})
    except Exception as e:
        return error_response(f'Failed to retrieve mess: {str(e)}', 500)

@messes_bp.route('', methods=['POST'])
@admin_required
def create_mess(current_user):
    try:
        data = request.get_json()
        if not data or not data.get('hostel_id'):
            return error_response('Hostel ID is required')
        mess = Mess(
            hostel_id=data['hostel_id'],
            menu=data.get('menu'),
            fees=data.get('fees')
        )
        db.session.add(mess)
        db.session.commit()
        return success_response('Mess created successfully', {'mess_id': mess.id}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create mess: {str(e)}', 500)

@messes_bp.route('/<int:mess_id>', methods=['PUT'])
@admin_required
def update_mess(current_user, mess_id):
    try:
        mess = Mess.query.get(mess_id)
        if not mess:
            return error_response('Mess not found', 404)
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        for field in ['hostel_id', 'menu', 'fees']:
            if field in data:
                setattr(mess, field, data[field])
        db.session.commit()
        return success_response('Mess updated successfully', {'mess': mess.__dict__})
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update mess: {str(e)}', 500)

@messes_bp.route('/<int:mess_id>', methods=['DELETE'])
@admin_required
def delete_mess(current_user, mess_id):
    try:
        mess = Mess.query.get(mess_id)
        if not mess:
            return error_response('Mess not found', 404)
        db.session.delete(mess)
        db.session.commit()
        return success_response('Mess deleted successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete mess: {str(e)}', 500)
