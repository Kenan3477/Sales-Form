import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    console.log('🔧 Manual backup requested by:', session.user.email)

    // Create backup directory if it doesn't exist
    const backupDir = path.join(process.cwd(), 'backups')
    try {
      await fs.access(backupDir)
    } catch {
      await fs.mkdir(backupDir, { recursive: true })
      console.log('📁 Created backup directory')
    }

    // Generate backup filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5)
    const backupName = `manual-backup-${timestamp}.sql`
    const backupPath = path.join(backupDir, backupName)

    // Get database URL from environment
    const databaseUrl = process.env.DATABASE_URL
    if (!databaseUrl) {
      throw new Error('DATABASE_URL not configured')
    }

    // Parse database URL to get connection details
    const url = new URL(databaseUrl)
    const dbName = url.pathname.slice(1)
    const host = url.hostname
    const port = url.port || '5432'
    const username = url.username
    const password = url.password

    console.log(`🗄️ Creating backup: ${backupName}`)

    // Create PostgreSQL dump
    const pgDumpCommand = `PGPASSWORD="${password}" pg_dump -h "${host}" -p ${port} -U "${username}" -d "${dbName}" --verbose --clean --no-owner --no-acl --format=plain`

    const { stdout, stderr } = await execAsync(`${pgDumpCommand} > "${backupPath}"`)
    
    if (stderr && !stderr.includes('NOTICE:')) {
      console.warn('pg_dump warnings:', stderr)
    }

    // Verify backup was created and has content
    const stats = await fs.stat(backupPath)
    if (stats.size === 0) {
      throw new Error('Backup file is empty')
    }

    console.log(`✅ Manual backup created successfully: ${backupName} (${Math.round(stats.size / 1024)} KB)`)

    // Create backup metadata
    const metadataPath = path.join(backupDir, `${backupName}.meta.json`)
    const metadata = {
      type: 'manual',
      created: new Date().toISOString(),
      size: stats.size,
      createdBy: session.user.email,
      description: 'Manual backup created via admin interface'
    }

    await fs.writeFile(metadataPath, JSON.stringify(metadata, null, 2))

    return NextResponse.json({
      success: true,
      message: 'Backup created successfully',
      backupName: backupName,
      size: stats.size,
      created: new Date().toISOString()
    })

  } catch (error) {
    console.error('❌ Manual backup failed:', error)
    
    return NextResponse.json({
      error: 'Backup creation failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}