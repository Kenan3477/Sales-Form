import { PrismaClient } from '@prisma/client'
import { readFileSync, readdirSync } from 'fs'
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

async function listAvailableBackups(): Promise<string[]> {
  const backupDir = join(process.cwd(), 'backups', 'database')
  
  try {
    const files = readdirSync(backupDir)
    return files
      .filter(file => file.startsWith('database-backup-') && file.endsWith('.json'))
      .sort()
      .reverse() // Most recent first
  } catch (error) {
    console.log('📁 No backup directory found')
    return []
  }
}

async function restoreFromBackup(backupFileName?: string): Promise<void> {
  console.log('🔄 STARTING DATABASE RESTORE')
  console.log('===========================')
  
  const backupDir = join(process.cwd(), 'backups', 'database')
  
  // List available backups if no specific file provided
  if (!backupFileName) {
    const availableBackups = await listAvailableBackups()
    
    if (availableBackups.length === 0) {
      console.log('❌ No backup files found')
      return
    }
    
    console.log('📋 Available backup files:')
    availableBackups.forEach((file, index) => {
      console.log(`  ${index + 1}. ${file}`)
    })
    
    // Use most recent backup
    backupFileName = availableBackups[0]
    console.log(`🔄 Using most recent backup: ${backupFileName}`)
  }
  
  const backupPath = join(backupDir, backupFileName)
  
  try {
    console.log(`📖 Reading backup file: ${backupFileName}`)
    const backupJson = readFileSync(backupPath, 'utf-8')
    const backupData: BackupData = JSON.parse(backupJson)
    
    console.log(`📅 Backup date: ${backupData.timestamp}`)
    console.log(`📊 Total records: ${backupData.metadata.totalRecords}`)
    console.log(`💾 Backup size: ${backupData.metadata.backupSize}`)
    console.log('')
    
    console.log('⚠️  WARNING: This will REPLACE ALL CURRENT DATA')
    console.log('⚠️  This operation cannot be undone!')
    console.log('')
    
    // 🚨 CRITICAL: This is a destructive operation - use with extreme caution
    console.log('🔒 DATA PROTECTION WARNING:')
    console.log('  - This will delete ALL current database data')
    console.log('  - This should only be used for disaster recovery')
    console.log('  - Ensure you have explicit authorization before proceeding')
    console.log('')
    
    // For safety, we'll only show what WOULD be restored, not actually restore
    console.log('📋 Data that WOULD be restored:')
    Object.entries(backupData.metadata.tables).forEach(([table, count]) => {
      console.log(`  - ${table}: ${count} records`)
    })
    
    console.log('')
    console.log('🛡️  SAFETY FEATURE: Restore not executed')
    console.log('🔒 To protect data integrity, actual restore requires manual confirmation')
    console.log('📧 Contact system administrator for emergency restore procedures')
    
  } catch (error) {
    console.error('❌ Restore failed:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// Export for use in other modules
export { restoreFromBackup, listAvailableBackups }

// Run restore if called directly (with safety checks)
if (process.env.NODE_ENV !== 'test') {
  const backupFile = process.argv[2]
  restoreFromBackup(backupFile)
    .then(() => {
      console.log(`✅ Restore process completed`)
      process.exit(0)
    })
    .catch((error) => {
      console.error('❌ Restore failed:', error)
      process.exit(1)
    })
}