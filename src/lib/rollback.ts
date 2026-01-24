import { PrismaClient } from '@prisma/client'
import { readFileSync, readdirSync, statSync, writeFileSync } from 'fs'
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
    console.log(`📊 Backup contains ${backupData.tables.sales?.length || 0} sales records`)
    
    const result = await prisma.$transaction(async (tx) => {
      console.log('🗑️  Clearing current data...')
      
      // Clear in correct order to respect foreign keys
      const deleted = await tx.generatedDocument.deleteMany({})
      console.log(`   Deleted ${deleted.count} generated documents`)
      
      await tx.sMSLog.deleteMany({})
      await tx.leadToSaleLink.deleteMany({})
      await tx.leadDispositionHistory.deleteMany({})
      await tx.leadAppliance.deleteMany({})
      await tx.lead.deleteMany({})
      await tx.leadImportBatch.deleteMany({})
      
      const deletedAppliances = await tx.appliance.deleteMany({})
      console.log(`   Deleted ${deletedAppliances.count} appliances`)
      
      const deletedSales = await tx.sale.deleteMany({})
      console.log(`   Deleted ${deletedSales.count} sales`)
      
      await tx.documentTemplate.deleteMany({})
      await tx.fieldConfiguration.deleteMany({})
      // Note: We preserve users table for system integrity

      console.log('📥 Restoring data from backup...')
      
      const restored: Record<string, number> = {}

      // Restore in dependency order
      if (backupData.tables.fieldConfigurations?.length > 0) {
        const created = await tx.fieldConfiguration.createMany({ 
          data: backupData.tables.fieldConfigurations,
          skipDuplicates: true 
        })
        restored.fieldConfigurations = created.count
        console.log(`   Restored ${created.count} field configurations`)
      }

      if (backupData.tables.documentTemplates?.length > 0) {
        const created = await tx.documentTemplate.createMany({ 
          data: backupData.tables.documentTemplates,
          skipDuplicates: true 
        })
        restored.documentTemplates = created.count
        console.log(`   Restored ${created.count} document templates`)
      }

      if (backupData.tables.sales?.length > 0) {
        console.log(`   Processing ${backupData.tables.sales.length} sales records for restoration...`)
        
        // Remove any appliances from sales data for createMany (they'll be created separately)
        const salesDataForCreate = backupData.tables.sales.map((sale: any) => {
          const { appliances, ...saleWithoutAppliances } = sale
          return saleWithoutAppliances
        })
        
        const created = await tx.sale.createMany({ 
          data: salesDataForCreate,
          skipDuplicates: true 
        })
        restored.sales = created.count
        console.log(`   Restored ${created.count} sales`)
      }

      if (backupData.tables.appliances?.length > 0) {
        console.log(`   Processing ${backupData.tables.appliances.length} appliance records for restoration...`)
        const created = await tx.appliance.createMany({ 
          data: backupData.tables.appliances,
          skipDuplicates: true 
        })
        restored.appliances = created.count
        console.log(`   Restored ${created.count} appliances`)
      }

      if (backupData.tables.leadImportBatches?.length > 0) {
        const created = await tx.leadImportBatch.createMany({ 
          data: backupData.tables.leadImportBatches,
          skipDuplicates: true 
        })
        restored.leadImportBatches = created.count
        console.log(`   Restored ${created.count} lead import batches`)
      }

      if (backupData.tables.leads?.length > 0) {
        const leadsDataForCreate = backupData.tables.leads.map((lead: any) => {
          const { appliances, ...leadWithoutAppliances } = lead
          return leadWithoutAppliances
        })
        
        const created = await tx.lead.createMany({ 
          data: leadsDataForCreate,
          skipDuplicates: true 
        })
        restored.leads = created.count
        console.log(`   Restored ${created.count} leads`)
      }

      if (backupData.tables.leadAppliances?.length > 0) {
        const created = await tx.leadAppliance.createMany({ 
          data: backupData.tables.leadAppliances,
          skipDuplicates: true 
        })
        restored.leadAppliances = created.count
        console.log(`   Restored ${created.count} lead appliances`)
      }

      if (backupData.tables.leadDispositionHistory?.length > 0) {
        const created = await tx.leadDispositionHistory.createMany({ 
          data: backupData.tables.leadDispositionHistory,
          skipDuplicates: true 
        })
        restored.leadDispositionHistory = created.count
        console.log(`   Restored ${created.count} lead disposition history`)
      }

      if (backupData.tables.leadToSaleLinks?.length > 0) {
        const created = await tx.leadToSaleLink.createMany({ 
          data: backupData.tables.leadToSaleLinks,
          skipDuplicates: true 
        })
        restored.leadToSaleLinks = created.count
        console.log(`   Restored ${created.count} lead to sale links`)
      }

      if (backupData.tables.smsLogs?.length > 0) {
        const created = await tx.sMSLog.createMany({ 
          data: backupData.tables.smsLogs,
          skipDuplicates: true 
        })
        restored.smsLogs = created.count
        console.log(`   Restored ${created.count} SMS logs`)
      }

      if (backupData.tables.generatedDocuments?.length > 0) {
        const created = await tx.generatedDocument.createMany({ 
          data: backupData.tables.generatedDocuments,
          skipDuplicates: true 
        })
        restored.generatedDocuments = created.count
        console.log(`   Restored ${created.count} generated documents`)
      }

      console.log('✅ Transaction restoration complete')
      return restored
    }, {
      maxWait: 10000, // 10 second timeout for Accelerate
      timeout: 15000 // 15 second overall timeout (Accelerate maximum)
    })

    console.log('✅ Database transaction completed successfully')

    // 🔍 STEP 4: POST-ROLLBACK VERIFICATION
    console.log('🔍 Step 4: Performing post-rollback verification...')
    
    const rolledBackSales = await prisma.sale.findMany()
    console.log(`✅ Verified ${rolledBackSales.length} sales records restored`)

    // Validate rolled back customer data integrity (no fake data)
    const rolledBackValidation = validateCustomerDataIntegrity(rolledBackSales)
    if (!rolledBackValidation.valid) {
      console.error('🚨 POST-ROLLBACK CUSTOMER DATA INTEGRITY VIOLATIONS:')
      rolledBackValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      throw new Error('Post-rollback validation failed: Customer data integrity violations detected')
    }

    // Check that we have the expected number of records
    const expectedSalesCount = backupData.metadata?.tables?.sales || backupData.tables?.sales?.length || 0
    if (rolledBackSales.length !== expectedSalesCount) {
      console.error(`🚨 RECORD COUNT MISMATCH: Expected ${expectedSalesCount} sales, found ${rolledBackSales.length}`)
      throw new Error(`Post-rollback validation failed: Expected ${expectedSalesCount} sales, found ${rolledBackSales.length}`)
    }

    console.log('✅ POST-ROLLBACK VALIDATION PASSED')
    console.log(`✅ Customer data integrity verified: NO fake data detected`)
    console.log(`✅ Record count verified: ${rolledBackSales.length} sales restored`)

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