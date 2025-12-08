import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { alertsApi } from '@/lib/api/alerts'

export const useActiveAlerts = () => {
  return useQuery({
    queryKey: ['alerts', 'active'],
    queryFn: () => alertsApi.getActiveAlerts(),
    refetchInterval: 30000, // Check every 30 seconds
  })
}

export const useAcknowledgeAlert = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => alertsApi.acknowledgeAlert(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts', 'active'] })
    },
  })
}

export const useAlertRules = () => {
  return useQuery({
    queryKey: ['alerts', 'rules'],
    queryFn: () => alertsApi.getRules(),
  })
}
