import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import SimpleLayout from './components/SimpleLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import BusManagement from './pages/BusManagement';
import DriverManagement from './pages/DriverManagement';
import RouteManagement from './pages/RouteManagement';
import StudentManagement from './pages/StudentManagement';
import TripManagement from './pages/TripManagement';
import AttendanceManagement from './pages/AttendanceManagement';
import MaintenanceManagement from './pages/MaintenanceManagement';
import FeeManagement from './pages/FeeManagement';
import BusTracking from './pages/BusTracking';
import Reports from './pages/Reports';

import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <SimpleLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              
              {/* Phase 1: Bus Setup & Staff Allocation */}
              <Route 
                path="buses" 
                element={
                  <ProtectedRoute requiredRoles={['admin']}>
                    <BusManagement />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="drivers" 
                element={
                  <ProtectedRoute requiredRoles={['admin']}>
                    <DriverManagement />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="routes" 
                element={
                  <ProtectedRoute requiredRoles={['admin']}>
                    <RouteManagement />
                  </ProtectedRoute>
                } 
              />
              
              {/* Phase 2: Daily Operations */}
              <Route
                path="students"
                element={
                  <ProtectedRoute requiredRoles={['admin', 'driver', 'conductor']}>
                    <StudentManagement />
                  </ProtectedRoute>
                }
              />
              <Route
                path="trips"
                element={
                  <ProtectedRoute requiredRoles={['admin', 'driver']}>
                    <TripManagement />
                  </ProtectedRoute>
                }
              />
              <Route
                path="attendance"
                element={
                  <ProtectedRoute requiredRoles={['admin', 'driver', 'conductor']}>
                    <AttendanceManagement />
                  </ProtectedRoute>
                }
              />
              <Route
                path="fees"
                element={
                  <ProtectedRoute requiredRoles={['admin']}>
                    <FeeManagement />
                  </ProtectedRoute>
                }
              />

              {/* Phase 3: Maintenance & Monitoring */}
              <Route
                path="maintenance"
                element={
                  <ProtectedRoute requiredRoles={['admin']}>
                    <MaintenanceManagement />
                  </ProtectedRoute>
                }
              />}

              <Route
                path="tracking"
                element={
                  <ProtectedRoute>
                    <BusTracking />
                  </ProtectedRoute>
                }
              />
              
              {/* Reports and Profile */}
              <Route
                path="reports"
                element={
                  <ProtectedRoute requiredRoles={['admin']}>
                    <Reports />
                  </ProtectedRoute>
                }
              />
              <Route path="profile" element={<Profile />} />
            </Route>
            
            {/* 404 route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
