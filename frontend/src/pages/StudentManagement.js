import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { UserCheck, Plus, QrCode, Search, Filter, Award, DollarSign, Phone, MapPin } from 'lucide-react';

const StudentManagement = () => {
  const [filters, setFilters] = useState({
    search: '',
    class_name: '',
    scholarship_type: '',
    status: '',
  });

  // Mock student data - in real app this would come from API
  const students = [
    {
      id: 1, student_id: 'STU001', full_name: 'Alice Brown',
      class_name: 'Grade 10', section: 'A', roll_number: '101',
      parent_name: 'Robert Brown', parent_phone: '+1234567896',
      route_id: 1, pickup_stop: 'City Center', drop_stop: 'School Gate',
      base_monthly_fee: 2000, scholarship_type: 'Merit', scholarship_percentage: 25,
      final_monthly_fee: 1500, status: 'Active', attendance_percentage: 95,
      family_income: 45000, academic_score: 92
    },
    {
      id: 2, student_id: 'STU002', full_name: 'Bob Davis',
      class_name: 'Grade 11', section: 'B', roll_number: '205',
      parent_name: 'Linda Davis', parent_phone: '+1234567897',
      route_id: 2, pickup_stop: 'Sunrise Apartments', drop_stop: 'University Gate',
      base_monthly_fee: 2200, scholarship_type: 'Need-based', scholarship_percentage: 40,
      final_monthly_fee: 1320, status: 'Active', attendance_percentage: 88,
      family_income: 25000, academic_score: 78
    },
    {
      id: 3, student_id: 'STU003', full_name: 'Carol Wilson',
      class_name: 'Grade 9', section: 'C', roll_number: '315',
      parent_name: 'James Wilson', parent_phone: '+1234567898',
      route_id: 3, pickup_stop: 'Industrial Gate', drop_stop: 'Tech Park',
      base_monthly_fee: 1800, scholarship_type: 'Sports', scholarship_percentage: 50,
      final_monthly_fee: 900, status: 'Active', attendance_percentage: 97,
      family_income: 35000, academic_score: 85
    },
    {
      id: 4, student_id: 'STU004', full_name: 'David Kumar',
      class_name: 'Grade 12', section: 'A', roll_number: '120',
      parent_name: 'Raj Kumar', parent_phone: '+1234567899',
      route_id: 4, pickup_stop: 'Metro Station', drop_stop: 'Airport',
      base_monthly_fee: 2500, scholarship_type: null, scholarship_percentage: 0,
      final_monthly_fee: 2500, status: 'Active', attendance_percentage: 91,
      family_income: 75000, academic_score: 88
    },
    {
      id: 5, student_id: 'STU005', full_name: 'Emma Thompson',
      class_name: 'Grade 10', section: 'B', roll_number: '210',
      parent_name: 'Sarah Thompson', parent_phone: '+1234567800',
      route_id: 1, pickup_stop: 'City Center', drop_stop: 'School Gate',
      base_monthly_fee: 2000, scholarship_type: 'Sibling', scholarship_percentage: 15,
      final_monthly_fee: 1700, status: 'Active', attendance_percentage: 93,
      family_income: 55000, academic_score: 89
    }
  ];

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getScholarshipBadge = (scholarshipType) => {
    if (!scholarshipType) return null;

    const scholarshipClasses = {
      Merit: 'badge-success',
      'Need-based': 'badge-warning',
      Sports: 'badge-primary',
      Sibling: 'badge-secondary',
      'Single Parent': 'badge-danger',
    };
    return `badge ${scholarshipClasses[scholarshipType] || 'badge-secondary'}`;
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      Active: 'badge-success',
      Inactive: 'badge-secondary',
      Suspended: 'badge-danger',
    };
    return `badge ${statusClasses[status] || 'badge-secondary'}`;
  };

  const filteredStudents = students.filter(student => {
    const matchesSearch = !filters.search ||
      student.full_name.toLowerCase().includes(filters.search.toLowerCase()) ||
      student.student_id.toLowerCase().includes(filters.search.toLowerCase());
    const matchesClass = !filters.class_name || student.class_name === filters.class_name;
    const matchesScholarship = !filters.scholarship_type || student.scholarship_type === filters.scholarship_type;
    const matchesStatus = !filters.status || student.status === filters.status;

    return matchesSearch && matchesClass && matchesScholarship && matchesStatus;
  });

  // Calculate summary statistics
  const totalStudents = students.length;
  const scholarshipStudents = students.filter(s => s.scholarship_type);
  const totalBaseFees = students.reduce((sum, s) => sum + s.base_monthly_fee, 0);
  const totalFinalFees = students.reduce((sum, s) => sum + s.final_monthly_fee, 0);
  const totalSavings = totalBaseFees - totalFinalFees;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Student Management</h1>
          <p className="text-gray-600">Manage students with scholarship-based fee reduction</p>
        </div>
        <button className="btn btn-primary flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Add Student</span>
        </button>
      </div>

      {/* Scholarship Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-100">
              <UserCheck className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Students</p>
              <p className="text-2xl font-bold text-gray-900">{totalStudents}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-100">
              <Award className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Scholarship Recipients</p>
              <p className="text-2xl font-bold text-gray-900">{scholarshipStudents.length}</p>
              <p className="text-xs text-gray-500">{Math.round((scholarshipStudents.length / totalStudents) * 100)}% of students</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-purple-100">
              <DollarSign className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
              <p className="text-2xl font-bold text-gray-900">₹{totalFinalFees.toLocaleString()}</p>
              <p className="text-xs text-gray-500">After scholarships</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-orange-100">
              <Award className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Scholarship Savings</p>
              <p className="text-2xl font-bold text-gray-900">₹{totalSavings.toLocaleString()}</p>
              <p className="text-xs text-gray-500">Monthly assistance</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              name="search"
              placeholder="Search students..."
              value={filters.search}
              onChange={handleFilterChange}
              className="input pl-10"
            />
          </div>

          <select
            name="class_name"
            value={filters.class_name}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Classes</option>
            <option value="Grade 9">Grade 9</option>
            <option value="Grade 10">Grade 10</option>
            <option value="Grade 11">Grade 11</option>
            <option value="Grade 12">Grade 12</option>
          </select>

          <select
            name="scholarship_type"
            value={filters.scholarship_type}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Scholarships</option>
            <option value="Merit">Merit</option>
            <option value="Need-based">Need-based</option>
            <option value="Sports">Sports</option>
            <option value="Sibling">Sibling</option>
            <option value="Single Parent">Single Parent</option>
          </select>

          <select
            name="status"
            value={filters.status}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Status</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
            <option value="Suspended">Suspended</option>
          </select>

          <button className="btn btn-outline flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>More Filters</span>
          </button>
        </div>
      </div>

      {/* Students Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredStudents.map((student) => (
          <div key={student.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {student.full_name}
                </h3>
                <p className="text-sm text-gray-600">
                  {student.student_id} • {student.class_name} {student.section}
                </p>
              </div>
              <div className="flex flex-col items-end space-y-1">
                <span className={getStatusBadge(student.status)}>
                  {student.status}
                </span>
                {student.scholarship_type && (
                  <span className={getScholarshipBadge(student.scholarship_type)}>
                    {student.scholarship_type}
                  </span>
                )}
              </div>
            </div>

            {/* Student Details */}
            <div className="space-y-2 text-sm mb-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Roll Number:</span>
                <span className="font-medium">{student.roll_number}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Parent:</span>
                <span className="font-medium">{student.parent_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Academic Score:</span>
                <span className="font-medium">{student.academic_score}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Attendance:</span>
                <span className="font-medium">{student.attendance_percentage}%</span>
              </div>
            </div>

            {/* Fee Information */}
            <div className="bg-gray-50 rounded-lg p-3 mb-4">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Fee Details</h4>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Base Fee:</span>
                  <span className="font-medium">₹{student.base_monthly_fee}</span>
                </div>
                {student.scholarship_type && (
                  <>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Scholarship:</span>
                      <span className="text-green-600 font-medium">-{student.scholarship_percentage}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Savings:</span>
                      <span className="text-green-600 font-medium">
                        ₹{student.base_monthly_fee - student.final_monthly_fee}
                      </span>
                    </div>
                  </>
                )}
                <div className="flex justify-between border-t pt-1">
                  <span className="text-gray-900 font-medium">Final Fee:</span>
                  <span className="text-gray-900 font-bold">₹{student.final_monthly_fee}</span>
                </div>
              </div>
            </div>

            {/* Route Information */}
            <div className="flex items-center space-x-2 text-sm text-gray-600 mb-4">
              <MapPin className="h-4 w-4" />
              <span>{student.pickup_stop} → {student.drop_stop}</span>
            </div>

            {/* Actions */}
            <div className="flex justify-between items-center">
              <div className="flex space-x-2">
                <button className="text-primary-600 hover:text-primary-900">
                  <QrCode className="h-4 w-4" />
                </button>
                <button className="text-blue-600 hover:text-blue-900">
                  <Phone className="h-4 w-4" />
                </button>
                <button className="text-green-600 hover:text-green-900">
                  <Award className="h-4 w-4" />
                </button>
              </div>

              <button className="btn btn-outline btn-sm">
                View Profile
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Scholarship Breakdown */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Scholarship Breakdown</h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {['Merit', 'Need-based', 'Sports', 'Sibling', 'Single Parent'].map(type => {
            const typeStudents = students.filter(s => s.scholarship_type === type);
            const typeSavings = typeStudents.reduce((sum, s) => sum + (s.base_monthly_fee - s.final_monthly_fee), 0);

            return (
              <div key={type} className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{typeStudents.length}</div>
                <div className="text-sm text-gray-600">{type}</div>
                <div className="text-xs text-green-600 font-medium">₹{typeSavings.toLocaleString()} saved</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Empty State */}
      {filteredStudents.length === 0 && (
        <div className="text-center py-12">
          <UserCheck className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <div className="text-gray-500 mb-4">No students found</div>
          <button className="btn btn-primary">
            Add Your First Student
          </button>
        </div>
      )}
    </div>
  );
};

export default StudentManagement;
