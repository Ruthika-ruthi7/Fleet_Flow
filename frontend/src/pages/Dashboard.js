import React from 'react';
import { useQuery } from 'react-query';
import { dashboardAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import {
  Bus, Users, UserCheck, AlertTriangle,
  TrendingUp, Clock, MapPin, DollarSign
} from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const { user, isAdmin, isDriver, isStudent } = useAuth();

  // Fetch dashboard stats
  const { data: statsData, isLoading } = useQuery(
    'dashboard-stats',
    dashboardAPI.getStats
  );

  if (isLoading) return <LoadingSpinner text="Loading dashboard..." />;

  const stats = statsData?.data?.data || {};

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold">
          Welcome back, {user?.first_name}!
        </h1>
        <p className="text-primary-100 mt-1">
          {isAdmin() && "Manage your bus fleet with AI-powered insights"}
          {isDriver() && "Your daily operations dashboard"}
          {isStudent() && "Track your bus and attendance"}
        </p>
      </div>

      {/* Admin Dashboard */}
      {isAdmin() && (
        <AdminDashboard stats={stats} />
      )}

      {/* Driver Dashboard */}
      {isDriver() && (
        <DriverDashboard stats={stats} />
      )}

      {/* Student Dashboard */}
      {isStudent() && (
        <StudentDashboard stats={stats} />
      )}
    </div>
  );
};

