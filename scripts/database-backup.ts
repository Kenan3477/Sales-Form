import { PrismaClient } from '@prisma/client'
import { writeFileSync, mkdirSync, existsSync, statSync } from 'fs'
import { join } from 'path'

const prisma = new PrismaClient()

// 🔒 DATA PROTECTION: Generate hash to detect any data modifications
function generateDataHash(data: any[]): string {
  const serialized = JSON.stringify(data.sort((a, b) => a.id?.localeCompare(b.id) || 0))
  let hash = 0
  for (let i = 0; i < serialized.length; i++) {
    const char = serialized.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32-bit integer
  }
  return hash.toString(36)
}

// 🛡️ CUSTOMER DATA PROTECTION: Validate that customer data contains no fake/corrupted information
function validateCustomerDataIntegrity(sales: any[]): { valid: boolean; issues: string[] } {
  const issues: string[] = []

  for (const sale of sales) {
    // Check for fake email domains
    if (sale.email && (
      sale.email.includes('@placeholder.') ||
      sale.email.includes('@example.') ||
      sale.email.includes('@test.') ||
      sale.email.includes('@fake.') ||
      sale.email.includes('@demo.')
    )) {
      issues.push(`CRITICAL: Fake email detected: ${sale.email} for customer ${sale.customerFirstName} ${sale.customerLastName}`)
    }

    // Check for obviously fake names
    if (sale.customerFirstName?.toLowerCase().includes('test') || 
        sale.customerLastName?.toLowerCase().includes('test') ||
        sale.customerFirstName?.toLowerCase().includes('fake') || 
        sale.customerLastName?.toLowerCase().includes('fake')) {
      issues.push(`WARNING: Suspicious customer name: ${sale.customerFirstName} ${sale.customerLastName}`)
    }

    // Check for fake phone numbers
    if (sale.phoneNumber && (
      sale.phoneNumber === '0000000000' ||
      sale.phoneNumber === '00000000000' ||
      sale.phoneNumber === '1111111111' ||
      sale.phoneNumber === '12345678901' ||
      /^(.)\1+$/.test(sale.phoneNumber) // All same digit
    )) {
      issues.push(`WARNING: Fake phone number detected: ${sale.phoneNumber} for customer ${sale.customerFirstName} ${sale.customerLastName}`)
    }
  }

  return {
    valid: issues.length === 0,
    issues
  }
}

interface BackupData {
  timestamp: string
  version: string
  tables: {
    users: any[]
    sales: any[]
    appliances: any[]
    fieldConfigurations: any[]
    documentTemplates: any[]
    generatedDocuments: any[]
    smsLogs: any[]
    emailLogs: any[]
    communicationLogs: any[]
    leads: any[]
    leadAppliances: any[]
    leadDispositionHistory: any[]
    leadToSaleLinks: any[]
    leadImportBatches: any[]
  }
  metadata: {
    totalRecords: number
    backupSize: string
    tables: Record<string, number>
    dataIntegrityHashes: {
      users: string
      sales: string
      appliances: string
      leads: string
      emailLogs: string
      communicationLogs: string
    }
    communicationSummary: {
      totalSMS: number
      totalEmails: number
      totalCommunications: number
      smsSuccessRate: number
      emailSuccessRate: number
    }
  }
}

