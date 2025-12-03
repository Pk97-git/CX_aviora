import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  AreaChart,
  Area
} from 'recharts'
import { 
  Clock, 
  Zap, 
  ShieldCheck,
  Download
} from "lucide-react"
import { 
  useFinancialImpact, 
  useROI, 
  useFinancialTrends, 
  useFinancialBreakdown 
} from "@/hooks/useFinancial"

const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];

export default function Financial() {
  // Force rebuild for Vercel deployment
  const [days, setDays] = useState(30)
  
  const { data: impact } = useFinancialImpact(days)
  const { data: roi } = useROI(days)
  const { data: trends } = useFinancialTrends(days)
  const { data: breakdown } = useFinancialBreakdown(days)

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(value || 0)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Financial Impact</h1>
          <p className="text-muted-foreground">ROI and value generation analysis.</p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant={days === 7 ? "default" : "outline"} 
            size="sm"
            onClick={() => setDays(7)}
          >
            7 Days
          </Button>
          <Button 
            variant={days === 30 ? "default" : "outline"} 
            size="sm"
            onClick={() => setDays(30)}
          >
            30 Days
          </Button>
          <Button variant="outline" size="sm">
            <Download className="mr-2 h-4 w-4" /> Export
          </Button>
        </div>
      </div>

      {/* ROI Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-indigo-50 to-white dark:from-indigo-950 dark:to-background border-indigo-100 dark:border-indigo-900">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Value Generated</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
              {formatCurrency(impact?.total_value_generated || 0)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Across all categories
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">ROI</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {(() => {
                console.log('ROI Data:', roi);
                const val = roi?.roi_percentage;
                return (typeof val === 'number' ? val : 0).toFixed(1);
              })()}%
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Payback: {(() => {
                const val = roi?.payback_period_months;
                return (typeof val === 'number' ? val : 0).toFixed(1);
              })()} months
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Cost Savings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(impact?.automation_cost_saved || 0)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              From automation
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Revenue Protected</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(impact?.revenue_protected || 0)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {impact?.churn_prevented_count || 0} churn risks prevented
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Value Generation Trend</CardTitle>
            <CardDescription>Daily financial impact over time</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              {trends ? (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trends}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={(value) => new Date(value).toLocaleDateString(undefined, { weekday: 'short' })}
                  />
                  <YAxis />
                  <Tooltip 
                    formatter={(value: number) => formatCurrency(value)}
                    labelFormatter={(label) => new Date(label).toLocaleDateString()}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="total_value" 
                    stroke="#6366f1" 
                    fillOpacity={1} 
                    fill="url(#colorValue)" 
                    name="Total Value"
                  />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-muted-foreground">
                  Loading trend data...
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Impact Breakdown</CardTitle>
            <CardDescription>Value distribution by category</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              {breakdown?.categories ? (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                  <Pie
                    data={breakdown?.categories || []}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    fill="#8884d8"
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {(breakdown?.categories || []).map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: number) => formatCurrency(value)} />
                  <Legend />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-muted-foreground">
                  Loading breakdown data...
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Time Saved</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{Math.round(impact?.resolution_time_saved_hours || 0)}h</div>
            <p className="text-xs text-muted-foreground">
              Agent hours saved via AI assistance
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Friction Reduced</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(impact?.friction_cost_reduced || 0)}</div>
            <p className="text-xs text-muted-foreground">
              Cost of friction points eliminated
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">SLA Bonus</CardTitle>
            <ShieldCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(impact?.sla_compliance_bonus || 0)}</div>
            <p className="text-xs text-muted-foreground">
              Penalties avoided & bonuses earned
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
