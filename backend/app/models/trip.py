from datetime import datetime
from app import db, ma

class Trip(db.Model):
    """Trip model for tracking bus journeys."""
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    conductor_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    
    # Trip details
    trip_date = db.Column(db.Date, nullable=False)
    trip_type = db.Column(db.Enum('Morning', 'Evening', 'Special', name='trip_types'), 
                         nullable=False, default='Morning')
    
    # Timing
    scheduled_start_time = db.Column(db.DateTime)
    actual_start_time = db.Column(db.DateTime)
    scheduled_end_time = db.Column(db.DateTime)
    actual_end_time = db.Column(db.DateTime)
    
    # Distance and fuel
    start_odometer = db.Column(db.Float)
    end_odometer = db.Column(db.Float)
    fuel_consumed = db.Column(db.Float)
    
    # Status
    status = db.Column(db.Enum('Scheduled', 'In Progress', 'Completed', 'Cancelled', 'Delayed', 
                              name='trip_status'), default='Scheduled')
    
    # Performance metrics
    total_students_boarded = db.Column(db.Integer, default=0)
    delay_minutes = db.Column(db.Integer, default=0)
    
    # Notes and issues
    notes = db.Column(db.Text)
    issues_reported = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conductor = db.relationship('Driver', foreign_keys=[conductor_id], backref='conducted_trips')
    attendance_records = db.relationship('Attendance', backref='trip', lazy='dynamic')
    
    @property
    def distance_covered(self):
        """Calculate distance covered in this trip."""
        if self.start_odometer and self.end_odometer:
            return self.end_odometer - self.start_odometer
        return 0
    
    @property
    def duration_minutes(self):
        """Calculate trip duration in minutes."""
        if self.actual_start_time and self.actual_end_time:
            delta = self.actual_end_time - self.actual_start_time
            return int(delta.total_seconds() / 60)
        return 0
    
    @property
    def is_on_time(self):
        """Check if trip was on time."""
        return self.delay_minutes <= 5  # Consider 5 minutes tolerance
    
    @property
    def fuel_efficiency(self):
        """Calculate fuel efficiency (km per liter)."""
        if self.fuel_consumed and self.fuel_consumed > 0 and self.distance_covered > 0:
            return round(self.distance_covered / self.fuel_consumed, 2)
        return 0
    
    def to_dict(self):
        """Convert trip to dictionary."""
        return {
            'id': self.id,
            'bus_id': self.bus_id,
            'bus_number': self.bus.bus_number if self.bus else None,
            'route_id': self.route_id,
            'route_name': self.route.route_name if self.route else None,
            'driver_id': self.driver_id,
            'driver_name': self.driver.full_name if self.driver else None,
            'conductor_id': self.conductor_id,
            'conductor_name': self.conductor.full_name if self.conductor else None,
            'trip_date': self.trip_date.isoformat() if self.trip_date else None,
            'trip_type': self.trip_type,
            'scheduled_start_time': self.scheduled_start_time.isoformat() if self.scheduled_start_time else None,
            'actual_start_time': self.actual_start_time.isoformat() if self.actual_start_time else None,
            'scheduled_end_time': self.scheduled_end_time.isoformat() if self.scheduled_end_time else None,
            'actual_end_time': self.actual_end_time.isoformat() if self.actual_end_time else None,
            'start_odometer': self.start_odometer,
            'end_odometer': self.end_odometer,
            'distance_covered': self.distance_covered,
            'fuel_consumed': self.fuel_consumed,
            'fuel_efficiency': self.fuel_efficiency,
            'status': self.status,
            'total_students_boarded': self.total_students_boarded,
            'delay_minutes': self.delay_minutes,
            'is_on_time': self.is_on_time,
            'duration_minutes': self.duration_minutes,
            'notes': self.notes,
            'issues_reported': self.issues_reported,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Trip {self.id}: {self.bus.bus_number if self.bus else "N/A"} - {self.trip_date}>'

class TripSchema(ma.SQLAlchemyAutoSchema):
    """Trip serialization schema."""
    class Meta:
        model = Trip
        load_instance = True
        include_fk = True

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
