import { useQuery } from '@tanstack/react-query'
import { financialApi } from '@/lib/api/financial'

export const useFinancialImpact = (days: number = 30) => {
  return useQuery({
    queryKey: ['financial', 'impact', days],
    queryFn: () => financialApi.getImpact(days),
  })
}

export const useROI = (days: number = 30) => {
  return useQuery({
    queryKey: ['financial', 'roi', days],
    queryFn: () => financialApi.getROI(days),
  })
}

export const useFinancialTrends = (days: number = 30) => {
  return useQuery({
    queryKey: ['financial', 'trends', days],
    queryFn: () => financialApi.getTrends(days),
  })
}

export const useFinancialBreakdown = (days: number = 30) => {
  return useQuery({
    queryKey: ['financial', 'breakdown', days],
    queryFn: () => financialApi.getBreakdown(days),
  })
}
