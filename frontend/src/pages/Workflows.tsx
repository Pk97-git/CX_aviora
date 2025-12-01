import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Workflow, Plus, Play, Pause, MoreHorizontal, Zap, Clock, CheckCircle2, Loader2 } from "lucide-react"
import { useWorkflows, useWorkflowStats } from "@/hooks/useWorkflows"

export default function Workflows() {
  const { data: workflows, isLoading: isLoadingWorkflows } = useWorkflows()
  const { data: stats, isLoading: isLoadingStats } = useWorkflowStats()

  if (isLoadingWorkflows || isLoadingStats) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-violet-600" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Automation Workflows</h1>
          <p className="text-muted-foreground">Manage automated rules to reduce manual workload.</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" /> Create Workflow
        </Button>
      </div>

      {/* ROI Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-gradient-to-br from-violet-50 to-white dark:from-violet-950 dark:to-background border-violet-100 dark:border-violet-900">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Clock className="h-4 w-4 text-violet-600" />
              Time Saved (Total)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-violet-700 dark:text-violet-400">
              {stats?.time_saved_hours.toLocaleString() ?? 0} Hours
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Across {stats?.total_executions.toLocaleString() ?? 0} executions
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Zap className="h-4 w-4 text-amber-500" />
              Active Automations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats?.active_workflows ?? 0}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Out of {stats?.total_workflows ?? 0} total workflows
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-600" />
              Success Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-700">
              {(stats?.avg_success_rate ? stats.avg_success_rate * 100 : 0).toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Average across all runs
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Workflow List */}
      <div className="grid gap-4">
        {workflows?.map((workflow) => (
          <Card key={workflow.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-6 flex items-center justify-between">
              <div className="flex items-start gap-4">
                <div className={`p-3 rounded-lg ${workflow.status === 'active' ? 'bg-violet-100 text-violet-600' : 'bg-gray-100 text-gray-500'}`}>
                  <Workflow className="h-6 w-6" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-lg">{workflow.name}</h3>
                    <Badge variant={workflow.status === 'active' ? 'default' : 'secondary'}>
                      {workflow.status}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Zap className="h-3 w-3" /> Trigger: {workflow.trigger}
                    </span>
                    <span>•</span>
                    <span>{workflow.actions.length} Actions</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="text-right">
                  <p className="text-sm font-medium">{workflow.executions.toLocaleString()} Runs</p>
                  <p className="text-xs text-green-600">Saved {workflow.time_saved_hours}h</p>
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="icon">
                    {workflow.status === 'active' ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                  </Button>
                  <Button variant="ghost" size="icon">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
