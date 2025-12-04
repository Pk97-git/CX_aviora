/**
 * Authentication context and utilities for frontend
 */
import { apiClient } from './api/client'

export interface User {
  id: string
  email: string
  full_name: string
  role: string
  tenant_id: string
  tenant_name: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface LoginRequest {
  email: string
  password: string
}

export interface SignupRequest {
  email: string
  password: string
  full_name: string
  tenant_name: string
  tenant_slug: string
}

class AuthService {
  private static TOKEN_KEY = 'auth_token'
  private static REFRESH_TOKEN_KEY = 'refresh_token'
  private static USER_KEY = 'user'

  async login(credentials: LoginRequest): Promise<AuthTokens> {
    const response = await apiClient.post('/api/auth/login', credentials)
    this.setTokens(response.data)
    return response.data
  }

  async signup(data: SignupRequest): Promise<AuthTokens> {
    const response = await apiClient.post('/api/auth/signup', data)
    this.setTokens(response.data)
    return response.data
  }

  async logout(): Promise<void> {
    localStorage.removeItem(AuthService.TOKEN_KEY)
    localStorage.removeItem(AuthService.REFRESH_TOKEN_KEY)
    localStorage.removeItem(AuthService.USER_KEY)
  }

  async getCurrentUser(): Promise<User | null> {
    const userStr = localStorage.getItem(AuthService.USER_KEY)
    if (!userStr) return null
    return JSON.parse(userStr)
  }

  getAccessToken(): string | null {
    return localStorage.getItem(AuthService.TOKEN_KEY)
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(AuthService.REFRESH_TOKEN_KEY)
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken()
  }

  private setTokens(data: AuthTokens): void {
    localStorage.setItem(AuthService.TOKEN_KEY, data.access_token)
    localStorage.setItem(AuthService.REFRESH_TOKEN_KEY, data.refresh_token)
    localStorage.setItem(AuthService.USER_KEY, JSON.stringify(data.user))
  }

  async refreshAccessToken(): Promise<string> {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await apiClient.post('/api/auth/refresh', { refresh_token: refreshToken })
    this.setTokens(response.data)
    return response.data.access_token
  }
}

export const authService = new AuthService()
