from flask import Blueprint

hostel_management_bp = Blueprint('hostel_management', __name__, url_prefix='/hostel_management')

from .hostels import hostels_bp
from .rooms import rooms_bp
from .messes import messes_bp
from .student_allocations import student_allocations_bp
from .visitor_logs import visitor_logs_bp
from .maintenance_records import maintenance_records_bp
from .grievances import grievances_bp
from .rule_violations import rule_violations_bp
from .hostel_exits import hostel_exits_bp

hostel_management_bp.register_blueprint(hostels_bp)
hostel_management_bp.register_blueprint(rooms_bp)
hostel_management_bp.register_blueprint(messes_bp)
hostel_management_bp.register_blueprint(student_allocations_bp)
hostel_management_bp.register_blueprint(visitor_logs_bp)
hostel_management_bp.register_blueprint(maintenance_records_bp)
hostel_management_bp.register_blueprint(grievances_bp)
hostel_management_bp.register_blueprint(rule_violations_bp)
hostel_management_bp.register_blueprint(hostel_exits_bp)
