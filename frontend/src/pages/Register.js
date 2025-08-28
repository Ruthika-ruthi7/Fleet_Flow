import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Bus, Eye, EyeOff } from 'lucide-react';
import toast from 'react-hot-toast';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'student',
    first_name: '',
    last_name: '',
    phone: '',
    address: '',
    // Role-specific fields
    license_number: '',
    class_name: '',
    parent_name: '',
    parent_phone: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

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

    // Validation
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match');
      setIsLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters long');
      setIsLoading(false);
      return;
    }

    try {
      const result = await register(formData);
      if (result.success) {
        toast.success('Registration successful! Please login with your credentials.');
        navigate('/login');
      }
    } catch (error) {
      // Error is handled by the auth context
    } finally {
      setIsLoading(false);
    }
  };

  const roleFields = {
    driver: ['license_number'],
    conductor: ['license_number'],
    student: ['class_name', 'parent_name', 'parent_phone'],
  };

  const currentRoleFields = roleFields[formData.role] || [];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="flex justify-center">
            <div className="flex items-center">
              <Bus className="h-12 w-12 text-primary-600" />
              <h1 className="ml-2 text-3xl font-bold text-gray-900">BusMS</h1>
            </div>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Join the Bus Management System
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/* Basic Information */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="first_name" className="form-label">
                  First Name
                </label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  className="input"
                  value={formData.first_name}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label htmlFor="last_name" className="form-label">
                  Last Name
                </label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  className="input"
                  value={formData.last_name}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <label htmlFor="username" className="form-label">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="input"
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="email" className="form-label">
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="input"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="role" className="form-label">
                Role
              </label>
              <select
                id="role"
                name="role"
                required
                className="input"
                value={formData.role}
                onChange={handleChange}
              >
                <option value="student">Student</option>
                <option value="driver">Driver</option>
                <option value="conductor">Conductor</option>
                <option value="parent">Parent</option>
              </select>
            </div>

            <div>
              <label htmlFor="phone" className="form-label">
                Phone Number
              </label>
              <input
                id="phone"
                name="phone"
                type="tel"
                className="input"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>

            {/* Role-specific fields */}
            {currentRoleFields.includes('license_number') && (
              <div>
                <label htmlFor="license_number" className="form-label">
                  License Number
                </label>
                <input
                  id="license_number"
                  name="license_number"
                  type="text"
                  required
                  className="input"
                  value={formData.license_number}
                  onChange={handleChange}
                />
              </div>
            )}

            {currentRoleFields.includes('class_name') && (
              <div>
                <label htmlFor="class_name" className="form-label">
                  Class/Grade
                </label>
                <input
                  id="class_name"
                  name="class_name"
                  type="text"
                  className="input"
                  value={formData.class_name}
                  onChange={handleChange}
                />
              </div>
            )}

            {currentRoleFields.includes('parent_name') && (
              <>
                <div>
                  <label htmlFor="parent_name" className="form-label">
                    Parent/Guardian Name
                  </label>
                  <input
                    id="parent_name"
                    name="parent_name"
                    type="text"
                    className="input"
                    value={formData.parent_name}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label htmlFor="parent_phone" className="form-label">
                    Parent/Guardian Phone
                  </label>
                  <input
                    id="parent_phone"
                    name="parent_phone"
                    type="tel"
                    className="input"
                    value={formData.parent_phone}
                    onChange={handleChange}
                  />
                </div>
              </>
            )}

            <div>
              <label htmlFor="address" className="form-label">
                Address
              </label>
              <textarea
                id="address"
                name="address"
                rows={3}
                className="input"
                value={formData.address}
                onChange={handleChange}
              />
            </div>

            {/* Password fields */}
            <div className="relative">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                required
                className="input pr-10"
                value={formData.password}
                onChange={handleChange}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center mt-6"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-400" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-400" />
                )}
              </button>
            </div>

            <div className="relative">
              <label htmlFor="confirmPassword" className="form-label">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type={showConfirmPassword ? 'text' : 'password'}
                required
                className="input pr-10"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center mt-6"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-5 w-5 text-gray-400" />
                ) : (
                  <Eye className="h-5 w-5 text-gray-400" />
                )}
              </button>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="loading-spinner h-4 w-4 mr-2"></div>
                  Creating account...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              Already have an account? Sign in
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
