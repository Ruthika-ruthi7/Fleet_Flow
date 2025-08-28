import React, { useState, useEffect } from 'react';
import {
  Users, QrCode, Clock, Search, Filter, Download,
  CheckCircle, XCircle, AlertCircle, Calendar,
  MapPin, Bus, User, Phone, Mail, UserCheck
} from 'lucide-react';

const AttendanceManagement = () => {
  const [attendanceData, setAttendanceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    date: new Date().toISOString().split('T')[0],
    route_id: '',
    status: '',
    trip_type: ''
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [summary, setSummary] = useState({});
  const [showQRScanner, setShowQRScanner] = useState(false);

  useEffect(() => {
    fetchAttendanceData();
  }, [filters, currentPage]);

  const fetchAttendanceData = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams({
        page: currentPage,
        per_page: 20,
        ...filters
      });

      const response = await fetch(`/api/attendance?${queryParams}`);
      const result = await response.json();

      if (result.success) {
        setAttendanceData(result.data.attendance);
        setSummary(result.data.summary);
      }
    } catch (error) {
      console.error('Error fetching attendance data:', error);
      // Set mock data for demo
      setAttendanceData([
        {
          id: 1,
          student_name: 'John Doe',
          student_roll: 'STU001',
          class: 'Grade 10',
          route_name: 'City Center Route',
          bus_number: 'BUS001',
          status: 'present',
          timestamp: '2024-01-15T07:15:00',
          boarding_location: 'Main Market',
          trip_type: 'morning',
          attendance_method: 'qr_scan',
          temperature: 98.6
        },
        {
          id: 2,
          student_name: 'Jane Smith',
          student_roll: 'STU002',
          class: 'Grade 11',
          route_name: 'Suburb Route',
          bus_number: 'BUS002',
          status: 'absent',
          timestamp: '2024-01-15T07:20:00',
          boarding_location: 'Park Avenue',
          trip_type: 'morning',
          parent_notified: true
        },
        {
          id: 3,
          student_name: 'Mike Johnson',
          student_roll: 'STU003',
          class: 'Grade 10',
          route_name: 'Downtown Route',
          bus_number: 'BUS003',
          status: 'late',
          timestamp: '2024-01-15T07:35:00',
          boarding_location: 'City Center',
          trip_type: 'morning',
          attendance_method: 'manual',
          notes: 'Late due to traffic'
        }
      ]);
      setSummary({
        total_records: 100,
        present_count: 85,
        absent_count: 12,
        late_count: 3,
        attendance_rate: 88.0
      });
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAttendance = async (studentId, status) => {
    try {
      const response = await fetch('/api/attendance/mark', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_id: studentId,
          status: status,
          timestamp: new Date().toISOString()
        })
      });

      if (response.ok) {
        fetchAttendanceData(); // Refresh data
      }
    } catch (error) {
      console.error('Error marking attendance:', error);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'present':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'absent':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'late':
        return <AlertCircle className="h-5 w-5 text-yellow-600" />;
      default:
        return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusBadge = (status) => {
    const baseClasses = "inline-flex px-2 py-1 text-xs font-semibold rounded-full";
    switch (status) {
      case 'present':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'absent':
        return `${baseClasses} bg-red-100 text-red-800`;
      case 'late':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  const filteredData = attendanceData.filter(record =>
    record.student_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.student_roll.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.bus_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Attendance Management</h1>
          <p className="text-gray-600">Track and manage student attendance with real-time monitoring</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowQRScanner(true)}
            className="btn btn-secondary flex items-center space-x-2"
          >
            <QrCode className="h-5 w-5" />
            <span>QR Scanner</span>
          </button>
          <button className="btn btn-primary flex items-center space-x-2">
            <Download className="h-5 w-5" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Students</p>
              <p className="text-2xl font-bold text-gray-900">{summary.total_records || 100}</p>
            </div>
            <Users className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Present</p>
              <p className="text-2xl font-bold text-green-600">{summary.present_count || 85}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Absent</p>
              <p className="text-2xl font-bold text-red-600">{summary.absent_count || 12}</p>
            </div>
            <XCircle className="h-8 w-8 text-red-600" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Attendance Rate</p>
              <p className="text-2xl font-bold text-blue-600">{summary.attendance_rate || 88}%</p>
            </div>
            <Clock className="h-8 w-8 text-blue-600" />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="card p-6">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              type="date"
              value={filters.date}
              onChange={(e) => setFilters({...filters, date: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Route</label>
            <select
              value={filters.route_id}
              onChange={(e) => setFilters({...filters, route_id: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Routes</option>
              <option value="1">City Center Route</option>
              <option value="2">Suburb Route</option>
              <option value="3">Downtown Route</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({...filters, status: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Status</option>
              <option value="present">Present</option>
              <option value="absent">Absent</option>
              <option value="late">Late</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Trip Type</label>
            <select
              value={filters.trip_type}
              onChange={(e) => setFilters({...filters, trip_type: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Trips</option>
              <option value="morning">Morning</option>
              <option value="evening">Evening</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search students..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Attendance Table */}
      <div className="card">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Attendance Records</h3>
        </div>

        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading attendance data...</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route & Bus</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredData.map((record) => (
                  <tr key={record.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <User className="h-5 w-5 text-blue-600" />
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{record.student_name}</div>
                          <div className="text-sm text-gray-500">{record.student_roll} • {record.class}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Bus className="h-4 w-4 text-gray-400 mr-2" />
                        <div>
                          <div className="text-sm text-gray-900">{record.route_name}</div>
                          <div className="text-sm text-gray-500">{record.bus_number}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getStatusIcon(record.status)}
                        <span className={`ml-2 ${getStatusBadge(record.status)}`}>
                          {record.status}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 text-gray-400 mr-2" />
                        <div>
                          <div>{new Date(record.timestamp).toLocaleTimeString()}</div>
                          <div className="text-xs text-gray-500 capitalize">{record.trip_type}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-900">{record.boarding_location}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        record.attendance_method === 'qr_scan'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {record.attendance_method === 'qr_scan' ? 'QR Scan' : 'Manual'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        {record.status !== 'present' && (
                          <button
                            onClick={() => handleMarkAttendance(record.student_id, 'present')}
                            className="text-green-600 hover:text-green-900"
                          >
                            Mark Present
                          </button>
                        )}
                        {record.status !== 'absent' && (
                          <button
                            onClick={() => handleMarkAttendance(record.student_id, 'absent')}
                            className="text-red-600 hover:text-red-900"
                          >
                            Mark Absent
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* QR Scanner Modal */}
      {showQRScanner && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <QrCode className="mx-auto h-16 w-16 text-blue-600 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-4">QR Code Scanner</h3>
              <p className="text-sm text-gray-600 mb-6">
                Position the QR code within the camera frame to mark attendance automatically.
              </p>
              <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center mb-4">
                <div className="text-center">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8">
                    <QrCode className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">Camera view would appear here</p>
                  </div>
                </div>
              </div>
              <div className="flex justify-center space-x-3">
                <button
                  onClick={() => setShowQRScanner(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button className="btn btn-primary">
                  Start Scanning
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AttendanceManagement;
