import React, { useState, useEffect } from 'react';
import {
  Wrench, Calendar, AlertTriangle, Search, Filter, Download,
  Plus, DollarSign, Clock, CheckCircle, XCircle,
  User, Phone, FileText, Package, Settings
} from 'lucide-react';

const MaintenanceManagement = () => {
  const [maintenanceData, setMaintenanceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    bus_id: '',
    status: '',
    maintenance_type: '',
    start_date: '',
    end_date: ''
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [summary, setSummary] = useState({});
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);

  useEffect(() => {
    fetchMaintenanceData();
  }, [filters, currentPage]);

  const fetchMaintenanceData = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams({
        page: currentPage,
        per_page: 20,
        ...filters
      });

      const response = await fetch(`/api/maintenance?${queryParams}`);
      const result = await response.json();

      if (result.success) {
        setMaintenanceData(result.data.maintenance);
        setSummary(result.data.summary);
      }
    } catch (error) {
      console.error('Error fetching maintenance data:', error);
      // Set mock data for demo
      setMaintenanceData([
        {
          id: 1,
          bus_number: 'BUS001',
          maintenance_type: 'Regular Service',
          category: 'Preventive',
          priority: 'Medium',
          description: 'Regular service for BUS001',
          cost: 5000,
          status: 'completed',
          maintenance_date: '2024-01-10',
          mechanic_name: 'Rajesh Kumar',
          vendor_name: 'City Auto Service',
          work_order_number: 'WO0001',
          next_maintenance_date: '2024-04-10'
        },
        {
          id: 2,
          bus_number: 'BUS002',
          maintenance_type: 'Engine Repair',
          category: 'Corrective',
          priority: 'High',
          description: 'Engine repair for BUS002',
          cost: 25000,
          status: 'in_progress',
          maintenance_date: '2024-01-15',
          mechanic_name: 'Amit Singh',
          vendor_name: 'Express Motors',
          work_order_number: 'WO0002',
          next_maintenance_date: '2025-01-15'
        },
        {
          id: 3,
          bus_number: 'BUS003',
          maintenance_type: 'Brake Service',
          category: 'Preventive',
          priority: 'Critical',
          description: 'Brake system maintenance',
          cost: 8000,
          status: 'scheduled',
          maintenance_date: '2024-01-20',
          mechanic_name: 'Suresh Patel',
          vendor_name: 'Prime Auto Care',
          work_order_number: 'WO0003',
          next_maintenance_date: '2024-07-20'
        }
      ]);
      setSummary({
        total_records: 100,
        total_cost: 250000,
        completed_count: 75,
        pending_count: 25,
        average_cost: 2500
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'in_progress':
        return <Clock className="h-5 w-5 text-blue-600" />;
      case 'scheduled':
        return <Calendar className="h-5 w-5 text-yellow-600" />;
      case 'cancelled':
        return <XCircle className="h-5 w-5 text-red-600" />;
      default:
        return <AlertTriangle className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusBadge = (status) => {
    const baseClasses = "inline-flex px-2 py-1 text-xs font-semibold rounded-full";
    switch (status) {
      case 'completed':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'in_progress':
        return `${baseClasses} bg-blue-100 text-blue-800`;
      case 'scheduled':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      case 'cancelled':
        return `${baseClasses} bg-red-100 text-red-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  const getPriorityBadge = (priority) => {
    const baseClasses = "inline-flex px-2 py-1 text-xs font-semibold rounded-full";
    switch (priority) {
      case 'Critical':
        return `${baseClasses} bg-red-100 text-red-800`;
      case 'High':
        return `${baseClasses} bg-orange-100 text-orange-800`;
      case 'Medium':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      case 'Low':
        return `${baseClasses} bg-green-100 text-green-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  const filteredData = maintenanceData.filter(record =>
    record.bus_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.maintenance_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.vendor_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Maintenance Management</h1>
          <p className="text-gray-600">Schedule and track vehicle maintenance with comprehensive analytics</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowScheduleModal(true)}
            className="btn btn-secondary flex items-center space-x-2"
          >
            <Calendar className="h-5 w-5" />
            <span>Schedule</span>
          </button>
          <button className="btn btn-primary flex items-center space-x-2">
            <Plus className="h-5 w-5" />
            <span>New Maintenance</span>
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Records</p>
              <p className="text-2xl font-bold text-gray-900">{summary.total_records || 100}</p>
            </div>
            <Wrench className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Cost</p>
              <p className="text-2xl font-bold text-green-600">₹{summary.total_cost?.toLocaleString() || '2,50,000'}</p>
            </div>
            <DollarSign className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-blue-600">{summary.completed_count || 75}</p>
            </div>
            <CheckCircle className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-2xl font-bold text-yellow-600">{summary.pending_count || 25}</p>
            </div>
            <Clock className="h-8 w-8 text-yellow-600" />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="card p-6">
        <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bus</label>
            <select
              value={filters.bus_id}
              onChange={(e) => setFilters({...filters, bus_id: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Buses</option>
              <option value="1">BUS001</option>
              <option value="2">BUS002</option>
              <option value="3">BUS003</option>
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
              <option value="completed">Completed</option>
              <option value="in_progress">In Progress</option>
              <option value="scheduled">Scheduled</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select
              value={filters.maintenance_type}
              onChange={(e) => setFilters({...filters, maintenance_type: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="Regular Service">Regular Service</option>
              <option value="Engine Repair">Engine Repair</option>
              <option value="Brake Service">Brake Service</option>
              <option value="Oil Change">Oil Change</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
            <input
              type="date"
              value={filters.start_date}
              onChange={(e) => setFilters({...filters, start_date: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
            <input
              type="date"
              value={filters.end_date}
              onChange={(e) => setFilters({...filters, end_date: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Maintenance Table */}
      <div className="card">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg font-medium text-gray-900">Maintenance Records</h3>
          <button className="btn btn-secondary flex items-center space-x-2">
            <Download className="h-4 w-4" />
            <span>Export</span>
          </button>
        </div>

        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading maintenance data...</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bus & Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredData.map((record) => (
                  <tr key={record.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{record.bus_number}</div>
                        <div className="text-sm text-gray-500">{record.maintenance_type}</div>
                        <div className="text-xs text-gray-400">{record.category}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={getPriorityBadge(record.priority)}>
                        {record.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getStatusIcon(record.status)}
                        <span className={`ml-2 ${getStatusBadge(record.status)}`}>
                          {record.status.replace('_', ' ')}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {new Date(record.maintenance_date).toLocaleDateString()}
                      </div>
                      <div className="text-xs text-gray-500">
                        Next: {new Date(record.next_maintenance_date).toLocaleDateString()}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        ₹{record.cost.toLocaleString()}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm text-gray-900">{record.vendor_name}</div>
                        <div className="text-sm text-gray-500">{record.mechanic_name}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => setSelectedRecord(record)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          View
                        </button>
                        <button className="text-green-600 hover:text-green-900">
                          Edit
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Schedule Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Schedule Maintenance</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Bus</label>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-md">
                    <option>Select Bus</option>
                    <option>BUS001</option>
                    <option>BUS002</option>
                    <option>BUS003</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Maintenance Type</label>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-md">
                    <option>Select Type</option>
                    <option>Regular Service</option>
                    <option>Engine Repair</option>
                    <option>Brake Service</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Scheduled Date</label>
                  <input type="date" className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-md">
                    <option>Medium</option>
                    <option>Low</option>
                    <option>High</option>
                    <option>Critical</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowScheduleModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button className="btn btn-primary">
                  Schedule
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MaintenanceManagement;
