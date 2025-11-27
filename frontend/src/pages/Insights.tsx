import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
} from 'recharts'
import { 
  TrendingUp, 
  DollarSign, 
  Users, 
  Download,
  Calendar
} from "lucide-react"
import { 
  useRCA, 
  useSentimentTrend 
} from "@/hooks/useAnalytics"

// Mock Data
const mockRcaData = [
  { name: 'Payment Failure', count: 145, cost: 4500 },
  { name: 'Login Issue', count: 89, cost: 2100 },
  { name: 'Shipping Delay', count: 67, cost: 1800 },
  { name: 'Wrong Item', count: 45, cost: 3200 },
  { name: 'Refund Status', count: 34, cost: 800 },
]

const mockSentimentData = [
  { date: 'Mon', score: 78 },
  { date: 'Tue', score: 82 },
  { date: 'Wed', score: 75 },
  { date: 'Thu', score: 85 },
  { date: 'Fri', score: 88 },
  { date: 'Sat', score: 92 },
  { date: 'Sun', score: 90 },
]

const volumeForecast = [
  { date: 'Mon', actual: 240, predicted: 245 },
  { date: 'Tue', actual: 280, predicted: 275 },
  { date: 'Wed', actual: 260, predicted: 265 },
  { date: 'Thu', actual: null, predicted: 310 }, // Future
  { date: 'Fri', actual: null, predicted: 290 }, // Future
  { date: 'Sat', actual: null, predicted: 180 }, // Future
  { date: 'Sun', actual: null, predicted: 160 }, // Future
]

const agentPerformance = [
  { name: 'Sarah J.', resolved: 45, csat: 4.8 },
  { name: 'Mike T.', resolved: 38, csat: 4.6 },
  { name: 'Emma W.', resolved: 42, csat: 4.9 },
  { name: 'David L.', resolved: 30, csat: 4.2 },
]

export default function Insights() {
  // Fetch real data from API
  const { data: apiRcaData } = useRCA()
  const { data: apiSentimentData } = useSentimentTrend()

  // Use API data if available, otherwise fall back to mock data
  const rcaData = apiRcaData || mockRcaData
  const sentimentData = apiSentimentData || mockSentimentData

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Executive Insights</h1>
          <p className="text-muted-foreground">Strategic overview of CX operations and financial impact.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Calendar className="mr-2 h-4 w-4" /> Last 7 Days
          </Button>
          <Button variant="outline" size="sm">
            <Download className="mr-2 h-4 w-4" /> Export Report
          </Button>
        </div>
      </div>

      {/* Financial Impact Row (CEO View) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-gradient-to-br from-indigo-50 to-white dark:from-indigo-950 dark:to-background border-indigo-100 dark:border-indigo-900">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-indigo-600" />
              Revenue at Risk (SLA Breaches)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-indigo-700 dark:text-indigo-400">$12,450</div>
            <p className="text-xs text-muted-foreground mt-1">
              Estimated loss from 15 critical breaches
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-green-600" />
              Cost Saved by AI
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-700 dark:text-green-400">$8,200</div>
            <p className="text-xs text-muted-foreground mt-1">
              450 tickets auto-resolved this week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Users className="h-4 w-4 text-blue-600" />
              Customer Retention Risk
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-amber-600">Low</div>
            <p className="text-xs text-muted-foreground mt-1">
              Sentiment score stable at 88/100
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Operational Deep Dive (Manager View) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* RCA Chart */}
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Root Cause Analysis (Top Issues)</CardTitle>
            <CardDescription>
              Volume drivers and their estimated financial impact.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rcaData} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" width={100} tick={{fontSize: 12}} />
                <Tooltip 
                  cursor={{fill: 'transparent'}}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={20} name="Ticket Volume" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Sentiment Trend */}
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Customer Sentiment Trend</CardTitle>
            <CardDescription>
              7-day moving average of AI-analyzed sentiment.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={sentimentData}>
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="date" tick={{fontSize: 12}} />
                <YAxis domain={[0, 100]} tick={{fontSize: 12}} />
                <Tooltip />
                <Area type="monotone" dataKey="score" stroke="#10b981" fillOpacity={1} fill="url(#colorScore)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Forecasting & Team (Strategic Planning) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Volume Forecast */}
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Volume Forecast (AI Prediction)</CardTitle>
            <CardDescription>
              Predicted ticket volume for the next 4 days.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={volumeForecast}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="actual" stroke="#6366f1" strokeWidth={2} name="Actual" />
                <Line type="monotone" dataKey="predicted" stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 5" name="AI Forecast" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Agent Leaderboard */}
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Top Performers</CardTitle>
            <CardDescription>Based on resolution speed & CSAT.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {agentPerformance.map((agent, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-xs">
                      {agent.name.charAt(0)}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{agent.name}</p>
                      <p className="text-xs text-muted-foreground">{agent.resolved} resolved</p>
                    </div>
                  </div>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                    {agent.csat} ★
                  </Badge>
                </div>
              ))}
            </div>
            <Button variant="ghost" className="w-full mt-4 text-xs">View All Agents</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
