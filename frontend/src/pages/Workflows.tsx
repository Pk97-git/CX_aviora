import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Workflow, Plus, Play, Pause, MoreHorizontal, Zap, Clock, CheckCircle2 } from "lucide-react"

const workflows = [
  {
    id: 1,
    name: "High Value Refund Approval",
    trigger: "Ticket Created > $500",
    actions: ["Check LTV", "Route to Manager", "Slack Alert"],
    status: "active",
    runs: 145,
    saved: "24h",
  },
  {
    id: 2,
    name: "Auto-Reply: Shipping Delays",
    trigger: "Intent = 'Shipping Status'",
    actions: ["Check Order Status", "Send Email"],
    status: "active",
    runs: 1250,
    saved: "180h",
  },
  {
    id: 3,
    name: "VIP Escalation",
    trigger: "Customer Tag = 'VIP'",
    actions: ["Set Priority = Urgent", "Assign to Senior Team"],
    status: "paused",
    runs: 45,
    saved: "5h",
  },
]

export default function Workflows() {
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
              Time Saved (This Month)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-violet-700 dark:text-violet-400">209 Hours</div>
            <p className="text-xs text-muted-foreground mt-1">
              Equivalent to 1.5 full-time agents
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
            <div className="text-3xl font-bold">12</div>
            <p className="text-xs text-muted-foreground mt-1">
              Handling 45% of total ticket volume
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
            <div className="text-3xl font-bold text-green-700">99.8%</div>
            <p className="text-xs text-muted-foreground mt-1">
              Only 3 failures requiring manual intervention
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Workflow List */}
      <div className="grid gap-4">
        {workflows.map((workflow) => (
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
                  <p className="text-sm font-medium">{workflow.runs} Runs</p>
                  <p className="text-xs text-green-600">Saved {workflow.saved}</p>
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
