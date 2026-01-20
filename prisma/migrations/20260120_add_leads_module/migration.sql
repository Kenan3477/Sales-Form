-- CreateEnum for Lead Status
CREATE TYPE "LeadStatus" AS ENUM (
  'NEW',
  'CALLED_NO_ANSWER', 
  'CALLBACK',
  'SALE_MADE',
  'CANCELLED',
  'DO_NOT_CALL',
  'CONVERSION_FAILED'
);

-- LeadImportBatch table
CREATE TABLE "LeadImportBatch" (
    "id" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "imported_by" TEXT NOT NULL,
    "imported_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "total_rows" INTEGER NOT NULL DEFAULT 0,
    "successful_rows" INTEGER NOT NULL DEFAULT 0,
    "failed_rows" INTEGER NOT NULL DEFAULT 0,
    "error_report_location" TEXT,
    "metadata" JSONB,

    CONSTRAINT "LeadImportBatch_pkey" PRIMARY KEY ("id")
);

-- Lead table (mirrors sales form structure)
CREATE TABLE "Lead" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "created_by" TEXT NOT NULL,
    "assigned_agent_id" TEXT,
    "source" TEXT NOT NULL DEFAULT 'manual',
    "import_batch_id" TEXT,
    
    -- Customer fields (mirror Sale model)
    "customer_first_name" TEXT NOT NULL,
    "customer_last_name" TEXT NOT NULL,
    "title" TEXT,
    "phone_number" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "mailing_street" TEXT,
    "mailing_city" TEXT,
    "mailing_province" TEXT,
    "mailing_postal_code" TEXT,
    "notes" TEXT,
    
    -- Plan fields (mirror Sale model)
    "appliance_cover_selected" BOOLEAN NOT NULL DEFAULT false,
    "boiler_cover_selected" BOOLEAN NOT NULL DEFAULT false,
    "boiler_price_selected" DECIMAL(65,30),
    "total_plan_cost" DECIMAL(65,30) NOT NULL,
    
    -- Lead-specific state fields
    "current_status" "LeadStatus" NOT NULL DEFAULT 'NEW',
    "last_disposition_at" TIMESTAMP(3),
    "last_disposition_by" TEXT,
    "do_not_call" BOOLEAN NOT NULL DEFAULT false,
    "callback_at" TIMESTAMP(3),
    "times_contacted" INTEGER NOT NULL DEFAULT 0,
    "last_contact_attempt_at" TIMESTAMP(3),
    
    -- Concurrency control
    "checked_out_by" TEXT,
    "checked_out_at" TIMESTAMP(3),

    CONSTRAINT "Lead_pkey" PRIMARY KEY ("id")
);

-- LeadAppliance table (mirror Appliance model)
CREATE TABLE "LeadAppliance" (
    "id" TEXT NOT NULL,
    "lead_id" TEXT NOT NULL,
    "appliance_type" TEXT NOT NULL,
    "brand" TEXT,
    "model" TEXT,
    "age" INTEGER,
    "price" DECIMAL(65,30) NOT NULL,

    CONSTRAINT "LeadAppliance_pkey" PRIMARY KEY ("id")
);

-- LeadDispositionHistory table (audit trail)
CREATE TABLE "LeadDispositionHistory" (
    "id" TEXT NOT NULL,
    "lead_id" TEXT NOT NULL,
    "agent_id" TEXT NOT NULL,
    "status" "LeadStatus" NOT NULL,
    "notes" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "metadata" JSONB,

    CONSTRAINT "LeadDispositionHistory_pkey" PRIMARY KEY ("id")
);

-- LeadToSaleLink table (conversion tracking)
CREATE TABLE "LeadToSaleLink" (
    "id" TEXT NOT NULL,
    "lead_id" TEXT NOT NULL,
    "sale_id" TEXT NOT NULL,
    "converted_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "converted_by" TEXT NOT NULL,

    CONSTRAINT "LeadToSaleLink_pkey" PRIMARY KEY ("id")
);

-- Add Foreign Keys
ALTER TABLE "LeadImportBatch" ADD CONSTRAINT "LeadImportBatch_imported_by_fkey" FOREIGN KEY ("imported_by") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE "Lead" ADD CONSTRAINT "Lead_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "Lead" ADD CONSTRAINT "Lead_assigned_agent_id_fkey" FOREIGN KEY ("assigned_agent_id") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "Lead" ADD CONSTRAINT "Lead_last_disposition_by_fkey" FOREIGN KEY ("last_disposition_by") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "Lead" ADD CONSTRAINT "Lead_checked_out_by_fkey" FOREIGN KEY ("checked_out_by") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE "Lead" ADD CONSTRAINT "Lead_import_batch_id_fkey" FOREIGN KEY ("import_batch_id") REFERENCES "LeadImportBatch"("id") ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE "LeadAppliance" ADD CONSTRAINT "LeadAppliance_lead_id_fkey" FOREIGN KEY ("lead_id") REFERENCES "Lead"("id") ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "LeadDispositionHistory" ADD CONSTRAINT "LeadDispositionHistory_lead_id_fkey" FOREIGN KEY ("lead_id") REFERENCES "Lead"("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "LeadDispositionHistory" ADD CONSTRAINT "LeadDispositionHistory_agent_id_fkey" FOREIGN KEY ("agent_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE "LeadToSaleLink" ADD CONSTRAINT "LeadToSaleLink_lead_id_fkey" FOREIGN KEY ("lead_id") REFERENCES "Lead"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "LeadToSaleLink" ADD CONSTRAINT "LeadToSaleLink_sale_id_fkey" FOREIGN KEY ("sale_id") REFERENCES "Sale"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "LeadToSaleLink" ADD CONSTRAINT "LeadToSaleLink_converted_by_fkey" FOREIGN KEY ("converted_by") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- Add Indexes for Performance
CREATE INDEX "Lead_assigned_agent_id_current_status_idx" ON "Lead"("assigned_agent_id", "current_status");
CREATE INDEX "Lead_callback_at_idx" ON "Lead"("callback_at") WHERE "callback_at" IS NOT NULL;
CREATE INDEX "Lead_created_at_idx" ON "Lead"("created_at");
CREATE INDEX "Lead_checked_out_at_idx" ON "Lead"("checked_out_at") WHERE "checked_out_at" IS NOT NULL;
CREATE INDEX "LeadDispositionHistory_lead_id_created_at_idx" ON "LeadDispositionHistory"("lead_id", "created_at");
CREATE INDEX "LeadAppliance_lead_id_idx" ON "LeadAppliance"("lead_id");

-- Add Unique Constraints
CREATE UNIQUE INDEX "LeadToSaleLink_lead_id_key" ON "LeadToSaleLink"("lead_id");
CREATE UNIQUE INDEX "LeadToSaleLink_sale_id_key" ON "LeadToSaleLink"("sale_id");