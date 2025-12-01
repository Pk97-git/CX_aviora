import { apiClient } from './client'

export interface Workflow {
  id: number
  name: string
  trigger: string
  actions: string[]
  status: string
  success_rate: number
  time_saved_hours: number
  executions: number
}

export interface WorkflowStats {
  total_workflows: number
  active_workflows: number
  total_executions: number
  time_saved_hours: number
  avg_success_rate: number
}

export const workflowsApi = {
  getWorkflows: async (): Promise<Workflow[]> => {
    const { data } = await apiClient.get('/api/workflows')
    return data
  },

  getStats: async (): Promise<WorkflowStats> => {
    const { data } = await apiClient.get('/api/workflows/stats')
    return data
  },
}
