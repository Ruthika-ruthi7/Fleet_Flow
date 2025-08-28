import React, { useState, useEffect } from 'react';
import { MapPin, Clock, Users, Navigation, Zap } from 'lucide-react';

const BusTracking = () => {
  const [trackingData, setTrackingData] = useState([]);
  const [selectedBus, setSelectedBus] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mock tracking data - in real app this would come from API
  useEffect(() => {
    const mockData = [
      {
        bus_id: 1,
        bus_number: 'TRP001',
        route_name: 'City Center → School District',
        current_location: { lat: 12.9716, lng: 77.5946 },
        current_stop: 'City Center Bus Terminal',
        next_stop: 'Mall Junction',
        eta_next_stop: 8,
        total_stops_remaining: 6,
        speed: 35,
        occupancy: 38,
        capacity: 45,
        driver_name: 'John Smith'
      },
      {
        bus_id: 2,
        bus_number: 'TRP002',
        route_name: 'Residential Area → College Campus',
        current_location: { lat: 12.9352, lng: 77.6245 },
        current_stop: 'Sunrise Apartments',
        next_stop: 'Tech University Gate',
        eta_next_stop: 12,
        total_stops_remaining: 8,
        speed: 28,
        occupancy: 36,
        capacity: 50,
        driver_name: 'Sarah Johnson'
      },
      {
        bus_id: 4,
        bus_number: 'TRP004',
        route_name: 'Industrial Area → Tech Park',
        current_location: { lat: 12.8456, lng: 77.6632 },
        current_stop: 'Industrial Complex Gate',
        next_stop: 'Software Tech Park',
        eta_next_stop: 15,
        total_stops_remaining: 4,
        speed: 42,
        occupancy: 50,
        capacity: 55,
        driver_name: 'Robert Davis'
      },
      {
        bus_id: 5,
        bus_number: 'TRP005',
        route_name: 'Metro Station → Airport',
        current_location: { lat: 13.1986, lng: 77.7066 },
        current_stop: 'Central Metro Station',
        next_stop: 'International Airport',
        eta_next_stop: 25,
        total_stops_remaining: 2,
        speed: 55,
        occupancy: 23,
        capacity: 35,
        driver_name: 'Emily Chen'
      }
    ];
    
    setTrackingData(mockData);
    setLoading(false);
  }, []);

  const getOccupancyColor = (occupancy, capacity) => {
    const percentage = (occupancy / capacity) * 100;
    if (percentage >= 90) return 'text-red-600 bg-red-100';
    if (percentage >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getSpeedColor = (speed) => {
    if (speed >= 50) return 'text-blue-600';
    if (speed >= 30) return 'text-green-600';
    if (speed > 0) return 'text-yellow-600';
    return 'text-gray-600';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Live Bus Tracking</h1>
          <p className="text-gray-600">Real-time location and ETA for all active buses</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span>Live Updates</span>
        </div>
      </div>

      {/* Google Maps Integration Notice */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="flex items-center space-x-3">
          <MapPin className="h-6 w-6 text-blue-600" />
          <div>
            <h3 className="text-lg font-medium text-blue-900">Google Maps Integration</h3>
            <p className="text-blue-700 text-sm">
              Interactive map with real-time bus locations, route visualization, and ETA calculations.
              Students can track their bus and get accurate arrival times.
            </p>
          </div>
        </div>
        <div className="mt-4 p-4 bg-white rounded-lg border border-blue-200">
          <div className="text-center text-gray-500">
            <MapPin className="h-16 w-16 mx-auto mb-2 text-gray-400" />
            <p className="text-sm">Google Maps will be integrated here</p>
            <p className="text-xs">Showing bus locations, routes, and real-time tracking</p>
          </div>
        </div>
      </div>

      {/* Active Buses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {trackingData.map((bus) => (
          <div key={bus.bus_id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {bus.bus_number}
                </h3>
                <p className="text-sm text-gray-600">{bus.route_name}</p>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 text-xs rounded-full ${getOccupancyColor(bus.occupancy, bus.capacity)}`}>
                  {Math.round((bus.occupancy / bus.capacity) * 100)}% Full
                </span>
                <span className="badge badge-success">Active</span>
              </div>
            </div>

            {/* Current Status */}
            <div className="space-y-3 mb-4">
              <div className="flex items-center space-x-3">
                <MapPin className="h-5 w-5 text-blue-600" />
                <div>
                  <span className="text-sm font-medium text-gray-900">Current Stop:</span>
                  <p className="text-sm text-gray-600">{bus.current_stop}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Navigation className="h-5 w-5 text-green-600" />
                <div>
                  <span className="text-sm font-medium text-gray-900">Next Stop:</span>
                  <p className="text-sm text-gray-600">{bus.next_stop}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Clock className="h-5 w-5 text-orange-600" />
                <div>
                  <span className="text-sm font-medium text-gray-900">ETA:</span>
                  <p className="text-sm text-gray-600">{bus.eta_next_stop} minutes</p>
                </div>
              </div>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{bus.occupancy}/{bus.capacity}</div>
                <div className="text-xs text-gray-600">Passengers</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className={`text-lg font-bold ${getSpeedColor(bus.speed)}`}>{bus.speed} km/h</div>
                <div className="text-xs text-gray-600">Speed</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-bold text-gray-900">{bus.total_stops_remaining}</div>
                <div className="text-xs text-gray-600">Stops Left</div>
              </div>
            </div>

            {/* Driver Info */}
            <div className="flex items-center justify-between pt-3 border-t border-gray-200">
              <div className="flex items-center space-x-2">
                <Users className="h-4 w-4 text-gray-400" />
                <span className="text-sm text-gray-600">Driver: {bus.driver_name}</span>
              </div>
              <button 
                onClick={() => setSelectedBus(bus)}
                className="btn btn-outline btn-sm"
              >
                View Route
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Student View Section */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Student Bus Tracking</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">For Students & Parents:</h4>
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Real-time bus location on map</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Accurate arrival time at your stop</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span>Bus occupancy and availability</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span>Route delays and notifications</span>
              </div>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Example Student View:</h4>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-blue-900">Your Bus: TRP001</span>
                <span className="text-sm text-blue-600">On Route</span>
              </div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-blue-700">Current Stop:</span>
                  <span className="text-blue-900">City Center</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-blue-700">Your Stop ETA:</span>
                  <span className="text-blue-900 font-medium">8 minutes</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-blue-700">Seats Available:</span>
                  <span className="text-blue-900">7 seats</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Route Details Modal */}
      {selectedBus && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {selectedBus.bus_number} Route Details
              </h3>
              <button 
                onClick={() => setSelectedBus(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-gray-900">Route:</span>
                <p className="text-sm text-gray-600">{selectedBus.route_name}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-900">Current Location:</span>
                <p className="text-sm text-gray-600">
                  {selectedBus.current_location.lat.toFixed(4)}, {selectedBus.current_location.lng.toFixed(4)}
                </p>
              </div>
              <div>
                <span className="text-sm font-medium text-gray-900">Next Stop ETA:</span>
                <p className="text-sm text-gray-600">{selectedBus.eta_next_stop} minutes</p>
              </div>
            </div>
            
            <div className="mt-6 flex justify-end">
              <button 
                onClick={() => setSelectedBus(null)}
                className="btn btn-primary"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BusTracking;
