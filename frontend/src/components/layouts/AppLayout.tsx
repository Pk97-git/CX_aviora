import { Outlet, Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, Ticket, Workflow, Shield, BarChart3, Settings, Globe, DollarSign } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import { AlertsPanel } from '@/components/AlertsPanel'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Tickets', href: '/tickets', icon: Ticket },
  { name: 'Workflows', href: '/workflows', icon: Workflow },
  { name: 'Policies', href: '/policies', icon: Shield },
  { name: 'Insights', href: '/insights', icon: BarChart3 },
  { name: 'Financial', href: '/financial', icon: DollarSign },
  { name: 'Strategy', href: '/strategy', icon: Globe },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function AppLayout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 h-screen bg-card border-r sticky top-0 flex flex-col">
          <div className="p-6 border-b flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
                Aivora
              </h1>
              <p className="text-xs text-muted-foreground mt-1">AI-First CX Ops</p>
            </div>
          </div>
          
          <nav className="flex-1 px-4 py-4 space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              const Icon = item.icon
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          <div className="p-4 border-t">
            <div className="flex items-center gap-3 px-3 py-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white text-sm font-medium">
                U
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">User Name</p>
                <p className="text-xs text-muted-foreground truncate">user@example.com</p>
              </div>
              <AlertsPanel />
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
