import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '@/lib/api/analytics'

export const useDashboardKPIs = () => {
  return useQuery({
    queryKey: ['analytics', 'summary'],
    queryFn: () => analyticsApi.getSummary(),
    refetchInterval: 1000 * 60, // Refetch every minute
  })
}

export const useRCA = (days: number = 30) => {
  return useQuery({
    queryKey: ['analytics', 'rca', days],
    queryFn: () => analyticsApi.getRCA(days),
  })
}

export const useSentimentTrend = (days: number = 7) => {
  return useQuery({
    queryKey: ['analytics', 'sentiment', days],
    queryFn: () => analyticsApi.getSentiment(days),
  })
}

export const useVolumeForecast = (days: number = 30) => {
  return useQuery({
    queryKey: ['analytics', 'forecast', days],
    queryFn: () => analyticsApi.getVolumeForecast(days),
  })
}
