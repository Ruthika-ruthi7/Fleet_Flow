import React, { useState, useEffect } from 'react';
import {
  BarChart3, Download, Filter, TrendingUp, TrendingDown,
  Users, DollarSign, Clock, AlertTriangle, Award, Target,
  Calendar, FileText, PieChart, Activity
} from 'lucide-react';

const Reports = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [reportData, setReportData] = useState({
    attendance: null,
    financial: null,
    performance: null,
    analytics: null,
    safety: null
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReportData();
  }, []);

  const fetchReportData = async () => {
    try {
      setLoading(true);
      // Simulate API calls
      const [attendanceRes, financialRes, performanceRes, analyticsRes, safetyRes] = await Promise.all([
        fetch('/api/reports/attendance'),
        fetch('/api/reports/financial'),
        fetch('/api/reports/performance'),
        fetch('/api/reports/analytics'),
        fetch('/api/reports/safety')
      ]);

      setReportData({
        attendance: await attendanceRes.json(),
        financial: await financialRes.json(),
        performance: await performanceRes.json(),
        analytics: await analyticsRes.json(),
        safety: await safetyRes.json()
      });
    } catch (error) {
      console.error('Error fetching report data:', error);
      // Set mock data for demo
      setReportData({
        attendance: {
          success: true,
          data: {
            monthly_summary: {
              total_students: 100,
              average_attendance: 92.5,
              total_school_days: 22,
              highest_attendance_day: '2024-01-15',
              lowest_attendance_day: '2024-01-08'
            }
          }
        },
        financial: {
          success: true,
          data: {
            fee_collection: {
              total_fees_due: 200000,
              total_collected: 180000,
              collection_rate: 90.0,
              pending_amount: 20000
            },
            yearly_summary: {
              total_income: 2100000,
              total_expenses: 1890000,
              net_profit: 210000
            }
          }
        },
        performance: {
          success: true,
          data: {
            driver_performance: [
              { driver_name: 'John Smith', on_time_percentage: 95.5, safety_score: 98 },
              { driver_name: 'Sarah Johnson', on_time_percentage: 92.0, safety_score: 96 }
            ]
          }
        },
        analytics: {
          success: true,
          data: {
            trends: {
              attendance_trend: { current_month: 92.5, trend: 'increasing', change_percentage: 3.7 },
              fuel_efficiency_trend: { current_month: 8.2, trend: 'improving', change_percentage: 3.8 }
            },
            insights: [
              {
                title: 'Route Optimization Opportunity',
                description: 'Route 2 shows 15% better fuel efficiency.',
                impact: 'high',
                potential_savings: 8500
              }
            ]
          }
        },
        safety: {
          success: true,
          data: {
            incident_summary: {
              total_incidents: 3,
              days_since_last_incident: 45
            }
          }
        }
      });
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'attendance', label: 'Attendance', icon: Users },
    { id: 'financial', label: 'Financial', icon: DollarSign },
    { id: 'performance', label: 'Performance', icon: TrendingUp },
    { id: 'analytics', label: 'Analytics', icon: Activity },
    { id: 'safety', label: 'Safety', icon: AlertTriangle }
  ];

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
            <p className="text-gray-600">Loading comprehensive reports...</p>
          </div>
        </div>
        <div className="card p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
          <p className="text-gray-600">Comprehensive reporting with AI-powered insights</p>
        </div>
        <div className="flex space-x-3">
          <button className="btn btn-secondary flex items-center space-x-2">
            <Filter className="h-5 w-5" />
            <span>Filter</span>
          </button>
          <button className="btn btn-primary flex items-center space-x-2">
            <Download className="h-5 w-5" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'overview' && <OverviewTab reportData={reportData} />}
        {activeTab === 'attendance' && <AttendanceTab data={reportData.attendance?.data} />}
        {activeTab === 'financial' && <FinancialTab data={reportData.financial?.data} />}
        {activeTab === 'performance' && <PerformanceTab data={reportData.performance?.data} />}
        {activeTab === 'analytics' && <AnalyticsTab data={reportData.analytics?.data} />}
        {activeTab === 'safety' && <SafetyTab data={reportData.safety?.data} />}
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab = ({ reportData }) => {
  const getMetricCard = (title, value, change, icon, color = 'blue') => (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
            <div className={`flex items-center mt-1 text-sm ${
              change > 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {change > 0 ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
              {Math.abs(change)}% from last month
            </div>
          )}
        </div>
        <div className={`p-3 rounded-full bg-${color}-100`}>
          {icon}
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {getMetricCard(
          'Average Attendance',
          '92.5%',
          3.7,
          <Users className="h-6 w-6 text-blue-600" />,
          'blue'
        )}
        {getMetricCard(
          'Monthly Revenue',
          '₹1,80,000',
          5.2,
          <DollarSign className="h-6 w-6 text-green-600" />,
          'green'
        )}
        {getMetricCard(
          'On-Time Performance',
          '94.5%',
          2.9,
          <Clock className="h-6 w-6 text-purple-600" />,
          'purple'
        )}
        {getMetricCard(
          'Safety Score',
          '96.8',
          1.2,
          <Award className="h-6 w-6 text-yellow-600" />,
          'yellow'
        )}
      </div>

      {/* Quick Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Insights</h3>
          <div className="space-y-4">
            {reportData.analytics?.data?.insights?.slice(0, 3).map((insight, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className={`p-2 rounded-full ${
                  insight.impact === 'high' ? 'bg-red-100' :
                  insight.impact === 'medium' ? 'bg-yellow-100' : 'bg-green-100'
                }`}>
                  <Target className={`h-4 w-4 ${
                    insight.impact === 'high' ? 'text-red-600' :
                    insight.impact === 'medium' ? 'text-yellow-600' : 'text-green-600'
                  }`} />
                </div>
                <div>
                  <p className="font-medium text-gray-900">{insight.title}</p>
                  <p className="text-sm text-gray-600">{insight.description}</p>
                  {insight.potential_savings && (
                    <p className="text-sm text-green-600 font-medium">
                      Potential savings: ₹{insight.potential_savings.toLocaleString()}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Trends</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Attendance Rate</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">92.5%</span>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Fuel Efficiency</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">8.2 km/l</span>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">On-Time Performance</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">94.5%</span>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Safety Incidents</span>
              <div className="flex items-center space-x-2">
                <span className="font-medium">3 this month</span>
                <TrendingDown className="h-4 w-4 text-red-600" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Attendance Tab Component
const AttendanceTab = ({ data }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Monthly Summary</h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Total Students</span>
            <span className="font-medium">{data?.monthly_summary?.total_students || 100}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Average Attendance</span>
            <span className="font-medium">{data?.monthly_summary?.average_attendance || 92.5}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">School Days</span>
            <span className="font-medium">{data?.monthly_summary?.total_school_days || 22}</span>
          </div>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Class-wise Performance</h3>
        <div className="space-y-2">
          {data?.class_wise?.map((cls, index) => (
            <div key={index} className="flex justify-between">
              <span className="text-gray-600">{cls.class}</span>
              <span className="font-medium">{cls.average_attendance}%</span>
            </div>
          )) || (
            <>
              <div className="flex justify-between">
                <span className="text-gray-600">10th Grade A</span>
                <span className="font-medium">95.0%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">10th Grade B</span>
                <span className="font-medium">88.0%</span>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Route-wise Performance</h3>
        <div className="space-y-2">
          {data?.route_wise?.map((route, index) => (
            <div key={index} className="flex justify-between">
              <span className="text-gray-600">{route.route}</span>
              <span className="font-medium">{route.average_attendance}%</span>
            </div>
          )) || (
            <>
              <div className="flex justify-between">
                <span className="text-gray-600">City Center</span>
                <span className="font-medium">93.0%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Suburb Route</span>
                <span className="font-medium">91.0%</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>

    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Attendance Trends</h3>
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <PieChart className="h-12 w-12 text-gray-400 mx-auto mb-2" />
          <p className="text-gray-600">Attendance chart visualization would go here</p>
        </div>
      </div>
    </div>
  </div>
);

// Financial Tab Component
const FinancialTab = ({ data }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Total Revenue</h3>
        <p className="text-2xl font-bold text-gray-900">₹{data?.yearly_summary?.total_income?.toLocaleString() || '21,00,000'}</p>
        <p className="text-sm text-green-600">+12% from last year</p>
      </div>
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Total Expenses</h3>
        <p className="text-2xl font-bold text-gray-900">₹{data?.yearly_summary?.total_expenses?.toLocaleString() || '18,90,000'}</p>
        <p className="text-sm text-red-600">+8% from last year</p>
      </div>
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Net Profit</h3>
        <p className="text-2xl font-bold text-gray-900">₹{data?.yearly_summary?.net_profit?.toLocaleString() || '2,10,000'}</p>
        <p className="text-sm text-green-600">+25% from last year</p>
      </div>
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Collection Rate</h3>
        <p className="text-2xl font-bold text-gray-900">{data?.fee_collection?.collection_rate || 90}%</p>
        <p className="text-sm text-green-600">+3% from last month</p>
      </div>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Fee Collection Status</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Total Due</span>
            <span className="font-medium">₹{data?.fee_collection?.total_fees_due?.toLocaleString() || '2,00,000'}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Collected</span>
            <span className="font-medium text-green-600">₹{data?.fee_collection?.total_collected?.toLocaleString() || '1,80,000'}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Pending</span>
            <span className="font-medium text-red-600">₹{data?.fee_collection?.pending_amount?.toLocaleString() || '20,000'}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Overdue</span>
            <span className="font-medium text-red-600">₹{data?.fee_collection?.overdue_amount?.toLocaleString() || '15,000'}</span>
          </div>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Expense Breakdown</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Fuel Cost</span>
            <span className="font-medium">₹{data?.expenses?.fuel_cost?.toLocaleString() || '50,000'}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Driver Salary</span>
            <span className="font-medium">₹{data?.expenses?.driver_salary?.toLocaleString() || '80,000'}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Maintenance</span>
            <span className="font-medium">₹{data?.expenses?.maintenance_cost?.toLocaleString() || '30,000'}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Insurance</span>
            <span className="font-medium">₹{data?.expenses?.insurance?.toLocaleString() || '25,000'}</span>
          </div>
        </div>
      </div>
    </div>

    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Profit/Loss Trend</h3>
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
          <p className="text-gray-600">Financial trend chart would go here</p>
        </div>
      </div>
    </div>
  </div>
);

// Performance Tab Component
const PerformanceTab = ({ data }) => (
  <div className="space-y-6">
    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Driver Performance</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Driver</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">On-Time %</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Safety Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fuel Efficiency</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Trips</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.driver_performance?.map((driver, index) => (
              <tr key={index}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {driver.driver_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    driver.on_time_percentage >= 95 ? 'bg-green-100 text-green-800' :
                    driver.on_time_percentage >= 90 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {driver.on_time_percentage}%
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    driver.safety_score >= 95 ? 'bg-green-100 text-green-800' :
                    driver.safety_score >= 90 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {driver.safety_score}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {driver.fuel_efficiency || 8.2} km/l
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {driver.total_trips || 220}
                </td>
              </tr>
            )) || (
              <>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">John Smith</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">95.5%</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">98</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">8.5 km/l</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">220</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Sarah Johnson</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">92.0%</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">96</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">7.8 km/l</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">200</td>
                </tr>
              </>
            )}
          </tbody>
        </table>
      </div>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Route Efficiency</h3>
        <div className="space-y-4">
          <div className="border-l-4 border-green-400 pl-4">
            <h4 className="font-medium text-gray-900">City Center to School</h4>
            <p className="text-sm text-gray-600">Efficiency Score: 90%</p>
            <p className="text-sm text-gray-600">Avg Trip Time: 45 min</p>
          </div>
          <div className="border-l-4 border-blue-400 pl-4">
            <h4 className="font-medium text-gray-900">Suburb to College</h4>
            <p className="text-sm text-gray-600">Efficiency Score: 95%</p>
            <p className="text-sm text-gray-600">Avg Trip Time: 38 min</p>
          </div>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Bus Utilization</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">BUS001</span>
            <div className="text-right">
              <p className="font-medium">75% occupancy</p>
              <p className="text-sm text-gray-600">15,500 km</p>
            </div>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">BUS002</span>
            <div className="text-right">
              <p className="font-medium">68% occupancy</p>
              <p className="text-sm text-gray-600">14,200 km</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

// Analytics Tab Component
const AnalyticsTab = ({ data }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Trend Analysis</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Attendance</span>
            <div className="flex items-center space-x-2">
              <span className="font-medium">{data?.trends?.attendance_trend?.current_month || 92.5}%</span>
              <TrendingUp className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600">+{data?.trends?.attendance_trend?.change_percentage || 3.7}%</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Fuel Efficiency</span>
            <div className="flex items-center space-x-2">
              <span className="font-medium">{data?.trends?.fuel_efficiency_trend?.current_month || 8.2} km/l</span>
              <TrendingUp className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600">+{data?.trends?.fuel_efficiency_trend?.change_percentage || 3.8}%</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-600">On-Time Performance</span>
            <div className="flex items-center space-x-2">
              <span className="font-medium">{data?.trends?.on_time_performance?.current_month || 94.5}%</span>
              <TrendingUp className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600">+{data?.trends?.on_time_performance?.change_percentage || 2.9}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Predictions</h3>
        <div className="space-y-3">
          <div>
            <p className="text-sm text-gray-600">Next Month Attendance</p>
            <p className="text-xl font-bold text-blue-600">{data?.predictions?.next_month_attendance || 94.2}%</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Fuel Cost Forecast</p>
            <p className="text-xl font-bold text-orange-600">₹{data?.predictions?.fuel_cost_forecast?.next_month?.toLocaleString() || '52,000'}</p>
            <p className="text-xs text-gray-500">Confidence: {data?.predictions?.fuel_cost_forecast?.confidence || 78}%</p>
          </div>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Benchmarks</h3>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Our Attendance</span>
            <span className="font-medium text-green-600">{data?.benchmarks?.our_attendance || 92.5}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Industry Avg</span>
            <span className="font-medium text-gray-500">{data?.benchmarks?.industry_average_attendance || 88.5}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Our Fuel Efficiency</span>
            <span className="font-medium text-green-600">{data?.benchmarks?.our_fuel_efficiency || 8.2} km/l</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Industry Avg</span>
            <span className="font-medium text-gray-500">{data?.benchmarks?.industry_fuel_efficiency || 7.2} km/l</span>
          </div>
        </div>
      </div>
    </div>

    <div className="card p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">AI-Powered Insights</h3>
      <div className="space-y-4">
        {data?.insights?.map((insight, index) => (
          <div key={index} className="border-l-4 border-blue-400 pl-4 py-2">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="font-medium text-gray-900">{insight.title}</h4>
                <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                {insight.potential_savings && (
                  <p className="text-sm text-green-600 font-medium mt-1">
                    Potential savings: ₹{insight.potential_savings.toLocaleString()}
                  </p>
                )}
                {insight.potential_improvement && (
                  <p className="text-sm text-blue-600 font-medium mt-1">
                    Potential improvement: {insight.potential_improvement}
                  </p>
                )}
              </div>
              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                insight.impact === 'high' ? 'bg-red-100 text-red-800' :
                insight.impact === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {insight.impact} impact
              </span>
            </div>
          </div>
        )) || (
          <>
            <div className="border-l-4 border-blue-400 pl-4 py-2">
              <h4 className="font-medium text-gray-900">Route Optimization Opportunity</h4>
              <p className="text-sm text-gray-600 mt-1">Route 2 shows 15% better fuel efficiency. Consider applying similar optimization to Route 1.</p>
              <p className="text-sm text-green-600 font-medium mt-1">Potential savings: ₹8,500</p>
            </div>
            <div className="border-l-4 border-green-400 pl-4 py-2">
              <h4 className="font-medium text-gray-900">Preventive Maintenance Success</h4>
              <p className="text-sm text-gray-600 mt-1">Buses with regular maintenance show 25% less downtime.</p>
              <p className="text-sm text-green-600 font-medium mt-1">Potential savings: ₹12,000</p>
            </div>
          </>
        )}
      </div>
    </div>
  </div>
);

// Safety Tab Component
const SafetyTab = ({ data }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Total Incidents</h3>
        <p className="text-2xl font-bold text-gray-900">{data?.incident_summary?.total_incidents || 3}</p>
        <p className="text-sm text-green-600">-2 from last month</p>
      </div>
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Safety Score</h3>
        <p className="text-2xl font-bold text-gray-900">{data?.safety_metrics?.average_safety_score || 96.8}</p>
        <p className="text-sm text-green-600">+1.2 from last month</p>
      </div>
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Days Since Incident</h3>
        <p className="text-2xl font-bold text-gray-900">{data?.incident_summary?.days_since_last_incident || 45}</p>
        <p className="text-sm text-green-600">Improving</p>
      </div>
      <div className="card p-6">
        <h3 className="text-sm font-medium text-gray-600">Training Completion</h3>
        <p className="text-2xl font-bold text-gray-900">{data?.safety_metrics?.driver_safety_training_completion || 100}%</p>
        <p className="text-sm text-green-600">All drivers trained</p>
      </div>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Incidents</h3>
        <div className="space-y-4">
          {data?.incident_details?.map((incident, index) => (
            <div key={index} className="border-l-4 border-red-400 pl-4 py-2">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-medium text-gray-900">{incident.type}</h4>
                  <p className="text-sm text-gray-600">{incident.description}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {incident.date} • {incident.bus_number} • {incident.driver}
                  </p>
                </div>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                  incident.status === 'resolved' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {incident.status}
                </span>
              </div>
            </div>
          )) || (
            <>
              <div className="border-l-4 border-red-400 pl-4 py-2">
                <h4 className="font-medium text-gray-900">Minor Accident</h4>
                <p className="text-sm text-gray-600">Minor fender bender in parking lot</p>
                <p className="text-xs text-gray-500 mt-1">2024-01-10 • BUS002 • Sarah Johnson</p>
              </div>
              <div className="border-l-4 border-orange-400 pl-4 py-2">
                <h4 className="font-medium text-gray-900">Breakdown</h4>
                <p className="text-sm text-gray-600">Engine overheating</p>
                <p className="text-xs text-gray-500 mt-1">2023-12-15 • BUS003 • Mike Wilson</p>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Safety Recommendations</h3>
        <div className="space-y-3">
          {data?.safety_recommendations?.map((recommendation, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="p-1 rounded-full bg-blue-100">
                <AlertTriangle className="h-3 w-3 text-blue-600" />
              </div>
              <p className="text-sm text-gray-700">{recommendation}</p>
            </div>
          )) || (
            <>
              <div className="flex items-start space-x-3">
                <div className="p-1 rounded-full bg-blue-100">
                  <AlertTriangle className="h-3 w-3 text-blue-600" />
                </div>
                <p className="text-sm text-gray-700">Increase frequency of vehicle inspections</p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="p-1 rounded-full bg-blue-100">
                  <AlertTriangle className="h-3 w-3 text-blue-600" />
                </div>
                <p className="text-sm text-gray-700">Implement advanced driver assistance systems</p>
              </div>
              <div className="flex items-start space-x-3">
                <div className="p-1 rounded-full bg-blue-100">
                  <AlertTriangle className="h-3 w-3 text-blue-600" />
                </div>
                <p className="text-sm text-gray-700">Conduct monthly safety training sessions</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  </div>
);

export default Reports;
