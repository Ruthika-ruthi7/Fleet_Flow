from datetime import datetime, date
from app import db, ma

class Fee(db.Model):
    """Student fee management model."""
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # Fee period
    academic_year = db.Column(db.String(10), nullable=False)  # e.g., "2023-24"
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    
    # Fee details
    base_amount = db.Column(db.Decimal(10, 2), nullable=False)
    discount_percentage = db.Column(db.Decimal(5, 2), default=0.0)
    discount_amount = db.Column(db.Decimal(10, 2), default=0.0)
    final_amount = db.Column(db.Decimal(10, 2), nullable=False)
    
    # Payment details
    paid_amount = db.Column(db.Decimal(10, 2), default=0.0)
    payment_date = db.Column(db.Date)
    payment_method = db.Column(db.Enum('Cash', 'Card', 'Online', 'Cheque', 'UPI', 'Bank Transfer', 
                                      name='payment_methods'))
    transaction_id = db.Column(db.String(100))
    receipt_number = db.Column(db.String(50))
    
    # Due date and status
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Pending', 'Paid', 'Partial', 'Overdue', 'Waived', 
                              name='fee_status'), default='Pending')
    
    # Late fee
    late_fee_amount = db.Column(db.Decimal(10, 2), default=0.0)
    late_fee_applied_date = db.Column(db.Date)
    
    # Scholarship/Concession details
    scholarship_type = db.Column(db.String(50))
    scholarship_amount = db.Column(db.Decimal(10, 2), default=0.0)
    concession_reason = db.Column(db.String(200))
    
    # Additional details
    remarks = db.Column(db.String(500))
    collected_by = db.Column(db.String(100))  # Staff member who collected
    
    # Notification tracking
    reminder_sent_count = db.Column(db.Integer, default=0)
    last_reminder_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'academic_year', 'month', 'year', 
                                         name='unique_student_fee_period'),)
    
    @property
    def balance_amount(self):
        """Calculate remaining balance."""
        return float(self.final_amount + self.late_fee_amount - self.paid_amount)
    
    @property
    def is_overdue(self):
        """Check if fee is overdue."""
        return self.status != 'Paid' and date.today() > self.due_date
    
    @property
    def days_overdue(self):
        """Get number of days overdue."""
        if self.is_overdue:
            return (date.today() - self.due_date).days
        return 0
    
    @property
    def payment_percentage(self):
        """Calculate payment percentage."""
        total_due = float(self.final_amount + self.late_fee_amount)
        if total_due > 0:
            return round((float(self.paid_amount) / total_due) * 100, 2)
        return 0.0
    
    @property
    def effective_discount_percentage(self):
        """Calculate effective discount percentage including scholarship."""
        total_discount = float(self.discount_amount + self.scholarship_amount)
        if self.base_amount > 0:
            return round((total_discount / float(self.base_amount)) * 100, 2)
        return 0.0
    
    def calculate_late_fee(self, late_fee_per_day=10.0, max_late_fee=500.0):
        """Calculate and apply late fee."""
        if self.is_overdue and self.late_fee_amount == 0:
            late_fee = min(self.days_overdue * late_fee_per_day, max_late_fee)
            self.late_fee_amount = late_fee
            self.late_fee_applied_date = date.today()
            return late_fee
        return 0
    
    def update_status(self):
        """Update fee status based on payment."""
        total_due = float(self.final_amount + self.late_fee_amount)
        
        if self.paid_amount >= total_due:
            self.status = 'Paid'
        elif self.paid_amount > 0:
            self.status = 'Partial'
        elif self.is_overdue:
            self.status = 'Overdue'
        else:
            self.status = 'Pending'
    
    def to_dict(self):
        """Convert fee to dictionary."""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_number': self.student.student_id if self.student else None,
            'student_class': self.student.class_name if self.student else None,
            'academic_year': self.academic_year,
            'month': self.month,
            'year': self.year,
            'month_name': datetime(self.year, self.month, 1).strftime('%B'),
            'base_amount': float(self.base_amount),
            'discount_percentage': float(self.discount_percentage),
            'discount_amount': float(self.discount_amount),
            'scholarship_type': self.scholarship_type,
            'scholarship_amount': float(self.scholarship_amount),
            'final_amount': float(self.final_amount),
            'late_fee_amount': float(self.late_fee_amount),
            'total_due': float(self.final_amount + self.late_fee_amount),
            'paid_amount': float(self.paid_amount),
            'balance_amount': self.balance_amount,
            'payment_percentage': self.payment_percentage,
            'effective_discount_percentage': self.effective_discount_percentage,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'receipt_number': self.receipt_number,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'is_overdue': self.is_overdue,
            'days_overdue': self.days_overdue,
            'late_fee_applied_date': self.late_fee_applied_date.isoformat() if self.late_fee_applied_date else None,
            'concession_reason': self.concession_reason,
            'remarks': self.remarks,
            'collected_by': self.collected_by,
            'reminder_sent_count': self.reminder_sent_count,
            'last_reminder_date': self.last_reminder_date.isoformat() if self.last_reminder_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_student_fee_summary(student_id, academic_year=None):
        """Get fee summary for a student."""
        query = Fee.query.filter_by(student_id=student_id)
        if academic_year:
            query = query.filter_by(academic_year=academic_year)
        
        fees = query.all()
        
        total_amount = sum(float(fee.final_amount + fee.late_fee_amount) for fee in fees)
        paid_amount = sum(float(fee.paid_amount) for fee in fees)
        balance_amount = total_amount - paid_amount
        overdue_count = sum(1 for fee in fees if fee.is_overdue)
        
        return {
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'balance_amount': balance_amount,
            'overdue_count': overdue_count,
            'total_fees': len(fees),
            'payment_percentage': round((paid_amount / total_amount) * 100, 2) if total_amount > 0 else 0
        }
    
    def __repr__(self):
        return f'<Fee {self.student.student_id if self.student else "N/A"} - {self.academic_year} - {self.month}/{self.year}>'

class FeeSchema(ma.SQLAlchemyAutoSchema):
    """Fee serialization schema."""
    class Meta:
        model = Fee
        load_instance = True
        include_fk = True

fee_schema = FeeSchema()
fees_schema = FeeSchema(many=True)
