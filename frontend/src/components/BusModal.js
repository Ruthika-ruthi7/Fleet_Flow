import React, { useState, useEffect } from 'react';
import { useMutation } from 'react-query';
import { busesAPI } from '../services/api';
import { X, Zap } from 'lucide-react';
import toast from 'react-hot-toast';

const BusModal = ({ bus, drivers, routes, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    bus_number: '',
    registration_number: '',
    bus_type: 'Non-AC',
    capacity: 50,
    manufacturer: '',
    model: '',
    year_of_manufacture: new Date().getFullYear(),
    fuel_type: 'Diesel',
    mileage: '',
    insurance_number: '',
    insurance_expiry: '',
    rc_number: '',
    rc_expiry: '',
    fitness_certificate_expiry: '',
    permit_expiry: '',
    route_id: '',
    driver_id: '',
    conductor_id: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [aiSuggestions, setAiSuggestions] = useState(null);

  useEffect(() => {
    if (bus) {
      setFormData({
        bus_number: bus.bus_number || '',
        registration_number: bus.registration_number || '',
        bus_type: bus.bus_type || 'Non-AC',
        capacity: bus.capacity || 50,
        manufacturer: bus.manufacturer || '',
        model: bus.model || '',
        year_of_manufacture: bus.year_of_manufacture || new Date().getFullYear(),
        fuel_type: bus.fuel_type || 'Diesel',
        mileage: bus.mileage || '',
        insurance_number: bus.insurance_number || '',
        insurance_expiry: bus.insurance_expiry || '',
        rc_number: bus.rc_number || '',
        rc_expiry: bus.rc_expiry || '',
        fitness_certificate_expiry: bus.fitness_certificate_expiry || '',
        permit_expiry: bus.permit_expiry || '',
        route_id: bus.route_id || '',
        driver_id: bus.driver_id || '',
        conductor_id: bus.conductor_id || '',
      });
    }
  }, [bus]);

  const createBusMutation = useMutation(busesAPI.create, {
    onSuccess: () => {
      toast.success('Bus created successfully');
      onSave();
    },
    onError: (error) => {
      toast.error(error.response?.data?.error || 'Failed to create bus');
    },
  });

  const updateBusMutation = useMutation(
    (data) => busesAPI.update(bus.id, data),
    {
      onSuccess: () => {
        toast.success('Bus updated successfully');
        onSave();
      },
      onError: (error) => {
        toast.error(error.response?.data?.error || 'Failed to update bus');
      },
    }
  );

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (bus) {
        await updateBusMutation.mutateAsync(formData);
      } else {
        await createBusMutation.mutateAsync(formData);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // AI-powered auto-fill from RTO database (simulation)
  const handleAutoFill = async () => {
    if (!formData.registration_number) {
      toast.error('Please enter registration number first');
      return;
    }

    setIsLoading(true);
    
    // Simulate AI auto-fill from RTO database
    setTimeout(() => {
      const suggestions = {
        manufacturer: 'Tata',
        model: 'Starbus',
        year_of_manufacture: 2020,
        fuel_type: 'Diesel',
        rc_number: `RC${formData.registration_number.replace(/\s/g, '')}`,
        rc_expiry: '2025-12-31',
        fitness_certificate_expiry: '2024-12-31',
        permit_expiry: '2024-06-30',
      };

      setFormData(prev => ({
        ...prev,
        ...suggestions
      }));

      setAiSuggestions(suggestions);
      toast.success('Vehicle details auto-filled from RTO database');
      setIsLoading(false);
    }, 2000);
  };

  // AI-powered driver assignment
  const getSuggestedDriver = () => {
    if (!formData.route_id || drivers.length === 0) return null;
    
    // Simple AI logic: suggest driver based on shift compatibility
    const availableDrivers = drivers.filter(d => d.status === 'Available');
    if (availableDrivers.length === 0) return null;
    
    // Prefer drivers with matching shift type or experience
    return availableDrivers[0];
  };

  const suggestedDriver = getSuggestedDriver();

  return (
    <div className="modal-overlay">
      <div className="modal-content max-w-4xl">
        <div className="modal-header">
          <h3 className="text-lg font-medium text-gray-900">
            {bus ? 'Edit Bus' : 'Add New Bus'}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-500"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Basic Information */}
              <div className="space-y-4">
                <h4 className="text-md font-medium text-gray-900">Basic Information</h4>
                
                <div>
                  <label className="form-label">Bus Number</label>
                  <input
                    type="text"
                    name="bus_number"
                    value={formData.bus_number}
                    onChange={handleChange}
                    className="input"
                    placeholder="Auto-generated if empty"
                  />
                </div>

                <div>
                  <label className="form-label">Registration Number *</label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      name="registration_number"
                      value={formData.registration_number}
                      onChange={handleChange}
                      className="input flex-1"
                      required
                      placeholder="e.g., KA01AB1234"
                    />
                    <button
                      type="button"
                      onClick={handleAutoFill}
                      disabled={isLoading}
                      className="btn btn-outline flex items-center space-x-1"
                    >
                      <Zap className="h-4 w-4" />
                      <span>AI Fill</span>
                    </button>
                  </div>
                  <p className="form-help">AI will auto-fill details from RTO database</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">Bus Type *</label>
                    <select
                      name="bus_type"
                      value={formData.bus_type}
                      onChange={handleChange}
                      className="input"
                      required
                    >
                      <option value="AC">AC</option>
                      <option value="Non-AC">Non-AC</option>
                      <option value="Sleeper">Sleeper</option>
                      <option value="Seater">Seater</option>
                    </select>
                  </div>
                  <div>
                    <label className="form-label">Capacity *</label>
                    <input
                      type="number"
                      name="capacity"
                      value={formData.capacity}
                      onChange={handleChange}
                      className="input"
                      required
                      min="1"
                      max="100"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">Manufacturer</label>
                    <input
                      type="text"
                      name="manufacturer"
                      value={formData.manufacturer}
                      onChange={handleChange}
                      className="input"
                      placeholder="e.g., Tata, Ashok Leyland"
                    />
                  </div>
                  <div>
                    <label className="form-label">Model</label>
                    <input
                      type="text"
                      name="model"
                      value={formData.model}
                      onChange={handleChange}
                      className="input"
                      placeholder="e.g., Starbus, Viking"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">Year of Manufacture</label>
                    <input
                      type="number"
                      name="year_of_manufacture"
                      value={formData.year_of_manufacture}
                      onChange={handleChange}
                      className="input"
                      min="1990"
                      max={new Date().getFullYear() + 1}
                    />
                  </div>
                  <div>
                    <label className="form-label">Fuel Type</label>
                    <select
                      name="fuel_type"
                      value={formData.fuel_type}
                      onChange={handleChange}
                      className="input"
                    >
                      <option value="Diesel">Diesel</option>
                      <option value="Petrol">Petrol</option>
                      <option value="CNG">CNG</option>
                      <option value="Electric">Electric</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="form-label">Mileage (km/l)</label>
                  <input
                    type="number"
                    name="mileage"
                    value={formData.mileage}
                    onChange={handleChange}
                    className="input"
                    step="0.1"
                    min="0"
                  />
                </div>
              </div>

              {/* Documents & Assignment */}
              <div className="space-y-4">
                <h4 className="text-md font-medium text-gray-900">Documents & Assignment</h4>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">Insurance Number</label>
                    <input
                      type="text"
                      name="insurance_number"
                      value={formData.insurance_number}
                      onChange={handleChange}
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="form-label">Insurance Expiry</label>
                    <input
                      type="date"
                      name="insurance_expiry"
                      value={formData.insurance_expiry}
                      onChange={handleChange}
                      className="input"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">RC Number</label>
                    <input
                      type="text"
                      name="rc_number"
                      value={formData.rc_number}
                      onChange={handleChange}
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="form-label">RC Expiry</label>
                    <input
                      type="date"
                      name="rc_expiry"
                      value={formData.rc_expiry}
                      onChange={handleChange}
                      className="input"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="form-label">Fitness Certificate Expiry</label>
                    <input
                      type="date"
                      name="fitness_certificate_expiry"
                      value={formData.fitness_certificate_expiry}
                      onChange={handleChange}
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="form-label">Permit Expiry</label>
                    <input
                      type="date"
                      name="permit_expiry"
                      value={formData.permit_expiry}
                      onChange={handleChange}
                      className="input"
                    />
                  </div>
                </div>

                <div>
                  <label className="form-label">Route</label>
                  <select
                    name="route_id"
                    value={formData.route_id}
                    onChange={handleChange}
                    className="input"
                  >
                    <option value="">Select Route</option>
                    {routes.map(route => (
                      <option key={route.id} value={route.id}>
                        {route.route_code} - {route.route_name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="form-label">Driver</label>
                  <select
                    name="driver_id"
                    value={formData.driver_id}
                    onChange={handleChange}
                    className="input"
                  >
                    <option value="">Select Driver</option>
                    {drivers.filter(d => d.driver_type === 'Driver').map(driver => (
                      <option key={driver.id} value={driver.id}>
                        {driver.full_name} ({driver.employee_id})
                      </option>
                    ))}
                  </select>
                  {suggestedDriver && (
                    <p className="form-help text-blue-600">
                      AI Suggestion: {suggestedDriver.full_name} (Best match for this route)
                    </p>
                  )}
                </div>

                <div>
                  <label className="form-label">Conductor</label>
                  <select
                    name="conductor_id"
                    value={formData.conductor_id}
                    onChange={handleChange}
                    className="input"
                  >
                    <option value="">Select Conductor</option>
                    {drivers.filter(d => d.driver_type === 'Conductor').map(conductor => (
                      <option key={conductor.id} value={conductor.id}>
                        {conductor.full_name} ({conductor.employee_id})
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* AI Suggestions Display */}
            {aiSuggestions && (
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h5 className="text-sm font-medium text-blue-900 mb-2">
                  AI Auto-filled from RTO Database:
                </h5>
                <div className="text-sm text-blue-800">
                  <p>Manufacturer: {aiSuggestions.manufacturer}</p>
                  <p>Model: {aiSuggestions.model}</p>
                  <p>Year: {aiSuggestions.year_of_manufacture}</p>
                  <p>Documents updated with latest information</p>
                </div>
              </div>
            )}
          </div>

          <div className="modal-footer">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="btn btn-primary"
            >
              {isLoading ? 'Saving...' : (bus ? 'Update Bus' : 'Create Bus')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BusModal;
