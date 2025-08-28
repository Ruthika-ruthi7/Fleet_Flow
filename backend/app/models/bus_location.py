from datetime import datetime
from app import db

class BusLocation(db.Model):
    """Model for storing bus GPS location data"""
    __tablename__ = 'bus_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)  # Decimal degrees
    longitude = db.Column(db.Numeric(11, 8), nullable=False)  # Decimal degrees
    speed = db.Column(db.Float)  # Speed in km/h
    heading = db.Column(db.Float)  # Direction in degrees (0-360)
    accuracy = db.Column(db.Float)  # GPS accuracy in meters
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    bus = db.relationship('Bus', backref=db.backref('locations', lazy=True))
    
    def __repr__(self):
        return f'<BusLocation {self.bus_id} at ({self.latitude}, {self.longitude})>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'bus_id': self.bus_id,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'speed': self.speed,
            'heading': self.heading,
            'accuracy': self.accuracy,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
