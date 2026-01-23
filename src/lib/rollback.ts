import { PrismaClient } from '@prisma/client'
import { readFileSync, readdirSync, statSync } from 'fs'
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

    // NOTE: We do NOT check phone numbers here because we know there's one legitimate customer
    // with corrupted phone data that the user has not authorized us to fix
  }

  return {
    valid: issues.length === 0,
    issues
  }
}

// 🔒 CRITICAL: Validate backup integrity before rollback
function validateBackupIntegrity(backupData: any): { valid: boolean; issues: string[] } {
  const issues: string[] = []

  try {
    // Check required structure
    if (!backupData.tables) {
      issues.push('Backup missing tables section')
    }
    
    if (!backupData.metadata) {
      issues.push('Backup missing metadata section')
    }

    // Validate sales data if present
    if (backupData.tables?.sales) {
      const customerValidation = validateCustomerDataIntegrity(backupData.tables.sales)
      if (!customerValidation.valid) {
        issues.push(...customerValidation.issues.map((issue: string) => `Backup contains corrupted data: ${issue}`))
      }
    }

    // Verify data integrity hashes if available
    if (backupData.tables && backupData.metadata?.dataIntegrityHashes) {
      const salesHash = generateDataHash(backupData.tables.sales?.map((sale: any) => ({
        id: sale.id,
        customerFirstName: sale.customerFirstName,
        customerLastName: sale.customerLastName,
        email: sale.email,
        phoneNumber: sale.phoneNumber,
        mailingStreet: sale.mailingStreet,
        mailingCity: sale.mailingCity,
        mailingPostalCode: sale.mailingPostalCode
      })) || [])

      if (salesHash !== backupData.metadata.dataIntegrityHashes.sales) {
        issues.push('CRITICAL: Sales data integrity hash mismatch - data may be corrupted')
      }
    }

  } catch (error) {
    issues.push(`Backup validation failed: ${error}`)
  }

  return {
    valid: issues.length === 0,
    issues
  }
}

interface RollbackPoint {
  filename: string
  timestamp: string
  fullPath: string
  size: string
  recordCount: number
  dataIntegrityVerified: boolean
}

export async function listAvailableRollbackPoints(): Promise<RollbackPoint[]> {
  const backupDir = join(process.cwd(), 'backups', 'database')
  const rollbackPoints: RollbackPoint[] = []

  try {
    const files = readdirSync(backupDir)
    const backupFiles = files.filter(f => f.startsWith('database-backup-') && f.endsWith('.json'))

    for (const filename of backupFiles) {
      const fullPath = join(backupDir, filename)
      const stats = statSync(fullPath)
      const fileSizeInMB = (stats.size / (1024 * 1024)).toFixed(2)

      try {
        const backupJson = readFileSync(fullPath, 'utf-8')
        const backupData = JSON.parse(backupJson)
        
        // Validate backup integrity
        const validation = validateBackupIntegrity(backupData)

        rollbackPoints.push({
          filename,
          timestamp: backupData.timestamp || 'Unknown',
          fullPath,
          size: `${fileSizeInMB}MB`,
          recordCount: backupData.metadata?.totalRecords || 0,
          dataIntegrityVerified: validation.valid
        })
      } catch (error) {
        console.warn(`⚠️  Could not read backup file: ${filename} - ${error}`)
      }
    }

    // Sort by timestamp (newest first)
    rollbackPoints.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())

    return rollbackPoints
  } catch (error) {
    console.error('Error listing rollback points:', error)
    return []
  }
}

