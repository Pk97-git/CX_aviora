-- ============================================================================
-- FRESH DATABASE INITIALIZATION WITH REALISTIC COMPANY DATA
-- ============================================================================
-- This creates a production-like dataset with multiple companies, users, and tickets
-- Password for all users: password123

-- ============================================================================
-- STEP 1: DROP ALL EXISTING TABLES
-- ============================================================================

DROP TABLE IF EXISTS ticket_comments CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS integrations CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;
DROP TABLE IF EXISTS ai_analysis CASCADE;
DROP TABLE IF EXISTS sentiment_metrics CASCADE;
DROP TABLE IF EXISTS category_metrics CASCADE;
DROP TABLE IF EXISTS alerts CASCADE;
DROP TABLE IF EXISTS alert_rules CASCADE;
DROP TABLE IF EXISTS regional_data CASCADE;
DROP TABLE IF EXISTS churn_predictions CASCADE;
DROP TABLE IF EXISTS friction_costs CASCADE;
DROP TABLE IF EXISTS strategic_recommendations CASCADE;
DROP TABLE IF EXISTS workflows CASCADE;
DROP TABLE IF EXISTS workflow_steps CASCADE;
DROP TABLE IF EXISTS policies CASCADE;

-- ============================================================================
-- STEP 2: CREATE SCHEMA
-- ============================================================================

CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB DEFAULT '{}',
    plan VARCHAR(50) DEFAULT 'free',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    permissions JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tenant_id, email)
);

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    permissions JSONB DEFAULT '[]',
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    config JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    external_id VARCHAR(255),
    source VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(20),
    customer_email VARCHAR(255),
    customer_name VARCHAR(255),
    customer_id VARCHAR(255),
    assigned_to UUID REFERENCES users(id),
    assigned_team VARCHAR(100),
    ai_summary TEXT,
    ai_intent VARCHAR(100),
    ai_entities JSONB,
    ai_sentiment FLOAT,
    ai_priority VARCHAR(20),
    ai_suggested_actions JSONB,
    ai_category VARCHAR(100),
    tags JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    closed_at TIMESTAMP
);

CREATE TABLE ticket_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    author_type VARCHAR(20),
    author_id UUID REFERENCES users(id),
    author_name VARCHAR(255),
    author_email VARCHAR(255),
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create Indexes
CREATE INDEX idx_tenants_slug ON tenants(slug);
CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_api_keys_tenant ON api_keys(tenant_id);
CREATE INDEX idx_integrations_tenant ON integrations(tenant_id);
CREATE INDEX idx_tickets_tenant ON tickets(tenant_id);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_created ON tickets(created_at);
CREATE INDEX idx_comments_ticket ON ticket_comments(ticket_id);

-- ============================================================================
-- STEP 3: INSERT REALISTIC COMPANY DATA
-- ============================================================================

-- Company 1: TechStart Inc (SaaS Startup)
INSERT INTO tenants VALUES
('11111111-1111-1111-1111-111111111111', 'TechStart Inc', 'techstart', '{"timezone": "America/Los_Angeles", "business_hours": "9-5"}', 'pro', 'active', NOW() - INTERVAL '6 months', NOW());

