import { 
  Bell, 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  XCircle 
} from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { useActiveAlerts, useAcknowledgeAlert } from "@/hooks/useAlerts"
import { cn } from "@/lib/utils/cn"

export function AlertsPanel() {
  const { data: alerts, isLoading } = useActiveAlerts()
  const acknowledgeMutation = useAcknowledgeAlert()

  const activeCount = alerts?.length || 0

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
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {activeCount > 0 && (
            <span className="absolute top-1 right-1 h-2.5 w-2.5 rounded-full bg-red-600 animate-pulse ring-2 ring-background" />
          )}
        </Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            System Alerts
            {activeCount > 0 && (
              <Badge variant="destructive" className="rounded-full px-2 py-0.5 text-xs">
                {activeCount}
              </Badge>
            )}
          </SheetTitle>
          <SheetDescription>
            Real-time notifications about system health and KPIs.
          </SheetDescription>
        </SheetHeader>

        <ScrollArea className="h-[calc(100vh-8rem)] mt-6 pr-4">
          {isLoading ? (
            <div className="text-center py-8 text-muted-foreground">Loading alerts...</div>
          ) : activeCount === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center text-muted-foreground">
              <CheckCircle className="h-12 w-12 text-green-500 mb-4" />
              <p className="font-medium text-foreground">All Systems Normal</p>
              <p className="text-sm">No active alerts at this time.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts?.map((alert) => (
                <div 
                  key={alert.id} 
                  className="p-4 rounded-lg border bg-card shadow-sm space-y-3"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2">
                      {getSeverityIcon(alert.severity)}
                      <span className="font-semibold text-sm">{alert.rule_name}</span>
                    </div>
                    <Badge className={cn("text-[10px] capitalize", getSeverityColor(alert.severity))}>
                      {alert.severity}
                    </Badge>
                  </div>
                  
                  <p className="text-sm text-muted-foreground">
                    {alert.message}
                  </p>
                  
                  <div className="flex items-center justify-between pt-2">
                    <span className="text-xs text-muted-foreground">
                      {new Date(alert.created_at).toLocaleTimeString()}
                    </span>
                    <Button 
                      size="sm" 
                      variant="outline" 
                      className="h-7 text-xs"
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
        </ScrollArea>
      </SheetContent>
    </Sheet>
  )
}
