import { useQuery } from '@tanstack/react-query'
import { workflowsApi } from '@/lib/api/workflows'

export const useWorkflows = () => {
  return useQuery({
    queryKey: ['workflows'],
    queryFn: () => workflowsApi.getWorkflows(),
  })
}

export const useWorkflowStats = () => {
  return useQuery({
    queryKey: ['workflows', 'stats'],
    queryFn: () => workflowsApi.getStats(),
  })
}
