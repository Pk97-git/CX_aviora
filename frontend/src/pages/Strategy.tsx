import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { 
  ScatterChart, 
  Scatter, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
  Legend,
  Line,
  Area,
  ReferenceLine,
  ComposedChart
} from 'recharts'
import { 
  Globe, 
  BrainCircuit, 
  Lightbulb, 
  ArrowRight,
  Users,
  DollarSign,
  Calendar
} from "lucide-react"
import { 
  useTopicClusters, 
  useRegionalIntelligence, 
  useStrategicRecommendations 
} from "@/hooks/useStrategy"

// Mock Data for Topic Clusters
const mockTopicClusters = [
  { topic: 'Shipping Delay', volume: 450, sentiment: 25, impact: 'High' },
  { topic: 'Login Error', volume: 320, sentiment: 15, impact: 'Critical' },
  { topic: 'Sizing Issue', volume: 210, sentiment: 60, impact: 'Medium' },
  { topic: 'Promo Code', volume: 180, sentiment: 85, impact: 'Low' },
  { topic: 'Refund Status', volume: 150, sentiment: 45, impact: 'Medium' },
  { topic: 'App Crash', volume: 90, sentiment: 10, impact: 'Critical' },
]

// Mock Data for Regional Intelligence
const mockRegionalData = [
  { region: 'North America', volume: 1200, sentiment: 78, frictionCost: 4500 },
  { region: 'Europe', volume: 850, sentiment: 65, frictionCost: 3200 },
  { region: 'Asia Pacific', volume: 600, sentiment: 82, frictionCost: 1800 },
  { region: 'LATAM', volume: 300, sentiment: 70, frictionCost: 900 },
]

const mockRecommendations = [
  {
    id: 1,
    type: 'Logistics',
    title: 'Invest in EU Distribution Partner',
    description: 'Shipping delays in Europe are driving 40% of negative sentiment. A local partner could reduce friction cost by $3.2k/week.',
    impact: 'High',
    confidence: '94%'
  },
  {
    id: 2,
    type: 'Product',
    title: 'Fix "Login Loop" Bug on iOS',
    description: 'Critical cluster "App Crash" is correlated with the latest iOS update. 150 VIP customers affected.',
    impact: 'Critical',
    confidence: '98%'
  },
  {
    id: 3,
    type: 'Policy',
    title: 'Relax Return Policy for "Sizing"',
    description: 'Sizing issues have neutral sentiment but high volume. Simplifying returns could boost LTV by 15%.',
    impact: 'Medium',
    confidence: '85%'
  }
]

// Churn Prediction Data
const churnRiskData = [
  { customer: 'Acme Corp', ltv: 45000, sentiment: 25, churnRisk: 'High', tickets: 12 },
  { customer: 'TechStart Inc', ltv: 32000, sentiment: 40, churnRisk: 'High', tickets: 8 },
  { customer: 'Global Retail', ltv: 28000, sentiment: 55, churnRisk: 'Medium', tickets: 5 },
  { customer: 'FastShip Co', ltv: 18000, sentiment: 70, churnRisk: 'Low', tickets: 3 },
  { customer: 'CloudBase', ltv: 52000, sentiment: 80, churnRisk: 'Low', tickets: 2 },
  { customer: 'DataFlow Ltd', ltv: 15000, sentiment: 35, churnRisk: 'High', tickets: 10 },
]

// Cost of Friction Analysis
const frictionCostData = [
  { category: 'Potential Revenue', value: 125000, type: 'positive' },
  { category: 'Shipping Delays', value: -12000, type: 'negative' },
  { category: 'Login Issues', value: -8500, type: 'negative' },
  { category: 'Sizing Returns', value: -6200, type: 'negative' },
  { category: 'App Crashes', value: -4300, type: 'negative' },
  { category: 'Net Revenue', value: 94000, type: 'result' },
]

// 30-Day Forecast
const forecastData = [
  { day: 'Day 1', actual: 280, predicted: 285, lower: 270, upper: 300 },
  { day: 'Day 2', actual: 295, predicted: 290, lower: 275, upper: 305 },
  { day: 'Day 3', actual: 310, predicted: 305, lower: 290, upper: 320 },
  { day: 'Day 4', actual: 288, predicted: 295, lower: 280, upper: 310 },
  { day: 'Day 5', actual: 305, predicted: 300, lower: 285, upper: 315 },
  { day: 'Day 7', actual: null, predicted: 315, lower: 295, upper: 335 },
  { day: 'Day 10', actual: null, predicted: 325, lower: 300, upper: 350 },
  { day: 'Day 15', actual: null, predicted: 340, lower: 310, upper: 370 },
  { day: 'Day 20', actual: null, predicted: 330, lower: 300, upper: 360 },
  { day: 'Day 25', actual: null, predicted: 320, lower: 290, upper: 350 },
  { day: 'Day 30', actual: null, predicted: 310, lower: 280, upper: 340 },
]

