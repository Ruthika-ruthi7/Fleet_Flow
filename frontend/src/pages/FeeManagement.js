import React, { useState } from 'react';
import { DollarSign, Plus, CreditCard, Calculator, Award, TrendingUp, Users, AlertCircle } from 'lucide-react';

const FeeManagement = () => {
  const [showCalculator, setShowCalculator] = useState(false);
  const [calculatorData, setCalculatorData] = useState({
    family_income: '',
    academic_score: '',
    attendance_percentage: '',
    has_sibling: false,
    is_single_parent: false,
    has_sports_achievement: false,
    base_fee: 2000
  });
  const [calculationResult, setCalculationResult] = useState(null);

  // Mock fee data
  const feeStats = {
    total_students: 5,
    scholarship_recipients: 4,
    scholarship_percentage: 80,
    total_base_revenue: 10500,
    total_actual_revenue: 7920,
    total_scholarship_amount: 2580,
    average_scholarship_percentage: 32.5,
    scholarship_breakdown: {
      Merit: { count: 1, total_savings: 500, average_percentage: 25 },
      'Need-based': { count: 1, total_savings: 880, average_percentage: 40 },
      Sports: { count: 1, total_savings: 900, average_percentage: 50 },
      Sibling: { count: 1, total_savings: 300, average_percentage: 15 }
    }
  };

  const scholarshipTypes = [
    {
      type: 'Merit',
      description: 'Academic excellence scholarship',
      criteria: 'Academic score >= 90%',
      percentage_range: [20, 30],
      max_income: 60000
    },
    {
      type: 'Need-based',
      description: 'Financial assistance for low-income families',
      criteria: 'Family income < 30,000',
      percentage_range: [30, 50],
      max_income: 30000
    },
    {
      type: 'Sports',
      description: 'Athletic achievement scholarship',
      criteria: 'Sports excellence + attendance >= 95%',
      percentage_range: [25, 50],
      max_income: 50000
    },
    {
      type: 'Sibling',
      description: 'Multiple children from same family',
      criteria: 'Second child onwards',
      percentage_range: [10, 20],
      max_income: 70000
    },
    {
      type: 'Single Parent',
      description: 'Support for single-parent families',
      criteria: 'Single parent household',
      percentage_range: [20, 35],
      max_income: 40000
    }
  ];

  const handleCalculatorChange = (e) => {
    const { name, value, type, checked } = e.target;
    setCalculatorData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const calculateScholarship = () => {
    const { family_income, academic_score, attendance_percentage, has_sibling, is_single_parent, has_sports_achievement, base_fee } = calculatorData;

    const eligible_scholarships = [];

    // Merit scholarship
    if (academic_score >= 90 && family_income <= 60000) {
      const percentage = Math.min(30, 20 + (academic_score - 90) * 2);
      eligible_scholarships.push({
        type: 'Merit',
        percentage: percentage,
        amount: base_fee * percentage / 100,
        reason: `Academic score: ${academic_score}%`
      });
    }

    // Need-based scholarship
    if (family_income <= 30000) {
      const percentage = Math.max(30, Math.min(50, 60 - (family_income / 1000)));
      eligible_scholarships.push({
        type: 'Need-based',
        percentage: percentage,
        amount: base_fee * percentage / 100,
        reason: `Family income: ₹${parseInt(family_income).toLocaleString()}`
      });
    }

    // Sports scholarship
    if (has_sports_achievement && attendance_percentage >= 95 && family_income <= 50000) {
      const percentage = attendance_percentage >= 98 ? 40 : 30;
      eligible_scholarships.push({
        type: 'Sports',
        percentage: percentage,
        amount: base_fee * percentage / 100,
        reason: `Sports achievement + ${attendance_percentage}% attendance`
      });
    }

    // Sibling scholarship
    if (has_sibling && family_income <= 70000) {
      eligible_scholarships.push({
        type: 'Sibling',
        percentage: 15,
        amount: base_fee * 15 / 100,
        reason: 'Multiple children discount'
      });
    }

    // Single Parent scholarship
    if (is_single_parent && family_income <= 40000) {
      const percentage = Math.min(35, 20 + (40000 - family_income) / 1000);
      eligible_scholarships.push({
        type: 'Single Parent',
        percentage: percentage,
        amount: base_fee * percentage / 100,
        reason: 'Single parent household support'
      });
    }

    const best_scholarship = eligible_scholarships.length > 0
      ? eligible_scholarships.reduce((max, current) => current.amount > max.amount ? current : max)
      : null;

    const final_fee = best_scholarship ? base_fee - best_scholarship.amount : base_fee;

    setCalculationResult({
      base_fee: parseInt(base_fee),
      eligible_scholarships,
      recommended_scholarship: best_scholarship,
      final_fee,
      total_savings: best_scholarship ? best_scholarship.amount : 0
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Fee Management</h1>
          <p className="text-gray-600">Comprehensive fee management with scholarship support</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowCalculator(!showCalculator)}
            className="btn btn-outline flex items-center space-x-2"
          >
            <Calculator className="h-5 w-5" />
            <span>Scholarship Calculator</span>
          </button>
          <button className="btn btn-primary flex items-center space-x-2">
            <Plus className="h-5 w-5" />
            <span>Generate Fees</span>
          </button>
        </div>
      </div>

      {/* Fee Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-100">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
              <p className="text-2xl font-bold text-gray-900">₹{feeStats.total_actual_revenue.toLocaleString()}</p>
              <p className="text-xs text-gray-500">After scholarships</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-100">
              <Award className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Scholarship Savings</p>
              <p className="text-2xl font-bold text-gray-900">₹{feeStats.total_scholarship_amount.toLocaleString()}</p>
              <p className="text-xs text-gray-500">Monthly assistance</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-purple-100">
              <Users className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Recipients</p>
              <p className="text-2xl font-bold text-gray-900">{feeStats.scholarship_recipients}</p>
              <p className="text-xs text-gray-500">{feeStats.scholarship_percentage}% of students</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-orange-100">
              <TrendingUp className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg. Scholarship</p>
              <p className="text-2xl font-bold text-gray-900">{feeStats.average_scholarship_percentage}%</p>
              <p className="text-xs text-gray-500">Per recipient</p>
            </div>
          </div>
        </div>
      </div>

      {/* Scholarship Calculator */}
      {showCalculator && (
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Scholarship Calculator</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="form-label">Family Annual Income (₹)</label>
                <input
                  type="number"
                  name="family_income"
                  value={calculatorData.family_income}
                  onChange={handleCalculatorChange}
                  className="input"
                  placeholder="e.g., 45000"
                />
              </div>

              <div>
                <label className="form-label">Academic Score (%)</label>
                <input
                  type="number"
                  name="academic_score"
                  value={calculatorData.academic_score}
                  onChange={handleCalculatorChange}
                  className="input"
                  placeholder="e.g., 92"
                  min="0"
                  max="100"
                />
              </div>

              <div>
                <label className="form-label">Attendance Percentage (%)</label>
                <input
                  type="number"
                  name="attendance_percentage"
                  value={calculatorData.attendance_percentage}
                  onChange={handleCalculatorChange}
                  className="input"
                  placeholder="e.g., 95"
                  min="0"
                  max="100"
                />
              </div>

              <div>
                <label className="form-label">Base Monthly Fee (₹)</label>
                <input
                  type="number"
                  name="base_fee"
                  value={calculatorData.base_fee}
                  onChange={handleCalculatorChange}
                  className="input"
                />
              </div>
            </div>

            <div className="space-y-4">
              <div className="space-y-3">
                <label className="form-label">Additional Criteria</label>

                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="has_sibling"
                    checked={calculatorData.has_sibling}
                    onChange={handleCalculatorChange}
                    className="rounded border-gray-300"
                  />
                  <span className="text-sm">Has sibling in school</span>
                </label>

                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="is_single_parent"
                    checked={calculatorData.is_single_parent}
                    onChange={handleCalculatorChange}
                    className="rounded border-gray-300"
                  />
                  <span className="text-sm">Single parent household</span>
                </label>

                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    name="has_sports_achievement"
                    checked={calculatorData.has_sports_achievement}
                    onChange={handleCalculatorChange}
                    className="rounded border-gray-300"
                  />
                  <span className="text-sm">Sports achievement</span>
                </label>
              </div>

              <button
                onClick={calculateScholarship}
                className="btn btn-primary w-full flex items-center justify-center space-x-2"
              >
                <Calculator className="h-5 w-5" />
                <span>Calculate Scholarship</span>
              </button>
            </div>
          </div>

          {/* Calculation Result */}
          {calculationResult && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <h4 className="text-lg font-medium text-blue-900 mb-3">Scholarship Calculation Result</h4>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">₹{calculationResult.base_fee}</div>
                  <div className="text-sm text-gray-600">Base Fee</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">₹{Math.round(calculationResult.total_savings)}</div>
                  <div className="text-sm text-gray-600">Scholarship Savings</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">₹{Math.round(calculationResult.final_fee)}</div>
                  <div className="text-sm text-gray-600">Final Fee</div>
                </div>
              </div>

              {calculationResult.recommended_scholarship ? (
                <div className="bg-white rounded-lg p-4">
                  <h5 className="font-medium text-gray-900 mb-2">Recommended Scholarship</h5>
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="badge badge-success">{calculationResult.recommended_scholarship.type}</span>
                      <p className="text-sm text-gray-600 mt-1">{calculationResult.recommended_scholarship.reason}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-green-600">
                        {Math.round(calculationResult.recommended_scholarship.percentage)}% OFF
                      </div>
                      <div className="text-sm text-gray-600">
                        ₹{Math.round(calculationResult.recommended_scholarship.amount)} savings
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                  <div className="flex items-center space-x-2">
                    <AlertCircle className="h-5 w-5 text-yellow-600" />
                    <span className="text-yellow-800">No scholarships available based on current criteria</span>
                  </div>
                </div>
              )}

              {calculationResult.eligible_scholarships.length > 1 && (
                <div className="mt-4">
                  <h5 className="font-medium text-gray-900 mb-2">All Eligible Scholarships</h5>
                  <div className="space-y-2">
                    {calculationResult.eligible_scholarships.map((scholarship, index) => (
                      <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span className="text-sm">{scholarship.type} - {scholarship.reason}</span>
                        <span className="text-sm font-medium">{Math.round(scholarship.percentage)}% (₹{Math.round(scholarship.amount)})</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Scholarship Types */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Available Scholarship Types</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {scholarshipTypes.map((scholarship, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-gray-900">{scholarship.type}</h4>
                <span className="text-sm text-green-600 font-medium">
                  {scholarship.percentage_range[0]}-{scholarship.percentage_range[1]}%
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{scholarship.description}</p>
              <p className="text-xs text-gray-500 mb-2">{scholarship.criteria}</p>
              <p className="text-xs text-gray-500">Max income: ₹{scholarship.max_income.toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Scholarship Breakdown */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Current Scholarship Distribution</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {Object.entries(feeStats.scholarship_breakdown).map(([type, data]) => (
            <div key={type} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-lg font-bold text-gray-900">{data.count}</div>
              <div className="text-sm text-gray-600">{type}</div>
              <div className="text-xs text-green-600 font-medium">₹{data.total_savings.toLocaleString()} saved</div>
              <div className="text-xs text-gray-500">{Math.round(data.average_percentage)}% avg</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FeeManagement;
