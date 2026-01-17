-- Paperwork Module Database Schema (Additive Only)
-- These new models extend the existing system without modifying it

-- Document Templates
CREATE TABLE document_templates (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL, -- 'WELCOME_LETTER', 'SERVICE_AGREEMENT', 'DIRECT_DEBIT', 'RENEWAL'
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    html_template TEXT NOT NULL,
    css_template TEXT,
    variables JSONB, -- Available template variables
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by TEXT REFERENCES users(id),
    
    UNIQUE(name, version)
);

-- Generated Documents
CREATE TABLE generated_documents (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid(),
    sale_id TEXT NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    template_id TEXT NOT NULL REFERENCES document_templates(id),
    template_version INTEGER NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DRAFT', -- 'DRAFT', 'FINAL'
    delivery_method VARCHAR(50), -- 'DOWNLOAD', 'EMAIL', 'POST'
    
    -- Document content
    rendered_html TEXT NOT NULL,
    pdf_file_path TEXT, -- Path to stored PDF file
    
    -- Metadata
    generated_by TEXT NOT NULL REFERENCES users(id),
    generated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    file_size INTEGER,
    page_count INTEGER,
    
    -- Audit fields
    variables_used JSONB, -- Snapshot of variables used in generation
    customer_data JSONB, -- Snapshot of customer data at time of generation
    
    UNIQUE(sale_id, template_id, template_version, generated_at)
);

-- Document Generation Log (Audit Trail)
CREATE TABLE document_generation_log (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id TEXT REFERENCES generated_documents(id) ON DELETE CASCADE,
    sale_id TEXT NOT NULL REFERENCES sales(id),
    action VARCHAR(100) NOT NULL, -- 'GENERATED', 'DOWNLOADED', 'EMAILED', 'REGENERATED'
    user_id TEXT NOT NULL REFERENCES users(id),
    user_ip TEXT,
    user_agent TEXT,
    metadata JSONB, -- Additional context
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_generated_documents_sale_id ON generated_documents(sale_id);
CREATE INDEX idx_generated_documents_status ON generated_documents(status);
CREATE INDEX idx_generated_documents_type ON generated_documents(document_type);
CREATE INDEX idx_document_log_sale_id ON document_generation_log(sale_id);
CREATE INDEX idx_document_log_action ON document_generation_log(action);
CREATE INDEX idx_document_templates_category ON document_templates(category);
CREATE INDEX idx_document_templates_active ON document_templates(is_active);