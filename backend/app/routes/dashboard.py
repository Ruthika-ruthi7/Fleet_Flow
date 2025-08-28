from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, timedelta
from sqlalchemy import func
from app import db
from app.models.student import Student
from app.models.bus import Bus
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.attendance import Attendance
from app.models.fee import Fee
from app.models.maintenance import Maintenance
from app.utils.helpers import success_response, error_response

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get overall dashboard statistics"""
    try:
        # Basic counts
        total_students = Student.query.count()
        total_buses = Bus.query.count()
        total_drivers = Driver.query.count()
        
        # Active trips today
        today = date.today()
        active_trips = Trip.query.filter(
            func.date(Trip.start_time) == today,
            Trip.status.in_(['scheduled', 'in_progress'])
        ).count()
        
        # Attendance rate for today
        today_attendance = Attendance.query.filter(
            func.date(Attendance.timestamp) == today
        ).all()
        
        if today_attendance:
            present_count = len([a for a in today_attendance if a.status in ['present', 'boarded']])
            attendance_rate = round((present_count / len(today_attendance)) * 100, 2)
        else:
            attendance_rate = 0
        
        # Fee collection stats
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        monthly_fees = Fee.query.filter_by(month=current_month, year=current_year).all()
        total_monthly_amount = sum([float(f.amount) for f in monthly_fees if f.amount])
        collected_amount = sum([float(f.amount) for f in monthly_fees if f.status == 'paid' and f.amount])
        collection_rate = round((collected_amount / total_monthly_amount) * 100, 2) if total_monthly_amount > 0 else 0
        
        # Maintenance alerts
        upcoming_maintenance = Maintenance.query.filter(
            Maintenance.next_maintenance_date <= (datetime.now() + timedelta(days=7)),
            Maintenance.status.in_(['scheduled', 'pending'])
        ).count()
        
        stats_data = {
            'total_students': total_students,
            'total_buses': total_buses,
            'total_drivers': total_drivers,
            'active_trips_today': active_trips,
            'attendance_rate_today': attendance_rate,
            'monthly_collection_rate': collection_rate,
            'upcoming_maintenance_alerts': upcoming_maintenance,
            'total_monthly_fees': total_monthly_amount,
            'collected_fees': collected_amount
        }
        
        return success_response(stats_data)
    except Exception as e:
        return error_response(f"Error fetching dashboard stats: {str(e)}")

@dashboard_bp.route('/recent-activities', methods=['GET'])
@jwt_required()
def get_recent_activities():
    """Get recent activities for dashboard"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Recent trips
        recent_trips = Trip.query.order_by(Trip.created_at.desc()).limit(limit).all()
        
        # Recent attendance records
        recent_attendance = Attendance.query.order_by(Attendance.created_at.desc()).limit(limit).all()
        
        # Recent fee payments
        recent_payments = Fee.query.filter_by(status='paid').order_by(Fee.paid_date.desc()).limit(limit).all()
        
        activities = []
        
        # Add trip activities
        for trip in recent_trips:
            activities.append({
                'type': 'trip',
                'description': f"Trip {trip.id} - {trip.status}",
                'timestamp': trip.created_at.isoformat() if trip.created_at else None,
                'details': {
                    'trip_id': trip.id,
                    'bus_id': trip.bus_id,
                    'status': trip.status
                }
            })
        
        # Add attendance activities
        for attendance in recent_attendance:
            activities.append({
                'type': 'attendance',
                'description': f"Student {attendance.student_id} - {attendance.status}",
                'timestamp': attendance.created_at.isoformat() if attendance.created_at else None,
                'details': {
                    'student_id': attendance.student_id,
                    'status': attendance.status,
                    'trip_id': attendance.trip_id
                }
            })
        
        # Add payment activities
        for payment in recent_payments:
            activities.append({
                'type': 'payment',
                'description': f"Fee payment - Student {payment.student_id}",
                'timestamp': payment.paid_date.isoformat() if payment.paid_date else None,
                'details': {
                    'student_id': payment.student_id,
                    'amount': float(payment.amount) if payment.amount else None,
                    'month': payment.month,
                    'year': payment.year
                }
            })
        
        # Sort activities by timestamp (most recent first)
        activities.sort(key=lambda x: x['timestamp'] or '', reverse=True)
        
        return success_response(activities[:limit])
    except Exception as e:
        return error_response(f"Error fetching recent activities: {str(e)}")

