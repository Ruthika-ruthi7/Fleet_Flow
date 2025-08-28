from datetime import datetime, date
from app import db, ma

class Bus(db.Model):
    """Bus model."""
    __tablename__ = 'buses'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), nullable=False, unique=True, index=True)
    registration_number = db.Column(db.String(20), nullable=False, unique=True)
    bus_type = db.Column(db.Enum('AC', 'Non-AC', 'Sleeper', 'Seater', name='bus_types'), 
                         nullable=False, default='Non-AC')
    capacity = db.Column(db.Integer, nullable=False, default=50)
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year_of_manufacture = db.Column(db.Integer)
    fuel_type = db.Column(db.Enum('Diesel', 'Petrol', 'CNG', 'Electric', name='fuel_types'), 
                          default='Diesel')
    mileage = db.Column(db.Float)  # km per liter
    
    # Insurance and documents
    insurance_number = db.Column(db.String(50))
    insurance_expiry = db.Column(db.Date)
    rc_number = db.Column(db.String(50))
    rc_expiry = db.Column(db.Date)
    fitness_certificate_expiry = db.Column(db.Date)
    permit_expiry = db.Column(db.Date)
    
    # Current status
    status = db.Column(db.Enum('Active', 'Maintenance', 'Out of Service', 'Retired', 
                              name='bus_status'), default='Active')
    current_location_lat = db.Column(db.Float)
    current_location_lng = db.Column(db.Float)
    last_location_update = db.Column(db.DateTime)
    
    # Operational details
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    conductor_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    driver = db.relationship('Driver', foreign_keys=[driver_id], backref='assigned_buses')
    conductor = db.relationship('Driver', foreign_keys=[conductor_id], backref='conducted_buses')
    trips = db.relationship('Trip', backref='bus', lazy='dynamic')
    maintenance_records = db.relationship('Maintenance', backref='bus', lazy='dynamic')
    documents = db.relationship('Document', backref='bus', lazy='dynamic')
    
    @property
    def is_insurance_expired(self):
        """Check if insurance is expired."""
        if self.insurance_expiry:
            return date.today() > self.insurance_expiry
        return True
    
    @property
    def is_rc_expired(self):
        """Check if RC is expired."""
        if self.rc_expiry:
            return date.today() > self.rc_expiry
        return True
    
    @property
    def days_to_insurance_expiry(self):
        """Get days until insurance expiry."""
        if self.insurance_expiry:
            delta = self.insurance_expiry - date.today()
            return delta.days if delta.days > 0 else 0
        return 0
    
    @property
    def current_occupancy(self):
        """Get current occupancy count."""
        # This would be calculated based on active trips and student assignments
        return 0  # Placeholder
    
    @property
    def occupancy_percentage(self):
        """Get occupancy percentage."""
        if self.capacity > 0:
            return (self.current_occupancy / self.capacity) * 100
        return 0
    
    def to_dict(self):
        """Convert bus to dictionary."""
        return {
            'id': self.id,
            'bus_number': self.bus_number,
            'registration_number': self.registration_number,
            'bus_type': self.bus_type,
            'capacity': self.capacity,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'year_of_manufacture': self.year_of_manufacture,
            'fuel_type': self.fuel_type,
            'mileage': self.mileage,
            'insurance_number': self.insurance_number,
            'insurance_expiry': self.insurance_expiry.isoformat() if self.insurance_expiry else None,
            'rc_number': self.rc_number,
            'rc_expiry': self.rc_expiry.isoformat() if self.rc_expiry else None,
            'fitness_certificate_expiry': self.fitness_certificate_expiry.isoformat() if self.fitness_certificate_expiry else None,
            'permit_expiry': self.permit_expiry.isoformat() if self.permit_expiry else None,
            'status': self.status,
            'current_location': {
                'lat': self.current_location_lat,
                'lng': self.current_location_lng
            } if self.current_location_lat and self.current_location_lng else None,
            'last_location_update': self.last_location_update.isoformat() if self.last_location_update else None,
            'route_id': self.route_id,
            'driver_id': self.driver_id,
            'conductor_id': self.conductor_id,
            'driver_name': self.driver.full_name if self.driver else None,
            'conductor_name': self.conductor.full_name if self.conductor else None,
            'is_insurance_expired': self.is_insurance_expired,
            'is_rc_expired': self.is_rc_expired,
            'days_to_insurance_expiry': self.days_to_insurance_expiry,
            'current_occupancy': self.current_occupancy,
            'occupancy_percentage': self.occupancy_percentage,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Bus {self.bus_number}>'

class BusSchema(ma.SQLAlchemyAutoSchema):
    """Bus serialization schema."""
    class Meta:
        model = Bus
        load_instance = True
        include_fk = True

bus_schema = BusSchema()
buses_schema = BusSchema(many=True)
