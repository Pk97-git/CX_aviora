"""
Admin API for user and tenant management
"""
import { apiClient } from './client'

export interface User {
  id: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
}

export interface Tenant {
  id: string
  name: string
  slug: string
  plan: string
  status: string
  settings: Record<string, any>
  created_at: string
}

export interface Integration {
  id: string
  type: string
  name: string
  status: string
  last_sync_at: string | null
  created_at: string
}

export const adminApi = {
  // User Management
  listUsers: async (): Promise<User[]> => {
    const response = await apiClient.get('/api/admin/users')
    return response.data
  },

  createUser: async (data: {
    email: string
    password: string
    full_name: string
    role: string
  }): Promise<User> => {
    const response = await apiClient.post('/api/admin/users', data)
    return response.data
  },

  updateUser: async (
    userId: string,
    data: {
      full_name?: string
      role?: string
      is_active?: boolean
    }
  ): Promise<User> => {
    const response = await apiClient.put(`/api/admin/users/${userId}`, data)
    return response.data
  },

  deleteUser: async (userId: string): Promise<void> => {
    await apiClient.delete(`/api/admin/users/${userId}`)
  },

  // Tenant Management
  getTenant: async (): Promise<Tenant> => {
    const response = await apiClient.get('/api/admin/tenant')
    return response.data
  },

  updateTenant: async (data: {
    name?: string
    settings?: Record<string, any>
  }): Promise<Tenant> => {
    const response = await apiClient.put('/api/admin/tenant', data)
    return response.data
  },

  // Integration Management
  listIntegrations: async (): Promise<Integration[]> => {
    const response = await apiClient.get('/api/admin/integrations')
    return response.data
  },

  createIntegration: async (data: {
    type: string
    name: string
    config: Record<string, any>
  }): Promise<Integration> => {
    const response = await apiClient.post('/api/admin/integrations', data)
    return response.data
  },

  deleteIntegration: async (integrationId: string): Promise<void> => {
    await apiClient.delete(`/api/admin/integrations/${integrationId}`)
  },
}
