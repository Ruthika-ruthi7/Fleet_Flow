from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import func
from app import db, socketio
from app.models.bus_location import BusLocation
from app.models.bus import Bus
from app.models.trip import Trip
from app.utils.helpers import success_response, error_response

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/locations', methods=['GET'])
@jwt_required()
def get_bus_locations():
    """Get current locations of all buses"""
    try:
        # Get query parameters
        bus_id = request.args.get('bus_id')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        query = BusLocation.query
        
        if bus_id:
            query = query.filter_by(bus_id=bus_id)
        
        if active_only:
            # Get only the latest location for each bus
            subquery = db.session.query(
                BusLocation.bus_id,
                func.max(BusLocation.timestamp).label('latest_timestamp')
            ).group_by(BusLocation.bus_id).subquery()
            
            query = query.join(
                subquery,
                (BusLocation.bus_id == subquery.c.bus_id) &
                (BusLocation.timestamp == subquery.c.latest_timestamp)
            )
        
        locations = query.all()
        locations_data = []
        
        for location in locations:
            locations_data.append({
                'id': location.id,
                'bus_id': location.bus_id,
                'latitude': float(location.latitude) if location.latitude else None,
                'longitude': float(location.longitude) if location.longitude else None,
                'speed': float(location.speed) if location.speed else None,
                'heading': float(location.heading) if location.heading else None,
                'timestamp': location.timestamp.isoformat() if location.timestamp else None,
                'accuracy': float(location.accuracy) if location.accuracy else None
            })
        
        return success_response(locations_data)
    except Exception as e:
        return error_response(f"Error fetching bus locations: {str(e)}")

@tracking_bp.route('/locations/<int:bus_id>', methods=['GET'])
@jwt_required()
def get_bus_location_history(bus_id):
    """Get location history for a specific bus"""
    try:
        # Get query parameters for time range
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        limit = request.args.get('limit', 100, type=int)
        
        query = BusLocation.query.filter_by(bus_id=bus_id)
        
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            query = query.filter(BusLocation.timestamp >= start_time)
        
        if end_time_str:
            end_time = datetime.fromisoformat(end_time_str)
            query = query.filter(BusLocation.timestamp <= end_time)
        
        locations = query.order_by(BusLocation.timestamp.desc()).limit(limit).all()
        
        locations_data = []
        for location in locations:
            locations_data.append({
                'id': location.id,
                'latitude': float(location.latitude) if location.latitude else None,
                'longitude': float(location.longitude) if location.longitude else None,
                'speed': float(location.speed) if location.speed else None,
                'heading': float(location.heading) if location.heading else None,
                'timestamp': location.timestamp.isoformat() if location.timestamp else None,
                'accuracy': float(location.accuracy) if location.accuracy else None
            })
        
        return success_response(locations_data)
    except Exception as e:
        return error_response(f"Error fetching bus location history: {str(e)}")

@tracking_bp.route('/locations', methods=['POST'])
@jwt_required()
def update_bus_location():
    """Update bus location (typically called by GPS device or mobile app)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['bus_id', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        
        # Validate coordinate ranges
        if not (-90 <= data['latitude'] <= 90):
            return error_response("Latitude must be between -90 and 90")
        
        if not (-180 <= data['longitude'] <= 180):
            return error_response("Longitude must be between -180 and 180")
        
        # Create new location record
        location = BusLocation(
            bus_id=data['bus_id'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            speed=data.get('speed'),
            heading=data.get('heading'),
            accuracy=data.get('accuracy'),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.utcnow()
        )
        
        db.session.add(location)
        db.session.commit()
        
        # Emit real-time update via WebSocket
        socketio.emit('location_update', {
            'bus_id': location.bus_id,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'speed': float(location.speed) if location.speed else None,
            'heading': float(location.heading) if location.heading else None,
            'timestamp': location.timestamp.isoformat()
        }, room='tracking')
        
        return success_response({
            'id': location.id,
            'bus_id': location.bus_id,
            'message': 'Location updated successfully'
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating bus location: {str(e)}")

@tracking_bp.route('/active-trips', methods=['GET'])
@jwt_required()
def get_active_trips_with_locations():
    """Get active trips with their current bus locations"""
    try:
        # Get active trips
        active_trips = Trip.query.filter(
            Trip.status.in_(['scheduled', 'in_progress'])
        ).all()
        
        trips_data = []
        for trip in active_trips:
            # Get latest location for this bus
            latest_location = BusLocation.query.filter_by(
                bus_id=trip.bus_id
            ).order_by(BusLocation.timestamp.desc()).first()
            
            trip_data = {
                'trip_id': trip.id,
                'bus_id': trip.bus_id,
                'route_id': trip.route_id,
                'driver_id': trip.driver_id,
                'status': trip.status,
                'start_time': trip.start_time.isoformat() if trip.start_time else None,
                'trip_type': trip.trip_type,
                'current_location': None
            }
            
            if latest_location:
                trip_data['current_location'] = {
                    'latitude': float(latest_location.latitude) if latest_location.latitude else None,
                    'longitude': float(latest_location.longitude) if latest_location.longitude else None,
                    'speed': float(latest_location.speed) if latest_location.speed else None,
                    'heading': float(latest_location.heading) if latest_location.heading else None,
                    'timestamp': latest_location.timestamp.isoformat() if latest_location.timestamp else None
                }
            
            trips_data.append(trip_data)
        
        return success_response(trips_data)
    except Exception as e:
        return error_response(f"Error fetching active trips with locations: {str(e)}")

@tracking_bp.route('/geofence-check', methods=['POST'])
@jwt_required()
def check_geofence():
    """Check if a bus is within a specific geofence area"""
    try:
        data = request.get_json()
        
        required_fields = ['bus_id', 'center_lat', 'center_lng', 'radius_meters']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        
        # Get latest location for the bus
        latest_location = BusLocation.query.filter_by(
            bus_id=data['bus_id']
        ).order_by(BusLocation.timestamp.desc()).first()
        
        if not latest_location:
            return error_response("No location data found for this bus")
        
        # Calculate distance using Haversine formula (simplified)
        import math
        
        lat1 = math.radians(float(latest_location.latitude))
        lon1 = math.radians(float(latest_location.longitude))
        lat2 = math.radians(data['center_lat'])
        lon2 = math.radians(data['center_lng'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance_meters = 6371000 * c  # Earth's radius in meters
        
        is_inside = distance_meters <= data['radius_meters']
        
        result = {
            'bus_id': data['bus_id'],
            'is_inside_geofence': is_inside,
            'distance_from_center': round(distance_meters, 2),
            'radius_meters': data['radius_meters'],
            'current_location': {
                'latitude': float(latest_location.latitude),
                'longitude': float(latest_location.longitude),
                'timestamp': latest_location.timestamp.isoformat()
            }
        }
        
        return success_response(result)
    except Exception as e:
        return error_response(f"Error checking geofence: {str(e)}")

# WebSocket events for real-time tracking
@socketio.on('join_tracking')
def on_join_tracking():
    """Join the tracking room for real-time updates"""
    from flask_socketio import join_room
    join_room('tracking')
    socketio.emit('tracking_joined', {'message': 'Joined tracking updates'})

@socketio.on('leave_tracking')
def on_leave_tracking():
    """Leave the tracking room"""
    from flask_socketio import leave_room
    leave_room('tracking')
    socketio.emit('tracking_left', {'message': 'Left tracking updates'})
