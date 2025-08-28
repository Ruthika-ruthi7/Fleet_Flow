from datetime import datetime
from app import db, ma

class Notification(db.Model):
    """Notification model for SMS/Email alerts."""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Notification details
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.Enum('SMS', 'Email', 'Push', 'In-App', name='notification_types'), 
                                 nullable=False)
    
    # Categorization
    category = db.Column(db.Enum('Delay', 'Breakdown', 'Fee Reminder', 'Attendance', 'Maintenance', 
                                'General', 'Emergency', name='notification_categories'), 
                        nullable=False, default='General')
    
    # Target audience
    target_type = db.Column(db.Enum('Individual', 'Route', 'Bus', 'All Students', 'All Parents', 
                                   'All Drivers', 'All Staff', name='target_types'), 
                           nullable=False, default='Individual')
    target_id = db.Column(db.Integer)  # ID of route, bus, etc. if applicable
    
    # Delivery details
    recipient_phone = db.Column(db.String(15))
    recipient_email = db.Column(db.String(120))
    
    # Status tracking
    status = db.Column(db.Enum('Pending', 'Sent', 'Delivered', 'Failed', 'Cancelled', 
                              name='notification_status'), default='Pending')
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # External service details
    external_id = db.Column(db.String(100))  # Twilio message SID, etc.
    error_message = db.Column(db.Text)
    
    # Priority and scheduling
    priority = db.Column(db.Enum('Low', 'Medium', 'High', 'Urgent', name='priority_levels'), 
                        default='Medium')
    scheduled_at = db.Column(db.DateTime)  # For scheduled notifications
    
    # Template and personalization
    template_name = db.Column(db.String(50))
    template_data = db.Column(db.JSON)  # Data for template variables
    
    # Read status (for in-app notifications)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def is_delivered(self):
        """Check if notification was delivered."""
        return self.status == 'Delivered'
    
    @property
    def is_failed(self):
        """Check if notification failed."""
        return self.status == 'Failed'
    
    @property
    def delivery_time_minutes(self):
        """Calculate delivery time in minutes."""
        if self.sent_at and self.delivered_at:
            delta = self.delivered_at - self.sent_at
            return int(delta.total_seconds() / 60)
        return None
    
    def mark_as_sent(self, external_id=None):
        """Mark notification as sent."""
        self.status = 'Sent'
        self.sent_at = datetime.utcnow()
        if external_id:
            self.external_id = external_id
    
    def mark_as_delivered(self):
        """Mark notification as delivered."""
        self.status = 'Delivered'
        self.delivered_at = datetime.utcnow()
    
    def mark_as_failed(self, error_message=None):
        """Mark notification as failed."""
        self.status = 'Failed'
        if error_message:
            self.error_message = error_message
    
    def mark_as_read(self):
        """Mark in-app notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else None,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'category': self.category,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'recipient_phone': self.recipient_phone,
            'recipient_email': self.recipient_email,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'external_id': self.external_id,
            'error_message': self.error_message,
            'priority': self.priority,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'template_name': self.template_name,
            'template_data': self.template_data,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'is_delivered': self.is_delivered,
            'is_failed': self.is_failed,
            'delivery_time_minutes': self.delivery_time_minutes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.title} - {self.status}>'

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    """Notification serialization schema."""
    class Meta:
        model = Notification
        load_instance = True
        include_fk = True

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
