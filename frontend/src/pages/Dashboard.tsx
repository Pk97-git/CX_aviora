import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { TrendingUp, AlertTriangle, Clock, Zap } from "lucide-react"
import { useDashboardKPIs } from "@/hooks/useAnalytics"

export default function Dashboard() {
  const { data: kpis, isLoading, error } = useDashboardKPIs()

  if (error) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Failed to load dashboard</h2>
          <p className="text-muted-foreground">{error.message}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-sm text-muted-foreground">Last updated: Just now</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => window.location.href = '/insights'}>
            View Executive Insights
          </Button>
          <Button onClick={() => window.location.reload()}>Refresh</Button>
        </div>
      </div>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Open Tickets
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 bg-muted animate-pulse rounded" />
            ) : (
              <>
                <div className="text-2xl font-bold">{kpis?.open_tickets || 0}</div>
                <p className="text-xs text-green-600 mt-1">
                  {kpis?.total_tickets_7d || 0} total (7 days)
                </p>
              </>
            )}
          </CardContent>
        </Card>
        
        <Card className="border-amber-200 bg-amber-50 dark:bg-amber-950">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">
              SLA Risk (AI)
            </CardTitle>
            <AlertTriangle className="h-4 w-4 text-amber-600" />
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 bg-amber-200 animate-pulse rounded" />
            ) : (
              <>
                <div className="text-2xl font-bold text-amber-700 dark:text-amber-400">
                  {kpis?.sla_risk_count || 0}
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  tickets at risk
                </p>
              </>
            )}
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Avg Resolution
            </CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 bg-muted animate-pulse rounded" />
            ) : (
              <>
                <div className="text-2xl font-bold">{kpis?.avg_resolution_hours.toFixed(1) || '0.0'}h</div>
                <p className="text-xs text-green-600 mt-1">
                  {kpis?.resolved_tickets_7d || 0} resolved (7d)
                </p>
              </>
            )}
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Automation Rate
            </CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-8 bg-muted animate-pulse rounded" />
            ) : (
              <>
                <div className="text-2xl font-bold">{kpis?.automation_rate.toFixed(0) || 0}%</div>
                <p className="text-xs text-green-600 mt-1">
                  AI-powered resolution
                </p>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Welcome Card */}
      <Card>
        <CardHeader>
          <CardTitle>Welcome to Aivora</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Your AI-First CX Operations Platform is ready. The dashboard shows real-time metrics 
            for your customer support operations. Navigate to Tickets to start managing your queue.
          </p>
        </CardContent>
      </Card>

      {/* Activity Feed Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Live Activity Feed</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-start gap-3 text-sm">
              <div className="w-2 h-2 bg-violet-600 rounded-full mt-1.5"></div>
              <div>
                <p><span className="font-medium">AI</span> refunded $50 for Order #12345</p>
                <p className="text-xs text-muted-foreground">2 minutes ago</p>
              </div>
            </div>
            <div className="flex items-start gap-3 text-sm">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-1.5"></div>
              <div>
                <p><span className="font-medium">System</span> escalated Ticket #456 to Engineering</p>
                <p className="text-xs text-muted-foreground">5 minutes ago</p>
              </div>
            </div>
            <div className="flex items-start gap-3 text-sm">
              <div className="w-2 h-2 bg-green-600 rounded-full mt-1.5"></div>
              <div>
                <p><span className="font-medium">Workflow</span> "Auto-Refund" completed successfully</p>
                <p className="text-xs text-muted-foreground">8 minutes ago</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