@dashboard_bp.route('/attendance-trends', methods=['GET'])
@jwt_required()
def get_attendance_trends():
    """Get attendance trends for the last 7 days"""
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=6)  # Last 7 days including today
        
        trends = []
        current_date = start_date
        
        while current_date <= end_date:
            # Get attendance for this date
            day_attendance = Attendance.query.filter(
                func.date(Attendance.timestamp) == current_date
            ).all()
            
            if day_attendance:
                present_count = len([a for a in day_attendance if a.status in ['present', 'boarded']])
                total_count = len(day_attendance)
                attendance_rate = round((present_count / total_count) * 100, 2)
            else:
                present_count = 0
                total_count = 0
                attendance_rate = 0
            
            trends.append({
                'date': current_date.isoformat(),
                'present_count': present_count,
                'total_count': total_count,
                'attendance_rate': attendance_rate
            })
            
            current_date += timedelta(days=1)
        
        return success_response(trends)
    except Exception as e:
        return error_response(f"Error fetching attendance trends: {str(e)}")

@dashboard_bp.route('/fee-collection-trends', methods=['GET'])
@jwt_required()
def get_fee_collection_trends():
    """Get fee collection trends for the last 6 months"""
    try:
        trends = []
        current_date = datetime.now()
        
        for i in range(6):
            # Calculate month and year
            month = current_date.month
            year = current_date.year
            
            # Get fees for this month
            monthly_fees = Fee.query.filter_by(month=month, year=year).all()
            
            total_amount = sum([float(f.amount) for f in monthly_fees if f.amount])
            collected_amount = sum([float(f.amount) for f in monthly_fees if f.status == 'paid' and f.amount])
            collection_rate = round((collected_amount / total_amount) * 100, 2) if total_amount > 0 else 0
            
            trends.append({
                'month': month,
                'year': year,
                'month_name': current_date.strftime('%B'),
                'total_amount': total_amount,
                'collected_amount': collected_amount,
                'collection_rate': collection_rate
            })
            
            # Move to previous month
            if current_date.month == 1:
                current_date = current_date.replace(year=current_date.year - 1, month=12)
            else:
                current_date = current_date.replace(month=current_date.month - 1)
        
        # Reverse to show oldest to newest
        trends.reverse()
        
        return success_response(trends)
    except Exception as e:
        return error_response(f"Error fetching fee collection trends: {str(e)}")

@dashboard_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """Get system alerts and notifications"""
    try:
        alerts = []
        
        # Maintenance alerts
        upcoming_maintenance = Maintenance.query.filter(
            Maintenance.next_maintenance_date <= (datetime.now() + timedelta(days=7)),
            Maintenance.status.in_(['scheduled', 'pending'])
        ).all()
        
        for maintenance in upcoming_maintenance:
            days_until = (maintenance.next_maintenance_date - datetime.now()).days
            alerts.append({
                'type': 'maintenance',
                'priority': 'high' if days_until <= 2 else 'medium',
                'title': f"Maintenance Due - Bus {maintenance.bus_id}",
                'message': f"Maintenance scheduled in {days_until} days",
                'timestamp': maintenance.next_maintenance_date.isoformat()
            })
        
        # Overdue fees
        today = date.today()
        overdue_fees = Fee.query.filter(
            Fee.due_date < today,
            Fee.status.in_(['pending', 'overdue'])
        ).count()
        
        if overdue_fees > 0:
            alerts.append({
                'type': 'fees',
                'priority': 'medium',
                'title': 'Overdue Fees',
                'message': f"{overdue_fees} fee(s) are overdue",
                'timestamp': today.isoformat()
            })
        
        # Low attendance alert (if today's attendance is below 80%)
        today_attendance = Attendance.query.filter(
            func.date(Attendance.timestamp) == today
        ).all()
        
        if today_attendance:
            present_count = len([a for a in today_attendance if a.status in ['present', 'boarded']])
            attendance_rate = (present_count / len(today_attendance)) * 100
            
            if attendance_rate < 80:
                alerts.append({
                    'type': 'attendance',
                    'priority': 'medium',
                    'title': 'Low Attendance',
                    'message': f"Today's attendance is {attendance_rate:.1f}%",
                    'timestamp': today.isoformat()
                })
        
        # Sort alerts by priority and timestamp
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        alerts.sort(key=lambda x: (priority_order.get(x['priority'], 0), x['timestamp']), reverse=True)
        
        return success_response(alerts)
    except Exception as e:
        return error_response(f"Error fetching alerts: {str(e)}")
