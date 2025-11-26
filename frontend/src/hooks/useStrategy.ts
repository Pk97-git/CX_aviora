import { useQuery } from '@tanstack/react-query'
import { strategyApi } from '@/lib/api/strategy'

export const useTopicClusters = (days: number = 30) => {
  return useQuery({
    queryKey: ['strategy', 'topics', days],
    queryFn: () => strategyApi.getTopics(days),
  })
}

export const useRegionalIntelligence = (days: number = 30) => {
  return useQuery({
    queryKey: ['strategy', 'regional', days],
    queryFn: () => strategyApi.getRegional(days),
  })
}

export const useChurnPredictions = (days: number = 90) => {
  return useQuery({
    queryKey: ['strategy', 'churn', days],
    queryFn: () => strategyApi.getChurn(days),
  })
}

export const useFrictionCost = (days: number = 30) => {
  return useQuery({
    queryKey: ['strategy', 'friction', days],
    queryFn: () => strategyApi.getFrictionCost(days),
  })
}

export const useStrategicRecommendations = () => {
  return useQuery({
    queryKey: ['strategy', 'recommendations'],
    queryFn: () => strategyApi.getRecommendations(),
  })
}
