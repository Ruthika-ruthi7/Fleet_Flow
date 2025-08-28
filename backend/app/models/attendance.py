from datetime import datetime, date
from app import db, ma

class Attendance(db.Model):
    """Student attendance model."""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    
    # Attendance details
    date = db.Column(db.Date, nullable=False, default=date.today)
    trip_type = db.Column(db.Enum('Morning', 'Evening', name='trip_types'), nullable=False)
    
    # Boarding details
    boarding_time = db.Column(db.DateTime)
    boarding_stop_id = db.Column(db.Integer, db.ForeignKey('route_stops.id'))
    alighting_time = db.Column(db.DateTime)
    alighting_stop_id = db.Column(db.Integer, db.ForeignKey('route_stops.id'))
    
    # Status
    status = db.Column(db.Enum('Present', 'Absent', 'Late', 'Left Early', name='attendance_status'), 
                      nullable=False, default='Present')
    
    # Method of marking attendance
    marking_method = db.Column(db.Enum('QR Code', 'Manual', 'Biometric', 'RFID', name='marking_methods'), 
                              default='Manual')
    
    # Location data
    boarding_location_lat = db.Column(db.Float)
    boarding_location_lng = db.Column(db.Float)
    
    # Additional details
    notes = db.Column(db.String(200))
    marked_by_driver = db.Column(db.Boolean, default=False)
    marked_by_conductor = db.Column(db.Boolean, default=False)
    
    # Parent notification
    parent_notified = db.Column(db.Boolean, default=False)
    notification_time = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bus = db.relationship('Bus', backref='attendance_records')
    route = db.relationship('Route', backref='attendance_records')
    boarding_stop = db.relationship('RouteStop', foreign_keys=[boarding_stop_id], 
                                   backref='boarding_attendance')
    alighting_stop = db.relationship('RouteStop', foreign_keys=[alighting_stop_id], 
                                    backref='alighting_attendance')
    
    # Composite unique constraint to prevent duplicate entries
    __table_args__ = (db.UniqueConstraint('student_id', 'trip_id', 'trip_type', 
                                         name='unique_student_trip_attendance'),)
    
    @property
    def duration_minutes(self):
        """Calculate journey duration in minutes."""
        if self.boarding_time and self.alighting_time:
            delta = self.alighting_time - self.boarding_time
            return int(delta.total_seconds() / 60)
        return 0
    
    @property
    def is_late(self):
        """Check if student was late."""
        return self.status == 'Late'
    
    @property
    def is_present(self):
        """Check if student was present."""
        return self.status == 'Present'
    
    def to_dict(self):
        """Convert attendance to dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_number': self.student.student_id if self.student else None,
            'trip_id': self.trip_id,
            'bus_id': self.bus_id,
            'bus_number': self.bus.bus_number if self.bus else None,
            'route_id': self.route_id,
            'route_name': self.route.route_name if self.route else None,
            'date': self.date.isoformat() if self.date else None,
            'trip_type': self.trip_type,
            'boarding_time': self.boarding_time.isoformat() if self.boarding_time else None,
            'boarding_stop_id': self.boarding_stop_id,
            'boarding_stop_name': self.boarding_stop.stop_name if self.boarding_stop else None,
            'alighting_time': self.alighting_time.isoformat() if self.alighting_time else None,
            'alighting_stop_id': self.alighting_stop_id,
            'alighting_stop_name': self.alighting_stop.stop_name if self.alighting_stop else None,
            'status': self.status,
            'marking_method': self.marking_method,
            'boarding_location': {
                'lat': self.boarding_location_lat,
                'lng': self.boarding_location_lng
            } if self.boarding_location_lat and self.boarding_location_lng else None,
            'duration_minutes': self.duration_minutes,
            'notes': self.notes,
            'marked_by_driver': self.marked_by_driver,
            'marked_by_conductor': self.marked_by_conductor,
            'parent_notified': self.parent_notified,
            'notification_time': self.notification_time.isoformat() if self.notification_time else None,
            'is_late': self.is_late,
            'is_present': self.is_present,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_attendance_percentage(student_id, start_date=None, end_date=None):
        """Calculate attendance percentage for a student."""
        query = Attendance.query.filter_by(student_id=student_id)
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        total_days = query.count()
        if total_days == 0:
            return 100.0
        
        present_days = query.filter(Attendance.status.in_(['Present', 'Late'])).count()
        return round((present_days / total_days) * 100, 2)
    
    def __repr__(self):
        return f'<Attendance {self.student.student_id if self.student else "N/A"} - {self.date} - {self.status}>'

class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    """Attendance serialization schema."""
    class Meta:
        model = Attendance
        load_instance = True
        include_fk = True

attendance_schema = AttendanceSchema()
attendances_schema = AttendanceSchema(many=True)
