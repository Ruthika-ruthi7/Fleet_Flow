from datetime import datetime, date
from app import db, ma

class Driver(db.Model):
    """Driver/Conductor model."""
    __tablename__ = 'drivers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    employee_id = db.Column(db.String(20), nullable=False, unique=True, index=True)
    driver_type = db.Column(db.Enum('Driver', 'Conductor', name='driver_types'), 
                           nullable=False, default='Driver')
    
    # License information
    license_number = db.Column(db.String(50), nullable=False)
    license_type = db.Column(db.String(20))  # Heavy Vehicle, Light Vehicle, etc.
    license_expiry = db.Column(db.Date)
    
    # Personal details
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other', name='gender_types'))
    blood_group = db.Column(db.String(5))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(15))
    
    # Employment details
    joining_date = db.Column(db.Date, default=date.today)
    salary = db.Column(db.Decimal(10, 2))
    shift_type = db.Column(db.Enum('Morning', 'Evening', 'Full Day', 'Night', name='shift_types'), 
                          default='Full Day')
    shift_start_time = db.Column(db.Time)
    shift_end_time = db.Column(db.Time)
    
    # Performance metrics
    total_trips = db.Column(db.Integer, default=0)
    on_time_trips = db.Column(db.Integer, default=0)
    total_distance = db.Column(db.Float, default=0.0)  # in kilometers
    rating = db.Column(db.Float, default=5.0)  # out of 5
    
    # Current status
    status = db.Column(db.Enum('Available', 'On Trip', 'On Leave', 'Suspended', name='driver_status'), 
                      default='Available')
    current_bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    current_bus = db.relationship('Bus', foreign_keys=[current_bus_id], backref='current_staff')
    trips = db.relationship('Trip', backref='driver', lazy='dynamic')
    
    @property
    def full_name(self):
        """Get full name from user."""
        return self.user.full_name if self.user else ''
    
    @property
    def age(self):
        """Calculate age from date of birth."""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    @property
    def is_license_expired(self):
        """Check if license is expired."""
        if self.license_expiry:
            return date.today() > self.license_expiry
        return True
    
    @property
    def days_to_license_expiry(self):
        """Get days until license expiry."""
        if self.license_expiry:
            delta = self.license_expiry - date.today()
            return delta.days if delta.days > 0 else 0
        return 0
    
    @property
    def on_time_percentage(self):
        """Calculate on-time percentage."""
        if self.total_trips > 0:
            return round((self.on_time_trips / self.total_trips) * 100, 2)
        return 100.0
    
    @property
    def experience_years(self):
        """Calculate years of experience."""
        if self.joining_date:
            today = date.today()
            return today.year - self.joining_date.year
        return 0
    
    def to_dict(self):
        """Convert driver to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employee_id': self.employee_id,
            'driver_type': self.driver_type,
            'full_name': self.full_name,
            'email': self.user.email if self.user else None,
            'phone': self.user.phone if self.user else None,
            'license_number': self.license_number,
            'license_type': self.license_type,
            'license_expiry': self.license_expiry.isoformat() if self.license_expiry else None,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'joining_date': self.joining_date.isoformat() if self.joining_date else None,
            'salary': float(self.salary) if self.salary else None,
            'shift_type': self.shift_type,
            'shift_start_time': self.shift_start_time.strftime('%H:%M') if self.shift_start_time else None,
            'shift_end_time': self.shift_end_time.strftime('%H:%M') if self.shift_end_time else None,
            'total_trips': self.total_trips,
            'on_time_trips': self.on_time_trips,
            'on_time_percentage': self.on_time_percentage,
            'total_distance': self.total_distance,
            'rating': self.rating,
            'status': self.status,
            'current_bus_id': self.current_bus_id,
            'current_bus_number': self.current_bus.bus_number if self.current_bus else None,
            'is_license_expired': self.is_license_expired,
            'days_to_license_expiry': self.days_to_license_expiry,
            'experience_years': self.experience_years,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Driver {self.employee_id}: {self.full_name}>'

class DriverSchema(ma.SQLAlchemyAutoSchema):
    """Driver serialization schema."""
    class Meta:
        model = Driver
        load_instance = True
        include_fk = True

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)
