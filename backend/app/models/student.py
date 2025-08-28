from datetime import datetime, date
from app import db, ma

class Student(db.Model):
    """Student model."""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_id = db.Column(db.String(20), nullable=False, unique=True, index=True)
    
    # Personal details
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other', name='gender_types'))
    blood_group = db.Column(db.String(5))
    
    # Academic details
    class_name = db.Column(db.String(20))
    section = db.Column(db.String(10))
    roll_number = db.Column(db.String(20))
    academic_year = db.Column(db.String(10))  # e.g., "2023-24"
    
    # Parent/Guardian details
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(15))
    parent_email = db.Column(db.String(120))
    parent_address = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(15))
    
    # Transport details
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True)
    pickup_stop_id = db.Column(db.Integer, db.ForeignKey('route_stops.id'), nullable=True)
    drop_stop_id = db.Column(db.Integer, db.ForeignKey('route_stops.id'), nullable=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=True)
    seat_number = db.Column(db.String(10))
    
    # Fee details
    monthly_fee = db.Column(db.Decimal(10, 2))
    fee_discount = db.Column(db.Decimal(5, 2), default=0.0)  # percentage
    scholarship_type = db.Column(db.String(50))
    
    # Status
    transport_status = db.Column(db.Enum('Active', 'Inactive', 'Suspended', 'Graduated', 
                                        name='transport_status'), default='Active')
    enrollment_date = db.Column(db.Date, default=date.today)
    
    # QR Code for attendance
    qr_code = db.Column(db.String(100), unique=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bus = db.relationship('Bus', backref='students')
    drop_stop = db.relationship('RouteStop', foreign_keys=[drop_stop_id], backref='drop_students')
    attendance_records = db.relationship('Attendance', backref='student', lazy='dynamic')
    fee_records = db.relationship('Fee', backref='student', lazy='dynamic')
    
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
    def effective_monthly_fee(self):
        """Calculate effective monthly fee after discount."""
        if self.monthly_fee and self.fee_discount:
            discount_amount = (self.monthly_fee * self.fee_discount) / 100
            return self.monthly_fee - discount_amount
        return self.monthly_fee or 0
    
    @property
    def current_month_attendance_percentage(self):
        """Calculate current month attendance percentage."""
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        total_days = self.attendance_records.filter(
            db.extract('month', Attendance.date) == current_month,
            db.extract('year', Attendance.date) == current_year
        ).count()
        
        if total_days == 0:
            return 100.0
        
        present_days = self.attendance_records.filter(
            db.extract('month', Attendance.date) == current_month,
            db.extract('year', Attendance.date) == current_year,
            Attendance.status == 'Present'
        ).count()
        
        return round((present_days / total_days) * 100, 2)
    
    def generate_qr_code(self):
        """Generate unique QR code for student."""
        import uuid
        self.qr_code = f"STU_{self.student_id}_{uuid.uuid4().hex[:8].upper()}"
        return self.qr_code
    
    def to_dict(self):
        """Convert student to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'full_name': self.full_name,
            'email': self.user.email if self.user else None,
            'phone': self.user.phone if self.user else None,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'class_name': self.class_name,
            'section': self.section,
            'roll_number': self.roll_number,
            'academic_year': self.academic_year,
            'parent_name': self.parent_name,
            'parent_phone': self.parent_phone,
            'parent_email': self.parent_email,
            'parent_address': self.parent_address,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'route_id': self.route_id,
            'route_name': self.route.route_name if self.route else None,
            'pickup_stop_id': self.pickup_stop_id,
            'pickup_stop_name': self.pickup_stop.stop_name if self.pickup_stop else None,
            'drop_stop_id': self.drop_stop_id,
            'drop_stop_name': self.drop_stop.stop_name if self.drop_stop else None,
            'bus_id': self.bus_id,
            'bus_number': self.bus.bus_number if self.bus else None,
            'seat_number': self.seat_number,
            'monthly_fee': float(self.monthly_fee) if self.monthly_fee else None,
            'fee_discount': float(self.fee_discount) if self.fee_discount else 0.0,
            'effective_monthly_fee': float(self.effective_monthly_fee),
            'scholarship_type': self.scholarship_type,
            'transport_status': self.transport_status,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'qr_code': self.qr_code,
            'current_month_attendance_percentage': self.current_month_attendance_percentage,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.full_name}>'

class StudentSchema(ma.SQLAlchemyAutoSchema):
    """Student serialization schema."""
    class Meta:
        model = Student
        load_instance = True
        include_fk = True

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