async function createDatabaseBackup(): Promise<string> {
  console.log('🔄 STARTING AUTOMATED DATABASE BACKUP')
  console.log('====================================')
  console.log(`📅 Backup Date: ${new Date().toISOString()}`)
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const backupDir = join(process.cwd(), 'backups', 'database')
  
  // Ensure backup directory exists
  if (!existsSync(backupDir)) {
    mkdirSync(backupDir, { recursive: true })
    console.log('📁 Created backup directory:', backupDir)
  }
  
  try {
    console.log('📊 Fetching all database tables...')
    
    // 🔒 DATA PROTECTION: Read-only operations - NO modifications
    const [
      users,
      sales, 
      appliances,
      fieldConfigurations,
      documentTemplates,
      generatedDocuments,
      smsLogs,
      leads,
      leadAppliances,
      leadDispositionHistory,
      leadToSaleLinks,
      leadImportBatches
    ] = await Promise.all([
      prisma.user.findMany(),
      prisma.sale.findMany({ include: { appliances: true } }),
      prisma.appliance.findMany(),
      prisma.fieldConfiguration.findMany(),
      prisma.documentTemplate.findMany(),
      prisma.generatedDocument.findMany(),
      prisma.sMSLog.findMany(),
      prisma.lead.findMany({ include: { appliances: true } }),
      prisma.leadAppliance.findMany(),
      prisma.leadDispositionHistory.findMany(),
      prisma.leadToSaleLink.findMany(),
      prisma.leadImportBatch.findMany()
    ])
    
    // Placeholder for future communication tables
    const emailLogs: any[] = []
    const communicationLogs: any[] = []
    
    console.log('📈 Calculating communication metrics...')
    
    // Calculate communication summary
    const totalSMS = smsLogs.length
    const totalEmails = emailLogs.length 
    const totalCommunications = totalSMS + totalEmails + communicationLogs.length
    const successfulSMS = smsLogs.filter(sms => sms.smsStatus === 'SENT').length
    const smsSuccessRate = totalSMS > 0 ? (successfulSMS / totalSMS) * 100 : 0
    const successfulEmails = emailLogs.filter((email: any) => email.emailStatus === 'SENT').length
    const emailSuccessRate = totalEmails > 0 ? (successfulEmails / totalEmails) * 100 : 0
    
    console.log('🔒 Performing customer data integrity validation before backup...')
    
    // 🔒 CRITICAL: Validate customer data integrity before backup
    const customerValidation = validateCustomerDataIntegrity(sales)
    if (!customerValidation.valid) {
      console.error('🚨 CUSTOMER DATA INTEGRITY VIOLATIONS DETECTED:')
      customerValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      throw new Error(`Cannot create backup: Customer data integrity violations - ${customerValidation.issues.length} issues found`)
    }
    
    console.log('✅ Customer data integrity validation passed')
    
    // 🔒 Generate integrity hashes for all critical data
    const dataIntegrityHashes = {
      users: generateDataHash(users),
      sales: generateDataHash(sales.map((sale: any) => ({
        id: sale.id,
        customerFirstName: sale.customerFirstName,
        customerLastName: sale.customerLastName,
        email: sale.email,
        phoneNumber: sale.phoneNumber,
        mailingStreet: sale.mailingStreet,
        mailingCity: sale.mailingCity,
        mailingPostalCode: sale.mailingPostalCode
      }))),
      appliances: generateDataHash(appliances),
      leads: generateDataHash(leads.map((lead: any) => ({
        id: lead.id,
        customerFirstName: lead.customerFirstName,
        customerLastName: lead.customerLastName,
        email: lead.email,
        phoneNumber: lead.phoneNumber
      }))),
      emailLogs: generateDataHash(emailLogs),
      communicationLogs: generateDataHash(communicationLogs)
    }
    
    const backupData: BackupData = {
      timestamp: new Date().toISOString(),
      version: '2.1.0',
      tables: {
        users: users.map((user: any) => ({
          ...user,
          password: '[ENCRYPTED]' // Security: Don't backup actual passwords
        })),
        sales,
        appliances,
        fieldConfigurations,
        documentTemplates,
        generatedDocuments,
        smsLogs,
        emailLogs,
        communicationLogs,
        leads,
        leadAppliances,
        leadDispositionHistory,
        leadToSaleLinks,
        leadImportBatches
      },
      metadata: {
        totalRecords: users.length + sales.length + appliances.length + 
                     fieldConfigurations.length + documentTemplates.length + 
                     generatedDocuments.length + smsLogs.length + emailLogs.length +
                     communicationLogs.length + leads.length + leadAppliances.length +
                     leadDispositionHistory.length + leadToSaleLinks.length +
                     leadImportBatches.length,
        backupSize: '0MB', // Will be calculated after writing
        tables: {
          users: users.length,
          sales: sales.length,
          appliances: appliances.length,
          fieldConfigurations: fieldConfigurations.length,
          documentTemplates: documentTemplates.length,
          generatedDocuments: generatedDocuments.length,
          smsLogs: smsLogs.length,
          emailLogs: emailLogs.length,
          communicationLogs: communicationLogs.length,
          leads: leads.length,
          leadAppliances: leadAppliances.length,
          leadDispositionHistory: leadDispositionHistory.length,
          leadToSaleLinks: leadToSaleLinks.length,
          leadImportBatches: leadImportBatches.length
        },
        dataIntegrityHashes,
        communicationSummary: {
          totalSMS,
          totalEmails,
          totalCommunications,
          smsSuccessRate: Math.round(smsSuccessRate * 100) / 100,
          emailSuccessRate: Math.round(emailSuccessRate * 100) / 100
        }
      }
    }
    
    // Write backup file
    const backupFileName = `database-backup-${timestamp}.json`
    const backupPath = join(backupDir, backupFileName)
    
    const backupJson = JSON.stringify(backupData, null, 2)
    writeFileSync(backupPath, backupJson)
    
    // Calculate file size
    const stats = statSync(backupPath)
    const fileSizeInBytes = stats.size
    const fileSizeInMB = (fileSizeInBytes / (1024 * 1024)).toFixed(2)
    
    // Update metadata with actual file size
    backupData.metadata.backupSize = `${fileSizeInMB}MB`
    writeFileSync(backupPath, JSON.stringify(backupData, null, 2))
    
    console.log('✅ DATABASE BACKUP COMPLETE')
    console.log('==========================')
    console.log(`📁 Backup file: ${backupFileName}`)
    console.log(`📊 Total records: ${backupData.metadata.totalRecords}`)
    console.log(`💾 File size: ${fileSizeInMB}MB`)
    console.log('')
    console.log('📋 Table breakdown:')
    Object.entries(backupData.metadata.tables).forEach(([table, count]) => {
      console.log(`  - ${table}: ${count} records`)
    })
    console.log('')
    console.log('📞 Communication Summary:')
    console.log(`  - SMS Messages: ${totalSMS} (${smsSuccessRate.toFixed(1)}% success rate)`)
    console.log(`  - Email Messages: ${totalEmails} (${emailSuccessRate.toFixed(1)}% success rate)`)
    console.log(`  - Total Communications: ${totalCommunications}`)
    console.log('')
    console.log(`🔒 Data Protection: All customer data and communication history backed up safely without modification`)
    
    return backupPath
    
  } catch (error) {
    console.error('❌ Backup failed:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// Export for use in other modules
export { createDatabaseBackup }

// Run backup if called directly
if (process.env.NODE_ENV !== 'test') {
  createDatabaseBackup()
    .then((backupPath) => {
      console.log(`✅ Backup completed successfully: ${backupPath}`)
      process.exit(0)
    })
    .catch((error) => {
      console.error('❌ Backup failed:', error)
      process.exit(1)
    })
}