import React, { useState } from 'react';
import { MapPin, Plus, Search, Filter, Zap, Clock, Users, Bus } from 'lucide-react';

const RouteManagement = () => {
  const [filters, setFilters] = useState({
    search: '',
    route_type: '',
    status: '',
  });

  // Mock route data
  const routes = [
    {
      id: 1, route_name: 'City Center to School District', route_code: 'CC-SD-01',
      start_location: 'City Center Bus Terminal', end_location: 'Green Valley School',
      total_distance: 15.5, estimated_duration: 45, route_type: 'Urban',
      status: 'Active', stops_count: 8, daily_trips: 6,
      assigned_buses: ['TRP001'], students_count: 45,
      peak_occupancy: 85, avg_delay: 3
    },
    {
      id: 2, route_name: 'Residential Area to College Campus', route_code: 'RA-CC-02',
      start_location: 'Sunrise Apartments', end_location: 'Tech University',
      total_distance: 22.3, estimated_duration: 60, route_type: 'Suburban',
      status: 'Active', stops_count: 12, daily_trips: 8,
      assigned_buses: ['TRP002'], students_count: 36,
      peak_occupancy: 72, avg_delay: 5
    },
    {
      id: 3, route_name: 'Industrial Area to Tech Park', route_code: 'IA-TP-03',
      start_location: 'Industrial Complex Gate', end_location: 'Software Tech Park',
      total_distance: 18.7, estimated_duration: 50, route_type: 'Express',
      status: 'Active', stops_count: 6, daily_trips: 10,
      assigned_buses: ['TRP004'], students_count: 50,
      peak_occupancy: 90, avg_delay: 2
    },
    {
      id: 4, route_name: 'Metro Station to Airport', route_code: 'MS-AP-04',
      start_location: 'Central Metro Station', end_location: 'International Airport',
      total_distance: 35.2, estimated_duration: 75, route_type: 'Express',
      status: 'Active', stops_count: 4, daily_trips: 12,
      assigned_buses: ['TRP005'], students_count: 23,
      peak_occupancy: 65, avg_delay: 1
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
      Active: 'badge-success',
      Inactive: 'badge-secondary',
      'Under Review': 'badge-warning',
    };
    return `badge ${statusClasses[status] || 'badge-secondary'}`;
  };

  const getEfficiencyColor = (occupancy) => {
    if (occupancy >= 80) return 'text-green-600';
    if (occupancy >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredRoutes = routes.filter(route => {
    const matchesSearch = !filters.search ||
      route.route_name.toLowerCase().includes(filters.search.toLowerCase()) ||
      route.route_code.toLowerCase().includes(filters.search.toLowerCase());
    const matchesType = !filters.route_type || route.route_type === filters.route_type;
    const matchesStatus = !filters.status || route.status === filters.status;

    return matchesSearch && matchesType && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Route Management</h1>
          <p className="text-gray-600">Manage and optimize transport routes with AI insights</p>
        </div>
        <button className="btn btn-primary flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Create Route</span>
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
              placeholder="Search routes..."
              value={filters.search}
              onChange={handleFilterChange}
              className="input pl-10"
            />
          </div>

          <select
            name="route_type"
            value={filters.route_type}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Types</option>
            <option value="Urban">Urban</option>
            <option value="Suburban">Suburban</option>
            <option value="Express">Express</option>
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
            <option value="Under Review">Under Review</option>
          </select>

          <button className="btn btn-outline flex items-center space-x-2">
            <Zap className="h-5 w-5" />
            <span>AI Optimize</span>
          </button>
        </div>
      </div>

      {/* Routes Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredRoutes.map((route) => (
          <div key={route.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {route.route_name}
                </h3>
                <p className="text-sm text-gray-600">{route.route_code} • {route.route_type}</p>
              </div>
              <span className={getStatusBadge(route.status)}>
                {route.status}
              </span>
            </div>

            {/* Route Details */}
            <div className="space-y-3 mb-4">
              <div className="flex items-center space-x-2 text-sm">
                <MapPin className="h-4 w-4 text-gray-400" />
                <span className="text-gray-600">From:</span>
                <span className="font-medium">{route.start_location}</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <MapPin className="h-4 w-4 text-gray-400" />
                <span className="text-gray-600">To:</span>
                <span className="font-medium">{route.end_location}</span>
              </div>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{route.total_distance} km</div>
                <div className="text-xs text-gray-600">Distance</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{route.estimated_duration} min</div>
                <div className="text-xs text-gray-600">Duration</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{route.stops_count}</div>
                <div className="text-xs text-gray-600">Stops</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{route.daily_trips}</div>
                <div className="text-xs text-gray-600">Daily Trips</div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Assigned Buses:</span>
                <span className="font-medium">{route.assigned_buses.join(', ')}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Students:</span>
                <span className="font-medium">{route.students_count}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Peak Occupancy:</span>
                <span className={`font-medium ${getEfficiencyColor(route.peak_occupancy)}`}>
                  {route.peak_occupancy}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Delay:</span>
                <span className={`font-medium ${route.avg_delay <= 3 ? 'text-green-600' : 'text-yellow-600'}`}>
                  {route.avg_delay} min
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="mt-4 pt-4 border-t border-gray-200 flex justify-between items-center">
              <div className="flex space-x-2">
                <button className="text-primary-600 hover:text-primary-900">
                  <MapPin className="h-4 w-4" />
                </button>
                <button className="text-blue-600 hover:text-blue-900">
                  <Clock className="h-4 w-4" />
                </button>
                <button className="text-green-600 hover:text-green-900">
                  <Users className="h-4 w-4" />
                </button>
              </div>

              <button className="btn btn-outline btn-sm">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* AI Optimization Panel */}
      <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-blue-900">AI Route Optimization</h3>
            <p className="text-blue-700 text-sm">
              Optimize routes for better efficiency and reduced travel time
            </p>
          </div>
          <button className="btn btn-primary flex items-center space-x-2">
            <Zap className="h-5 w-5" />
            <span>Run Optimization</span>
          </button>
        </div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-900">15%</div>
            <div className="text-sm text-blue-700">Potential Time Savings</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-900">8%</div>
            <div className="text-sm text-blue-700">Fuel Cost Reduction</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-900">12%</div>
            <div className="text-sm text-blue-700">Capacity Improvement</div>
          </div>
        </div>
      </div>

      {/* Empty State */}
      {filteredRoutes.length === 0 && (
        <div className="text-center py-12">
          <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <div className="text-gray-500 mb-4">No routes found</div>
          <button className="btn btn-primary">
            Create Your First Route
          </button>
        </div>
      )}
    </div>
  );
};

export default RouteManagement;
