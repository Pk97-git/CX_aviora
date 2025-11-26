-- Performance Optimization Indexes for Aivora
-- Run this on your Neon PostgreSQL database

-- Tickets table indexes
CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
CREATE INDEX IF NOT EXISTS idx_tickets_customer_id ON tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee);
CREATE INDEX IF NOT EXISTS idx_tickets_status_created ON tickets(status, created_at DESC);

-- AI Analysis table indexes
CREATE INDEX IF NOT EXISTS idx_ai_analysis_ticket_id ON ai_analysis(ticket_id);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_sentiment ON ai_analysis(sentiment);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_intent ON ai_analysis(intent);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_created_at ON ai_analysis(created_at DESC);

-- Composite index for common query pattern (status + created_at)
CREATE INDEX IF NOT EXISTS idx_tickets_status_priority_created 
ON tickets(status, priority, created_at DESC);

-- Analyze tables to update statistics
ANALYZE tickets;
ANALYZE ai_analysis;

-- Verify indexes were created
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