export async function performDatabaseRollback(backupFilename: string, confirmationCode: string): Promise<{
  success: boolean
  message: string
  rolledBackTo: string
  recordsRestored: number
  dataIntegrityVerified: boolean
  error?: string
}> {
  try {
    console.log('🚨 EMERGENCY DATABASE ROLLBACK INITIATED')
    console.log('=======================================')
    console.log(`📁 Target backup: ${backupFilename}`)
    console.log(`🔐 Confirmation: ${confirmationCode}`)

    // Safety check - require specific confirmation code
    if (confirmationCode !== 'ROLLBACK_CONFIRMED_EMERGENCY') {
      return {
        success: false,
        message: 'Invalid confirmation code. For safety, rollback requires: ROLLBACK_CONFIRMED_EMERGENCY',
        rolledBackTo: '',
        recordsRestored: 0,
        dataIntegrityVerified: false,
        error: 'Invalid confirmation'
      }
    }

    // 🔒 STEP 1: CREATE SAFETY BACKUP OF CURRENT STATE
    console.log('🔒 Step 1: Creating safety backup of current state...')
    
    const currentBackup = await createEmergencyBackup()
    console.log(`✅ Current state backed up to: ${currentBackup}`)

    // 🔍 STEP 2: VALIDATE TARGET BACKUP
    console.log('🔍 Step 2: Validating target backup integrity...')
    
    const backupDir = join(process.cwd(), 'backups', 'database')
    const backupPath = join(backupDir, backupFilename)

    let backupData: any
    try {
      const backupJson = readFileSync(backupPath, 'utf-8')
      backupData = JSON.parse(backupJson)
    } catch (error) {
      return {
        success: false,
        message: 'Failed to read backup file. File may be corrupted or missing.',
        rolledBackTo: '',
        recordsRestored: 0,
        dataIntegrityVerified: false,
        error: `Backup read error: ${error}`
      }
    }

    const backupValidation = validateBackupIntegrity(backupData)
    if (!backupValidation.valid) {
      console.error('🚨 BACKUP INTEGRITY VIOLATIONS DETECTED:')
      backupValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      
      return {
        success: false,
        message: 'Cannot rollback: Backup integrity violations detected',
        rolledBackTo: '',
        recordsRestored: 0,
        dataIntegrityVerified: false,
        error: `Integrity violations: ${backupValidation.issues.join(', ')}`
      }
    }

    console.log('✅ Target backup integrity verified')

    // 🔄 STEP 3: PERFORM ROLLBACK IN TRANSACTION
    console.log('🔄 Step 3: Performing database rollback...')
    
    const result = await prisma.$transaction(async (tx) => {
      console.log('🗑️  Clearing current data...')
      
      // Clear in correct order to respect foreign keys
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
      // Note: We preserve users table for system integrity

      console.log('📥 Restoring data from backup...')
      
      const restored: Record<string, number> = {}

      // Restore in dependency order
      if (backupData.tables.fieldConfigurations?.length > 0) {
        await tx.fieldConfiguration.createMany({ data: backupData.tables.fieldConfigurations })
        restored.fieldConfigurations = backupData.tables.fieldConfigurations.length
      }

      if (backupData.tables.documentTemplates?.length > 0) {
        await tx.documentTemplate.createMany({ data: backupData.tables.documentTemplates })
        restored.documentTemplates = backupData.tables.documentTemplates.length
      }

      if (backupData.tables.sales?.length > 0) {
        await tx.sale.createMany({ data: backupData.tables.sales })
        restored.sales = backupData.tables.sales.length
      }

      if (backupData.tables.appliances?.length > 0) {
        await tx.appliance.createMany({ data: backupData.tables.appliances })
        restored.appliances = backupData.tables.appliances.length
      }

      if (backupData.tables.leadImportBatches?.length > 0) {
        await tx.leadImportBatch.createMany({ data: backupData.tables.leadImportBatches })
        restored.leadImportBatches = backupData.tables.leadImportBatches.length
      }

      if (backupData.tables.leads?.length > 0) {
        await tx.lead.createMany({ data: backupData.tables.leads })
        restored.leads = backupData.tables.leads.length
      }

      if (backupData.tables.leadAppliances?.length > 0) {
        await tx.leadAppliance.createMany({ data: backupData.tables.leadAppliances })
        restored.leadAppliances = backupData.tables.leadAppliances.length
      }

      if (backupData.tables.leadDispositionHistory?.length > 0) {
        await tx.leadDispositionHistory.createMany({ data: backupData.tables.leadDispositionHistory })
        restored.leadDispositionHistory = backupData.tables.leadDispositionHistory.length
      }

      if (backupData.tables.leadToSaleLinks?.length > 0) {
        await tx.leadToSaleLink.createMany({ data: backupData.tables.leadToSaleLinks })
        restored.leadToSaleLinks = backupData.tables.leadToSaleLinks.length
      }

      if (backupData.tables.smsLogs?.length > 0) {
        await tx.sMSLog.createMany({ data: backupData.tables.smsLogs })
        restored.smsLogs = backupData.tables.smsLogs.length
      }

      if (backupData.tables.generatedDocuments?.length > 0) {
        await tx.generatedDocument.createMany({ data: backupData.tables.generatedDocuments })
        restored.generatedDocuments = backupData.tables.generatedDocuments.length
      }

      return restored
    }, {
      maxWait: 60000, // 60 second timeout
      timeout: 120000 // 120 second overall timeout
    })

    // 🔍 STEP 4: POST-ROLLBACK VERIFICATION
    console.log('🔍 Step 4: Performing post-rollback verification...')
    
    const rolledBackSales = await prisma.sale.findMany()
    const rolledBackDataHash = generateDataHash(rolledBackSales.map(sale => ({
      id: sale.id,
      customerFirstName: sale.customerFirstName,
      customerLastName: sale.customerLastName,
      email: sale.email,
      phoneNumber: sale.phoneNumber
    })))

    // Validate rolled back customer data integrity
    const rolledBackValidation = validateCustomerDataIntegrity(rolledBackSales)
    if (!rolledBackValidation.valid) {
      console.error('🚨 POST-ROLLBACK CUSTOMER DATA INTEGRITY VIOLATIONS:')
      rolledBackValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      throw new Error('Post-rollback validation failed: Customer data integrity violations detected')
    }

    // Compare with backup hash if available
    if (backupData.metadata?.dataIntegrityHashes?.sales) {
      if (rolledBackDataHash !== backupData.metadata.dataIntegrityHashes.sales) {
        console.error('🚨 CRITICAL: Rolled back data hash does not match backup hash!')
        console.error(`  Backup hash:     ${backupData.metadata.dataIntegrityHashes.sales}`)
        console.error(`  Rolled back hash: ${rolledBackDataHash}`)
        throw new Error('Post-rollback validation failed: Data integrity hash mismatch')
      }
    }

    const totalRestored = Object.values(result).reduce((sum, count) => sum + count, 0)

    console.log('✅ DATABASE ROLLBACK COMPLETE')
    console.log('============================')
    console.log(`📅 Rolled back to: ${backupData.timestamp}`)
    console.log(`📊 Total records restored: ${totalRestored}`)
    console.log(`🔒 Data integrity verified: YES`)
    console.log(`🔐 Customer data protected: YES`)

    return {
      success: true,
      message: `Database successfully rolled back to ${backupData.timestamp}`,
      rolledBackTo: backupData.timestamp,
      recordsRestored: totalRestored,
      dataIntegrityVerified: true
    }

  } catch (error) {
    console.error('❌ Database rollback failed:', error)
    return {
      success: false,
      message: 'Database rollback failed',
      rolledBackTo: '',
      recordsRestored: 0,
      dataIntegrityVerified: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    }
  } finally {
    await prisma.$disconnect()
  }
}

