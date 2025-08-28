from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from . import Base

class Hostel(Base):
    __tablename__ = 'hostels'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    warden = Column(String(100), nullable=True)
    capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    rooms = relationship("Room", back_populates="hostel")
    messes = relationship("Mess", back_populates="hostel")

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey('hostels.id'), nullable=False)
    room_type = Column(String(50), nullable=False)
    floor = Column(Integer, nullable=True)
    beds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    hostel = relationship("Hostel", back_populates="rooms")
    allocations = relationship("StudentAllocation", back_populates="room")

class Mess(Base):
    __tablename__ = 'messes'
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey('hostels.id'), nullable=False)
    menu = Column(Text, nullable=True)
    fees = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    hostel = relationship("Hostel", back_populates="messes")

class StudentAllocation(Base):
    __tablename__ = 'student_allocations'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)  # Assuming student model exists
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    allocation_date = Column(DateTime, default=datetime.utcnow)
    leave_requested = Column(Boolean, default=False)
    leave_approved = Column(Boolean, default=False)

    room = relationship("Room", back_populates="allocations")

class VisitorLog(Base):
    __tablename__ = 'visitor_logs'
    id = Column(Integer, primary_key=True)
    visitor_name = Column(String(100), nullable=False)
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    id_validated = Column(Boolean, default=False)

class MaintenanceRecord(Base):
    __tablename__ = 'maintenance_records'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    description = Column(Text, nullable=True)
    reported_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)

    room = relationship("Room")

class Grievance(Base):
    __tablename__ = 'grievances'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    reported_at = Column(DateTime, default=datetime.utcnow)
    escalated = Column(Boolean, default=False)

class RuleViolation(Base):
    __tablename__ = 'rule_violations'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    violation_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    reported_at = Column(DateTime, default=datetime.utcnow)
    categorized = Column(Boolean, default=False)

class HostelExit(Base):
    __tablename__ = 'hostel_exits'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    exit_date = Column(DateTime, default=datetime.utcnow)
    no_dues_generated = Column(Boolean, default=False)
    clearance_done = Column(Boolean, default=False)
