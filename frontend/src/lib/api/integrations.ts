import { apiClient } from './client'

export const integrationsApi = {
  testConnection: async (integrationId: string) => {
    const response = await apiClient.post(`/api/integrations/${integrationId}/test`)
    return response.data
  },

  createJiraIssue: async (ticketId: string) => {
    const response = await apiClient.post(`/api/tickets/${ticketId}/create-jira-issue`)
    return response.data
  },

  sendSlackNotification: async (ticketId: string) => {
    const response = await apiClient.post(`/api/tickets/${ticketId}/notify-slack`)
    return response.data
  },
}
