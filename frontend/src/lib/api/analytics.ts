import { apiClient } from './client'

export interface DashboardKPIs {
  open_tickets: number
  sla_risk_count: number
  avg_resolution_hours: number
  automation_rate: number
  total_tickets_7d: number
  resolved_tickets_7d: number
}

export interface RCAItem {
  name: string
  count: number
  cost?: number
}

export interface SentimentTrendPoint {
  date: string
  score: number
}

export interface VolumeDataPoint {
  date: string
  actual?: number
  predicted: number
  lower_bound?: number
  upper_bound?: number
}

export const analyticsApi = {
  getSummary: async (): Promise<DashboardKPIs> => {
    const response = await apiClient.get('/api/analytics/summary')
    return response.data
  },

  getRCA: async (days: number = 30): Promise<RCAItem[]> => {
    const response = await apiClient.get('/api/analytics/rca', { params: { days } })
    return response.data
  },

  getSentiment: async (days: number = 7): Promise<SentimentTrendPoint[]> => {
    const response = await apiClient.get('/api/analytics/sentiment', { params: { days } })
    return response.data
  },

  getVolumeForecast: async (days: number = 30): Promise<VolumeDataPoint[]> => {
    const response = await apiClient.get('/api/analytics/volume-forecast', { params: { days } })
    return response.data
  },
}
