import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh and errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(
            `${process.env.REACT_APP_API_URL || 'http://localhost:5000/api'}/auth/refresh`,
            {},
            {
              headers: {
                Authorization: `Bearer ${refreshToken}`,
              },
            }
          );

          const { access_token } = response.data.data;
          localStorage.setItem('access_token', access_token);

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Show error toast for non-401 errors
    if (error.response?.status !== 401) {
      const errorMessage = error.response?.data?.error || 'An error occurred';
      toast.error(errorMessage);
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  refresh: () => api.post('/auth/refresh'),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get('/auth/profile'),
  changePassword: (passwordData) => api.post('/auth/change-password', passwordData),
};

// Buses API
export const busesAPI = {
  getAll: (params = {}) => api.get('/buses', { params }),
  getById: (id) => api.get(`/buses/${id}`),
  create: (busData) => api.post('/buses', busData),
  update: (id, busData) => api.put(`/buses/${id}`, busData),
  delete: (id) => api.delete(`/buses/${id}`),
  updateLocation: (id, location) => api.patch(`/buses/${id}/location`, location),
  getDocuments: (id) => api.get(`/buses/${id}/documents`),
  uploadDocument: (id, formData) => api.post(`/buses/${id}/documents`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
};

// Drivers API
export const driversAPI = {
  getAll: (params = {}) => api.get('/drivers', { params }),
  getById: (id) => api.get(`/drivers/${id}`),
  create: (driverData) => api.post('/drivers', driverData),
  update: (id, driverData) => api.put(`/drivers/${id}`, driverData),
  delete: (id) => api.delete(`/drivers/${id}`),
  getPerformance: (id) => api.get(`/drivers/${id}/performance`),
  updateStatus: (id, status) => api.patch(`/drivers/${id}/status`, { status }),
};

// Routes API
export const routesAPI = {
  getAll: (params = {}) => api.get('/routes', { params }),
  getById: (id) => api.get(`/routes/${id}`),
  create: (routeData) => api.post('/routes', routeData),
  update: (id, routeData) => api.put(`/routes/${id}`, routeData),
  delete: (id) => api.delete(`/routes/${id}`),
  getStops: (id) => api.get(`/routes/${id}/stops`),
  addStop: (id, stopData) => api.post(`/routes/${id}/stops`, stopData),
  updateStop: (routeId, stopId, stopData) => api.put(`/routes/${routeId}/stops/${stopId}`, stopData),
  deleteStop: (routeId, stopId) => api.delete(`/routes/${routeId}/stops/${stopId}`),
  optimize: (id) => api.post(`/routes/${id}/optimize`),
};

// Students API
export const studentsAPI = {
  getAll: (params = {}) => api.get('/students', { params }),
  getById: (id) => api.get(`/students/${id}`),
  create: (studentData) => api.post('/students', studentData),
  update: (id, studentData) => api.put(`/students/${id}`, studentData),
  delete: (id) => api.delete(`/students/${id}`),
  assignRoute: (id, routeData) => api.post(`/students/${id}/assign-route`, routeData),
  getAttendance: (id, params = {}) => api.get(`/students/${id}/attendance`, { params }),
  getFees: (id, params = {}) => api.get(`/students/${id}/fees`, { params }),
  generateQR: (id) => api.post(`/students/${id}/generate-qr`),
};

// Trips API
export const tripsAPI = {
  getAll: (params = {}) => api.get('/trips', { params }),
  getById: (id) => api.get(`/trips/${id}`),
  create: (tripData) => api.post('/trips', tripData),
  update: (id, tripData) => api.put(`/trips/${id}`, tripData),
  delete: (id) => api.delete(`/trips/${id}`),
  start: (id) => api.post(`/trips/${id}/start`),
  end: (id, endData) => api.post(`/trips/${id}/end`, endData),
  getAttendance: (id) => api.get(`/trips/${id}/attendance`),
};

// Maintenance API
export const maintenanceAPI = {
  getAll: (params = {}) => api.get('/maintenance', { params }),
  getById: (id) => api.get(`/maintenance/${id}`),
  create: (maintenanceData) => api.post('/maintenance', maintenanceData),
  update: (id, maintenanceData) => api.put(`/maintenance/${id}`, maintenanceData),
  delete: (id) => api.delete(`/maintenance/${id}`),
  schedule: (maintenanceData) => api.post('/maintenance/schedule', maintenanceData),
  complete: (id, completionData) => api.post(`/maintenance/${id}/complete`, completionData),
  getPredictive: (busId) => api.get(`/maintenance/predictive/${busId}`),
};

// Attendance API
export const attendanceAPI = {
  getAll: (params = {}) => api.get('/attendance', { params }),
  markAttendance: (attendanceData) => api.post('/attendance/mark', attendanceData),
  scanQR: (qrData) => api.post('/attendance/scan-qr', qrData),
  getBulk: (params = {}) => api.get('/attendance/bulk', { params }),
  getReport: (params = {}) => api.get('/attendance/report', { params }),
};

// Fees API
export const feesAPI = {
  getAll: (params = {}) => api.get('/fees', { params }),
  getById: (id) => api.get(`/fees/${id}`),
  create: (feeData) => api.post('/fees', feeData),
  update: (id, feeData) => api.put(`/fees/${id}`, feeData),
  delete: (id) => api.delete(`/fees/${id}`),
  payFee: (id, paymentData) => api.post(`/fees/${id}/pay`, paymentData),
  generateReceipt: (id) => api.get(`/fees/${id}/receipt`),
  sendReminder: (id) => api.post(`/fees/${id}/reminder`),
  bulkGenerate: (generationData) => api.post('/fees/bulk-generate', generationData),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
  getRecentActivity: () => api.get('/dashboard/recent-activity'),
  getAlerts: () => api.get('/dashboard/alerts'),
  getPerformanceMetrics: () => api.get('/dashboard/performance'),
};

// Tracking API
export const trackingAPI = {
  getLiveLocation: (busId) => api.get(`/tracking/live/${busId}`),
  getAllLiveLocations: () => api.get('/tracking/live'),
  updateLocation: (busId, locationData) => api.post(`/tracking/update/${busId}`, locationData),
  getRouteProgress: (tripId) => api.get(`/tracking/route-progress/${tripId}`),
  getETA: (busId, stopId) => api.get(`/tracking/eta/${busId}/${stopId}`),
};

// Notifications API
export const notificationsAPI = {
  getAll: (params = {}) => api.get('/notifications', { params }),
  markAsRead: (id) => api.patch(`/notifications/${id}/read`),
  markAllAsRead: () => api.patch('/notifications/mark-all-read'),
  send: (notificationData) => api.post('/notifications/send', notificationData),
  sendBulk: (bulkData) => api.post('/notifications/send-bulk', bulkData),
};

export default api;
