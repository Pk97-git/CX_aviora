import { apiClient } from './client'

export interface Ticket {
  id: string
  title: string
  description: string | null
  status: string
  priority: string | null
  customer_name: string | null
  customer_email: string | null
  assigned_to: string | null
  assigned_team: string | null
  ai_summary: string | null
  ai_intent: string | null
  ai_category: string | null
  ai_sentiment: number | null
  ai_priority: string | null
  ai_suggested_actions: Array<{
    action: string
    confidence: number
    reason: string
  }> | null
  created_at: string
  updated_at: string
}

export interface TicketDetail extends Ticket {
  ai_entities: Record<string, any> | null
  tags: string[]
  metadata: Record<string, any>
  resolved_at: string | null
  closed_at: string | null
}

export interface Comment {
  id: string
  author_name: string | null
  author_type: string
  content: string
  is_internal: boolean
  created_at: string
}

export interface TicketStats {
  by_status: Record<string, number>
  by_priority: Record<string, number>
  by_category: Record<string, number>
  total: number
}

export const ticketsApi = {
  list: async (params?: {
    status?: string
    priority?: string
    category?: string
    assigned_to?: string
    search?: string
    limit?: number
    offset?: number
  }): Promise<Ticket[]> => {
    const response = await apiClient.get('/api/tickets', { params })
    return response.data
  },

  get: async (id: string): Promise<TicketDetail> => {
    const response = await apiClient.get(`/api/tickets/${id}`)
    return response.data
  },

  update: async (
    id: string,
    data: {
      status?: string
      priority?: string
      assigned_to?: string
      assigned_team?: string
      tags?: string[]
    }
  ): Promise<TicketDetail> => {
    const response = await apiClient.put(`/api/tickets/${id}`, data)
    return response.data
  },

  getComments: async (ticketId: string): Promise<Comment[]> => {
    const response = await apiClient.get(`/api/tickets/${ticketId}/comments`)
    return response.data
  },

  addComment: async (
    ticketId: string,
    data: {
      content: string
      is_internal: boolean
    }
  ): Promise<Comment> => {
    const response = await apiClient.post(`/api/tickets/${ticketId}/comments`, data)
    return response.data
  },

  getStats: async (): Promise<TicketStats> => {
    const response = await apiClient.get('/api/tickets/stats/summary')
    return response.data
  },
}
