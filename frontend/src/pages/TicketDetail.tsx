import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  ArrowLeft, 
  Send, 
  Paperclip, 
  MoreVertical, 
  User, 
  Sparkles,
  MessageSquare,
  Mail,
  ShoppingBag,
  AlertCircle,
  CheckCircle2
} from "lucide-react"
import { useNavigate, useParams } from "react-router-dom"

export default function TicketDetail() {
  const navigate = useNavigate()
  const { id } = useParams()

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-8">
      {/* Left Sidebar - Ticket List (Collapsed/Mini view could go here, but keeping it simple for now) */}
      
      {/* Main Content - Conversation Stream */}
      <div className="flex-1 flex flex-col border-r bg-background">
        {/* Header */}
        <div className="h-16 border-b flex items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate('/tickets')}>
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="font-semibold text-lg">Refund request {'>'} $500</h2>
                <Badge variant="outline" className="bg-violet-50 text-violet-700">#{id || 'a3f2b1c4'}</Badge>
              </div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span className="flex items-center gap-1"><Mail className="h-3 w-3" /> via Email</span>
                <span>•</span>
                <span>Created 2 hours ago</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <User className="mr-2 h-4 w-4" /> Assign
            </Button>
            <Button variant="default" size="sm" className="bg-green-600 hover:bg-green-700">
              <CheckCircle2 className="mr-2 h-4 w-4" /> Resolve
            </Button>
            <Button variant="ghost" size="icon">
              <MoreVertical className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50/50 dark:bg-slate-950/50">
          
          {/* Customer Message */}
          <div className="flex gap-4">
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold shrink-0">
              JD
            </div>
            <div className="flex-1 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm">John Doe</span>
                <span className="text-xs text-muted-foreground">Today, 10:23 AM</span>
              </div>
              <div className="bg-white dark:bg-card border rounded-lg p-4 shadow-sm text-sm leading-relaxed">
                <p>Hi,</p>
                <p className="mt-2">I recently purchased the Premium Enterprise Plan (Order #ORD-2024-889) but realized it doesn't fit our current needs. We haven't used any of the features yet.</p>
                <p className="mt-2">Since it's been less than 24 hours, I'd like to request a full refund of the $599 charge.</p>
                <p className="mt-2">Thanks,<br/>John</p>
              </div>
            </div>
          </div>

          {/* Internal Note */}
          <div className="flex gap-4 px-8">
            <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center text-amber-600 font-bold shrink-0 text-xs">
              SYS
            </div>
            <div className="flex-1 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm text-amber-600">Aivora System Note</span>
                <span className="text-xs text-muted-foreground">Today, 10:24 AM</span>
              </div>
              <div className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 rounded-lg p-3 text-sm text-amber-800 dark:text-amber-200">
                <div className="flex items-center gap-2 font-medium mb-1">
                  <AlertCircle className="h-4 w-4" /> High Value Refund Detected
                </div>
                Ticket value ($599) exceeds auto-approval threshold ($500). Routed to Manager Approval Queue.
              </div>
            </div>
          </div>

        </div>

        {/* Input Area */}
        <div className="p-4 border-t bg-background">
          <div className="border rounded-lg shadow-sm bg-white dark:bg-card focus-within:ring-1 focus-within:ring-primary transition-all">
            <div className="flex items-center gap-2 p-2 border-b bg-slate-50 dark:bg-slate-900/50 rounded-t-lg">
              <Button variant="ghost" size="sm" className="h-8 text-xs font-medium bg-white dark:bg-slate-800 shadow-sm">Reply</Button>
              <Button variant="ghost" size="sm" className="h-8 text-xs text-muted-foreground hover:text-amber-600">Internal Note</Button>
              <div className="h-4 w-px bg-border mx-1" />
              <Button variant="ghost" size="icon" className="h-8 w-8"><Sparkles className="h-4 w-4 text-violet-500" /></Button>
            </div>
            <textarea 
              className="w-full p-3 min-h-[100px] resize-none bg-transparent border-none focus:outline-none text-sm"
              placeholder="Type your reply... Use @ to mention teammates."
            />
            <div className="flex items-center justify-between p-2">
              <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground">
                <Paperclip className="h-4 w-4" />
              </Button>
              <Button size="sm" className="gap-2">
                Send Reply <Send className="h-3 w-3" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Context & AI */}
      <div className="w-[350px] border-l bg-slate-50/50 dark:bg-slate-950/50 overflow-y-auto p-4 space-y-6">
        
        {/* Customer Profile */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <User className="h-4 w-4 text-muted-foreground" />
              Customer Profile
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center text-lg font-bold">
                JD
              </div>
              <div>
                <h3 className="font-semibold">John Doe</h3>
                <p className="text-xs text-muted-foreground">john.doe@example.com</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="p-2 bg-background rounded border text-center">
                <p className="text-xs text-muted-foreground">LTV</p>
                <p className="font-semibold text-green-600">$2,450</p>
              </div>
              <div className="p-2 bg-background rounded border text-center">
                <p className="text-xs text-muted-foreground">Orders</p>
                <p className="font-semibold">12</p>
              </div>
              <div className="p-2 bg-background rounded border text-center col-span-2">
                <p className="text-xs text-muted-foreground">Tags</p>
                <div className="flex gap-1 justify-center mt-1">
                  <Badge variant="secondary" className="text-[10px]">VIP</Badge>
                  <Badge variant="secondary" className="text-[10px]">Enterprise</Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* AI Copilot */}
        <Card className="border-violet-200 dark:border-violet-900 bg-gradient-to-b from-violet-50 to-white dark:from-violet-950/30 dark:to-background">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2 text-violet-700 dark:text-violet-400">
              <Sparkles className="h-4 w-4" />
              AI Copilot
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            
            {/* Sentiment */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-muted-foreground">Sentiment Analysis</span>
                <span className="font-medium text-amber-600">Neutral (45%)</span>
              </div>
              <div className="w-full bg-secondary h-1.5 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 w-[45%] rounded-full" />
              </div>
            </div>

            {/* Suggested Actions */}
            <div className="space-y-2">
              <p className="text-xs font-medium text-muted-foreground">Suggested Actions</p>
              <Button variant="outline" className="w-full justify-start h-auto py-2 px-3 text-xs bg-white dark:bg-card hover:border-violet-300 hover:bg-violet-50 transition-colors">
                <CheckCircle2 className="h-3 w-3 mr-2 text-green-600" />
                Approve Refund ($599)
              </Button>
              <Button variant="outline" className="w-full justify-start h-auto py-2 px-3 text-xs bg-white dark:bg-card hover:border-violet-300 hover:bg-violet-50 transition-colors">
                <MessageSquare className="h-3 w-3 mr-2 text-blue-600" />
                Ask for Feedback
              </Button>
            </div>

            {/* Smart Summary */}
            <div className="bg-white dark:bg-card rounded-lg p-3 text-xs border shadow-sm">
              <p className="font-medium mb-1 text-violet-700 dark:text-violet-400">Smart Summary</p>
              <p className="text-muted-foreground leading-relaxed">
                Customer requesting refund for Enterprise Plan ($599) purchased {`<`}24h ago. Reason: Features don't fit needs. Policy allows refund, but amount requires approval.
              </p>
            </div>

          </CardContent>
        </Card>

        {/* Recent Orders */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <ShoppingBag className="h-4 w-4 text-muted-foreground" />
              Recent Orders
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <div>
                <p className="font-medium">#ORD-2024-889</p>
                <p className="text-xs text-muted-foreground">Yesterday</p>
              </div>
              <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">$599.00</Badge>
            </div>
            <div className="flex items-center justify-between text-sm">
              <div>
                <p className="font-medium">#ORD-2024-102</p>
                <p className="text-xs text-muted-foreground">2 weeks ago</p>
              </div>
              <Badge variant="outline" className="text-slate-600">$49.00</Badge>
            </div>
          </CardContent>
        </Card>

      </div>
    </div>
  )
}
