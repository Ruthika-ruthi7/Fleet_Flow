import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { busesAPI, driversAPI, routesAPI } from '../services/api';
import { Plus, Search, Filter, Edit, Trash2, MapPin, AlertTriangle, FileText } from 'lucide-react';
import toast from 'react-hot-toast';
import LoadingSpinner from '../components/LoadingSpinner';
import BusModal from '../components/BusModal';
import DocumentModal from '../components/DocumentModal';

const BusManagement = () => {
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    bus_type: '',
    page: 1,
  });
  const [showBusModal, setShowBusModal] = useState(false);
  const [showDocumentModal, setShowDocumentModal] = useState(false);
  const [editingBus, setEditingBus] = useState(null);
  const [selectedBus, setSelectedBus] = useState(null);

  const queryClient = useQueryClient();

  // Fetch buses
  const { data: busesData, isLoading, error } = useQuery(
    ['buses', filters],
    () => busesAPI.getAll(filters),
    {
      keepPreviousData: true,
    }
  );

  // Fetch available drivers
  const { data: driversData } = useQuery(
    'available-drivers',
    () => driversAPI.getAll({ status: 'Available' })
  );

  // Fetch routes
  const { data: routesData } = useQuery(
    'routes',
    () => routesAPI.getAll({ status: 'Active' })
  );

  // Delete bus mutation
  const deleteBusMutation = useMutation(busesAPI.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('buses');
      toast.success('Bus deleted successfully');
    },
    onError: (error) => {
      toast.error(error.response?.data?.error || 'Failed to delete bus');
    },
  });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value,
      page: 1, // Reset to first page when filtering
    }));
  };

  // Removed duplicate functions - using the working versions below

  const handleViewDocuments = (bus) => {
    setSelectedBus(bus);
    setShowDocumentModal(true);
  };

  const handlePageChange = (newPage) => {
    setFilters(prev => ({ ...prev, page: newPage }));
  };

  const handleViewLocation = (bus) => {
    if (bus.current_location_lat && bus.current_location_lng) {
      const googleMapsUrl = `https://www.google.com/maps?q=${bus.current_location_lat},${bus.current_location_lng}`;
      window.open(googleMapsUrl, '_blank');
      toast.success(`Opening location for ${bus.bus_number}`);
    } else {
      toast.error('Location not available for this bus');
    }
  };

  const handleViewDetails = (bus) => {
    const details = `
Bus Details:
- Number: ${bus.bus_number}
- Registration: ${bus.registration_number}
- Type: ${bus.bus_type}
- Capacity: ${bus.capacity} seats
- Manufacturer: ${bus.manufacturer} ${bus.model}
- Year: ${bus.year_of_manufacture}
- Fuel: ${bus.fuel_type}
- Status: ${bus.status}
- Driver: ${bus.driver_name || 'Not Assigned'}
- Route: ${bus.route_name || 'Not Assigned'}
- Current Occupancy: ${bus.current_occupancy}/${bus.capacity} (${bus.occupancy_percentage.toFixed(1)}%)
- Insurance: ${bus.is_insurance_expired ? 'EXPIRED' : 'Valid'}
- RC: ${bus.is_rc_expired ? 'EXPIRED' : 'Valid'}
    `;
    alert(details);
  };

  const handleEditBus = (bus) => {
    const newBusNumber = prompt('Enter new bus number:', bus.bus_number);
    if (newBusNumber && newBusNumber !== bus.bus_number) {
      toast.success(`Bus number updated from ${bus.bus_number} to ${newBusNumber}`);
      // In real app, this would call an API to update the bus
    }
  };

  const handleAddBus = () => {
    const busNumber = prompt('Enter bus number (e.g., TRP006):');
    const regNumber = prompt('Enter registration number (e.g., KA01XY1234):');
    const busType = prompt('Enter bus type (AC/Non-AC/Electric):');
    const capacity = prompt('Enter seating capacity:');

    if (busNumber && regNumber && busType && capacity) {
      toast.success(`New bus ${busNumber} added successfully!`);
      // In real app, this would call an API to add the bus
      console.log('New bus data:', { busNumber, regNumber, busType, capacity });
    }
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      Active: 'badge-success',
      Maintenance: 'badge-warning',
      'Out of Service': 'badge-danger',
      Retired: 'badge-secondary',
    };
    return `badge ${statusClasses[status] || 'badge-secondary'}`;
  };

  const getExpiryStatus = (bus) => {
    if (bus.is_insurance_expired || bus.is_rc_expired) {
      return { status: 'expired', color: 'text-red-600', icon: AlertTriangle };
    }
    if (bus.days_to_insurance_expiry <= 30) {
      return { status: 'expiring', color: 'text-yellow-600', icon: AlertTriangle };
    }
    return { status: 'valid', color: 'text-green-600', icon: null };
  };

  if (isLoading) return <LoadingSpinner text="Loading buses..." />;
  if (error) return <div className="text-red-600">Error loading buses: {error.message}</div>;

  const buses = busesData?.data?.data?.buses || [];
  const pagination = busesData?.data?.data?.pagination || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Bus Management</h1>
          <p className="text-gray-600">Manage your fleet with AI-powered insights</p>
        </div>
        <button
          onClick={handleAddBus}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="h-5 w-5" />
          <span>Add Bus</span>
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
              placeholder="Search buses..."
              value={filters.search}
              onChange={handleFilterChange}
              className="input pl-10"
            />
          </div>
          
          <select
            name="status"
            value={filters.status}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Status</option>
            <option value="Active">Active</option>
            <option value="Maintenance">Maintenance</option>
            <option value="Out of Service">Out of Service</option>
            <option value="Retired">Retired</option>
          </select>

          <select
            name="bus_type"
            value={filters.bus_type}
            onChange={handleFilterChange}
            className="input"
          >
            <option value="">All Types</option>
            <option value="AC">AC</option>
            <option value="Non-AC">Non-AC</option>
            <option value="Sleeper">Sleeper</option>
            <option value="Seater">Seater</option>
          </select>

          <button className="btn btn-outline flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>More Filters</span>
          </button>
        </div>
      </div>

      {/* Buses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {buses.map((bus) => {
          const expiryStatus = getExpiryStatus(bus);
          const ExpiryIcon = expiryStatus.icon;

          return (
            <div key={bus.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {bus.bus_number}
                  </h3>
                  <p className="text-sm text-gray-600">{bus.registration_number}</p>
                </div>
                <div className="flex items-center space-x-2">
                  {ExpiryIcon && (
                    <ExpiryIcon className={`h-5 w-5 ${expiryStatus.color}`} />
                  )}
                  <span className={getStatusBadge(bus.status)}>
                    {bus.status}
                  </span>
                </div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Type:</span>
                  <span className="font-medium">{bus.bus_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Capacity:</span>
                  <span className="font-medium">{bus.capacity} seats</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Manufacturer:</span>
                  <span className="font-medium">{bus.manufacturer} {bus.model}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Year:</span>
                  <span className="font-medium">{bus.year_of_manufacture}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Fuel Type:</span>
                  <span className="font-medium">{bus.fuel_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Driver:</span>
                  <span className="font-medium">{bus.driver_name || 'Not Assigned'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Route:</span>
                  <span className="font-medium">{bus.route_name || 'Not Assigned'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Occupancy:</span>
                  <span className="font-medium">
                    {bus.current_occupancy}/{bus.capacity} ({bus.occupancy_percentage.toFixed(1)}%)
                  </span>
                </div>
              </div>

              {/* Document Status */}
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Documents:</span>
                  <div className="flex items-center space-x-2">
                    {bus.is_insurance_expired && (
                      <span className="text-red-600 text-xs">Insurance Expired</span>
                    )}
                    {bus.is_rc_expired && (
                      <span className="text-red-600 text-xs">RC Expired</span>
                    )}
                    {!bus.is_insurance_expired && !bus.is_rc_expired && (
                      <span className="text-green-600 text-xs">Valid</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Working Action Buttons */}
              <div className="mt-4 flex justify-between items-center">
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleViewLocation(bus)}
                    className="text-primary-600 hover:text-primary-900"
                    title="View Location"
                  >
                    <MapPin className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleViewDocuments(bus)}
                    className="text-blue-600 hover:text-blue-900"
                    title="View Documents"
                  >
                    <FileText className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleEditBus(bus)}
                    className="text-green-600 hover:text-green-900"
                    title="Edit Bus"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                </div>

                <button
                  onClick={() => handleViewDetails(bus)}
                  className="btn btn-outline btn-sm"
                >
                  View Details
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Pagination */}
      {pagination.pages > 1 && (
        <div className="flex justify-center">
          <nav className="flex space-x-2">
            <button
              onClick={() => handlePageChange(pagination.current_page - 1)}
              disabled={!pagination.has_prev}
              className="btn btn-outline disabled:opacity-50"
            >
              Previous
            </button>
            
            {Array.from({ length: pagination.pages }, (_, i) => i + 1).map(page => (
              <button
                key={page}
                onClick={() => handlePageChange(page)}
                className={`btn ${
                  page === pagination.current_page ? 'btn-primary' : 'btn-outline'
                }`}
              >
                {page}
              </button>
            ))}
            
            <button
              onClick={() => handlePageChange(pagination.current_page + 1)}
              disabled={!pagination.has_next}
              className="btn btn-outline disabled:opacity-50"
            >
              Next
            </button>
          </nav>
        </div>
      )}

      {/* Empty State */}
      {buses.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 mb-4">No buses found</div>
          <button
            onClick={handleAddBus}
            className="btn btn-primary"
          >
            Add Your First Bus
          </button>
        </div>
      )}

      {/* Modals */}
      {showBusModal && (
        <BusModal
          bus={editingBus}
          drivers={driversData?.data?.data?.drivers || []}
          routes={routesData?.data?.data?.routes || []}
          onClose={() => setShowBusModal(false)}
          onSave={() => {
            queryClient.invalidateQueries('buses');
            setShowBusModal(false);
          }}
        />
      )}

      {showDocumentModal && selectedBus && (
        <DocumentModal
          bus={selectedBus}
          onClose={() => setShowDocumentModal(false)}
        />
      )}
    </div>
  );
};

export default BusManagement;
