import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Shield, FileText, Check, History, Loader2, Plus } from "lucide-react"
import { usePolicies, usePolicyStats } from "@/hooks/usePolicies"

export default function Policies() {
  const { data: policies, isLoading: isLoadingPolicies } = usePolicies()
  const { data: stats, isLoading: isLoadingStats } = usePolicyStats()

  if (isLoadingPolicies || isLoadingStats) {
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
          <h1 className="text-3xl font-bold">Governance & Policies</h1>
          <p className="text-muted-foreground">Define rules to ensure compliance and quality.</p>
        </div>
        <Button>
          <Shield className="mr-2 h-4 w-4" /> Add Policy
        </Button>
      </div>

      {/* Compliance Overview */}
      <Card className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 text-green-700 rounded-full">
                <Check className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">System Compliance is Healthy</h3>
                <p className="text-sm text-muted-foreground">All critical policies are being enforced correctly.</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                {stats?.avg_compliance ? stats.avg_compliance.toFixed(1) : 0}%
              </p>
              <p className="text-xs text-muted-foreground">Overall Score</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Policy Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {policies?.map((policy) => (
          <Card key={policy.id} className="flex flex-col">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg w-fit mb-3">
                  <FileText className="h-5 w-5" />
                </div>
                <Badge variant={policy.status === 'active' ? 'default' : 'secondary'}>
                  {policy.status}
                </Badge>
              </div>
              <CardTitle className="text-lg">{policy.name}</CardTitle>
              <CardDescription className="line-clamp-2 h-10">
                {policy.description}
              </CardDescription>
            </CardHeader>
            <CardContent className="mt-auto pt-0">
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Compliance</span>
                  <span className={`font-medium ${policy.compliance_score < 90 ? 'text-amber-600' : 'text-green-600'}`}>
                    {policy.compliance_score}%
                  </span>
                </div>
                <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${policy.compliance_score < 90 ? 'bg-amber-500' : 'bg-green-500'}`} 
                    style={{ width: `${policy.compliance_score}%` }}
                  ></div>
                </div>
                <div className="flex items-center gap-2 text-xs text-muted-foreground pt-2 border-t">
                  <History className="h-3 w-3" />
                  Updated {policy.last_updated}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Add New Placeholder */}
        <button className="flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-xl hover:bg-slate-50 dark:hover:bg-slate-900 transition-colors group">
          <div className="p-4 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 group-hover:text-indigo-600 transition-colors mb-3">
            <Plus className="h-6 w-6" />
          </div>
          <p className="font-medium text-slate-600 dark:text-slate-400">Create New Policy</p>
        </button>
      </div>
    </div>
  )
}

function Plus({ className }: { className?: string }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
    >
      <path d="M5 12h14" />
      <path d="M12 5v14" />
    </svg>
  )
}
