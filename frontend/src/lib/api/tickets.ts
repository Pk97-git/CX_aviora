import { apiClient } from './client'

export interface TicketFilters {
  status?: string
  priority?: string
  start_date?: string
  end_date?: string
  page?: number
  page_size?: number
}

export interface Ticket {
  id: string
  subject: string
  description: string
  status: string
  priority: string
  source: string
  customer_id?: string
  customer_email?: string
  assignee?: string
  created_at: string
  updated_at: string
  resolved_at?: string
  sla_breach_at?: string
  ai_analysis?: {
    sentiment: number
    intent: string
    priority_score: number
    summary: string
    suggested_actions: string[]
  }
}

export interface TicketListResponse {
  tickets: Ticket[]
  total: number
  page: number
  page_size: number
  has_more: boolean
}

export const ticketsApi = {
  list: async (filters?: TicketFilters): Promise<TicketListResponse> => {
    const response = await apiClient.get('/api/tickets', { params: filters })
    return response.data
  },

  getById: async (id: string): Promise<Ticket> => {
    const response = await apiClient.get(`/api/tickets/${id}`)
    return response.data
  },

  update: async (id: string, data: { status?: string; assignee?: string }): Promise<Ticket> => {
    const response = await apiClient.patch(`/api/tickets/${id}`, data)
    return response.data
  },
}
