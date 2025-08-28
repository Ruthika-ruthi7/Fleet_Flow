import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Users, Plus, Search, Filter, Star, AlertTriangle, Phone, Calendar } from 'lucide-react';

const DriverManagement = () => {
  const [filters, setFilters] = useState({
    search: '',
    driver_type: '',
    status: '',
  });

  // Mock driver data - in real app this would come from API
  const drivers = [
    {
      id: 1, employee_id: 'DRV001', full_name: 'John Smith',
      driver_type: 'Driver', license_number: 'DL123456789',
      license_expiry: '2025-12-31', phone: '+1234567891',
      status: 'Available', shift_type: 'Morning', rating: 4.8,
      experience_years: 8, assigned_bus: 'TRP001',
      total_trips: 1250, on_time_percentage: 96
    },
    {
      id: 2, employee_id: 'DRV002', full_name: 'Sarah Johnson',
      driver_type: 'Driver', license_number: 'DL987654321',
      license_expiry: '2025-08-15', phone: '+1234567892',
      status: 'On Trip', shift_type: 'Evening', rating: 4.6,
      experience_years: 5, assigned_bus: 'TRP002',
      total_trips: 890, on_time_percentage: 94
    },
    {
      id: 3, employee_id: 'CON001', full_name: 'Mike Wilson',
      driver_type: 'Conductor', license_number: 'DL456789123',
      license_expiry: '2024-10-20', phone: '+1234567893',
      status: 'Available', shift_type: 'Full Day', rating: 4.7,
      experience_years: 3, assigned_bus: 'TRP001',
      total_trips: 650, on_time_percentage: 92
    },
    {
      id: 4, employee_id: 'DRV003', full_name: 'Robert Davis',
      driver_type: 'Driver', license_number: 'DL789123456',
      license_expiry: '2025-06-30', phone: '+1234567894',
      status: 'On Trip', shift_type: 'Morning', rating: 4.9,
      experience_years: 12, assigned_bus: 'TRP004',
      total_trips: 2100, on_time_percentage: 98
    },
    {
      id: 5, employee_id: 'DRV004', full_name: 'Emily Chen',
      driver_type: 'Driver', license_number: 'DL321654987',
      license_expiry: '2026-03-15', phone: '+1234567895',
      status: 'Available', shift_type: 'Evening', rating: 4.5,
      experience_years: 4, assigned_bus: 'TRP005',
      total_trips: 720, on_time_percentage: 91
    }
  ];

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      Available: 'badge-success',
      'On Trip': 'badge-primary',
      'Off Duty': 'badge-secondary',
      'On Leave': 'badge-warning',
    };
    return `badge ${statusClasses[status] || 'badge-secondary'}`;
  };

  const isLicenseExpiring = (expiryDate) => {
    const today = new Date();
    const expiry = new Date(expiryDate);
    const daysToExpiry = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24));
    return daysToExpiry <= 90; // Alert if expiring within 90 days
  };

  const filteredDrivers = drivers.filter(driver => {
    const matchesSearch = !filters.search ||
      driver.full_name.toLowerCase().includes(filters.search.toLowerCase()) ||
      driver.employee_id.toLowerCase().includes(filters.search.toLowerCase());
    const matchesType = !filters.driver_type || driver.driver_type === filters.driver_type;
    const matchesStatus = !filters.status || driver.status === filters.status;

    return matchesSearch && matchesType && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Driver Management</h1>
          <p className="text-gray-600">Manage drivers and conductors with performance tracking</p>
        </div>
        <button className="btn btn-primary flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Add Driver</span>
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              name="search"
              placeholder="Search drivers..."
              value={filters.search}
              onChange={handleFilterChange}
              className="input pl-10"
            />
          </div>

          <select
            name="driver_type"
            value={filters.driver_type}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Types</option>
            <option value="Driver">Driver</option>
            <option value="Conductor">Conductor</option>
          </select>

          <select
            name="status"
            value={filters.status}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Status</option>
            <option value="Available">Available</option>
            <option value="On Trip">On Trip</option>
            <option value="Off Duty">Off Duty</option>
            <option value="On Leave">On Leave</option>
          </select>

          <button className="btn btn-outline flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>More Filters</span>
          </button>
        </div>
      </div>

      {/* Drivers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredDrivers.map((driver) => (
          <div key={driver.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {driver.full_name}
                </h3>
                <p className="text-sm text-gray-600">{driver.employee_id} • {driver.driver_type}</p>
              </div>
              <div className="flex items-center space-x-2">
                {isLicenseExpiring(driver.license_expiry) && (
                  <AlertTriangle className="h-5 w-5 text-yellow-500" />
                )}
                <span className={getStatusBadge(driver.status)}>
                  {driver.status}
                </span>
              </div>
            </div>

            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Experience:</span>
                <span className="font-medium">{driver.experience_years} years</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Rating:</span>
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-500 fill-current" />
                  <span className="font-medium">{driver.rating}</span>
                </div>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Assigned Bus:</span>
                <span className="font-medium">{driver.assigned_bus || 'Not Assigned'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Shift:</span>
                <span className="font-medium">{driver.shift_type}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Trips:</span>
                <span className="font-medium">{driver.total_trips.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">On-Time Rate:</span>
                <span className="font-medium">{driver.on_time_percentage}%</span>
              </div>
            </div>

            {/* License Status */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">License:</span>
                <div className="flex items-center space-x-2">
                  {isLicenseExpiring(driver.license_expiry) ? (
                    <span className="text-yellow-600 text-xs">Expires Soon</span>
                  ) : (
                    <span className="text-green-600 text-xs">Valid</span>
                  )}
                  <Calendar className="h-4 w-4 text-gray-400" />
                </div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Expires: {new Date(driver.license_expiry).toLocaleDateString()}
              </p>
            </div>

            {/* Actions */}
            <div className="mt-4 flex justify-between items-center">
              <div className="flex space-x-2">
                <button className="text-primary-600 hover:text-primary-900">
                  <Users className="h-4 w-4" />
                </button>
                <button className="text-blue-600 hover:text-blue-900">
                  <Phone className="h-4 w-4" />
                </button>
              </div>

              <button className="btn btn-outline btn-sm">
                View Profile
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredDrivers.length === 0 && (
        <div className="text-center py-12">
          <Users className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <div className="text-gray-500 mb-4">No drivers found</div>
          <button className="btn btn-primary">
            Add Your First Driver
          </button>
        </div>
      )}
    </div>
  );
};

export default DriverManagement;
