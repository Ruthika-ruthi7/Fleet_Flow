import React from 'react';
import { MapPin, Navigation, Clock } from 'lucide-react';

const LiveTracking = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Live Tracking</h1>
          <p className="text-gray-600">Real-time GPS tracking with location-based notifications</p>
        </div>
      </div>

      <div className="card text-center py-12">
        <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Live GPS Tracking</h3>
        <p className="text-gray-600 mb-6">
          Real-time bus tracking with interactive maps and smart notifications.
        </p>
        <div className="space-y-2 text-sm text-gray-500">
          <p>✓ Real-time GPS tracking on interactive maps</p>
          <p>✓ Live location updates via WebSocket</p>
          <p>✓ ETA calculations for each stop</p>
          <p>✓ Geofencing and location-based alerts</p>
          <p>✓ Route deviation detection</p>
          <p>✓ Parent and student notifications</p>
        </div>
      </div>
    </div>
  );
};

export default LiveTracking;
