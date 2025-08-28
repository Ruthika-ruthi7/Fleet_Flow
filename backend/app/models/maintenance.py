from datetime import datetime, date
from app import db, ma

class Maintenance(db.Model):
    """Maintenance record model."""
    __tablename__ = 'maintenance'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    
    # Maintenance details
    maintenance_type = db.Column(db.Enum('Routine', 'Preventive', 'Breakdown', 'Emergency', 
                                        name='maintenance_types'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Scheduling
    scheduled_date = db.Column(db.Date)
    actual_date = db.Column(db.Date)
    estimated_duration = db.Column(db.Integer)  # in hours
    actual_duration = db.Column(db.Integer)  # in hours
    
    # Cost details
    labor_cost = db.Column(db.Decimal(10, 2), default=0.0)
    parts_cost = db.Column(db.Decimal(10, 2), default=0.0)
    total_cost = db.Column(db.Decimal(10, 2), default=0.0)
    
    # Service details
    service_provider = db.Column(db.String(100))
    mechanic_name = db.Column(db.String(100))
    odometer_reading = db.Column(db.Float)
    
    # Status
    status = db.Column(db.Enum('Scheduled', 'In Progress', 'Completed', 'Cancelled', 
                              name='maintenance_status'), default='Scheduled')
    priority = db.Column(db.Enum('Low', 'Medium', 'High', 'Critical', name='priority_levels'), 
                        default='Medium')
    
    # Parts and work done
    parts_replaced = db.Column(db.JSON)  # List of parts replaced
    work_performed = db.Column(db.Text)
    
    # Next maintenance prediction
    next_maintenance_date = db.Column(db.Date)
    next_maintenance_odometer = db.Column(db.Float)
    
    # Quality and feedback
    quality_rating = db.Column(db.Integer)  # 1-5 scale
    feedback = db.Column(db.Text)
    
    # Documentation
    invoice_number = db.Column(db.String(50))
    warranty_period = db.Column(db.Integer)  # in months
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_overdue(self):
        """Check if maintenance is overdue."""
        if self.scheduled_date and self.status in ['Scheduled', 'In Progress']:
            return date.today() > self.scheduled_date
        return False
    
    @property
    def days_overdue(self):
        """Get number of days overdue."""
        if self.is_overdue:
            return (date.today() - self.scheduled_date).days
        return 0
    
    @property
    def is_under_warranty(self):
        """Check if maintenance is still under warranty."""
        if self.actual_date and self.warranty_period:
            from dateutil.relativedelta import relativedelta
            warranty_end = self.actual_date + relativedelta(months=self.warranty_period)
            return date.today() <= warranty_end
        return False
    
    @property
    def efficiency_score(self):
        """Calculate maintenance efficiency score."""
        score = 100
        
        # Deduct points for delays
        if self.is_overdue:
            score -= min(self.days_overdue * 2, 30)
        
        # Deduct points for cost overruns (if estimated cost was provided)
        # This would require additional fields for estimated costs
        
        # Add points for quality
        if self.quality_rating:
            score += (self.quality_rating - 3) * 5  # Bonus/penalty based on rating
        
        return max(0, min(100, score))
    
    def calculate_total_cost(self):
        """Calculate and update total cost."""
        self.total_cost = (self.labor_cost or 0) + (self.parts_cost or 0)
        return self.total_cost
    
    def to_dict(self):
        """Convert maintenance record to dictionary."""
        return {
            'id': self.id,
            'bus_id': self.bus_id,
            'bus_number': self.bus.bus_number if self.bus else None,
            'maintenance_type': self.maintenance_type,
            'description': self.description,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'actual_date': self.actual_date.isoformat() if self.actual_date else None,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'labor_cost': float(self.labor_cost) if self.labor_cost else 0.0,
            'parts_cost': float(self.parts_cost) if self.parts_cost else 0.0,
            'total_cost': float(self.total_cost) if self.total_cost else 0.0,
            'service_provider': self.service_provider,
            'mechanic_name': self.mechanic_name,
            'odometer_reading': self.odometer_reading,
            'status': self.status,
            'priority': self.priority,
            'parts_replaced': self.parts_replaced,
            'work_performed': self.work_performed,
            'next_maintenance_date': self.next_maintenance_date.isoformat() if self.next_maintenance_date else None,
            'next_maintenance_odometer': self.next_maintenance_odometer,
            'quality_rating': self.quality_rating,
            'feedback': self.feedback,
            'invoice_number': self.invoice_number,
            'warranty_period': self.warranty_period,
            'is_overdue': self.is_overdue,
            'days_overdue': self.days_overdue,
            'is_under_warranty': self.is_under_warranty,
            'efficiency_score': self.efficiency_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Maintenance {self.id}: {self.bus.bus_number if self.bus else "N/A"} - {self.maintenance_type}>'

class MaintenanceSchema(ma.SQLAlchemyAutoSchema):
    """Maintenance serialization schema."""
    class Meta:
        model = Maintenance
        load_instance = True
        include_fk = True

maintenance_schema = MaintenanceSchema()
maintenances_schema = MaintenanceSchema(many=True)
