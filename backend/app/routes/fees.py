from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from app import db
from app.models.fee import Fee
from app.models.student import Student
from app.utils.helpers import success_response, error_response

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/', methods=['GET'])
@jwt_required()
def get_fees():
    """Get all fee records"""
    try:
        # Get query parameters for filtering
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        month = request.args.get('month')
        year = request.args.get('year')
        
        query = Fee.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if month:
            query = query.filter_by(month=int(month))
        if year:
            query = query.filter_by(year=int(year))
        
        fees = query.all()
        fees_data = []
        for fee in fees:
            fees_data.append({
                'id': fee.id,
                'student_id': fee.student_id,
                'amount': float(fee.amount) if fee.amount else None,
                'month': fee.month,
                'year': fee.year,
                'status': fee.status,
                'due_date': fee.due_date.isoformat() if fee.due_date else None,
                'paid_date': fee.paid_date.isoformat() if fee.paid_date else None,
                'payment_method': fee.payment_method,
                'transaction_id': fee.transaction_id,
                'created_at': fee.created_at.isoformat() if fee.created_at else None
            })
        return success_response(fees_data)
    except Exception as e:
        return error_response(f"Error fetching fees: {str(e)}")

@fees_bp.route('/<int:fee_id>', methods=['GET'])
@jwt_required()
def get_fee(fee_id):
    """Get a specific fee record"""
    try:
        fee = Fee.query.get_or_404(fee_id)
        fee_data = {
            'id': fee.id,
            'student_id': fee.student_id,
            'amount': float(fee.amount) if fee.amount else None,
            'month': fee.month,
            'year': fee.year,
            'status': fee.status,
            'due_date': fee.due_date.isoformat() if fee.due_date else None,
            'paid_date': fee.paid_date.isoformat() if fee.paid_date else None,
            'payment_method': fee.payment_method,
            'transaction_id': fee.transaction_id,
            'created_at': fee.created_at.isoformat() if fee.created_at else None
        }
        return success_response(fee_data)
    except Exception as e:
        return error_response(f"Error fetching fee: {str(e)}")

@fees_bp.route('/', methods=['POST'])
@jwt_required()
def create_fee():
    """Create a new fee record"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'amount', 'month', 'year']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Missing required field: {field}")
        
        # Validate month and year
        if not (1 <= data['month'] <= 12):
            return error_response("Month must be between 1 and 12")
        
        if data['year'] < 2020 or data['year'] > 2030:
            return error_response("Year must be between 2020 and 2030")
        
        # Check if fee already exists for this student, month, and year
        existing_fee = Fee.query.filter_by(
            student_id=data['student_id'],
            month=data['month'],
            year=data['year']
        ).first()
        
        if existing_fee:
            return error_response("Fee record already exists for this student, month, and year")
        
        # Create new fee record
        fee = Fee(
            student_id=data['student_id'],
            amount=data['amount'],
            month=data['month'],
            year=data['year'],
            status=data.get('status', 'pending'),
            due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None,
            payment_method=data.get('payment_method'),
            transaction_id=data.get('transaction_id')
        )
        
        db.session.add(fee)
        db.session.commit()
        
        return success_response({
            'id': fee.id,
            'student_id': fee.student_id,
            'amount': float(fee.amount),
            'month': fee.month,
            'year': fee.year,
            'message': 'Fee record created successfully'
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating fee: {str(e)}")

@fees_bp.route('/<int:fee_id>', methods=['PUT'])
@jwt_required()
def update_fee(fee_id):
    """Update a fee record"""
    try:
        fee = Fee.query.get_or_404(fee_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'amount' in data:
            fee.amount = data['amount']
        if 'status' in data:
            valid_statuses = ['pending', 'paid', 'overdue', 'cancelled']
            if data['status'] not in valid_statuses:
                return error_response(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            fee.status = data['status']
        if 'due_date' in data:
            fee.due_date = datetime.fromisoformat(data['due_date']).date() if data['due_date'] else None
        if 'paid_date' in data:
            fee.paid_date = datetime.fromisoformat(data['paid_date']).date() if data['paid_date'] else None
        if 'payment_method' in data:
            fee.payment_method = data['payment_method']
        if 'transaction_id' in data:
            fee.transaction_id = data['transaction_id']
        
        db.session.commit()
        
        return success_response({
            'id': fee.id,
            'status': fee.status,
            'message': 'Fee record updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating fee: {str(e)}")

@fees_bp.route('/<int:fee_id>', methods=['DELETE'])
@jwt_required()
def delete_fee(fee_id):
    """Delete a fee record"""
    try:
        fee = Fee.query.get_or_404(fee_id)
        db.session.delete(fee)
        db.session.commit()
        
        return success_response({'message': 'Fee record deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting fee: {str(e)}")

@fees_bp.route('/<int:fee_id>/pay', methods=['POST'])
@jwt_required()
def pay_fee(fee_id):
    """Mark a fee as paid"""
    try:
        fee = Fee.query.get_or_404(fee_id)
        data = request.get_json()
        
        fee.status = 'paid'
        fee.paid_date = date.today()
        fee.payment_method = data.get('payment_method', 'cash')
        fee.transaction_id = data.get('transaction_id')
        
        db.session.commit()
        
        return success_response({
            'id': fee.id,
            'status': fee.status,
            'paid_date': fee.paid_date.isoformat(),
            'message': 'Fee payment recorded successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error recording fee payment: {str(e)}")

@fees_bp.route('/student/<int:student_id>/summary', methods=['GET'])
@jwt_required()
def get_student_fee_summary(student_id):
    """Get fee summary for a specific student"""
    try:
        fees = Fee.query.filter_by(student_id=student_id).all()
        
        total_fees = len(fees)
        paid_fees = len([f for f in fees if f.status == 'paid'])
        pending_fees = len([f for f in fees if f.status == 'pending'])
        overdue_fees = len([f for f in fees if f.status == 'overdue'])
        
        total_amount = sum([float(f.amount) for f in fees if f.amount])
        paid_amount = sum([float(f.amount) for f in fees if f.status == 'paid' and f.amount])
        pending_amount = sum([float(f.amount) for f in fees if f.status in ['pending', 'overdue'] and f.amount])
        
        summary_data = {
            'student_id': student_id,
            'total_fees': total_fees,
            'paid_fees': paid_fees,
            'pending_fees': pending_fees,
            'overdue_fees': overdue_fees,
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'pending_amount': pending_amount
        }
        
        return success_response(summary_data)
    except Exception as e:
        return error_response(f"Error fetching fee summary: {str(e)}")

@fees_bp.route('/overdue', methods=['GET'])
@jwt_required()
def get_overdue_fees():
    """Get all overdue fees"""
    try:
        today = date.today()
        overdue_fees = Fee.query.filter(
            Fee.due_date < today,
            Fee.status.in_(['pending', 'overdue'])
        ).all()
        
        fees_data = []
        for fee in overdue_fees:
            fees_data.append({
                'id': fee.id,
                'student_id': fee.student_id,
                'amount': float(fee.amount) if fee.amount else None,
                'month': fee.month,
                'year': fee.year,
                'due_date': fee.due_date.isoformat() if fee.due_date else None,
                'days_overdue': (today - fee.due_date).days if fee.due_date else 0
            })
        
        return success_response(fees_data)
    except Exception as e:
        return error_response(f"Error fetching overdue fees: {str(e)}")
