-- CreateEnum
CREATE TYPE "SMSStatus" AS ENUM ('NOT_SENT', 'SENDING', 'SENT', 'FAILED', 'SKIPPED');

-- CreateTable
CREATE TABLE "sms_logs" (
    "id" TEXT NOT NULL,
    "sale_id" TEXT NOT NULL,
    "phone_number" TEXT NOT NULL,
    "normalized_phone" TEXT,
    "message_content" TEXT NOT NULL,
    "sms_status" "SMSStatus" NOT NULL DEFAULT 'NOT_SENT',
    "sms_sent_at" TIMESTAMP(3),
    "sms_provider_message_id" TEXT,
    "sms_error" TEXT,
    "sms_external_reference" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "sms_logs_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "sms_logs_sms_external_reference_key" ON "sms_logs"("sms_external_reference");

-- CreateIndex
CREATE INDEX "sms_logs_sale_id_idx" ON "sms_logs"("sale_id");

-- CreateIndex
CREATE INDEX "sms_logs_sms_status_idx" ON "sms_logs"("sms_status");

-- AddForeignKey
ALTER TABLE "sms_logs" ADD CONSTRAINT "sms_logs_sale_id_fkey" FOREIGN KEY ("sale_id") REFERENCES "sales"("id") ON DELETE CASCADE ON UPDATE CASCADE;