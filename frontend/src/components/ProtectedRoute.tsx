import { Navigate, useLocation } from 'react-router-dom'
import { authService } from '@/lib/auth'
import { useEffect, useState } from 'react'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: 'admin' | 'manager' | 'agent'
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)
  const [userRole, setUserRole] = useState<string | null>(null)
  const location = useLocation()

  useEffect(() => {
    const checkAuth = async () => {
      const authenticated = authService.isAuthenticated()
      setIsAuthenticated(authenticated)

      if (authenticated) {
        const user = await authService.getCurrentUser()
        setUserRole(user?.role || null)
      }
    }

    checkAuth()
  }, [])

  // Loading state
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  // Not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // Check role if required
  if (requiredRole && userRole) {
    const roleHierarchy: Record<string, number> = {
      agent: 1,
      manager: 2,
      admin: 3,
    }

    const userLevel = roleHierarchy[userRole] || 0
    const requiredLevel = roleHierarchy[requiredRole] || 999

    if (userLevel < requiredLevel) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-2">Access Denied</h1>
            <p className="text-muted-foreground">
              You don't have permission to access this page.
            </p>
          </div>
        </div>
      )
    }
  }

  return <>{children}</>
}
