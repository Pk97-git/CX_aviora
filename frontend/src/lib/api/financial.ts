import { apiClient } from './client'

export interface FinancialMetric {
  revenue_protected: number
  automation_cost_saved: number
  resolution_time_saved_hours: number
  friction_cost_reduced: number
  sla_compliance_bonus: number
  total_value_generated: number
  churn_prevented_count: number
}

export interface ROICalculation {
  total_investment: number
  total_return: number
  net_profit: number
  roi_percentage: number
  payback_period_months: number
}

export interface FinancialTrendPoint {
  date: string
  revenue_protected: number
  cost_saved: number
  total_value: number
}

export interface FinancialBreakdownItem {
  category: string
  value: number
  percentage: number
}

export const financialApi = {
  getImpact: async (days: number = 30): Promise<FinancialMetric> => {
    const response = await apiClient.get('/api/financial/impact', { params: { days } })
    return response.data
  },

  getROI: async (days: number = 30): Promise<ROICalculation> => {
    const response = await apiClient.get('/api/financial/roi', { params: { days } })
    return response.data
  },

  getTrends: async (days: number = 30): Promise<FinancialTrendPoint[]> => {
    const response = await apiClient.get('/api/financial/trends', { params: { days } })
    return response.data
  },

  getBreakdown: async (days: number = 30): Promise<FinancialBreakdownItem[]> => {
    const response = await apiClient.get('/api/financial/breakdown', { params: { days } })
    return response.data
  },
}
