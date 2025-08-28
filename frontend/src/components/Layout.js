import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  Bus, Users, UserCheck, Calendar, Wrench,
  MapPin, DollarSign, BarChart3, User, LogOut, Menu, X
} from 'lucide-react';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3, roles: ['admin', 'driver', 'conductor', 'student', 'parent'] },
    
    // Phase 1: Bus Setup & Staff Allocation
    { name: 'Bus Management', href: '/buses', icon: Bus, roles: ['admin'] },
    { name: 'Driver Management', href: '/drivers', icon: Users, roles: ['admin'] },
    { name: 'Route Management', href: '/routes', icon: MapPin, roles: ['admin'] },
    
    // Phase 2: Daily Operations
    { name: 'Student Management', href: '/students', icon: UserCheck, roles: ['admin'] },
    { name: 'Fee Management', href: '/fees', icon: DollarSign, roles: ['admin'] },

    // Phase 3: Live Tracking
    { name: 'Live Tracking', href: '/tracking', icon: MapPin, roles: ['admin'] },
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
              <X className="h-6 w-6 text-white" />
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
            className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 md:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
          
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex">
              <div className="w-full flex md:ml-0">
                <div className="relative w-full text-gray-400 focus-within:text-gray-600">
                  <div className="absolute inset-y-0 left-0 flex items-center pointer-events-none">
                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                    </svg>
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
                    className="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    <User className="h-6 w-6" />
                  </Link>
                  
                  <button
                    onClick={handleLogout}
                    className="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    <LogOut className="h-6 w-6" />
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
          <Bus className="h-8 w-8 text-primary-600" />
          <h1 className="ml-2 text-xl font-bold text-gray-900">BusMS</h1>
        </div>
      </div>
      
      <nav className="mt-5 flex-1 px-2 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          const Icon = item.icon;
          
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`${
                isActive
                  ? 'sidebar-link-active'
                  : 'sidebar-link-inactive'
              } sidebar-link group`}
            >
              <Icon
                className={`${
                  isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                } mr-3 h-6 w-6`}
              />
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

export default Layout;
