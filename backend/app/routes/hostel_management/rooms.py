from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app import db
from app.models.hostel_management import Room
from app.utils.decorators import admin_required
from app.utils.helpers import success_response, error_response, paginate_query

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@rooms_bp.route('', methods=['GET'])
@jwt_required()
def get_rooms():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        query = Room.query
        paginated = paginate_query(query, page, per_page)
        if not paginated:
            return error_response('Invalid pagination parameters')
        rooms_data = [room.__dict__ for room in paginated['items']]
        for r in rooms_data:
            r.pop('_sa_instance_state', None)
        return success_response('Rooms retrieved successfully', {
            'rooms': rooms_data,
            'pagination': paginated
        })
    except Exception as e:
        return error_response(f'Failed to retrieve rooms: {str(e)}', 500)

@rooms_bp.route('/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    try:
        room = Room.query.get(room_id)
        if not room:
            return error_response('Room not found', 404)
        data = room.__dict__
        data.pop('_sa_instance_state', None)
        return success_response('Room retrieved successfully', {'room': data})
    except Exception as e:
        return error_response(f'Failed to retrieve room: {str(e)}', 500)

@rooms_bp.route('', methods=['POST'])
@admin_required
def create_room(current_user):
    try:
        data = request.get_json()
        required_fields = ['hostel_id', 'room_type']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'{field} is required')
        room = Room(
            hostel_id=data['hostel_id'],
            room_type=data['room_type'],
            floor=data.get('floor'),
            beds=data.get('beds')
        )
        db.session.add(room)
        db.session.commit()
        return success_response('Room created successfully', {'room_id': room.id}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create room: {str(e)}', 500)

@rooms_bp.route('/<int:room_id>', methods=['PUT'])
@admin_required
def update_room(current_user, room_id):
    try:
        room = Room.query.get(room_id)
        if not room:
            return error_response('Room not found', 404)
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        for field in ['hostel_id', 'room_type', 'floor', 'beds']:
            if field in data:
                setattr(room, field, data[field])
        db.session.commit()
        return success_response('Room updated successfully', {'room': room.__dict__})
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update room: {str(e)}', 500)

@rooms_bp.route('/<int:room_id>', methods=['DELETE'])
@admin_required
def delete_room(current_user, room_id):
    try:
        room = Room.query.get(room_id)
        if not room:
            return error_response('Room not found', 404)
        db.session.delete(room)
        db.session.commit()
        return success_response('Room deleted successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete room: {str(e)}', 500)
