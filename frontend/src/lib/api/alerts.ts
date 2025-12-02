import { apiClient } from './client'

export interface Alert {
  id: string
  rule_id: string
  rule_name: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  message: string
  value: number
  threshold: number
  status: 'active' | 'acknowledged' | 'resolved'
  created_at: string
}

export interface AlertRule {
  id: string
  name: string
  metric_type: string
  threshold_value: number
  severity: string
  enabled: boolean
}

export const alertsApi = {
  getActiveAlerts: async (): Promise<Alert[]> => {
    const response = await apiClient.get('/api/alerts/active')
    return response.data
  },

  acknowledgeAlert: async (id: string): Promise<void> => {
    await apiClient.put(`/api/alerts/${id}/acknowledge`)
  },

  getRules: async (): Promise<AlertRule[]> => {
    const response = await apiClient.get('/api/alerts/rules')
    return response.data
  },

  createRule: async (rule: Omit<AlertRule, 'id'>): Promise<AlertRule> => {
    const response = await apiClient.post('/api/alerts/rules', rule)
    return response.data
  },
  
  deleteRule: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/alerts/rules/${id}`)
  }
}
