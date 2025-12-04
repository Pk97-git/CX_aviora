-- Tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    
    -- Source Information
    external_id VARCHAR(255),
    source VARCHAR(50) NOT NULL,
    
    -- Basic Fields
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(20),
    
    -- Customer Information
    customer_email VARCHAR(255),
    customer_name VARCHAR(255),
    customer_id VARCHAR(255),
    
    -- Assignment
    assigned_to UUID REFERENCES users(id),
    assigned_team VARCHAR(100),
    
    -- AI-Generated Fields
    ai_summary TEXT,
    ai_intent VARCHAR(100),
    ai_entities JSONB,
    ai_sentiment FLOAT,
    ai_priority VARCHAR(20),
    ai_suggested_actions JSONB,
    ai_category VARCHAR(100),
    
    -- Metadata
    tags JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    closed_at TIMESTAMP,
    
    UNIQUE(tenant_id, source, external_id)
);

CREATE INDEX idx_tickets_tenant_status ON tickets(tenant_id, status);
CREATE INDEX idx_tickets_assigned ON tickets(assigned_to);
CREATE INDEX idx_tickets_created ON tickets(created_at DESC);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_category ON tickets(ai_category);

-- Ticket Comments table
CREATE TABLE IF NOT EXISTS ticket_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    
    -- Author Information
    author_type VARCHAR(20),
    author_id UUID REFERENCES users(id),
    author_name VARCHAR(255),
    author_email VARCHAR(255),
    
    -- Content
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_comments_ticket ON ticket_comments(ticket_id);
CREATE INDEX idx_comments_created ON ticket_comments(created_at DESC);