INSERT INTO users (id, tenant_id, email, password_hash, full_name, role, last_login_at) VALUES
('11111111-1111-1111-1111-000000000001', '11111111-1111-1111-1111-111111111111', 'sarah.chen@techstart.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Sarah Chen', 'admin', NOW() - INTERVAL '2 hours'),
('11111111-1111-1111-1111-000000000002', '11111111-1111-1111-1111-111111111111', 'mike.rodriguez@techstart.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Mike Rodriguez', 'manager', NOW() - INTERVAL '1 day'),
('11111111-1111-1111-1111-000000000003', '11111111-1111-1111-1111-111111111111', 'emily.watson@techstart.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Emily Watson', 'agent', NOW() - INTERVAL '3 hours'),
('11111111-1111-1111-1111-000000000004', '11111111-1111-1111-1111-111111111111', 'james.kim@techstart.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'James Kim', 'agent', NOW() - INTERVAL '5 hours');

INSERT INTO integrations VALUES
('11111111-1111-1111-1111-222222222221', '11111111-1111-1111-1111-111111111111', 'freshdesk', 'Freshdesk Production', '{"domain": "techstart.freshdesk.com", "api_key": "***"}', 'active', NOW() - INTERVAL '1 hour', NOW(), NOW()),
('11111111-1111-1111-1111-222222222222', '11111111-1111-1111-1111-111111111111', 'slack', 'Slack #support', '{"bot_token": "xoxb-***", "channel": "#support"}', 'active', NULL, NOW(), NOW()),
('11111111-1111-1111-1111-222222222223', '11111111-1111-1111-1111-111111111111', 'jira', 'JIRA Engineering', '{"domain": "techstart.atlassian.net", "email": "***", "api_token": "***", "project_key": "SUP"}', 'active', NULL, NOW(), NOW());

-- TechStart Tickets
INSERT INTO tickets (id, tenant_id, external_id, source, title, description, status, priority, customer_email, customer_name, assigned_to, ai_summary, ai_intent, ai_entities, ai_sentiment, ai_priority, ai_suggested_actions, ai_category, tags, created_at, updated_at) VALUES
('11111111-1111-1111-1111-333333333301', '11111111-1111-1111-1111-111111111111', 'TS-1847', 'freshdesk',
'Cannot login to dashboard after password reset',
'I reset my password yesterday but now I can''t login. It says "Invalid credentials" even though I''m using the new password. This is blocking my work!',
'open', 'urgent', 'alex.morgan@acmecorp.com', 'Alex Morgan', '11111111-1111-1111-1111-000000000003',
'User unable to login after password reset, receiving invalid credentials error',
'account_access',
'{"issue_type": "login_failure", "action_taken": "password_reset"}',
-0.7, 'urgent',
'[{"action": "verify_password_reset", "confidence": 0.92, "reason": "Password reset may not have completed properly"}, {"action": "check_account_status", "confidence": 0.88, "reason": "Account might be locked"}, {"action": "provide_manual_reset", "confidence": 0.85, "reason": "Manual intervention may be needed"}]',
'account', '["login", "password", "urgent"]',
NOW() - INTERVAL '45 minutes', NOW() - INTERVAL '30 minutes'),

('11111111-1111-1111-1111-333333333302', '11111111-1111-1111-1111-111111111111', 'TS-1848', 'freshdesk',
'Billing discrepancy - charged twice for subscription',
'I was charged $299 twice on December 1st for my annual subscription. My credit card shows two separate charges. Order IDs: #ORD-45231 and #ORD-45232. Please refund the duplicate charge immediately.',
'pending', 'high', 'jennifer.liu@globaltech.com', 'Jennifer Liu', '11111111-1111-1111-1111-000000000002',
'Customer charged twice ($299 each) for annual subscription, requesting refund for duplicate charge',
'billing_issue',
'{"order_ids": ["ORD-45231", "ORD-45232"], "amount": 299, "charge_count": 2, "date": "2024-12-01"}',
-0.8, 'high',
'[{"action": "verify_duplicate_charge", "confidence": 0.95, "reason": "Clear evidence of double billing"}, {"action": "process_refund", "confidence": 0.93, "reason": "Immediate refund warranted"}, {"action": "investigate_billing_system", "confidence": 0.78, "reason": "Prevent future occurrences"}]',
'billing', '["refund", "billing", "urgent"]',
NOW() - INTERVAL '2 hours', NOW() - INTERVAL '1 hour'),

('11111111-1111-1111-1111-333333333303', '11111111-1111-1111-1111-111111111111', 'TS-1849', 'manual',
'Feature request: Export data to CSV',
'It would be really helpful if we could export our analytics data to CSV format. Currently we can only view it in the dashboard but can''t download it for our monthly reports.',
'open', 'low', 'david.park@innovate.co', 'David Park', NULL,
'Customer requests CSV export functionality for analytics data to use in monthly reports',
'feature_request',
'{"feature": "csv_export", "data_type": "analytics"}',
0.4, 'low',
'[{"action": "add_to_product_roadmap", "confidence": 0.85, "reason": "Common and reasonable feature request"}, {"action": "assess_technical_feasibility", "confidence": 0.75, "reason": "Evaluate implementation effort"}, {"action": "gather_similar_requests", "confidence": 0.70, "reason": "Check if other customers want this"}]',
'product', '["feature", "export", "analytics"]',
NOW() - INTERVAL '5 hours', NOW() - INTERVAL '5 hours'),

('11111111-1111-1111-1111-333333333304', '11111111-1111-1111-1111-111111111111', 'TS-1850', 'freshdesk',
'Mobile app crashes when uploading large files',
'The iOS app crashes every time I try to upload a file larger than 10MB. I''m on iPhone 14 Pro with iOS 17.2. Smaller files work fine. This is a critical issue for our team.',
'open', 'high', 'rachel.green@designstudio.com', 'Rachel Green', '11111111-1111-1111-1111-000000000004',
'iOS app crashes when uploading files >10MB on iPhone 14 Pro, iOS 17.2',
'bug_report',
'{"platform": "iOS", "device": "iPhone 14 Pro", "os_version": "17.2", "file_size_limit": "10MB", "issue": "app_crash"}',
-0.5, 'high',
'[{"action": "escalate_to_engineering", "confidence": 0.94, "reason": "Technical bug requiring developer attention"}, {"action": "reproduce_issue", "confidence": 0.88, "reason": "Verify the bug in testing environment"}, {"action": "provide_workaround", "confidence": 0.72, "reason": "Suggest using web version temporarily"}]',
'technical', '["bug", "mobile", "ios", "crash"]',
NOW() - INTERVAL '3 hours', NOW() - INTERVAL '2 hours'),

('11111111-1111-1111-1111-333333333305', '11111111-1111-1111-1111-111111111111', 'TS-1851', 'freshdesk',
'Thank you for the excellent support!',
'I just wanted to say thank you to Emily for helping me resolve my integration issue yesterday. She was patient, knowledgeable, and went above and beyond. Great service!',
'resolved', 'low', 'thomas.anderson@matrix.io', 'Thomas Anderson', '11111111-1111-1111-1111-000000000003',
'Customer expressing gratitude for excellent support from Emily regarding integration issue',
'positive_feedback',
'{"agent_mentioned": "Emily", "issue_resolved": "integration"}',
0.95, 'low',
'[{"action": "share_with_team", "confidence": 0.98, "reason": "Positive feedback boosts team morale"}, {"action": "recognize_agent", "confidence": 0.92, "reason": "Acknowledge Emily''s excellent work"}, {"action": "close_ticket", "confidence": 0.90, "reason": "No further action needed"}]',
'feedback', '["positive", "kudos"]',
NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day');

-- Company 2: RetailPro Solutions (E-commerce Platform)
INSERT INTO tenants VALUES
('22222222-2222-2222-2222-222222222222', 'RetailPro Solutions', 'retailpro', '{"timezone": "America/New_York", "business_hours": "8-6"}', 'enterprise', 'active', NOW() - INTERVAL '1 year', NOW());

INSERT INTO users (id, tenant_id, email, password_hash, full_name, role, last_login_at) VALUES
('22222222-2222-2222-2222-000000000001', '22222222-2222-2222-2222-222222222222', 'admin@retailpro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Amanda Foster', 'admin', NOW() - INTERVAL '1 hour'),
('22222222-2222-2222-2222-000000000002', '22222222-2222-2222-2222-222222222222', 'carlos.martinez@retailpro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Carlos Martinez', 'manager', NOW() - INTERVAL '4 hours'),
('22222222-2222-2222-2222-000000000003', '22222222-2222-2222-2222-222222222222', 'lisa.thompson@retailpro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Lisa Thompson', 'agent', NOW() - INTERVAL '2 hours'),
('22222222-2222-2222-2222-000000000004', '22222222-2222-2222-2222-222222222222', 'kevin.nguyen@retailpro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Kevin Nguyen', 'agent', NOW() - INTERVAL '6 hours');

INSERT INTO integrations VALUES
('22222222-2222-2222-2222-333333333331', '22222222-2222-2222-2222-222222222222', 'zendesk', 'Zendesk Support', '{"domain": "retailpro.zendesk.com", "api_token": "***"}', 'active', NOW() - INTERVAL '30 minutes', NOW(), NOW()),
('22222222-2222-2222-2222-333333333332', '22222222-2222-2222-2222-222222222222', 'slack', 'Slack #customer-support', '{"bot_token": "xoxb-***", "channel": "#customer-support"}', 'active', NULL, NOW(), NOW());

-- RetailPro Tickets
INSERT INTO tickets (id, tenant_id, external_id, source, title, description, status, priority, customer_email, customer_name, assigned_to, ai_summary, ai_intent, ai_entities, ai_sentiment, ai_priority, ai_suggested_actions, ai_category, tags, created_at, updated_at, resolved_at) VALUES
('22222222-2222-2222-2222-444444444401', '22222222-2222-2222-2222-222222222222', 'ZD-8472', 'zendesk',
'Order #78945 never arrived - need refund',
'I ordered a laptop (SKU: LAP-X1-256) on November 28th for $1,299.99. Order #78945. Tracking shows it was delivered on Dec 1st but I never received it. My neighbor didn''t get it either. I need a full refund or replacement ASAP.',
'pending', 'urgent', 'michael.brown@email.com', 'Michael Brown', '22222222-2222-2222-2222-000000000003',
'Customer reports undelivered laptop order #78945 ($1,299.99), tracking shows delivered but not received',
'shipping_issue',
'{"order_id": "78945", "sku": "LAP-X1-256", "amount": 1299.99, "tracking_status": "delivered", "order_date": "2024-11-28"}',
-0.75, 'urgent',
'[{"action": "investigate_delivery", "confidence": 0.90, "reason": "Verify delivery with carrier"}, {"action": "process_refund_or_replacement", "confidence": 0.88, "reason": "Customer entitled to resolution"}, {"action": "file_carrier_claim", "confidence": 0.82, "reason": "Potential carrier liability"}]',
'shipping', '["refund", "shipping", "lost_package"]',
NOW() - INTERVAL '4 hours', NOW() - INTERVAL '1 hour', NULL),

('22222222-2222-2222-2222-444444444402', '22222222-2222-2222-2222-222222222222', 'ZD-8473', 'zendesk',
'Wrong item received - ordered blue, got red',
'I ordered a blue wireless mouse (SKU: MOU-BLU-001) but received a red one instead. Order #78950. I need the correct blue mouse. Can I return this without paying shipping?',
'open', 'medium', 'sophia.williams@company.com', 'Sophia Williams', '22222222-2222-2222-2222-000000000004',
'Customer received wrong color mouse (red instead of blue), requesting exchange with free return shipping',
'wrong_item',
'{"order_id": "78950", "sku_ordered": "MOU-BLU-001", "sku_received": "MOU-RED-001"}',
-0.3, 'medium',
'[{"action": "send_replacement", "confidence": 0.92, "reason": "Clear fulfillment error"}, {"action": "provide_return_label", "confidence": 0.90, "reason": "Free return for our mistake"}, {"action": "expedite_shipping", "confidence": 0.75, "reason": "Compensate for inconvenience"}]',
'fulfillment', '["wrong_item", "exchange"]',
NOW() - INTERVAL '6 hours', NOW() - INTERVAL '6 hours', NULL),

('22222222-2222-2222-2222-444444444403', '22222222-2222-2222-2222-222222222222', 'ZD-8474', 'manual',
'Product arrived damaged - screen cracked',
'The tablet I received (Order #78955) has a cracked screen. The box was damaged when it arrived. I took photos. This is unacceptable for a $599 product. I want a replacement or full refund including shipping.',
'open', 'high', 'daniel.lee@business.net', 'Daniel Lee', '22222222-2222-2222-2222-000000000002',
'Customer received damaged tablet with cracked screen, box also damaged, requesting replacement or refund',
'damaged_product',
'{"order_id": "78955", "product": "tablet", "amount": 599, "damage_type": "cracked_screen"}',
-0.85, 'high',
'[{"action": "approve_return_refund", "confidence": 0.95, "reason": "Clear damage during shipping"}, {"action": "file_carrier_claim", "confidence": 0.88, "reason": "Carrier responsible for damage"}, {"action": "offer_discount_on_replacement", "confidence": 0.70, "reason": "Retain customer goodwill"}]',
'quality', '["damaged", "refund", "replacement"]',
NOW() - INTERVAL '2 hours', NOW() - INTERVAL '2 hours', NULL),

('22222222-2222-2222-2222-444444444404', '22222222-2222-2222-2222-222222222222', 'ZD-8475', 'zendesk',
'How do I track my order?',
'Hi, I placed order #78960 yesterday and got a confirmation email but no tracking number yet. When will I get tracking info? Thanks!',
'resolved', 'low', 'emma.davis@mail.com', 'Emma Davis', '22222222-2222-2222-2222-000000000003',
'Customer inquiring about tracking information for order #78960 placed yesterday',
'order_status',
'{"order_id": "78960", "inquiry_type": "tracking"}',
0.1, 'low',
'[{"action": "provide_tracking_info", "confidence": 0.92, "reason": "Standard information request"}, {"action": "explain_shipping_timeline", "confidence": 0.85, "reason": "Set expectations"}, {"action": "close_ticket", "confidence": 0.80, "reason": "Simple inquiry resolved"}]',
'support', '["tracking", "order_status"]',
NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day');

-- Company 3: CloudBase (Cloud Infrastructure Provider)
INSERT INTO tenants VALUES
('33333333-3333-3333-3333-333333333333', 'CloudBase', 'cloudbase', '{"timezone": "Europe/London", "business_hours": "9-5"}', 'enterprise', 'active', NOW() - INTERVAL '2 years', NOW());

INSERT INTO users (id, tenant_id, email, password_hash, full_name, role, last_login_at) VALUES
('33333333-3333-3333-3333-000000000001', '33333333-3333-3333-3333-333333333333', 'admin@cloudbase.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Oliver Smith', 'admin', NOW() - INTERVAL '30 minutes'),
('33333333-3333-3333-3333-000000000002', '33333333-3333-3333-3333-333333333333', 'priya.patel@cloudbase.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Priya Patel', 'manager', NOW() - INTERVAL '2 hours'),
('33333333-3333-3333-3333-000000000003', '33333333-3333-3333-3333-333333333333', 'hans.mueller@cloudbase.io', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQu6', 'Hans Mueller', 'agent', NOW() - INTERVAL '1 hour');

INSERT INTO integrations VALUES
('33333333-3333-3333-3333-444444444441', '33333333-3333-3333-3333-333333333333', 'freshdesk', 'Freshdesk Enterprise', '{"domain": "cloudbase.freshdesk.com", "api_key": "***"}', 'active', NOW() - INTERVAL '15 minutes', NOW(), NOW()),
('33333333-3333-3333-3333-444444444442', '33333333-3333-3333-3333-333333333333', 'jira', 'JIRA Cloud', '{"domain": "cloudbase.atlassian.net", "email": "***", "api_token": "***", "project_key": "CLOUD"}', 'active', NULL, NOW(), NOW());

-- CloudBase Tickets
INSERT INTO tickets (id, tenant_id, external_id, source, title, description, status, priority, customer_email, customer_name, assigned_to, ai_summary, ai_intent, ai_entities, ai_sentiment, ai_priority, ai_suggested_actions, ai_category, tags, created_at, updated_at) VALUES
('33333333-3333-3333-3333-555555555501', '33333333-3333-3333-3333-333333333333', 'CB-2891', 'freshdesk',
'API rate limit too restrictive for production use',
'Our application is hitting the API rate limit of 1000 requests/hour during peak times. We''re on the Enterprise plan and need this increased to at least 5000/hour. This is impacting our production service. Account ID: ENT-4729',
'open', 'urgent', 'tech@startup.com', 'Tech Team - StartupCo', '33333333-3333-3333-3333-000000000002',
'Enterprise customer hitting API rate limit (1000/hr), requesting increase to 5000/hr for production needs',
'api_limit',
'{"account_id": "ENT-4729", "current_limit": 1000, "requested_limit": 5000, "plan": "Enterprise"}',
-0.6, 'urgent',
'[{"action": "increase_rate_limit", "confidence": 0.93, "reason": "Enterprise customer with valid need"}, {"action": "review_usage_patterns", "confidence": 0.85, "reason": "Ensure appropriate usage"}, {"action": "escalate_to_engineering", "confidence": 0.78, "reason": "May need infrastructure review"}]',
'technical', '["api", "rate_limit", "enterprise"]',
NOW() - INTERVAL '3 hours', NOW() - INTERVAL '2 hours'),

('33333333-3333-3333-3333-555555555502', '33333333-3333-3333-3333-333333333333', 'CB-2892', 'manual',
'Documentation outdated for v3 API',
'The documentation for the v3 API still shows examples from v2. Specifically, the authentication section is completely wrong. This wasted 4 hours of our dev time. Please update it urgently.',
'open', 'medium', 'dev@techcorp.io', 'Development Team', '33333333-3333-3333-3333-000000000003',
'Customer reports outdated v3 API documentation showing v2 examples, particularly authentication section',
'documentation_issue',
'{"api_version": "v3", "section": "authentication", "time_wasted": "4 hours"}',
-0.5, 'medium',
'[{"action": "update_documentation", "confidence": 0.95, "reason": "Clear documentation error"}, {"action": "notify_docs_team", "confidence": 0.90, "reason": "Prevent future issues"}, {"action": "apologize_for_inconvenience", "confidence": 0.85, "reason": "Acknowledge customer frustration"}]',
'documentation', '["docs", "api", "v3"]',
NOW() - INTERVAL '5 hours', NOW() - INTERVAL '5 hours');

-- Add Comments to Various Tickets
INSERT INTO ticket_comments (tenant_id, ticket_id, author_type, author_id, author_name, content, is_internal, created_at) VALUES
-- TechStart comments
('11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-333333333301', 'user', '11111111-1111-1111-1111-000000000003', 'Emily Watson', 'Hi Alex, I''ve reset your password manually and sent you a temporary password via email. Please try logging in with that and then change it to your preferred password.', false, NOW() - INTERVAL '25 minutes'),
('11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-333333333301', 'user', '11111111-1111-1111-1111-000000000003', 'Emily Watson', 'Internal note: Account was locked due to 5 failed login attempts. Reset lock and password.', true, NOW() - INTERVAL '26 minutes'),
('11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-333333333302', 'user', '11111111-1111-1111-1111-000000000002', 'Mike Rodriguez', 'Hi Jennifer, I''ve verified the duplicate charge and initiated a refund for $299. You should see it in 3-5 business days. I''ve also added a credit to your account as an apology for the inconvenience.', false, NOW() - INTERVAL '50 minutes'),

-- RetailPro comments
('22222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-444444444401', 'user', '22222222-2222-2222-2222-000000000003', 'Lisa Thompson', 'Hi Michael, I''m so sorry about this! I''ve contacted the carrier and they''re investigating. In the meantime, I''m processing a full refund of $1,299.99 which you''ll receive within 3-5 business days.', false, NOW() - INTERVAL '45 minutes'),
('22222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-444444444402', 'user', '22222222-2222-2222-2222-000000000004', 'Kevin Nguyen', 'Hi Sophia! I''ve shipped the correct blue mouse via expedited shipping - you should receive it tomorrow. I''ve also emailed you a prepaid return label for the red mouse. No rush on returning it!', false, NOW() - INTERVAL '5 hours'),

-- CloudBase comments
('33333333-3333-3333-3333-333333333333', '33333333-3333-3333-3333-555555555501', 'user', '33333333-3333-3333-3333-000000000002', 'Priya Patel', 'Hi there, I''ve escalated your request to our infrastructure team. Given your Enterprise plan and production needs, we should be able to increase your limit to 5000/hour. I''ll update you within 2 hours.', false, NOW() - INTERVAL '1 hour'),
('33333333-3333-3333-3333-333333333333', '33333333-3333-3333-3333-555555555502', 'user', '33333333-3333-3333-3333-000000000003', 'Hans Mueller', 'Thank you for reporting this! I''ve notified our documentation team and they''re updating the v3 API docs right now. The corrected version should be live within the hour. Sorry for the confusion!', false, NOW() - INTERVAL '4 hours');

-- Verification
SELECT 'Database Initialized Successfully!' as status;
SELECT 'Tenants' as table_name, COUNT(*) as count FROM tenants
UNION ALL SELECT 'Users', COUNT(*) FROM users
UNION ALL SELECT 'Integrations', COUNT(*) FROM integrations
UNION ALL SELECT 'Tickets', COUNT(*) FROM tickets
UNION ALL SELECT 'Comments', COUNT(*) FROM ticket_comments;
