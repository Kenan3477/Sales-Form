-- Migration: Add document generation status tracking

-- Add fields to track document generation status
ALTER TABLE "sales" ADD COLUMN "documentsGenerated" BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE "sales" ADD COLUMN "documentsGeneratedAt" TIMESTAMP(3) NULL;
ALTER TABLE "sales" ADD COLUMN "documentsGeneratedBy" TEXT NULL;

-- Add index for filtering sales by document status
CREATE INDEX "sales_documentsGenerated_idx" ON "sales"("documentsGenerated");

-- Add foreign key for documentsGeneratedBy
ALTER TABLE "sales" ADD CONSTRAINT "sales_documentsGeneratedBy_fkey" FOREIGN KEY ("documentsGeneratedBy") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;