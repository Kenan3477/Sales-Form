-- Add EmailLog table to track email communications
-- This table will store all email communications with customers

-- First, let's add the EmailLog table
CREATE TABLE IF NOT EXISTS "EmailLog" (
    "id" TEXT NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    "saleId" TEXT,
    "leadId" TEXT,
    "recipientEmail" TEXT NOT NULL,
    "recipientName" TEXT,
    "senderEmail" TEXT NOT NULL DEFAULT 'system@salesportal.com',
    "subject" TEXT NOT NULL,
    "messageContent" TEXT NOT NULL,
    "emailStatus" TEXT NOT NULL DEFAULT 'NOT_SENT', -- NOT_SENT, SENDING, SENT, FAILED, BOUNCED, OPENED, CLICKED
    "emailSentAt" TIMESTAMP,
    "emailProviderMessageId" TEXT,
    "emailError" TEXT,
    "emailExternalReference" TEXT UNIQUE,
    "isTemplateEmail" BOOLEAN DEFAULT false,
    "templateType" TEXT, -- welcome_letter, policy_document, reminder, etc.
    "metadata" JSONB, -- Store additional email tracking data
    "createdAt" TIMESTAMP NOT NULL DEFAULT now(),
    "updatedAt" TIMESTAMP NOT NULL DEFAULT now(),
    
    -- Foreign key constraints
    CONSTRAINT "EmailLog_saleId_fkey" FOREIGN KEY ("saleId") REFERENCES "sales"("id") ON DELETE CASCADE,
    CONSTRAINT "EmailLog_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES "Lead"("id") ON DELETE CASCADE
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS "EmailLog_saleId_idx" ON "EmailLog"("saleId");
CREATE INDEX IF NOT EXISTS "EmailLog_leadId_idx" ON "EmailLog"("leadId");
CREATE INDEX IF NOT EXISTS "EmailLog_recipientEmail_idx" ON "EmailLog"("recipientEmail");
CREATE INDEX IF NOT EXISTS "EmailLog_emailStatus_idx" ON "EmailLog"("emailStatus");
CREATE INDEX IF NOT EXISTS "EmailLog_createdAt_idx" ON "EmailLog"("createdAt");
CREATE INDEX IF NOT EXISTS "EmailLog_emailSentAt_idx" ON "EmailLog"("emailSentAt");

-- Add CommunicationLog table for general communications tracking
CREATE TABLE IF NOT EXISTS "CommunicationLog" (
    "id" TEXT NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    "saleId" TEXT,
    "leadId" TEXT,
    "communicationType" TEXT NOT NULL, -- 'email', 'sms', 'call', 'letter', 'meeting'
    "direction" TEXT NOT NULL DEFAULT 'outbound', -- 'inbound', 'outbound'
    "subject" TEXT,
    "content" TEXT,
    "recipient" TEXT,
    "sender" TEXT,
    "status" TEXT NOT NULL DEFAULT 'completed', -- 'scheduled', 'completed', 'failed', 'cancelled'
    "scheduledAt" TIMESTAMP,
    "completedAt" TIMESTAMP,
    "agentId" TEXT,
    "metadata" JSONB, -- Store additional communication data
    "createdAt" TIMESTAMP NOT NULL DEFAULT now(),
    "updatedAt" TIMESTAMP NOT NULL DEFAULT now(),
    
    -- Foreign key constraints
    CONSTRAINT "CommunicationLog_saleId_fkey" FOREIGN KEY ("saleId") REFERENCES "sales"("id") ON DELETE CASCADE,
    CONSTRAINT "CommunicationLog_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES "Lead"("id") ON DELETE CASCADE,
    CONSTRAINT "CommunicationLog_agentId_fkey" FOREIGN KEY ("agentId") REFERENCES "users"("id") ON DELETE SET NULL
);

-- Add indexes for CommunicationLog
CREATE INDEX IF NOT EXISTS "CommunicationLog_saleId_idx" ON "CommunicationLog"("saleId");
CREATE INDEX IF NOT EXISTS "CommunicationLog_leadId_idx" ON "CommunicationLog"("leadId");
CREATE INDEX IF NOT EXISTS "CommunicationLog_communicationType_idx" ON "CommunicationLog"("communicationType");
CREATE INDEX IF NOT EXISTS "CommunicationLog_status_idx" ON "CommunicationLog"("status");
CREATE INDEX IF NOT EXISTS "CommunicationLog_createdAt_idx" ON "CommunicationLog"("createdAt");
CREATE INDEX IF NOT EXISTS "CommunicationLog_agentId_idx" ON "CommunicationLog"("agentId");

-- Create a view for communication summary
CREATE OR REPLACE VIEW "CommunicationSummaryView" AS
SELECT 
    COALESCE(s.id, l.id) as customer_id,
    COALESCE(s."customerFirstName", l."customerFirstName") as first_name,
    COALESCE(s."customerLastName", l."customerLastName") as last_name,
    COALESCE(s.email, l.email) as email,
    COALESCE(s."phoneNumber", l."phoneNumber") as phone,
    
    -- Email statistics
    COUNT(CASE WHEN el.id IS NOT NULL THEN 1 END) as total_emails,
    COUNT(CASE WHEN el."emailStatus" = 'SENT' THEN 1 END) as emails_sent,
    COUNT(CASE WHEN el."emailStatus" = 'OPENED' THEN 1 END) as emails_opened,
    COUNT(CASE WHEN el."emailStatus" = 'FAILED' THEN 1 END) as emails_failed,
    
    -- SMS statistics (from existing SMS table)
    COUNT(CASE WHEN sms.id IS NOT NULL THEN 1 END) as total_sms,
    COUNT(CASE WHEN sms."smsStatus" = 'SENT' THEN 1 END) as sms_sent,
    COUNT(CASE WHEN sms."smsStatus" = 'FAILED' THEN 1 END) as sms_failed,
    
    -- General communication statistics
    COUNT(CASE WHEN cl.id IS NOT NULL THEN 1 END) as total_communications,
    COUNT(CASE WHEN cl."communicationType" = 'call' THEN 1 END) as total_calls,
    
    -- Last contact dates
    MAX(el."emailSentAt") as last_email_sent,
    MAX(sms."smsSentAt") as last_sms_sent,
    MAX(cl."completedAt") as last_communication
    
FROM "sales" s
FULL OUTER JOIN "Lead" l ON false -- This creates a UNION-like effect
LEFT JOIN "EmailLog" el ON (el."saleId" = s.id OR el."leadId" = l.id)
LEFT JOIN "sms_logs" sms ON sms."saleId" = s.id
LEFT JOIN "CommunicationLog" cl ON (cl."saleId" = s.id OR cl."leadId" = l.id)
GROUP BY 
    COALESCE(s.id, l.id),
    COALESCE(s."customerFirstName", l."customerFirstName"),
    COALESCE(s."customerLastName", l."customerLastName"),
    COALESCE(s.email, l.email),
    COALESCE(s."phoneNumber", l."phoneNumber");

-- Add comments for documentation
COMMENT ON TABLE "EmailLog" IS 'Tracks all email communications with customers and leads';
COMMENT ON TABLE "CommunicationLog" IS 'Tracks all types of communications (email, SMS, calls, etc.) with customers and leads';
COMMENT ON VIEW "CommunicationSummaryView" IS 'Provides a summary of all communication activities per customer/lead';

-- Add trigger to automatically update updatedAt timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW."updatedAt" = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
DROP TRIGGER IF EXISTS update_emaillog_updated_at ON "EmailLog";
CREATE TRIGGER update_emaillog_updated_at 
    BEFORE UPDATE ON "EmailLog" 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_communicationlog_updated_at ON "CommunicationLog";
CREATE TRIGGER update_communicationlog_updated_at 
    BEFORE UPDATE ON "CommunicationLog" 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();