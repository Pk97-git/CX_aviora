import { useQuery } from '@tanstack/react-query'
import { policiesApi } from '@/lib/api/policies'

export const usePolicies = () => {
  return useQuery({
    queryKey: ['policies'],
    queryFn: () => policiesApi.getPolicies(),
  })
}

export const usePolicyStats = () => {
  return useQuery({
    queryKey: ['policies', 'stats'],
    queryFn: () => policiesApi.getStats(),
  })
}
