import { useState, useRef, useEffect } from 'react'
import { 
  Bell, 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  XCircle 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useActiveAlerts, useAcknowledgeAlert } from "@/hooks/useAlerts"
import { cn } from "@/lib/utils/cn"

export function AlertsPanel() {
  const [isOpen, setIsOpen] = useState(false)
  const panelRef = useRef<HTMLDivElement>(null)
  
  const { data: alerts, isLoading } = useActiveAlerts()
  const acknowledgeMutation = useAcknowledgeAlert()

  const activeCount = alerts?.length || 0

  // Close when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (panelRef.current && !panelRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <XCircle className="h-4 w-4 text-red-500" />
      case 'high': return <AlertTriangle className="h-4 w-4 text-orange-500" />
      case 'medium': return <Info className="h-4 w-4 text-blue-500" />
      default: return <Info className="h-4 w-4 text-gray-500" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
      case 'high': return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200"
      case 'medium': return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
      default: return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
    }
  }

  return (
    <div className="relative" ref={panelRef}>
      <Button 
        variant="ghost" 
        size="icon" 
        className="relative"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Bell className="h-5 w-5" />
        {activeCount > 0 && (
          <span className="absolute top-1 right-1 h-2.5 w-2.5 rounded-full bg-red-600 animate-pulse ring-2 ring-background" />
        )}
      </Button>

      {isOpen && (
        <div className="absolute right-0 bottom-full mb-2 w-80 md:w-96 rounded-lg border bg-card shadow-lg z-50 overflow-hidden">
          <div className="p-4 border-b bg-muted/50">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold flex items-center gap-2">
                System Alerts
                {activeCount > 0 && (
                  <Badge variant="destructive" className="rounded-full px-2 py-0.5 text-xs">
                    {activeCount}
                  </Badge>
                )}
              </h3>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Real-time notifications about system health.
            </p>
          </div>

          <div className="max-h-[400px] overflow-y-auto p-2">
            {isLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading alerts...</div>
            ) : activeCount === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-center text-muted-foreground">
                <CheckCircle className="h-10 w-10 text-green-500 mb-3" />
                <p className="font-medium text-foreground text-sm">All Systems Normal</p>
                <p className="text-xs">No active alerts at this time.</p>
              </div>
            ) : (
              <div className="space-y-2">
                {alerts?.map((alert) => (
                  <div 
                    key={alert.id} 
                    className="p-3 rounded-md border bg-background hover:bg-accent/50 transition-colors space-y-2"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2">
                        {getSeverityIcon(alert.severity)}
                        <span className="font-medium text-sm">{alert.rule_name}</span>
                      </div>
                      <Badge className={cn("text-[10px] px-1.5 py-0 capitalize", getSeverityColor(alert.severity))}>
                        {alert.severity}
                      </Badge>
                    </div>
                    
                    <p className="text-xs text-muted-foreground pl-6">
                      {alert.message}
                    </p>
                    
                    <div className="flex items-center justify-between pt-1 pl-6">
                      <span className="text-[10px] text-muted-foreground">
                        {new Date(alert.created_at).toLocaleTimeString()}
                      </span>
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="h-6 text-[10px] px-2"
                        onClick={() => acknowledgeMutation.mutate(alert.id)}
                        disabled={acknowledgeMutation.isPending}
                      >
                        Acknowledge
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
