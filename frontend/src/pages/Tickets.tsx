import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { ticketsApi, Ticket } from '@/lib/api/tickets'
import { Search, Filter } from 'lucide-react'

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [priorityFilter, setPriorityFilter] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()
  const { toast } = useToast()

  useEffect(() => {
    loadTickets()
  }, [statusFilter, priorityFilter])

  const loadTickets = async () => {
    try {
      const data = await ticketsApi.list({
        status: statusFilter || undefined,
        priority: priorityFilter || undefined,
        search: searchQuery || undefined,
      })
      setTickets(data)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: 'Failed to load tickets',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = () => {
    loadTickets()
  }

  const getSentimentColor = (sentiment: number | null) => {
    if (!sentiment) return 'bg-gray-100 text-gray-800'
    if (sentiment > 0.3) return 'bg-green-100 text-green-800'
    if (sentiment < -0.3) return 'bg-red-100 text-red-800'
    return 'bg-yellow-100 text-yellow-800'
  }

  const getSentimentLabel = (sentiment: number | null) => {
    if (!sentiment) return 'Neutral'
    if (sentiment > 0.3) return 'Positive'
    if (sentiment < -0.3) return 'Negative'
    return 'Neutral'
  }

  const getPriorityColor = (priority: string | null) => {
    switch (priority) {
      case 'urgent':
        return 'bg-red-100 text-red-800'
      case 'high':
        return 'bg-orange-100 text-orange-800'
      case 'medium':
        return 'bg-blue-100 text-blue-800'
      case 'low':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Tickets</h1>
        <p className="text-muted-foreground">Manage customer support tickets with AI insights</p>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Filters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="flex gap-2">
              <Input
                placeholder="Search tickets..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
              <Button onClick={handleSearch} size="icon">
                <Search className="h-4 w-4" />
              </Button>
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger>
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Statuses</SelectItem>
                <SelectItem value="open">Open</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="resolved">Resolved</SelectItem>
                <SelectItem value="closed">Closed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={priorityFilter} onValueChange={setPriorityFilter}>
              <SelectTrigger>
                <SelectValue placeholder="All Priorities" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Priorities</SelectItem>
                <SelectItem value="urgent">Urgent</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <Button
              variant="outline"
              onClick={() => {
                setStatusFilter('')
                setPriorityFilter('')
                setSearchQuery('')
              }}
            >
              Clear Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tickets Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Tickets ({tickets.length})</CardTitle>
          <CardDescription>Click on a ticket to view details</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Customer</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>AI Category</TableHead>
                <TableHead>Sentiment</TableHead>
                <TableHead>Created</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tickets.map((ticket) => (
                <TableRow
                  key={ticket.id}
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => navigate(`/tickets/${ticket.id}`)}
                >
                  <TableCell className="font-medium max-w-md">
                    <div className="truncate">{ticket.title}</div>
                    {ticket.ai_summary && (
                      <div className="text-xs text-muted-foreground truncate mt-1">
                        {ticket.ai_summary}
                      </div>
                    )}
                  </TableCell>
                  <TableCell>
                    <div>{ticket.customer_name || 'Unknown'}</div>
                    <div className="text-xs text-muted-foreground">
                      {ticket.customer_email}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="capitalize">
                      {ticket.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={getPriorityColor(ticket.priority)}>
                      {ticket.priority || 'None'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className="capitalize">
                      {ticket.ai_category || 'Uncategorized'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={getSentimentColor(ticket.ai_sentiment)}>
                      {getSentimentLabel(ticket.ai_sentiment)}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {new Date(ticket.created_at).toLocaleDateString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {tickets.length === 0 && (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No tickets found</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