export default function Strategy() {
  // Fetch real data from API
  const { data: apiTopicClusters, isLoading: loadingTopics } = useTopicClusters()
  const { data: apiRegionalData, isLoading: loadingRegional } = useRegionalIntelligence()
  const { data: apiRecommendations, isLoading: loadingRecs } = useStrategicRecommendations()

  // Use API data if available, otherwise fall back to mock data
  const topicClusters = apiTopicClusters || mockTopicClusters
  const regionalData = apiRegionalData || mockRegionalData
  const recommendations = apiRecommendations || mockRecommendations

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Globe className="h-8 w-8 text-indigo-600" />
            Global Strategy Command
          </h1>
          <p className="text-muted-foreground">Macro-level intelligence for HQ leadership.</p>
        </div>
        <div className="flex gap-2">
          <Badge variant="outline" className="px-3 py-1 text-sm bg-indigo-50 text-indigo-700 border-indigo-200">
            <BrainCircuit className="w-3 h-3 mr-2" />
            AI Analysis: Live
          </Badge>
          <Button>Generate Q3 Report</Button>
        </div>
      </div>

      {/* Strategic AI Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-3 bg-gradient-to-r from-slate-900 to-slate-800 text-white border-none shadow-xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-amber-400">
              <Lightbulb className="h-5 w-5" />
              Strategic AI Recommendations
            </CardTitle>
            <CardDescription className="text-slate-300">
              Top 3 moves to improve global CX and reduce revenue leakage.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {recommendations.map((rec) => (
                <div key={rec.id} className="bg-white/10 p-4 rounded-lg hover:bg-white/15 transition-colors cursor-pointer border border-white/5">
                  <div className="flex justify-between items-start mb-2">
                    <Badge variant="secondary" className="bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 border-none">
                      {rec.type}
                    </Badge>
                    <span className="text-xs text-slate-400 font-mono">Conf: {rec.confidence}</span>
                  </div>
                  <h3 className="font-semibold text-lg mb-1">{rec.title}</h3>
                  <p className="text-sm text-slate-300 leading-relaxed mb-3">
                    {rec.description}
                  </p>
                  <div className="flex items-center text-xs text-amber-400 font-medium">
                    View Analysis <ArrowRight className="h-3 w-3 ml-1" />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Semantic Topic Clusters */}
        <Card>
          <CardHeader>
            <CardTitle>Semantic Topic Clusters</CardTitle>
            <CardDescription>
              Volume vs. Sentiment. <span className="text-red-500 font-medium">Red</span> = Critical Issues.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" dataKey="sentiment" name="Sentiment" unit="%" domain={[0, 100]} label={{ value: 'Sentiment Score', position: 'bottom', offset: 0 }} />
                <YAxis type="number" dataKey="volume" name="Volume" unit=" tix" label={{ value: 'Ticket Volume', angle: -90, position: 'insideLeft' }} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-white dark:bg-slate-900 p-3 border rounded shadow-lg">
                        <p className="font-bold">{data.topic}</p>
                        <p className="text-sm">Volume: {data.volume}</p>
                        <p className="text-sm">Sentiment: {data.sentiment}%</p>
                        <p className="text-sm">Impact: {data.impact}</p>
                      </div>
                    );
                  }
                  return null;
                }} />
                <Scatter name="Topics" data={topicClusters} fill="#8884d8">
                  {topicClusters.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.sentiment < 40 ? '#ef4444' : entry.sentiment < 70 ? '#f59e0b' : '#10b981'} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Global Regional Intelligence */}
        <Card>
          <CardHeader>
            <CardTitle>Regional Intelligence</CardTitle>
            <CardDescription>
              Sentiment & Friction Cost by Region.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionalData} layout="vertical" margin={{ left: 40 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                <XAxis type="number" hide />
                <YAxis dataKey="region" type="category" width={100} tick={{fontSize: 12, fontWeight: 600}} />
                <Tooltip 
                  cursor={{fill: 'transparent'}}
                  contentStyle={{ borderRadius: '8px' }}
                />
                <Legend />
                <Bar dataKey="sentiment" name="Sentiment Score" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={20} />
                <Bar dataKey="frictionCost" name="Friction Cost ($)" fill="#ef4444" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

      </div>

      {/* Churn Prediction & Cost Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Churn Prediction Radar */}
        <Card className="border-red-100 dark:border-red-900">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5 text-red-600" />
              Churn Prediction Radar
            </CardTitle>
            <CardDescription>
              High-value customers at risk. <span className="text-red-600 font-semibold">Red zone</span> = immediate action needed.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  type="number" 
                  dataKey="sentiment" 
                  name="Sentiment" 
                  unit="%" 
                  domain={[0, 100]} 
                  label={{ value: 'Sentiment Score', position: 'bottom', offset: 0 }} 
                />
                <YAxis 
                  type="number" 
                  dataKey="ltv" 
                  name="LTV" 
                  unit="$" 
                  label={{ value: 'Customer LTV ($)', angle: -90, position: 'insideLeft' }} 
                />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-white dark:bg-slate-900 p-3 border rounded shadow-lg">
                        <p className="font-bold">{data.customer}</p>
                        <p className="text-sm">LTV: ${data.ltv.toLocaleString()}</p>
                        <p className="text-sm">Sentiment: {data.sentiment}%</p>
                        <p className="text-sm">Tickets: {data.tickets}</p>
                        <p className={`text-sm font-semibold ${data.churnRisk === 'High' ? 'text-red-600' : data.churnRisk === 'Medium' ? 'text-amber-600' : 'text-green-600'}`}>
                          Risk: {data.churnRisk}
                        </p>
                      </div>
                    );
                  }
                  return null;
                }} />
                <ReferenceLine x={50} stroke="#ef4444" strokeDasharray="3 3" label={{ value: 'Risk Threshold', position: 'top' }} />
                <Scatter name="Customers" data={churnRiskData} fill="#8884d8">
                  {churnRiskData.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={entry.churnRisk === 'High' ? '#ef4444' : entry.churnRisk === 'Medium' ? '#f59e0b' : '#10b981'} 
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Cost of Friction */}
        <Card className="border-amber-100 dark:border-amber-900">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5 text-amber-600" />
              Cost of Friction Analysis
            </CardTitle>
            <CardDescription>
              Revenue impact of CX friction points this month.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <div className="space-y-4">
              {frictionCostData.map((item, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${item.type === 'result' ? 'text-lg font-bold' : ''}`}>
                      {item.category}
                    </p>
                  </div>
                  <div className={`text-right ${
                    item.type === 'positive' ? 'text-green-600' : 
                    item.type === 'negative' ? 'text-red-600' : 
                    'text-indigo-600 font-bold text-lg'
                  }`}>
                    {item.type === 'positive' ? '+' : ''}{item.value < 0 ? '' : ''}${Math.abs(item.value).toLocaleString()}
                  </div>
                </div>
              ))}
              <div className="pt-4 border-t">
                <div className="flex justify-between items-center">
                  <p className="text-sm text-muted-foreground">Total Friction Cost</p>
                  <p className="text-xl font-bold text-red-600">-$31,000</p>
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Addressing top 2 issues could recover <span className="font-semibold text-green-600">$20.5k</span>
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

      </div>

      {/* Predictive Horizon */}
      <Card className="border-indigo-100 dark:border-indigo-900">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5 text-indigo-600" />
            30-Day Predictive Horizon
          </CardTitle>
          <CardDescription>
            AI-powered volume forecast with 95% confidence intervals. Plan resources proactively.
          </CardDescription>
        </CardHeader>
        <CardContent className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={forecastData}>
              <defs>
                <linearGradient id="confidenceGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0.05}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="day" tick={{fontSize: 11}} />
              <YAxis label={{ value: 'Ticket Volume', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="upper" 
                stroke="none" 
                fill="url(#confidenceGradient)" 
                name="Upper Bound"
              />
              <Area 
                type="monotone" 
                dataKey="lower" 
                stroke="none" 
                fill="#fff" 
                name="Lower Bound"
              />
              <Line 
                type="monotone" 
                dataKey="actual" 
                stroke="#10b981" 
                strokeWidth={2} 
                dot={{ r: 4 }} 
                name="Actual Volume"
              />
              <Line 
                type="monotone" 
                dataKey="predicted" 
                stroke="#6366f1" 
                strokeWidth={2} 
                strokeDasharray="5 5" 
                dot={{ r: 3 }} 
                name="AI Forecast"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

    </div>
  )
}
