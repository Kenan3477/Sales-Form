import { PrismaClient } from '@prisma/client'
import { writeFileSync, mkdirSync, existsSync } from 'fs'
import { join } from 'path'

const prisma = new PrismaClient()

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
      prisma.sale.findMany({ include: { appliances: true, user: true } }),
      prisma.appliance.findMany(),
      prisma.fieldConfiguration.findMany(),
      prisma.documentTemplate.findMany(),
      prisma.generatedDocument.findMany({ include: { sale: true, template: true } }),
      prisma.sMSLog.findMany(),
      prisma.lead.findMany({ include: { appliances: true } }),
      prisma.leadAppliance.findMany(),
      prisma.leadDispositionHistory.findMany(),
      prisma.leadToSaleLink.findMany(),
      prisma.leadImportBatch.findMany()
    ])
    
    const backupData: BackupData = {
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      tables: {
        users: users.map(user => ({
          ...user,
          password: '[ENCRYPTED]' // Security: Don't backup actual passwords
        })),
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
      },
      metadata: {
        totalRecords: users.length + sales.length + appliances.length + 
                     fieldConfigurations.length + documentTemplates.length + 
                     generatedDocuments.length + smsLogs.length + leads.length +
                     leadAppliances.length + leadDispositionHistory.length +
                     leadToSaleLinks.length + leadImportBatches.length,
        backupSize: '0MB', // Will be calculated after writing
        tables: {
          users: users.length,
          sales: sales.length,
          appliances: appliances.length,
          fieldConfigurations: fieldConfigurations.length,
          documentTemplates: documentTemplates.length,
          generatedDocuments: generatedDocuments.length,
          smsLogs: smsLogs.length,
          leads: leads.length,
          leadAppliances: leadAppliances.length,
          leadDispositionHistory: leadDispositionHistory.length,
          leadToSaleLinks: leadToSaleLinks.length,
          leadImportBatches: leadImportBatches.length
        }
      }
    }
    
    // Write backup file
    const backupFileName = `database-backup-${timestamp}.json`
    const backupPath = join(backupDir, backupFileName)
    
    const backupJson = JSON.stringify(backupData, null, 2)
    writeFileSync(backupPath, backupJson)
    
    // Calculate file size
    const stats = require('fs').statSync(backupPath)
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
    console.log(`🔒 Data Protection: All customer data backed up safely without modification`)
    
    return backupPath
    
  } catch (error) {
    console.error('❌ Backup failed:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// Run backup if called directly
if (require.main === module) {
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

export { createDatabaseBackup }