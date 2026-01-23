import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { readdirSync, readFileSync } from 'fs'
import { join } from 'path'

interface BackupFile {
  filename: string
  timestamp: string
  size: string
  records: number
  tables: Record<string, number>
}

export async function GET() {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    console.log('📋 Listing available database backups...')

    const backupDir = join(process.cwd(), 'backups', 'database')
    
    try {
      const files = readdirSync(backupDir)
        .filter((file: string) => file.startsWith('database-backup-') && file.endsWith('.json'))
        .sort()
        .reverse() // Most recent first

      const backups: BackupFile[] = []

      for (const file of files) {
        try {
          const filePath = join(backupDir, file)
          const content = readFileSync(filePath, 'utf-8')
          const backupData = JSON.parse(content)
          
          backups.push({
            filename: file,
            timestamp: backupData.timestamp,
            size: backupData.metadata?.backupSize || 'Unknown',
            records: backupData.metadata?.totalRecords || 0,
            tables: backupData.metadata?.tables || {}
          })
        } catch (error) {
          console.warn(`⚠️  Skipping corrupted backup file: ${file}`)
          continue
        }
      }

      console.log(`✅ Found ${backups.length} valid backup files`)

      return NextResponse.json({
        backups,
        count: backups.length
      })

    } catch (error) {
      console.log('📁 No backup directory found or empty')
      return NextResponse.json({
        backups: [],
        count: 0,
        message: 'No backup directory found. Run a backup first.'
      })
    }

  } catch (error) {
    console.error('❌ Failed to list backups:', error)
    return NextResponse.json(
      { error: 'Failed to list backups' },
      { status: 500 }
    )
  }
}