async function createEmergencyBackup(): Promise<string> {
  console.log('🆘 Creating emergency backup of current state...')
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  
  // Get all current data
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

  // Generate integrity hashes
  const dataIntegrityHashes = {
    users: generateDataHash(users),
    sales: generateDataHash(sales.map(sale => ({
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
    leads: generateDataHash(leads.map(lead => ({
      id: lead.id,
      customerFirstName: lead.customerFirstName,
      customerLastName: lead.customerLastName,
      email: lead.email,
      phoneNumber: lead.phoneNumber
    })))
  }

  const emergencyBackup = {
    timestamp,
    version: '2.0.0-emergency',
    tables: {
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
    },
    metadata: {
      totalRecords: users.length + sales.length + appliances.length + 
                   fieldConfigurations.length + documentTemplates.length + 
                   generatedDocuments.length + smsLogs.length + leads.length +
                   leadAppliances.length + leadDispositionHistory.length +
                   leadToSaleLinks.length + leadImportBatches.length,
      backupSize: '0MB',
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
      },
      dataIntegrityHashes
    }
  }

  const backupDir = join(process.cwd(), 'backups', 'database')
  const backupFileName = `database-backup-${timestamp}-EMERGENCY.json`
  const backupPath = join(backupDir, backupFileName)

  const { writeFileSync, statSync } = require('fs')
  const backupJson = JSON.stringify(emergencyBackup, null, 2)
  writeFileSync(backupPath, backupJson)

  // Update file size
  const stats = statSync(backupPath)
  const fileSizeInMB = (stats.size / (1024 * 1024)).toFixed(2)
  emergencyBackup.metadata.backupSize = `${fileSizeInMB}MB`
  writeFileSync(backupPath, JSON.stringify(emergencyBackup, null, 2))

  console.log(`✅ Emergency backup created: ${backupFileName} (${fileSizeInMB}MB)`)
  
  return backupFileName
}