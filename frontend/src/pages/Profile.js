import React from 'react';
import { User, Edit, Key } from 'lucide-react';

const Profile = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600">Manage your account settings and preferences</p>
        </div>
        <button className="btn btn-primary flex items-center space-x-2">
          <Edit className="h-5 w-5" />
          <span>Edit Profile</span>
        </button>
      </div>

      <div className="card text-center py-12">
        <User className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">User Profile</h3>
        <p className="text-gray-600 mb-6">
          Manage your personal information, preferences, and security settings.
        </p>
        <div className="space-y-2 text-sm text-gray-500">
          <p>✓ Personal information management</p>
          <p>✓ Password and security settings</p>
          <p>✓ Notification preferences</p>
          <p>✓ Role-specific profile data</p>
          <p>✓ Account activity history</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;
