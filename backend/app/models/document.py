from datetime import datetime, date
from app import db, ma

class Document(db.Model):
    """Document model for storing bus-related documents."""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    
    # Document details
    document_type = db.Column(db.Enum('Insurance', 'RC', 'Fitness Certificate', 'Permit', 
                                     'Pollution Certificate', 'Tax Receipt', 'Service Record', 
                                     'Other', name='document_types'), nullable=False)
    document_name = db.Column(db.String(200), nullable=False)
    document_number = db.Column(db.String(100))
    
    # File details
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    file_type = db.Column(db.String(50))  # MIME type
    
    # Validity and expiry
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    issuing_authority = db.Column(db.String(200))
    
    # OCR extracted data
    ocr_data = db.Column(db.JSON)  # Extracted text and structured data
    ocr_confidence = db.Column(db.Float)  # OCR confidence score (0-1)
    
    # Verification status
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.String(100))
    verified_at = db.Column(db.DateTime)
    
    # Alert settings
    alert_days_before_expiry = db.Column(db.Integer, default=30)
    last_alert_sent = db.Column(db.Date)
    
    # Additional metadata
    description = db.Column(db.Text)
    tags = db.Column(db.JSON)  # Array of tags for categorization
    
    # Version control
    version = db.Column(db.Integer, default=1)
    parent_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent_document = db.relationship('Document', remote_side=[id], backref='versions')
    
    @property
    def is_expired(self):
        """Check if document is expired."""
        if self.expiry_date:
            return date.today() > self.expiry_date
        return False
    
    @property
    def days_to_expiry(self):
        """Get days until expiry."""
        if self.expiry_date:
            delta = self.expiry_date - date.today()
            return delta.days if delta.days > 0 else 0
        return None
    
    @property
    def is_expiring_soon(self):
        """Check if document is expiring soon."""
        if self.days_to_expiry is not None:
            return self.days_to_expiry <= self.alert_days_before_expiry
        return False
    
    @property
    def file_size_mb(self):
        """Get file size in MB."""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    @property
    def validity_status(self):
        """Get validity status."""
        if self.is_expired:
            return 'Expired'
        elif self.is_expiring_soon:
            return 'Expiring Soon'
        elif self.expiry_date:
            return 'Valid'
        else:
            return 'No Expiry'
    
    def needs_alert(self):
        """Check if alert needs to be sent."""
        if not self.is_expiring_soon:
            return False
        
        if not self.last_alert_sent:
            return True
        
        # Send alert every 7 days when expiring soon
        days_since_last_alert = (date.today() - self.last_alert_sent).days
        return days_since_last_alert >= 7
    
    def mark_alert_sent(self):
        """Mark that alert has been sent."""
        self.last_alert_sent = date.today()
    
    def extract_ocr_data(self, ocr_text, confidence=None):
        """Store OCR extracted data."""
        self.ocr_data = {
            'text': ocr_text,
            'extracted_at': datetime.utcnow().isoformat(),
            'structured_data': self._parse_document_data(ocr_text)
        }
        if confidence:
            self.ocr_confidence = confidence
    
    def _parse_document_data(self, text):
        """Parse structured data from OCR text based on document type."""
        # This would contain logic to extract specific fields based on document type
        # For example, for RC: registration number, owner name, vehicle class, etc.
        # For Insurance: policy number, insurer name, coverage amount, etc.
        structured_data = {}
        
        # Basic parsing logic (would be enhanced with regex patterns)
        if self.document_type == 'RC':
            # Extract registration number, engine number, etc.
            pass
        elif self.document_type == 'Insurance':
            # Extract policy number, insurer, etc.
            pass
        
        return structured_data
    
    def to_dict(self):
        """Convert document to dictionary."""
        return {
            'id': self.id,
            'bus_id': self.bus_id,
            'bus_number': self.bus.bus_number if self.bus else None,
            'document_type': self.document_type,
            'document_name': self.document_name,
            'document_number': self.document_number,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_size_mb': self.file_size_mb,
            'file_type': self.file_type,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'issuing_authority': self.issuing_authority,
            'ocr_data': self.ocr_data,
            'ocr_confidence': self.ocr_confidence,
            'is_verified': self.is_verified,
            'verified_by': self.verified_by,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None,
            'alert_days_before_expiry': self.alert_days_before_expiry,
            'last_alert_sent': self.last_alert_sent.isoformat() if self.last_alert_sent else None,
            'description': self.description,
            'tags': self.tags,
            'version': self.version,
            'parent_document_id': self.parent_document_id,
            'is_expired': self.is_expired,
            'days_to_expiry': self.days_to_expiry,
            'is_expiring_soon': self.is_expiring_soon,
            'validity_status': self.validity_status,
            'needs_alert': self.needs_alert(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Document {self.id}: {self.document_type} - {self.bus.bus_number if self.bus else "N/A"}>'

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    """Document serialization schema."""
    class Meta:
        model = Document
        load_instance = True
        include_fk = True

document_schema = DocumentSchema()
documents_schema = DocumentSchema(many=True)