const AdminDashboard = ({ stats }) => {
  const quickStats = [
    {
      name: 'Total Buses',
      value: stats.total_buses || 0,
      icon: Bus,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      change: `${stats.active_buses || 0} Active, ${stats.maintenance_buses || 0} Maintenance`,
    },
    {
      name: 'Drivers & Staff',
      value: stats.total_drivers || 0,
      icon: Users,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      change: 'Drivers & Conductors',
    },
    {
      name: 'Students Enrolled',
      value: stats.total_students || 0,
      icon: UserCheck,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      change: 'Active enrollments',
    },
    {
      name: 'Active Routes',
      value: stats.total_routes || 0,
      icon: MapPin,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
      change: `${stats.daily_trips || 0} daily trips`,
    },
    {
      name: 'Average Occupancy',
      value: `${Math.round(stats.average_occupancy || 0)}%`,
      icon: TrendingUp,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100',
      change: 'Fleet utilization',
    },
    {
      name: 'Daily Revenue',
      value: `₹${(stats.revenue_today || 0).toLocaleString()}`,
      icon: DollarSign,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-100',
      change: 'Today\'s earnings',
    },
  ];

  const alerts = [
    {
      type: 'danger',
      message: 'TRP004 (Eicher Skyline) - Insurance EXPIRED! Immediate action required',
      icon: AlertTriangle,
      priority: 'high'
    },
    {
      type: 'warning',
      message: 'TRP003 (Mahindra Tourister) currently under maintenance',
      icon: Clock,
      priority: 'medium'
    },
    {
      type: 'warning',
      message: 'Mike Wilson\'s license expires in 45 days (Oct 2024)',
      icon: AlertTriangle,
      priority: 'medium'
    },
    {
      type: 'info',
      message: 'TRP002 insurance expires in 90 days - renewal reminder',
      icon: Clock,
      priority: 'low'
    },
    {
      type: 'info',
      message: 'Route optimization available: 15% efficiency improvement possible',
      icon: TrendingUp,
      priority: 'low'
    },
  ];

  return (
    <>
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {quickStats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-xs text-gray-500">{stat.change}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alerts */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">System Alerts & Notifications</h3>
          <div className="space-y-3">
            {alerts.map((alert, index) => {
              const Icon = alert.icon;
              const alertStyles = {
                danger: 'bg-red-50 border-red-200 text-red-800',
                warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
                info: 'bg-blue-50 border-blue-200 text-blue-800'
              };
              const iconStyles = {
                danger: 'text-red-600',
                warning: 'text-yellow-600',
                info: 'text-blue-600'
              };

              return (
                <div key={index} className={`flex items-start space-x-3 p-3 border rounded-lg ${alertStyles[alert.type]}`}>
                  <Icon className={`h-5 w-5 mt-0.5 ${iconStyles[alert.type]}`} />
                  <div className="flex-1">
                    <span className="text-sm font-medium">{alert.message}</span>
                    {alert.priority && (
                      <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
                        alert.priority === 'high' ? 'bg-red-100 text-red-700' :
                        alert.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {alert.priority.toUpperCase()}
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Fleet Overview */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Fleet Overview</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <span className="text-sm font-medium text-green-900">TRP001 - Tata Starbus</span>
                  <p className="text-xs text-green-700">AC, 45 seats • John Smith (Driver)</p>
                </div>
              </div>
              <span className="text-xs text-green-600 font-medium">85% Occupied</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <div>
                  <span className="text-sm font-medium text-green-900">TRP002 - Ashok Leyland Viking</span>
                  <p className="text-xs text-green-700">Non-AC, 50 seats • Sarah Johnson (Driver)</p>
                </div>
              </div>
              <span className="text-xs text-green-600 font-medium">72% Occupied</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div>
                  <span className="text-sm font-medium text-red-900">TRP004 - Eicher Skyline</span>
                  <p className="text-xs text-red-700">Non-AC, 55 seats • Insurance EXPIRED</p>
                </div>
              </div>
              <span className="text-xs text-red-600 font-medium">90% Occupied</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div>
                  <span className="text-sm font-medium text-yellow-900">TRP003 - Mahindra Tourister</span>
                  <p className="text-xs text-yellow-700">AC, 40 seats • Under Maintenance</p>
                </div>
              </div>
              <span className="text-xs text-yellow-600 font-medium">Offline</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <div>
                  <span className="text-sm font-medium text-blue-900">TRP005 - BYD K7M Electric</span>
                  <p className="text-xs text-blue-700">Electric, 35 seats • Emily Chen (Driver)</p>
                </div>
              </div>
              <span className="text-xs text-blue-600 font-medium">65% Occupied</span>
            </div>
          </div>
        </div>
      </div>

      {/* Routes and Drivers Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Routes */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Active Routes</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">City Center → School District</span>
                <p className="text-xs text-gray-600">15.5 km • 6 daily trips • 8 stops</p>
              </div>
              <span className="text-xs text-green-600 font-medium">TRP001</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">Residential Area → College Campus</span>
                <p className="text-xs text-gray-600">22.3 km • 8 daily trips • 12 stops</p>
              </div>
              <span className="text-xs text-green-600 font-medium">TRP002</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">Industrial Area → Tech Park</span>
                <p className="text-xs text-gray-600">18.7 km • 10 daily trips • 6 stops</p>
              </div>
              <span className="text-xs text-green-600 font-medium">TRP004</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">Metro Station → Airport</span>
                <p className="text-xs text-gray-600">35.2 km • 12 daily trips • 4 stops</p>
              </div>
              <span className="text-xs text-blue-600 font-medium">TRP005</span>
            </div>
          </div>
        </div>

        {/* Driver Performance */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Driver Performance</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">John Smith (Driver)</span>
                <p className="text-xs text-gray-600">TRP001 • 8 years experience</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-green-600 font-medium">4.8★</span>
                <p className="text-xs text-gray-500">Available</p>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">Sarah Johnson (Driver)</span>
                <p className="text-xs text-gray-600">TRP002 • 5 years experience</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-green-600 font-medium">4.6★</span>
                <p className="text-xs text-blue-500">On Trip</p>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">Robert Davis (Driver)</span>
                <p className="text-xs text-gray-600">TRP004 • 12 years experience</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-green-600 font-medium">4.9★</span>
                <p className="text-xs text-blue-500">On Trip</p>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <span className="text-sm font-medium text-gray-900">Mike Wilson (Conductor)</span>
                <p className="text-xs text-gray-600">TRP001 • License expires Oct 2024</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-green-600 font-medium">4.7★</span>
                <p className="text-xs text-yellow-500">License Alert</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

const DriverDashboard = ({ stats }) => {
  const driverStats = [
    {
      name: 'Today\'s Trips',
      value: stats.todays_trips || 0,
      icon: Bus,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      name: 'Students Transported',
      value: stats.students_transported || 0,
      icon: UserCheck,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      name: 'On-Time Performance',
      value: `${stats.on_time_percentage || 95}%`,
      icon: Clock,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      name: 'Distance Covered',
      value: `${stats.distance_covered || 0} km`,
      icon: MapPin,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
  ];

  return (
    <>
      {/* Driver Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {driverStats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Today's Schedule */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Today's Schedule</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
              <div>
                <p className="font-medium text-green-900">Morning Route</p>
                <p className="text-sm text-green-700">City Center → School</p>
              </div>
              <span className="badge badge-success">Completed</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
              <div>
                <p className="font-medium text-blue-900">Evening Route</p>
                <p className="text-sm text-blue-700">School → City Center</p>
              </div>
              <span className="badge badge-primary">Upcoming</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full btn btn-primary text-left">
              Start Trip
            </button>
            <button className="w-full btn btn-outline text-left">
              Mark Attendance
            </button>
            <button className="w-full btn btn-outline text-left">
              Report Issue
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

const StudentDashboard = ({ stats }) => {
  const studentStats = [
    {
      name: 'Attendance Rate',
      value: `${stats.attendance_percentage || 95}%`,
      icon: UserCheck,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      name: 'Monthly Fee',
      value: `₹${stats.monthly_fee || 2000}`,
      icon: DollarSign,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      name: 'Bus Status',
      value: stats.bus_status || 'On Route',
      icon: Bus,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      name: 'ETA',
      value: stats.eta || '15 min',
      icon: Clock,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
    },
  ];

  return (
    <>
      {/* Student Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {studentStats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bus Tracking */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Live Bus Tracking</h3>
          <div className="bg-gray-100 rounded-lg h-48 flex items-center justify-center">
            <div className="text-center">
              <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-600">Bus location will appear here</p>
            </div>
          </div>
        </div>

        {/* Recent Trips */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Trips</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium">Morning Trip</p>
                <p className="text-sm text-gray-600">Today, 7:30 AM</p>
              </div>
              <span className="badge badge-success">Present</span>
            </div>
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium">Evening Trip</p>
                <p className="text-sm text-gray-600">Yesterday, 3:30 PM</p>
              </div>
              <span className="badge badge-success">Present</span>
            </div>
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium">Morning Trip</p>
                <p className="text-sm text-gray-600">Yesterday, 7:30 AM</p>
              </div>
              <span className="badge badge-danger">Absent</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
