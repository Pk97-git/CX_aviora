import { apiClient } from './client'

export interface TopicCluster {
  topic: string
  volume: number
  sentiment: number
  impact: string
}

export interface RegionalData {
  region: string
  volume: number
  sentiment: number
  friction_cost: number
}

export interface ChurnPrediction {
  customer: string
  customer_id: string
  ltv: number
  sentiment: number
  ticket_count: number
  churn_risk: string
}

export interface FrictionCostItem {
  category: string
  value: number
  type: string
}

export interface StrategicRecommendation {
  id: number
  type: string
  title: string
  description: string
  impact: string
  confidence: string
}

export const strategyApi = {
  getTopics: async (days: number = 30): Promise<TopicCluster[]> => {
    const response = await apiClient.get('/api/strategy/topics', { params: { days } })
    return response.data
  },

  getRegional: async (days: number = 30): Promise<RegionalData[]> => {
    const response = await apiClient.get('/api/strategy/regional', { params: { days } })
    return response.data
  },

  getChurn: async (days: number = 90): Promise<ChurnPrediction[]> => {
    const response = await apiClient.get('/api/strategy/churn', { params: { days } })
    return response.data
  },

  getFrictionCost: async (days: number = 30): Promise<FrictionCostItem[]> => {
    const response = await apiClient.get('/api/strategy/friction-cost', { params: { days } })
    return response.data
  },

  getRecommendations: async (): Promise<StrategicRecommendation[]> => {
    const response = await apiClient.get('/api/strategy/recommendations')
    return response.data
  },
}
