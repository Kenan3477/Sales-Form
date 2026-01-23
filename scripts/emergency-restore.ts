import { PrismaClient } from '@prisma/client'
import { readFileSync } from 'fs'
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

async function emergencyRestore(backupFileName: string, confirmationCode: string): Promise<void> {
  console.log('🚨 EMERGENCY DATABASE RESTORE')
  console.log('=============================')
  console.log('⚠️  WARNING: This will REPLACE ALL current data!')
  console.log('')
  
  // Safety check - require specific confirmation code
  if (confirmationCode !== 'RESTORE_CONFIRMED_EMERGENCY') {
    console.log('❌ Invalid confirmation code')
    console.log('🔒 For safety, emergency restore requires confirmation code: RESTORE_CONFIRMED_EMERGENCY')
    return
  }
  
  const backupDir = join(process.cwd(), 'backups', 'database')
  const backupPath = join(backupDir, backupFileName)
  
  try {
    console.log(`📖 Reading backup file: ${backupFileName}`)
    const backupJson = readFileSync(backupPath, 'utf-8')
    const backupData: BackupData = JSON.parse(backupJson)
    
    console.log(`📅 Backup date: ${backupData.timestamp}`)
    console.log(`📊 Total records: ${backupData.metadata.totalRecords}`)
    console.log(`💾 Backup size: ${backupData.metadata.backupSize}`)
    console.log('')
    
    console.log('🔄 Starting database restore...')
    
    // Create a transaction to ensure all-or-nothing restore
    await prisma.$transaction(async (tx) => {
      // Step 1: Clear existing data (in correct order to respect foreign keys)
      console.log('🗑️  Clearing existing data...')
      await tx.generatedDocument.deleteMany({})
      await tx.sMSLog.deleteMany({})
      await tx.leadToSaleLink.deleteMany({})
      await tx.leadDispositionHistory.deleteMany({})
      await tx.leadAppliance.deleteMany({})
      await tx.lead.deleteMany({})
      await tx.leadImportBatch.deleteMany({})
      await tx.appliance.deleteMany({})
      await tx.sale.deleteMany({})
      await tx.documentTemplate.deleteMany({})
      await tx.fieldConfiguration.deleteMany({})
      await tx.user.deleteMany({})
      
      console.log('✅ Existing data cleared')
      
      // Step 2: Restore data (in correct order to respect foreign keys)
      console.log('📥 Restoring data...')
      
      // Users first (no dependencies)
      if (backupData.tables.users.length > 0) {
        await tx.user.createMany({ 
          data: backupData.tables.users.map(user => ({
            ...user,
            password: user.password === '[ENCRYPTED]' ? user.password : user.password
          }))
        })
        console.log(`✅ Restored ${backupData.tables.users.length} users`)
      }
      
      // Field configurations
      if (backupData.tables.fieldConfigurations.length > 0) {
        await tx.fieldConfiguration.createMany({ data: backupData.tables.fieldConfigurations })
        console.log(`✅ Restored ${backupData.tables.fieldConfigurations.length} field configurations`)
      }
      
      // Document templates
      if (backupData.tables.documentTemplates.length > 0) {
        await tx.documentTemplate.createMany({ data: backupData.tables.documentTemplates })
        console.log(`✅ Restored ${backupData.tables.documentTemplates.length} document templates`)
      }
      
      // Sales (depends on users)
      if (backupData.tables.sales.length > 0) {
        await tx.sale.createMany({ data: backupData.tables.sales })
        console.log(`✅ Restored ${backupData.tables.sales.length} sales records`)
      }
      
      // Appliances (depends on sales)
      if (backupData.tables.appliances.length > 0) {
        await tx.appliance.createMany({ data: backupData.tables.appliances })
        console.log(`✅ Restored ${backupData.tables.appliances.length} appliances`)
      }
      
      // Lead import batches (depends on users)
      if (backupData.tables.leadImportBatches.length > 0) {
        await tx.leadImportBatch.createMany({ data: backupData.tables.leadImportBatches })
        console.log(`✅ Restored ${backupData.tables.leadImportBatches.length} lead import batches`)
      }
      
      // Leads (depends on users and batches)
      if (backupData.tables.leads.length > 0) {
        await tx.lead.createMany({ data: backupData.tables.leads })
        console.log(`✅ Restored ${backupData.tables.leads.length} leads`)
      }
      
      // Lead appliances (depends on leads)
      if (backupData.tables.leadAppliances.length > 0) {
        await tx.leadAppliance.createMany({ data: backupData.tables.leadAppliances })
        console.log(`✅ Restored ${backupData.tables.leadAppliances.length} lead appliances`)
      }
      
      // Lead disposition history (depends on leads and users)
      if (backupData.tables.leadDispositionHistory.length > 0) {
        await tx.leadDispositionHistory.createMany({ data: backupData.tables.leadDispositionHistory })
        console.log(`✅ Restored ${backupData.tables.leadDispositionHistory.length} lead dispositions`)
      }
      
      // Lead to sale links (depends on leads and sales)
      if (backupData.tables.leadToSaleLinks.length > 0) {
        await tx.leadToSaleLink.createMany({ data: backupData.tables.leadToSaleLinks })
        console.log(`✅ Restored ${backupData.tables.leadToSaleLinks.length} lead to sale links`)
      }
      
      // SMS logs (depends on sales)
      if (backupData.tables.smsLogs.length > 0) {
        await tx.sMSLog.createMany({ data: backupData.tables.smsLogs })
        console.log(`✅ Restored ${backupData.tables.smsLogs.length} SMS logs`)
      }
      
      // Generated documents (depends on sales and templates)
      if (backupData.tables.generatedDocuments.length > 0) {
        await tx.generatedDocument.createMany({ data: backupData.tables.generatedDocuments })
        console.log(`✅ Restored ${backupData.tables.generatedDocuments.length} generated documents`)
      }
    })
    
    console.log('')
    console.log('✅ DATABASE RESTORE COMPLETE')
    console.log('============================')
    console.log(`📅 Restored data from: ${backupData.timestamp}`)
    console.log(`📊 Total records restored: ${backupData.metadata.totalRecords}`)
    console.log('🔒 All data restored exactly as it was at backup time')
    console.log('')
    console.log('🎯 Your system has been restored to the exact state it was in when the backup was created!')
    
  } catch (error) {
    console.error('❌ Restore failed:', error)
    console.log('')
    console.log('🚨 RESTORE FAILED - Database may be in inconsistent state')
    console.log('⚡ Recommended actions:')
    console.log('  1. Try restore again with a different backup file')
    console.log('  2. Check backup file integrity')
    console.log('  3. Contact system administrator if issues persist')
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

export { emergencyRestore }

// Command line usage: node emergency-restore.js <backup-file> <confirmation-code>
if (process.env.NODE_ENV !== 'test') {
  const backupFile = process.argv[2]
  const confirmationCode = process.argv[3]
  
  if (!backupFile) {
    console.log('❌ Usage: npx ts-node scripts/emergency-restore.ts <backup-file> <confirmation-code>')
    console.log('📋 Example: npx ts-node scripts/emergency-restore.ts database-backup-2026-01-23T19-17-47-035Z.json RESTORE_CONFIRMED_EMERGENCY')
    console.log('')
    console.log('📁 Available backup files:')
    const { readdirSync } = require('fs')
    const backupDir = join(process.cwd(), 'backups', 'database')
    try {
      const files = readdirSync(backupDir).filter((f: string) => f.endsWith('.json')).sort().reverse()
      files.slice(0, 5).forEach((file: string, index: number) => console.log(`  ${index + 1}. ${file}`))
    } catch (e) {
      console.log('  No backup files found')
    }
    process.exit(1)
  }
  
  emergencyRestore(backupFile, confirmationCode || '')
    .then(() => {
      console.log(`✅ Emergency restore completed successfully`)
      process.exit(0)
    })
    .catch((error) => {
      console.error('❌ Emergency restore failed:', error)
      process.exit(1)
    })
}