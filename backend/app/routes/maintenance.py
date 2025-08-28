from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.maintenance import Maintenance
from app.models.bus import Bus
from app.utils.helpers import success_response, error_response

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/', methods=['GET'])
@jwt_required()
def get_maintenance_records():
    """Get all maintenance records"""
    try:
        maintenance_records = Maintenance.query.all()
        records_data = []
        for record in maintenance_records:
            records_data.append({
                'id': record.id,
                'bus_id': record.bus_id,
                'maintenance_type': record.maintenance_type,
                'description': record.description,
                'cost': float(record.cost) if record.cost else None,
                'maintenance_date': record.maintenance_date.isoformat() if record.maintenance_date else None,
                'next_maintenance_date': record.next_maintenance_date.isoformat() if record.next_maintenance_date else None,
                'status': record.status,
                'created_at': record.created_at.isoformat() if record.created_at else None
            })
        return success_response(records_data)
    except Exception as e:
        return error_response(f"Error fetching maintenance records: {str(e)}")

@maintenance_bp.route('/<int:maintenance_id>', methods=['GET'])
@jwt_required()
def get_maintenance_record(maintenance_id):
    """Get a specific maintenance record"""
    try:
        record = Maintenance.query.get_or_404(maintenance_id)
        record_data = {
            'id': record.id,
            'bus_id': record.bus_id,
            'maintenance_type': record.maintenance_type,
            'description': record.description,
            'cost': float(record.cost) if record.cost else None,
            'maintenance_date': record.maintenance_date.isoformat() if record.maintenance_date else None,
            'next_maintenance_date': record.next_maintenance_date.isoformat() if record.next_maintenance_date else None,
            'status': record.status,
            'created_at': record.created_at.isoformat() if record.created_at else None
        }
        return success_response(record_data)
    except Exception as e:
        return error_response(f"Error fetching maintenance record: {str(e)}")

@maintenance_bp.route('/', methods=['POST'])
@jwt_required()
def create_maintenance_record():
    """Create a new maintenance record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['bus_id', 'maintenance_type', 'description']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}")
        
        # Create new maintenance record
        record = Maintenance(
            bus_id=data['bus_id'],
            maintenance_type=data['maintenance_type'],
            description=data['description'],
            cost=data.get('cost'),
            maintenance_date=datetime.fromisoformat(data['maintenance_date']) if data.get('maintenance_date') else datetime.utcnow(),
            next_maintenance_date=datetime.fromisoformat(data['next_maintenance_date']) if data.get('next_maintenance_date') else None,
            status=data.get('status', 'scheduled')
        )
        
        db.session.add(record)
        db.session.commit()
        
        return success_response({
            'id': record.id,
            'bus_id': record.bus_id,
            'maintenance_type': record.maintenance_type,
            'message': 'Maintenance record created successfully'
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating maintenance record: {str(e)}")

@maintenance_bp.route('/<int:maintenance_id>', methods=['PUT'])
@jwt_required()
def update_maintenance_record(maintenance_id):
    """Update a maintenance record"""
    try:
        record = Maintenance.query.get_or_404(maintenance_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'maintenance_type' in data:
            record.maintenance_type = data['maintenance_type']
        if 'description' in data:
            record.description = data['description']
        if 'cost' in data:
            record.cost = data['cost']
        if 'maintenance_date' in data:
            record.maintenance_date = datetime.fromisoformat(data['maintenance_date'])
        if 'next_maintenance_date' in data:
            record.next_maintenance_date = datetime.fromisoformat(data['next_maintenance_date']) if data['next_maintenance_date'] else None
        if 'status' in data:
            record.status = data['status']
        
        db.session.commit()
        
        return success_response({
            'id': record.id,
            'status': record.status,
            'message': 'Maintenance record updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating maintenance record: {str(e)}")

@maintenance_bp.route('/<int:maintenance_id>', methods=['DELETE'])
@jwt_required()
def delete_maintenance_record(maintenance_id):
    """Delete a maintenance record"""
    try:
        record = Maintenance.query.get_or_404(maintenance_id)
        db.session.delete(record)
        db.session.commit()
        
        return success_response({'message': 'Maintenance record deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting maintenance record: {str(e)}")

@maintenance_bp.route('/bus/<int:bus_id>', methods=['GET'])
@jwt_required()
def get_bus_maintenance_history(bus_id):
    """Get maintenance history for a specific bus"""
    try:
        records = Maintenance.query.filter_by(bus_id=bus_id).order_by(Maintenance.maintenance_date.desc()).all()
        records_data = []
        for record in records:
            records_data.append({
                'id': record.id,
                'maintenance_type': record.maintenance_type,
                'description': record.description,
                'cost': float(record.cost) if record.cost else None,
                'maintenance_date': record.maintenance_date.isoformat() if record.maintenance_date else None,
                'status': record.status
            })
        return success_response(records_data)
    except Exception as e:
        return error_response(f"Error fetching bus maintenance history: {str(e)}")

@maintenance_bp.route('/upcoming', methods=['GET'])
@jwt_required()
def get_upcoming_maintenance():
    """Get upcoming maintenance records"""
    try:
        upcoming_records = Maintenance.query.filter(
            Maintenance.next_maintenance_date >= datetime.utcnow(),
            Maintenance.status.in_(['scheduled', 'pending'])
        ).order_by(Maintenance.next_maintenance_date.asc()).all()
        
        records_data = []
        for record in upcoming_records:
            records_data.append({
                'id': record.id,
                'bus_id': record.bus_id,
                'maintenance_type': record.maintenance_type,
                'description': record.description,
                'next_maintenance_date': record.next_maintenance_date.isoformat(),
                'status': record.status
            })
        return success_response(records_data)
    except Exception as e:
        return error_response(f"Error fetching upcoming maintenance: {str(e)}")
