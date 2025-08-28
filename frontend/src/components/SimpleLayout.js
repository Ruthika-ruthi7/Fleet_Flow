import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const SimpleLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', roles: ['admin', 'driver', 'conductor', 'student', 'parent'] },
    { name: 'Bus Management', href: '/buses', roles: ['admin'] },
    { name: 'Driver Management', href: '/drivers', roles: ['admin'] },
    { name: 'Route Management', href: '/routes', roles: ['admin'] },
    { name: 'Student Management', href: '/students', roles: ['admin', 'driver', 'conductor'] },
    { name: 'Trip Management', href: '/trips', roles: ['admin', 'driver', 'conductor'] },
    { name: 'Attendance', href: '/attendance', roles: ['admin', 'driver', 'conductor'] },
    { name: 'Fee Management', href: '/fees', roles: ['admin'] },
    { name: 'Maintenance', href: '/maintenance', roles: ['admin'] },
    { name: 'Live Tracking', href: '/tracking', roles: ['admin', 'driver', 'conductor', 'student', 'parent'] },
    { name: 'Reports', href: '/reports', roles: ['admin'] },
  ];

  const filteredNavigation = navigation.filter(item => 
    !item.roles || item.roles.includes(user?.role)
  );

  return (
    <div className="h-screen flex overflow-hidden bg-gray-100">
      {/* Mobile sidebar */}
      <div className={`${sidebarOpen ? 'block' : 'hidden'} fixed inset-0 flex z-40 md:hidden`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)}></div>
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              ✕
            </button>
          </div>
          <SidebarContent navigation={filteredNavigation} location={location} />
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <SidebarContent navigation={filteredNavigation} location={location} />
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        {/* Top navigation */}
        <div className="relative z-10 flex-shrink-0 flex h-16 bg-white shadow">
          <button
            className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 md:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            ☰
          </button>
          
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex">
              <div className="w-full flex md:ml-0">
                <div className="relative w-full text-gray-400 focus-within:text-gray-600">
                  <div className="absolute inset-y-0 left-0 flex items-center pointer-events-none">
                    <span className="h-5 w-5">🔍</span>
                  </div>
                  <input
                    className="block w-full h-full pl-8 pr-3 py-2 border-transparent text-gray-900 placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-0 focus:border-transparent sm:text-sm"
                    placeholder="Search buses, routes, students..."
                    type="search"
                  />
                </div>
              </div>
            </div>
            
            <div className="ml-4 flex items-center md:ml-6">
              <div className="ml-3 relative">
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <div className="text-sm font-medium text-gray-700">
                      {user?.first_name} {user?.last_name}
                    </div>
                    <div className="text-xs text-gray-500 capitalize">
                      {user?.role}
                    </div>
                  </div>
                  
                  <Link
                    to="/profile"
                    className="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    👤
                  </Link>
                  
                  <button
                    onClick={handleLogout}
                    className="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    🚪
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

const SidebarContent = ({ navigation, location }) => (
  <div className="flex flex-col h-0 flex-1 border-r border-gray-200 bg-white">
    <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
      <div className="flex items-center flex-shrink-0 px-4">
        <div className="flex items-center">
          <span className="text-2xl">🚌</span>
          <h1 className="ml-2 text-xl font-bold text-gray-900">BusMS</h1>
        </div>
      </div>
      
      <nav className="mt-5 flex-1 px-2 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`${
                isActive
                  ? 'bg-blue-100 border-blue-500 text-blue-700'
                  : 'border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              } group flex items-center px-2 py-2 text-sm font-medium border-l-4`}
            >
              <span className="mr-3 text-lg">
                {item.name === 'Dashboard' && '📊'}
                {item.name === 'Bus Management' && '🚌'}
                {item.name === 'Driver Management' && '👨‍💼'}
                {item.name === 'Route Management' && '🗺️'}
                {item.name === 'Student Management' && '👨‍🎓'}
                {item.name === 'Trip Management' && '📅'}
                {item.name === 'Attendance' && '✅'}
                {item.name === 'Fee Management' && '💰'}
                {item.name === 'Maintenance' && '🔧'}
                {item.name === 'Live Tracking' && '📍'}
                {item.name === 'Reports' && '📈'}
              </span>
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
    
    <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
      <div className="text-xs text-gray-500">
        Bus Management System v1.0
      </div>
    </div>
  </div>
);

export default SimpleLayout;
