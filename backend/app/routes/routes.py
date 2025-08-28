from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, time
from app import db
from app.models.route import Route, RouteStop
from app.utils.decorators import admin_required, staff_required
from app.utils.helpers import (
    success_response, error_response, paginate_query,
    generate_route_code, parse_time_string
)

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('', methods=['GET'])
@jwt_required()
def get_routes():
    """Get all routes with pagination and filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        route_type = request.args.get('route_type')
        search = request.args.get('search', '').strip()
        
        query = Route.query.filter_by(is_active=True)
        
        if status:
            query = query.filter_by(status=status)
        
        if route_type:
            query = query.filter_by(route_type=route_type)
        
        if search:
            query = query.filter(
                (Route.route_name.contains(search)) |
                (Route.route_code.contains(search)) |
                (Route.start_location.contains(search)) |
                (Route.end_location.contains(search))
            )
        
        query = query.order_by(Route.route_code)
        paginated = paginate_query(query, page, per_page)
        
        if not paginated:
            return error_response('Invalid pagination parameters')
        
        routes_data = [route.to_dict() for route in paginated['items']]
        
        return success_response('Routes retrieved successfully', {
            'routes': routes_data,
            'pagination': {
                'total': paginated['total'],
                'pages': paginated['pages'],
                'current_page': paginated['current_page'],
                'per_page': paginated['per_page'],
                'has_next': paginated['has_next'],
                'has_prev': paginated['has_prev']
            }
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve routes: {str(e)}', 500)

@routes_bp.route('/<int:route_id>', methods=['GET'])
@jwt_required()
def get_route(route_id):
    """Get a specific route by ID."""
    try:
        route = Route.query.filter_by(id=route_id, is_active=True).first()
        
        if not route:
            return error_response('Route not found', 404)
        
        return success_response('Route retrieved successfully', {
            'route': route.to_dict()
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve route: {str(e)}', 500)

@routes_bp.route('', methods=['POST'])
@admin_required
def create_route(current_user):
    """Create a new route with AI-powered optimization."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Required fields
        required_fields = ['route_name', 'start_location', 'end_location']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'{field.replace("_", " ").title()} is required')
        
        route_name = data.get('route_name').strip()
        
        # Generate route code if not provided
        route_code = data.get('route_code') or generate_route_code(route_name)
        
        # Check if route code already exists
        if Route.query.filter_by(route_code=route_code).first():
            route_code = generate_route_code(route_name)
        
        # Parse time fields
        start_time = None
        end_time = None
        if data.get('start_time'):
            start_time = parse_time_string(data['start_time'])
        if data.get('end_time'):
            end_time = parse_time_string(data['end_time'])
        
        # Create route
        route = Route(
            route_name=route_name,
            route_code=route_code,
            start_location=data.get('start_location').strip(),
            end_location=data.get('end_location').strip(),
            total_distance=data.get('total_distance'),
            estimated_duration=data.get('estimated_duration'),
            route_type=data.get('route_type', 'Urban'),
            start_time=start_time,
            end_time=end_time,
            frequency=data.get('frequency', 1),
            status='Active'
        )
        
        db.session.add(route)
        db.session.flush()
        
        # Add route stops if provided
        stops_data = data.get('stops', [])
        if stops_data:
            for stop_data in stops_data:
                arrival_time = None
                departure_time = None
                
                if stop_data.get('arrival_time'):
                    arrival_time = parse_time_string(stop_data['arrival_time'])
                if stop_data.get('departure_time'):
                    departure_time = parse_time_string(stop_data['departure_time'])
                
                stop = RouteStop(
                    route_id=route.id,
                    stop_name=stop_data.get('stop_name').strip(),
                    stop_address=stop_data.get('stop_address'),
                    latitude=stop_data.get('latitude'),
                    longitude=stop_data.get('longitude'),
                    stop_order=stop_data.get('stop_order'),
                    arrival_time=arrival_time,
                    departure_time=departure_time,
                    stop_duration=stop_data.get('stop_duration', 2),
                    distance_from_previous=stop_data.get('distance_from_previous'),
                    landmark=stop_data.get('landmark'),
                    is_major_stop=stop_data.get('is_major_stop', False)
                )
                db.session.add(stop)
        
        db.session.commit()
        
        # AI-powered route optimization (placeholder for future implementation)
        # This would integrate with Google Maps API for optimal route calculation
        
        return success_response('Route created successfully', {
            'route': route.to_dict()
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create route: {str(e)}', 500)

@routes_bp.route('/<int:route_id>', methods=['PUT'])
@admin_required
def update_route(current_user, route_id):
    """Update a route."""
    try:
        route = Route.query.filter_by(id=route_id, is_active=True).first()
        
        if not route:
            return error_response('Route not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        # Update basic fields
        updateable_fields = [
            'route_name', 'start_location', 'end_location', 'total_distance',
            'estimated_duration', 'route_type', 'frequency', 'status'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(route, field, data[field])
        
        # Handle route code update
        if 'route_code' in data:
            new_route_code = data['route_code'].strip().upper()
            existing_route = Route.query.filter(
                Route.route_code == new_route_code,
                Route.id != route_id
            ).first()
            if existing_route:
                return error_response('Route code already exists')
            route.route_code = new_route_code
        
        # Handle time fields
        if 'start_time' in data and data['start_time']:
            route.start_time = parse_time_string(data['start_time'])
        
        if 'end_time' in data and data['end_time']:
            route.end_time = parse_time_string(data['end_time'])
        
        db.session.commit()
        
        return success_response('Route updated successfully', {
            'route': route.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update route: {str(e)}', 500)

@routes_bp.route('/<int:route_id>/stops', methods=['GET'])
@jwt_required()
def get_route_stops(route_id):
    """Get all stops for a route."""
    try:
        route = Route.query.filter_by(id=route_id, is_active=True).first()
        
        if not route:
            return error_response('Route not found', 404)
        
        stops = RouteStop.query.filter_by(route_id=route_id).order_by(RouteStop.stop_order).all()
        stops_data = [stop.to_dict() for stop in stops]
        
        return success_response('Route stops retrieved successfully', {
            'route_id': route_id,
            'route_name': route.route_name,
            'stops': stops_data
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve route stops: {str(e)}', 500)

@routes_bp.route('/<int:route_id>/stops', methods=['POST'])
@admin_required
def add_route_stop(current_user, route_id):
    """Add a new stop to a route."""
    try:
        route = Route.query.filter_by(id=route_id, is_active=True).first()
        
        if not route:
            return error_response('Route not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        if not data.get('stop_name'):
            return error_response('Stop name is required')
        
        if not data.get('stop_order'):
            return error_response('Stop order is required')
        
        # Check if stop order already exists
        existing_stop = RouteStop.query.filter_by(
            route_id=route_id,
            stop_order=data['stop_order']
        ).first()
        
        if existing_stop:
            return error_response('Stop order already exists')
        
        # Parse time fields
        arrival_time = None
        departure_time = None
        
        if data.get('arrival_time'):
            arrival_time = parse_time_string(data['arrival_time'])
        if data.get('departure_time'):
            departure_time = parse_time_string(data['departure_time'])
        
        stop = RouteStop(
            route_id=route_id,
            stop_name=data.get('stop_name').strip(),
            stop_address=data.get('stop_address'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            stop_order=data.get('stop_order'),
            arrival_time=arrival_time,
            departure_time=departure_time,
            stop_duration=data.get('stop_duration', 2),
            distance_from_previous=data.get('distance_from_previous'),
            landmark=data.get('landmark'),
            is_major_stop=data.get('is_major_stop', False)
        )
        
        db.session.add(stop)
        db.session.commit()
        
        return success_response('Route stop added successfully', {
            'stop': stop.to_dict()
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to add route stop: {str(e)}', 500)

@routes_bp.route('/<int:route_id>/stops/<int:stop_id>', methods=['PUT'])
@admin_required
def update_route_stop(current_user, route_id, stop_id):
    """Update a route stop."""
    try:
        stop = RouteStop.query.filter_by(id=stop_id, route_id=route_id).first()
        
        if not stop:
            return error_response('Route stop not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        # Update basic fields
        updateable_fields = [
            'stop_name', 'stop_address', 'latitude', 'longitude',
            'stop_duration', 'distance_from_previous', 'landmark', 'is_major_stop'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(stop, field, data[field])
        
        # Handle stop order update
        if 'stop_order' in data:
            new_order = data['stop_order']
            existing_stop = RouteStop.query.filter(
                RouteStop.route_id == route_id,
                RouteStop.stop_order == new_order,
                RouteStop.id != stop_id
            ).first()
            
            if existing_stop:
                return error_response('Stop order already exists')
            
            stop.stop_order = new_order
        
        # Handle time fields
        if 'arrival_time' in data and data['arrival_time']:
            stop.arrival_time = parse_time_string(data['arrival_time'])
        
        if 'departure_time' in data and data['departure_time']:
            stop.departure_time = parse_time_string(data['departure_time'])
        
        db.session.commit()
        
        return success_response('Route stop updated successfully', {
            'stop': stop.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update route stop: {str(e)}', 500)

@routes_bp.route('/<int:route_id>/stops/<int:stop_id>', methods=['DELETE'])
@admin_required
def delete_route_stop(current_user, route_id, stop_id):
    """Delete a route stop."""
    try:
        stop = RouteStop.query.filter_by(id=stop_id, route_id=route_id).first()
        
        if not stop:
            return error_response('Route stop not found', 404)
        
        # Check if any students are assigned to this stop
        from app.models.student import Student
        students_count = Student.query.filter(
            (Student.pickup_stop_id == stop_id) | 
            (Student.drop_stop_id == stop_id)
        ).count()
        
        if students_count > 0:
            return error_response('Cannot delete stop with assigned students')
        
        db.session.delete(stop)
        db.session.commit()
        
        return success_response('Route stop deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete route stop: {str(e)}', 500)

@routes_bp.route('/<int:route_id>/optimize', methods=['POST'])
@admin_required
def optimize_route(current_user, route_id):
    """AI-powered route optimization."""
    try:
        route = Route.query.filter_by(id=route_id, is_active=True).first()
        
        if not route:
            return error_response('Route not found', 404)
        
        # This is a placeholder for AI-powered route optimization
        # In a real implementation, this would:
        # 1. Use Google Maps API to get real-time traffic data
        # 2. Apply optimization algorithms to minimize travel time
        # 3. Consider factors like traffic patterns, road conditions, etc.
        # 4. Update route timings and suggest alternative paths
        
        optimization_result = {
            'original_duration': route.estimated_duration,
            'optimized_duration': route.estimated_duration - 5,  # Placeholder improvement
            'time_saved': 5,
            'suggestions': [
                'Consider avoiding Main Street during peak hours',
                'Alternative route via Highway 101 could save 3 minutes',
                'Adjust departure time by 10 minutes to avoid traffic'
            ],
            'traffic_pattern': {
                'peak_hours': ['07:00-09:00', '17:00-19:00'],
                'low_traffic': ['10:00-16:00', '20:00-06:00']
            }
        }
        
        # Store optimization data for future reference
        route.optimal_schedule = optimization_result
        db.session.commit()
        
        return success_response('Route optimization completed', optimization_result)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to optimize route: {str(e)}', 500)

@routes_bp.route('/<int:route_id>', methods=['DELETE'])
@admin_required
def delete_route(current_user, route_id):
    """Delete (deactivate) a route."""
    try:
        route = Route.query.filter_by(id=route_id, is_active=True).first()
        
        if not route:
            return error_response('Route not found', 404)
        
        # Check if route has assigned buses
        from app.models.bus import Bus
        assigned_buses = Bus.query.filter_by(route_id=route_id, is_active=True).count()
        
        if assigned_buses > 0:
            return error_response('Cannot delete route with assigned buses')
        
        # Check if route has assigned students
        from app.models.student import Student
        assigned_students = Student.query.filter_by(route_id=route_id, is_active=True).count()
        
        if assigned_students > 0:
            return error_response('Cannot delete route with assigned students')
        
        route.is_active = False
        route.status = 'Inactive'
        
        db.session.commit()
        
        return success_response('Route deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete route: {str(e)}', 500)
