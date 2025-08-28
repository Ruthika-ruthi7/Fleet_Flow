from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.trip import Trip
from app.models.bus import Bus
from app.models.route import Route
from app.utils.helpers import success_response, error_response

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/', methods=['GET'])
@jwt_required()
def get_trips():
    """Get all trips"""
    try:
        trips = Trip.query.all()
        trips_data = []
        for trip in trips:
            trips_data.append({
                'id': trip.id,
                'bus_id': trip.bus_id,
                'route_id': trip.route_id,
                'driver_id': trip.driver_id,
                'start_time': trip.start_time.isoformat() if trip.start_time else None,
                'end_time': trip.end_time.isoformat() if trip.end_time else None,
                'status': trip.status,
                'trip_type': trip.trip_type,
                'created_at': trip.created_at.isoformat() if trip.created_at else None
            })
        return success_response(trips_data)
    except Exception as e:
        return error_response(f"Error fetching trips: {str(e)}")

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    """Get a specific trip"""
    try:
        trip = Trip.query.get_or_404(trip_id)
        trip_data = {
            'id': trip.id,
            'bus_id': trip.bus_id,
            'route_id': trip.route_id,
            'driver_id': trip.driver_id,
            'start_time': trip.start_time.isoformat() if trip.start_time else None,
            'end_time': trip.end_time.isoformat() if trip.end_time else None,
            'status': trip.status,
            'trip_type': trip.trip_type,
            'created_at': trip.created_at.isoformat() if trip.created_at else None
        }
        return success_response(trip_data)
    except Exception as e:
        return error_response(f"Error fetching trip: {str(e)}")

@trips_bp.route('/', methods=['POST'])
@jwt_required()
def create_trip():
    """Create a new trip"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['bus_id', 'route_id', 'driver_id', 'trip_type']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}")
        
        # Create new trip
        trip = Trip(
            bus_id=data['bus_id'],
            route_id=data['route_id'],
            driver_id=data['driver_id'],
            trip_type=data['trip_type'],
            start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
            end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            status=data.get('status', 'scheduled')
        )
        
        db.session.add(trip)
        db.session.commit()
        
        return success_response({
            'id': trip.id,
            'bus_id': trip.bus_id,
            'route_id': trip.route_id,
            'message': 'Trip created successfully'
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating trip: {str(e)}")

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    """Update a trip"""
    try:
        trip = Trip.query.get_or_404(trip_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'bus_id' in data:
            trip.bus_id = data['bus_id']
        if 'route_id' in data:
            trip.route_id = data['route_id']
        if 'driver_id' in data:
            trip.driver_id = data['driver_id']
        if 'start_time' in data:
            trip.start_time = datetime.fromisoformat(data['start_time']) if data['start_time'] else None
        if 'end_time' in data:
            trip.end_time = datetime.fromisoformat(data['end_time']) if data['end_time'] else None
        if 'status' in data:
            trip.status = data['status']
        if 'trip_type' in data:
            trip.trip_type = data['trip_type']
        
        db.session.commit()
        
        return success_response({
            'id': trip.id,
            'status': trip.status,
            'message': 'Trip updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating trip: {str(e)}")

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    """Delete a trip"""
    try:
        trip = Trip.query.get_or_404(trip_id)
        db.session.delete(trip)
        db.session.commit()
        
        return success_response({'message': 'Trip deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting trip: {str(e)}")

@trips_bp.route('/<int:trip_id>/start', methods=['POST'])
@jwt_required()
def start_trip(trip_id):
    """Start a trip"""
    try:
        trip = Trip.query.get_or_404(trip_id)
        trip.status = 'in_progress'
        trip.start_time = datetime.utcnow()
        
        db.session.commit()
        
        return success_response({
            'id': trip.id,
            'status': trip.status,
            'start_time': trip.start_time.isoformat(),
            'message': 'Trip started successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error starting trip: {str(e)}")

@trips_bp.route('/<int:trip_id>/complete', methods=['POST'])
@jwt_required()
def complete_trip(trip_id):
    """Complete a trip"""
    try:
        trip = Trip.query.get_or_404(trip_id)
        trip.status = 'completed'
        trip.end_time = datetime.utcnow()
        
        db.session.commit()
        
        return success_response({
            'id': trip.id,
            'status': trip.status,
            'end_time': trip.end_time.isoformat(),
            'message': 'Trip completed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error completing trip: {str(e)}")
