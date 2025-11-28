import { apiClient } from './client'

export interface Policy {
  id: number
  name: string
  category: string
  description: string
  status: string
  compliance_score: number
  violations: number
  last_updated: string
}

export interface PolicyStats {
  total_policies: number
  active_policies: number
  avg_compliance: number
  total_violations: number
}

export const policiesApi = {
  getPolicies: async (): Promise<Policy[]> => {
    const { data } = await apiClient.get('/api/policies/policies')
    return data
  },

  getStats: async (): Promise<PolicyStats> => {
    const { data } = await apiClient.get('/api/policies/policies/stats')
    return data
  },
}
