import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { PrismaClient } from '@prisma/client'
import { readFileSync } from 'fs'
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

// 🔒 CRITICAL: Validate backup integrity before restore
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
    dataIntegrityHashes?: {
      users: string
      sales: string
      appliances: string
      leads: string
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { backupFilename, confirmationCode } = await request.json()

    console.log('🚨 EMERGENCY DATABASE RESTORE REQUEST')
    console.log(`👤 Requested by: ${session.user.email}`)
    console.log(`📁 Backup file: ${backupFilename}`)

    // Safety check - require specific confirmation code
    if (confirmationCode !== 'RESTORE_CONFIRMED_EMERGENCY') {
      return NextResponse.json(
        { error: 'Invalid confirmation code. For safety, restore requires confirmation code: RESTORE_CONFIRMED_EMERGENCY' },
        { status: 400 }
      )
    }

    if (!backupFilename) {
      return NextResponse.json(
        { error: 'Backup filename is required' },
        { status: 400 }
      )
    }

    const backupDir = join(process.cwd(), 'backups', 'database')
    const backupPath = join(backupDir, backupFilename)

    // Read and validate backup file
    let backupData: BackupData
    try {
      const backupJson = readFileSync(backupPath, 'utf-8')
      backupData = JSON.parse(backupJson)
    } catch (error) {
      return NextResponse.json(
        { error: 'Failed to read backup file. File may be corrupted or missing.' },
        { status: 400 }
      )
    }

    console.log(`📅 Backup date: ${backupData.timestamp}`)
    console.log(`📊 Total records: ${backupData.metadata.totalRecords}`)

    console.log('🔒 Performing backup integrity validation...')
    
    // 🔒 CRITICAL: Validate backup integrity before restore
    const backupValidation = validateBackupIntegrity(backupData)
    if (!backupValidation.valid) {
      console.error('🚨 BACKUP INTEGRITY VIOLATIONS DETECTED:')
      backupValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      return NextResponse.json(
        { 
          error: 'Cannot restore: Backup integrity violations detected', 
          issues: backupValidation.issues 
        },
        { status: 400 }
      )
    }
    
    console.log('✅ Backup integrity validation passed')
    
    // Get current data for verification BEFORE restore
    const currentSales = await prisma.sale.findMany()
    const currentDataHash = generateDataHash(currentSales.map(sale => ({
      id: sale.id,
      customerFirstName: sale.customerFirstName,
      customerLastName: sale.customerLastName,
      email: sale.email,
      phoneNumber: sale.phoneNumber
    })))
    
    console.log(`📊 Current database state: ${currentSales.length} sales records`)
    console.log(`🔒 Current data hash: ${currentDataHash}`)

    // Perform the restore in a transaction
    const result = await prisma.$transaction(async (tx) => {
      console.log('🔄 Starting database restore...')
      
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

      // Step 2: Restore data (in correct order to respect foreign keys)
      console.log('📥 Restoring data...')

      const restored = {
        users: 0,
        fieldConfigurations: 0,
        documentTemplates: 0,
        sales: 0,
        appliances: 0,
        leadImportBatches: 0,
        leads: 0,
        leadAppliances: 0,
        leadDispositionHistory: 0,
        leadToSaleLinks: 0,
        smsLogs: 0,
        generatedDocuments: 0
      }

      // Users first (no dependencies)
      if (backupData.tables.users.length > 0) {
        await tx.user.createMany({ 
          data: backupData.tables.users.map(user => ({
            ...user,
            // Keep encrypted passwords as they are - they're already hashed
            password: user.password
          }))
        })
        restored.users = backupData.tables.users.length
      }

      // Field configurations
      if (backupData.tables.fieldConfigurations.length > 0) {
        await tx.fieldConfiguration.createMany({ data: backupData.tables.fieldConfigurations })
        restored.fieldConfigurations = backupData.tables.fieldConfigurations.length
      }

      // Document templates
      if (backupData.tables.documentTemplates.length > 0) {
        await tx.documentTemplate.createMany({ data: backupData.tables.documentTemplates })
        restored.documentTemplates = backupData.tables.documentTemplates.length
      }

      // Sales (depends on users)
      if (backupData.tables.sales.length > 0) {
        await tx.sale.createMany({ data: backupData.tables.sales })
        restored.sales = backupData.tables.sales.length
      }

      // Appliances (depends on sales)
      if (backupData.tables.appliances.length > 0) {
        await tx.appliance.createMany({ data: backupData.tables.appliances })
        restored.appliances = backupData.tables.appliances.length
      }

      // Lead import batches (depends on users)
      if (backupData.tables.leadImportBatches.length > 0) {
        await tx.leadImportBatch.createMany({ data: backupData.tables.leadImportBatches })
        restored.leadImportBatches = backupData.tables.leadImportBatches.length
      }

      // Leads (depends on users and batches)
      if (backupData.tables.leads.length > 0) {
        await tx.lead.createMany({ data: backupData.tables.leads })
        restored.leads = backupData.tables.leads.length
      }

      // Lead appliances (depends on leads)
      if (backupData.tables.leadAppliances.length > 0) {
        await tx.leadAppliance.createMany({ data: backupData.tables.leadAppliances })
        restored.leadAppliances = backupData.tables.leadAppliances.length
      }

      // Lead disposition history (depends on leads and users)
      if (backupData.tables.leadDispositionHistory.length > 0) {
        await tx.leadDispositionHistory.createMany({ data: backupData.tables.leadDispositionHistory })
        restored.leadDispositionHistory = backupData.tables.leadDispositionHistory.length
      }

      // Lead to sale links (depends on leads and sales)
      if (backupData.tables.leadToSaleLinks.length > 0) {
        await tx.leadToSaleLink.createMany({ data: backupData.tables.leadToSaleLinks })
        restored.leadToSaleLinks = backupData.tables.leadToSaleLinks.length
      }

      // SMS logs (depends on sales)
      if (backupData.tables.smsLogs.length > 0) {
        await tx.sMSLog.createMany({ data: backupData.tables.smsLogs })
        restored.smsLogs = backupData.tables.smsLogs.length
      }

      // Generated documents (depends on sales and templates)
      if (backupData.tables.generatedDocuments.length > 0) {
        await tx.generatedDocument.createMany({ data: backupData.tables.generatedDocuments })
        restored.generatedDocuments = backupData.tables.generatedDocuments.length
      }

      return restored
    }, {
      maxWait: 30000, // 30 second timeout
      timeout: 60000  // 60 second overall timeout
    })

    // 🔒 POST-RESTORE VERIFICATION: Ensure data integrity was maintained
    console.log('🔍 Performing post-restore data integrity verification...')
    
    const restoredSales = await prisma.sale.findMany()
    const restoredDataHash = generateDataHash(restoredSales.map(sale => ({
      id: sale.id,
      customerFirstName: sale.customerFirstName,
      customerLastName: sale.customerLastName,
      email: sale.email,
      phoneNumber: sale.phoneNumber
    })))
    
    // Validate restored customer data integrity
    const restoredCustomerValidation = validateCustomerDataIntegrity(restoredSales)
    if (!restoredCustomerValidation.valid) {
      console.error('🚨 POST-RESTORE CUSTOMER DATA INTEGRITY VIOLATIONS:')
      restoredCustomerValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      // This is critical - we should not allow corrupted data to remain
      throw new Error('Post-restore validation failed: Customer data integrity violations detected')
    }
    
    // Compare with backup hash if available
    if (backupData.metadata?.dataIntegrityHashes?.sales) {
      if (restoredDataHash !== backupData.metadata.dataIntegrityHashes.sales) {
        console.error('🚨 CRITICAL: Restored data hash does not match backup hash!')
        console.error(`  Backup hash:    ${backupData.metadata.dataIntegrityHashes.sales}`)
        console.error(`  Restored hash:  ${restoredDataHash}`)
        throw new Error('Post-restore validation failed: Data integrity hash mismatch')
      }
    }
    
    console.log('✅ Post-restore data integrity verification PASSED')
    console.log(`📊 Restored database state: ${restoredSales.length} sales records`)
    console.log(`🔒 Restored data hash: ${restoredDataHash}`)

    console.log('✅ DATABASE RESTORE COMPLETE')
    console.log(`📊 Total records restored: ${Object.values(result).reduce((sum, count) => sum + count, 0)}`)
    console.log('🔐 All customer data integrity preserved during restore')

    return NextResponse.json({
      success: true,
      message: 'Database restored successfully with integrity verification',
      backupDate: backupData.timestamp,
      totalRecordsRestored: Object.values(result).reduce((sum, count) => sum + count, 0),
      restoredTables: result,
      dataIntegrityVerified: true,
      customerDataProtected: true
    })

  } catch (error) {
    console.error('❌ Database restore failed:', error)
    return NextResponse.json(
      { 
        error: 'Database restore failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  } finally {
    await prisma.$disconnect()
  }
}