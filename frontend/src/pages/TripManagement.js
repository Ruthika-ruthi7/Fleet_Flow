import React from 'react';
import { Calendar, Plus, Clock } from 'lucide-react';

const TripManagement = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Trip Management</h1>
          <p className="text-gray-600">Schedule and track daily bus operations</p>
        </div>
        <button className="btn btn-primary flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>Schedule Trip</span>
        </button>
      </div>

      <div className="card text-center py-12">
        <Calendar className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Trip Management</h3>
        <p className="text-gray-600 mb-6">
          Daily trip scheduling with AI-powered delay predictions.
        </p>
        <div className="space-y-2 text-sm text-gray-500">
          <p>✓ Daily trip scheduling and management</p>
          <p>✓ Real-time trip tracking and updates</p>
          <p>✓ AI-powered delay prediction using traffic data</p>
          <p>✓ Automatic parent notifications</p>
          <p>✓ Trip performance analytics</p>
        </div>
      </div>
    </div>
  );
};

export default TripManagement;
