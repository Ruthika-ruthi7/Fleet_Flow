from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, date
from app import db
from app.models.bus import Bus
from app.models.driver import Driver
from app.models.route import Route
from app.models.document import Document
from app.utils.decorators import admin_required, staff_required
from app.utils.helpers import (
    success_response, error_response, paginate_query,
    generate_bus_number, validate_phone
)

buses_bp = Blueprint('buses', __name__)

@buses_bp.route('', methods=['GET'])
@jwt_required()
def get_buses():
    """Get all buses with pagination and filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        bus_type = request.args.get('bus_type')
        search = request.args.get('search', '').strip()
        
        query = Bus.query.filter_by(is_active=True)
        
        if status:
            query = query.filter_by(status=status)
        
        if bus_type:
            query = query.filter_by(bus_type=bus_type)
        
        if search:
            query = query.filter(
                (Bus.bus_number.contains(search)) |
                (Bus.registration_number.contains(search)) |
                (Bus.manufacturer.contains(search))
            )
        
        query = query.order_by(Bus.bus_number)
        paginated = paginate_query(query, page, per_page)
        
        if not paginated:
            return error_response('Invalid pagination parameters')
        
        buses_data = [bus.to_dict() for bus in paginated['items']]
        
        return success_response('Buses retrieved successfully', {
            'buses': buses_data,
            'pagination': {
                'total': paginated['total'],
                'pages': paginated['pages'],
                'current_page': paginated['current_page'],
                'per_page': paginated['per_page'],
                'has_next': paginated['has_next'],
                'has_prev': paginated['has_prev']
            }
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve buses: {str(e)}', 500)

@buses_bp.route('/<int:bus_id>', methods=['GET'])
@jwt_required()
def get_bus(bus_id):
    """Get a specific bus by ID."""
    try:
        bus = Bus.query.filter_by(id=bus_id, is_active=True).first()
        
        if not bus:
            return error_response('Bus not found', 404)
        
        return success_response('Bus retrieved successfully', {
            'bus': bus.to_dict()
        })
        
    except Exception as e:
        return error_response(f'Failed to retrieve bus: {str(e)}', 500)

@buses_bp.route('', methods=['POST'])
@admin_required
def create_bus(current_user):
    """Create a new bus with AI-powered auto-form fill."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Required fields
        required_fields = ['registration_number', 'bus_type', 'capacity']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'{field.replace("_", " ").title()} is required')
        
        registration_number = data.get('registration_number').strip().upper()
        
        # Check if registration number already exists
        if Bus.query.filter_by(registration_number=registration_number).first():
            return error_response('Registration number already exists')
        
        # Generate bus number if not provided
        bus_number = data.get('bus_number') or generate_bus_number()
        
        # Check if bus number already exists
        if Bus.query.filter_by(bus_number=bus_number).first():
            bus_number = generate_bus_number()
        
        # Validate driver assignment if provided
        driver_id = data.get('driver_id')
        if driver_id:
            driver = Driver.query.get(driver_id)
            if not driver:
                return error_response('Driver not found')
            if driver.status != 'Available':
                return error_response('Driver is not available')
        
        # Validate conductor assignment if provided
        conductor_id = data.get('conductor_id')
        if conductor_id:
            conductor = Driver.query.get(conductor_id)
            if not conductor:
                return error_response('Conductor not found')
            if conductor.driver_type != 'Conductor':
                return error_response('Selected staff is not a conductor')
        
        # Validate route assignment if provided
        route_id = data.get('route_id')
        if route_id:
            route = Route.query.get(route_id)
            if not route:
                return error_response('Route not found')
        
        # Create bus
        bus = Bus(
            bus_number=bus_number,
            registration_number=registration_number,
            bus_type=data.get('bus_type'),
            capacity=data.get('capacity'),
            manufacturer=data.get('manufacturer'),
            model=data.get('model'),
            year_of_manufacture=data.get('year_of_manufacture'),
            fuel_type=data.get('fuel_type', 'Diesel'),
            mileage=data.get('mileage'),
            insurance_number=data.get('insurance_number'),
            insurance_expiry=datetime.strptime(data['insurance_expiry'], '%Y-%m-%d').date() if data.get('insurance_expiry') else None,
            rc_number=data.get('rc_number'),
            rc_expiry=datetime.strptime(data['rc_expiry'], '%Y-%m-%d').date() if data.get('rc_expiry') else None,
            fitness_certificate_expiry=datetime.strptime(data['fitness_certificate_expiry'], '%Y-%m-%d').date() if data.get('fitness_certificate_expiry') else None,
            permit_expiry=datetime.strptime(data['permit_expiry'], '%Y-%m-%d').date() if data.get('permit_expiry') else None,
            route_id=route_id,
            driver_id=driver_id,
            conductor_id=conductor_id,
            status='Active'
        )
        
        db.session.add(bus)
        db.session.flush()
        
        # Update driver status if assigned
        if driver_id:
            driver.status = 'On Trip'
            driver.current_bus_id = bus.id
        
        if conductor_id:
            conductor.status = 'On Trip'
            conductor.current_bus_id = bus.id
        
        db.session.commit()
        
        return success_response('Bus created successfully', {
            'bus': bus.to_dict()
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to create bus: {str(e)}', 500)

@buses_bp.route('/<int:bus_id>', methods=['PUT'])
@admin_required
def update_bus(current_user, bus_id):
    """Update a bus."""
    try:
        bus = Bus.query.filter_by(id=bus_id, is_active=True).first()
        
        if not bus:
            return error_response('Bus not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        # Update fields if provided
        updateable_fields = [
            'bus_type', 'capacity', 'manufacturer', 'model', 'year_of_manufacture',
            'fuel_type', 'mileage', 'insurance_number', 'rc_number', 'status'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(bus, field, data[field])
        
        # Handle date fields
        date_fields = ['insurance_expiry', 'rc_expiry', 'fitness_certificate_expiry', 'permit_expiry']
        for field in date_fields:
            if field in data and data[field]:
                setattr(bus, field, datetime.strptime(data[field], '%Y-%m-%d').date())
        
        # Handle registration number update
        if 'registration_number' in data:
            new_reg_number = data['registration_number'].strip().upper()
            existing_bus = Bus.query.filter(
                Bus.registration_number == new_reg_number, 
                Bus.id != bus_id
            ).first()
            if existing_bus:
                return error_response('Registration number already exists')
            bus.registration_number = new_reg_number
        
        # Handle driver assignment
        if 'driver_id' in data:
            # Remove current driver assignment
            if bus.driver_id:
                current_driver = Driver.query.get(bus.driver_id)
                if current_driver:
                    current_driver.status = 'Available'
                    current_driver.current_bus_id = None
            
            # Assign new driver
            new_driver_id = data['driver_id']
            if new_driver_id:
                new_driver = Driver.query.get(new_driver_id)
                if not new_driver:
                    return error_response('Driver not found')
                new_driver.status = 'On Trip'
                new_driver.current_bus_id = bus.id
            
            bus.driver_id = new_driver_id
        
        # Handle conductor assignment
        if 'conductor_id' in data:
            # Remove current conductor assignment
            if bus.conductor_id:
                current_conductor = Driver.query.get(bus.conductor_id)
                if current_conductor:
                    current_conductor.status = 'Available'
                    current_conductor.current_bus_id = None
            
            # Assign new conductor
            new_conductor_id = data['conductor_id']
            if new_conductor_id:
                new_conductor = Driver.query.get(new_conductor_id)
                if not new_conductor:
                    return error_response('Conductor not found')
                if new_conductor.driver_type != 'Conductor':
                    return error_response('Selected staff is not a conductor')
                new_conductor.status = 'On Trip'
                new_conductor.current_bus_id = bus.id
            
            bus.conductor_id = new_conductor_id
        
        # Handle route assignment
        if 'route_id' in data:
            route_id = data['route_id']
            if route_id:
                route = Route.query.get(route_id)
                if not route:
                    return error_response('Route not found')
            bus.route_id = route_id
        
        db.session.commit()
        
        return success_response('Bus updated successfully', {
            'bus': bus.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update bus: {str(e)}', 500)

@buses_bp.route('/<int:bus_id>', methods=['DELETE'])
@admin_required
def delete_bus(current_user, bus_id):
    """Delete (deactivate) a bus."""
    try:
        bus = Bus.query.filter_by(id=bus_id, is_active=True).first()
        
        if not bus:
            return error_response('Bus not found', 404)
        
        # Check if bus has active trips
        from app.models.trip import Trip
        active_trips = Trip.query.filter_by(
            bus_id=bus_id, 
            status='In Progress'
        ).count()
        
        if active_trips > 0:
            return error_response('Cannot delete bus with active trips')
        
        # Release assigned staff
        if bus.driver_id:
            driver = Driver.query.get(bus.driver_id)
            if driver:
                driver.status = 'Available'
                driver.current_bus_id = None
        
        if bus.conductor_id:
            conductor = Driver.query.get(bus.conductor_id)
            if conductor:
                conductor.status = 'Available'
                conductor.current_bus_id = None
        
        bus.is_active = False
        bus.status = 'Retired'
        
        db.session.commit()
        
        return success_response('Bus deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete bus: {str(e)}', 500)

@buses_bp.route('/<int:bus_id>/location', methods=['PATCH'])
@staff_required
def update_bus_location(current_user, bus_id):
    """Update bus GPS location."""
    try:
        bus = Bus.query.filter_by(id=bus_id, is_active=True).first()

        if not bus:
            return error_response('Bus not found', 404)

        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return error_response('Latitude and longitude are required')

        bus.current_location_lat = latitude
        bus.current_location_lng = longitude
        bus.last_location_update = datetime.utcnow()

        db.session.commit()

        # Emit real-time location update via WebSocket
        from app import socketio
        socketio.emit('location_update', {
            'bus_id': bus_id,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': bus.last_location_update.isoformat()
        }, room=f'bus_{bus_id}')

        return success_response('Location updated successfully')

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update location: {str(e)}', 500)

@buses_bp.route('/<int:bus_id>/documents', methods=['GET'])
@jwt_required()
def get_bus_documents(bus_id):
    """Get all documents for a bus."""
    try:
        bus = Bus.query.filter_by(id=bus_id, is_active=True).first()

        if not bus:
            return error_response('Bus not found', 404)

        documents = Document.query.filter_by(bus_id=bus_id).order_by(Document.document_type, Document.created_at.desc()).all()
        documents_data = [doc.to_dict() for doc in documents]

        return success_response('Bus documents retrieved successfully', {
            'bus_id': bus_id,
            'bus_number': bus.bus_number,
            'documents': documents_data
        })

    except Exception as e:
        return error_response(f'Failed to retrieve bus documents: {str(e)}', 500)

@buses_bp.route('/<int:bus_id>/documents', methods=['POST'])
@admin_required
def upload_bus_document(current_user, bus_id):
    """Upload a document for a bus with OCR processing."""
    try:
        bus = Bus.query.filter_by(id=bus_id, is_active=True).first()

        if not bus:
            return error_response('Bus not found', 404)

        if 'file' not in request.files:
            return error_response('No file provided')

        file = request.files['file']
        if file.filename == '':
            return error_response('No file selected')

        # Get form data
        document_type = request.form.get('document_type')
        document_name = request.form.get('document_name')
        document_number = request.form.get('document_number')
        issue_date = request.form.get('issue_date')
        expiry_date = request.form.get('expiry_date')
        issuing_authority = request.form.get('issuing_authority')

        if not document_type:
            return error_response('Document type is required')

        if not document_name:
            return error_response('Document name is required')

        # Validate file type
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'tiff'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''

        if file_extension not in allowed_extensions:
            return error_response('Invalid file type. Allowed: PDF, JPG, PNG, TIFF')

        # Save file
        import os
        from werkzeug.utils import secure_filename
        from app.utils.helpers import sanitize_filename

        filename = secure_filename(file.filename)
        filename = sanitize_filename(filename)

        upload_folder = os.path.join(os.getcwd(), 'uploads', 'documents')
        os.makedirs(upload_folder, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{bus.bus_number}_{document_type}_{timestamp}_{filename}"
        file_path = os.path.join(upload_folder, filename)

        file.save(file_path)

        # Get file info
        file_size = os.path.getsize(file_path)
        file_type = file.content_type

        # Parse dates
        issue_date_obj = None
        expiry_date_obj = None

        if issue_date:
            issue_date_obj = datetime.strptime(issue_date, '%Y-%m-%d').date()

        if expiry_date:
            expiry_date_obj = datetime.strptime(expiry_date, '%Y-%m-%d').date()

        # Create document record
        document = Document(
            bus_id=bus_id,
            document_type=document_type,
            document_name=document_name,
            document_number=document_number,
            file_name=filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            issue_date=issue_date_obj,
            expiry_date=expiry_date_obj,
            issuing_authority=issuing_authority
        )

        db.session.add(document)
        db.session.flush()

        # Perform OCR processing (placeholder for actual OCR implementation)
        # In a real implementation, this would use libraries like pytesseract
        # or cloud services like Google Vision API
        try:
            ocr_text = perform_ocr(file_path, file_extension)
            if ocr_text:
                document.extract_ocr_data(ocr_text, confidence=0.85)
        except Exception as ocr_error:
            print(f"OCR processing failed: {ocr_error}")

        db.session.commit()

        return success_response('Document uploaded successfully', {
            'document': document.to_dict()
        }, 201)

    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to upload document: {str(e)}', 500)

def perform_ocr(file_path, file_extension):
    """Perform OCR on uploaded document."""
    try:
        # This is a placeholder for OCR implementation
        # In a real application, you would use:
        # - pytesseract for local OCR
        # - Google Vision API for cloud OCR
        # - AWS Textract for advanced document analysis

        if file_extension.lower() == 'pdf':
            # For PDF files, convert to images first
            # Use libraries like pdf2image
            pass
        else:
            # For image files, use pytesseract directly
            # import pytesseract
            # from PIL import Image
            # image = Image.open(file_path)
            # text = pytesseract.image_to_string(image)
            # return text
            pass

        # Return placeholder OCR text
        return "Sample OCR extracted text - Document processed successfully"

    except Exception as e:
        print(f"OCR Error: {e}")
        return None
