from datetime import datetime, time
from app import db, ma

class Route(db.Model):
    """Bus route model."""
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100), nullable=False)
    route_code = db.Column(db.String(20), nullable=False, unique=True, index=True)
    start_location = db.Column(db.String(200), nullable=False)
    end_location = db.Column(db.String(200), nullable=False)
    
    # Route details
    total_distance = db.Column(db.Float)  # in kilometers
    estimated_duration = db.Column(db.Integer)  # in minutes
    route_type = db.Column(db.Enum('Urban', 'Suburban', 'Highway', name='route_types'), 
                          default='Urban')
    
    # Timing
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    frequency = db.Column(db.Integer, default=1)  # trips per day
    
    # Status
    status = db.Column(db.Enum('Active', 'Inactive', 'Under Maintenance', name='route_status'), 
                      default='Active')
    
    # AI optimization data
    traffic_pattern = db.Column(db.JSON)  # Store traffic data for AI optimization
    optimal_schedule = db.Column(db.JSON)  # AI-suggested optimal timings
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stops = db.relationship('RouteStop', backref='route', lazy='dynamic', 
                           cascade='all, delete-orphan', order_by='RouteStop.stop_order')
    buses = db.relationship('Bus', backref='route', lazy='dynamic')
    trips = db.relationship('Trip', backref='route', lazy='dynamic')
    students = db.relationship('Student', backref='route', lazy='dynamic')
    
    @property
    def total_stops(self):
        """Get total number of stops."""
        return self.stops.count()
    
    @property
    def assigned_buses_count(self):
        """Get number of assigned buses."""
        return self.buses.filter_by(is_active=True).count()
    
    @property
    def enrolled_students_count(self):
        """Get number of enrolled students."""
        return self.students.filter_by(is_active=True).count()
    
    def get_stops_list(self):
        """Get ordered list of stops."""
        return [stop.to_dict() for stop in self.stops.order_by(RouteStop.stop_order).all()]
    
    def to_dict(self):
        """Convert route to dictionary."""
        return {
            'id': self.id,
            'route_name': self.route_name,
            'route_code': self.route_code,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'total_distance': self.total_distance,
            'estimated_duration': self.estimated_duration,
            'route_type': self.route_type,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'frequency': self.frequency,
            'status': self.status,
            'total_stops': self.total_stops,
            'assigned_buses_count': self.assigned_buses_count,
            'enrolled_students_count': self.enrolled_students_count,
            'stops': self.get_stops_list(),
            'traffic_pattern': self.traffic_pattern,
            'optimal_schedule': self.optimal_schedule,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Route {self.route_code}: {self.route_name}>'

class RouteStop(db.Model):
    """Route stop model."""
    __tablename__ = 'route_stops'
    
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stop_order = db.Column(db.Integer, nullable=False)
    
    # Timing
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    stop_duration = db.Column(db.Integer, default=2)  # minutes
    
    # Distance from previous stop
    distance_from_previous = db.Column(db.Float)  # in kilometers
    
    # Stop details
    landmark = db.Column(db.String(100))
    is_major_stop = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='pickup_stop', lazy='dynamic')
    
    @property
    def student_count(self):
        """Get number of students at this stop."""
        return self.students.filter_by(is_active=True).count()
    
    def to_dict(self):
        """Convert route stop to dictionary."""
        return {
            'id': self.id,
            'route_id': self.route_id,
            'stop_name': self.stop_name,
            'stop_address': self.stop_address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'stop_order': self.stop_order,
            'arrival_time': self.arrival_time.strftime('%H:%M') if self.arrival_time else None,
            'departure_time': self.departure_time.strftime('%H:%M') if self.departure_time else None,
            'stop_duration': self.stop_duration,
            'distance_from_previous': self.distance_from_previous,
            'landmark': self.landmark,
            'is_major_stop': self.is_major_stop,
            'student_count': self.student_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<RouteStop {self.stop_name} (Order: {self.stop_order})>'

class RouteSchema(ma.SQLAlchemyAutoSchema):
    """Route serialization schema."""
    class Meta:
        model = Route
        load_instance = True
        include_fk = True

class RouteStopSchema(ma.SQLAlchemyAutoSchema):
    """Route stop serialization schema."""
    class Meta:
        model = RouteStop
        load_instance = True
        include_fk = True

route_schema = RouteSchema()
routes_schema = RouteSchema(many=True)
route_stop_schema = RouteStopSchema()
route_stops_schema = RouteStopSchema(many=True)
