import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { ticketsApi, TicketDetail, Comment } from '@/lib/api/tickets'
import { ArrowLeft, MessageSquare, Sparkles, TrendingUp, Tag } from 'lucide-react'

export default function TicketDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { toast } = useToast()
  
  const [ticket, setTicket] = useState<TicketDetail | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  const [loading, setLoading] = useState(true)
  const [newComment, setNewComment] = useState('')
  const [isInternal, setIsInternal] = useState(false)

  useEffect(() => {
    if (id) {
      loadTicket()
      loadComments()
    }
  }, [id])

  const loadTicket = async () => {
    try {
      const data = await ticketsApi.get(id!)
      setTicket(data)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: 'Failed to load ticket',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const loadComments = async () => {
    try {
      const data = await ticketsApi.getComments(id!)
      setComments(data)
    } catch (error: any) {
      console.error('Failed to load comments:', error)
    }
  }

  const handleStatusChange = async (status: string) => {
    try {
      await ticketsApi.update(id!, { status })
      toast({
        title: 'Success',
        description: 'Ticket status updated',
      })
      loadTicket()
    } catch (error: any) {
      toast({
        title: 'Error',
        description: 'Failed to update status',
        variant: 'destructive',
      })
    }
  }

  const handleAddComment = async () => {
    if (!newComment.trim()) return

    try {
      await ticketsApi.addComment(id!, {
        content: newComment,
        is_internal: isInternal,
      })
      toast({
        title: 'Success',
        description: 'Comment added',
      })
      setNewComment('')
      loadComments()
    } catch (error: any) {
      toast({
        title: 'Error',
        description: 'Failed to add comment',
        variant: 'destructive',
      })
    }
  }

  const getSentimentEmoji = (sentiment: number | null) => {
    if (!sentiment) return '😐'
    if (sentiment > 0.5) return '😊'
    if (sentiment > 0) return '🙂'
    if (sentiment > -0.5) return '😐'
    return '😞'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (!ticket) {
    return (
      <div className="container mx-auto py-6">
        <p>Ticket not found</p>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-6 max-w-6xl">
      <Button variant="ghost" onClick={() => navigate('/tickets')} className="mb-4">
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back to Tickets
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Ticket Header */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-2xl">{ticket.title}</CardTitle>
                  <CardDescription className="mt-2">
                    From {ticket.customer_name || 'Unknown'} ({ticket.customer_email})
                  </CardDescription>
                </div>
                <Select value={ticket.status} onValueChange={handleStatusChange}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="open">Open</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="resolved">Resolved</SelectItem>
                    <SelectItem value="closed">Closed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm whitespace-pre-wrap">{ticket.description}</p>
              <div className="flex gap-2 mt-4">
                <Badge>{ticket.priority || 'No priority'}</Badge>
                <Badge variant="outline">{ticket.status}</Badge>
                {ticket.ai_category && (
                  <Badge variant="secondary">{ticket.ai_category}</Badge>
                )}
              </div>
            </CardContent>
          </Card>

          {/* AI Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                AI Insights
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Summary */}
              {ticket.ai_summary && (
                <div>
                  <h4 className="font-semibold text-sm mb-1">Summary</h4>
                  <p className="text-sm text-muted-foreground">{ticket.ai_summary}</p>
                </div>
              )}

              {/* Intent & Category */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold text-sm mb-1">Intent</h4>
                  <Badge variant="outline" className="capitalize">
                    {ticket.ai_intent?.replace('_', ' ') || 'Unknown'}
                  </Badge>
                </div>
                <div>
                  <h4 className="font-semibold text-sm mb-1">Sentiment</h4>
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{getSentimentEmoji(ticket.ai_sentiment)}</span>
                    <span className="text-sm text-muted-foreground">
                      {ticket.ai_sentiment?.toFixed(2) || 'N/A'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Entities */}
              {ticket.ai_entities && Object.keys(ticket.ai_entities).length > 0 && (
                <div>
                  <h4 className="font-semibold text-sm mb-2">Extracted Entities</h4>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(ticket.ai_entities).map(([key, value]) => (
                      <Badge key={key} variant="secondary">
                        {key}: {String(value)}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {/* Suggested Actions */}
              {ticket.ai_suggested_actions && ticket.ai_suggested_actions.length > 0 && (
                <div>
                  <h4 className="font-semibold text-sm mb-2">Suggested Actions</h4>
                  <div className="space-y-2">
                    {ticket.ai_suggested_actions.map((action, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        <TrendingUp className="h-4 w-4 mt-0.5 text-green-600" />
                        <div className="flex-1">
                          <div className="font-medium">{action.action}</div>
                          <div className="text-xs text-muted-foreground">{action.reason}</div>
                          <div className="text-xs text-muted-foreground">
                            Confidence: {(action.confidence * 100).toFixed(0)}%
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Comments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />
                Comments ({comments.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {comments.map((comment) => (
                <div key={comment.id} className="border-l-2 pl-4 py-2">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-sm">
                      {comment.author_name || 'Unknown'}
                    </span>
                    <Badge variant="outline" className="text-xs">
                      {comment.author_type}
                    </Badge>
                    {comment.is_internal && (
                      <Badge variant="secondary" className="text-xs">
                        Internal
                      </Badge>
                    )}
                    <span className="text-xs text-muted-foreground ml-auto">
                      {new Date(comment.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="text-sm whitespace-pre-wrap">{comment.content}</p>
                </div>
              ))}

              <Separator />

              <div className="space-y-2">
                <Textarea
                  placeholder="Add a comment..."
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  rows={3}
                />
                <div className="flex items-center gap-2">
                  <label className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={isInternal}
                      onChange={(e) => setIsInternal(e.target.checked)}
                    />
                    Internal note
                  </label>
                  <Button onClick={handleAddComment} className="ml-auto">
                    Add Comment
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div>
                <div className="text-muted-foreground">Created</div>
                <div>{new Date(ticket.created_at).toLocaleString()}</div>
              </div>
              <div>
                <div className="text-muted-foreground">Updated</div>
                <div>{new Date(ticket.updated_at).toLocaleString()}</div>
              </div>
              {ticket.resolved_at && (
                <div>
                  <div className="text-muted-foreground">Resolved</div>
                  <div>{new Date(ticket.resolved_at).toLocaleString()}</div>
                </div>
              )}
              <div>
                <div className="text-muted-foreground">Source</div>
                <Badge variant="outline" className="capitalize">
                  {ticket.source || 'manual'}
                </Badge>
              </div>
              {ticket.assigned_team && (
                <div>
                  <div className="text-muted-foreground">Team</div>
                  <div className="capitalize">{ticket.assigned_team}</div>
                </div>
              )}
            </CardContent>
          </Card>

          {ticket.tags && ticket.tags.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center gap-2">
                  <Tag className="h-4 w-4" />
                  Tags
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {ticket.tags.map((tag, idx) => (
                    <Badge key={idx} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
