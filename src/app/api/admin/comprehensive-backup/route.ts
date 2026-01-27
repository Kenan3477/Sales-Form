import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
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

interface ComprehensiveBackupData {
  timestamp: string
  version: string
  backupType: 'comprehensive'
  createdBy: string
  reason: string
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
    dataIntegrityHashes: {
      users: string
      sales: string
      appliances: string
      leads: string
      smsLogs: string
      generatedDocuments: string
    }
    communicationSummary: {
      totalSMS: number
      totalDocuments: number
      smsSuccessRate: number
      documentsGenerated: number
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

    console.log('🔄 COMPREHENSIVE BACKUP REQUESTED')
    console.log('=================================')
    console.log(`👤 Requested by: ${session.user.email}`)

    // Parse request body for backup reason
    const body = await request.json().catch(() => ({}))
    const reason = body.reason || 'Manual comprehensive backup'

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const backupDir = join(process.cwd(), 'backups', 'comprehensive')
    
    // Ensure backup directory exists
    if (!existsSync(backupDir)) {
      mkdirSync(backupDir, { recursive: true })
      console.log('📁 Created comprehensive backup directory:', backupDir)
    }

    console.log('📊 Fetching ALL database tables and communication data...')
    
    // Fetch all data with comprehensive relationships
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
      // Users (anonymize passwords)
      prisma.user.findMany().then(users => users.map(user => ({
        ...user,
        password: '[ENCRYPTED]' // Security: Don't backup actual passwords
      }))),
      
      // Sales with full appliances relationship
      prisma.sale.findMany({ 
        include: { 
          appliances: true,
          smsLogs: true,
          generatedDocuments: {
            include: {
              template: {
                select: {
                  name: true,
                  templateType: true
                }
              }
            }
          }
        } 
      }),
      
      prisma.appliance.findMany(),
      prisma.fieldConfiguration.findMany(),
      prisma.documentTemplate.findMany(),
      
      // Include template relationships for documents
      prisma.generatedDocument.findMany({
        include: {
          template: {
            select: {
              name: true,
              templateType: true,
              description: true
            }
          },
          sale: {
            select: {
              customerFirstName: true,
              customerLastName: true,
              email: true
            }
          }
        }
      }),
      
      // SMS Logs with sale relationship
      prisma.sMSLog.findMany({
        include: {
          sale: {
            select: {
              customerFirstName: true,
              customerLastName: true,
              email: true,
              phoneNumber: true
            }
          }
        }
      }),
      
      // Leads with comprehensive relationships
      prisma.lead.findMany({ 
        include: { 
          appliances: true,
          dispositionHistory: {
            include: {
              agent: {
                select: {
                  email: true
                }
              }
            }
          }
        } 
      }),
      
      prisma.leadAppliance.findMany(),
      prisma.leadDispositionHistory.findMany({
        include: {
          agent: {
            select: {
              email: true
            }
          }
        }
      }),
      
      prisma.leadToSaleLink.findMany({
        include: {
          convertedByUser: {
            select: {
              email: true
            }
          }
        }
      }),
      
      prisma.leadImportBatch.findMany({
        include: {
          importedByUser: {
            select: {
              email: true
            }
          }
        }
      })
    ])

    console.log('📈 Calculating communication metrics...')
    
    // Calculate communication summary
    const totalSMS = smsLogs.length
    const successfulSMS = smsLogs.filter(sms => sms.smsStatus === 'SENT').length
    const smsSuccessRate = totalSMS > 0 ? (successfulSMS / totalSMS) * 100 : 0
    const documentsGenerated = generatedDocuments.length

    // 🔒 Generate integrity hashes for all critical data
    const dataIntegrityHashes = {
      users: generateDataHash(users.map(u => ({ id: u.id, email: u.email, role: u.role }))),
      sales: generateDataHash(sales.map(sale => ({
        id: sale.id,
        customerFirstName: sale.customerFirstName,
        customerLastName: sale.customerLastName,
        email: sale.email,
        phoneNumber: sale.phoneNumber,
        totalPlanCost: sale.totalPlanCost
      }))),
      appliances: generateDataHash(appliances),
      leads: generateDataHash(leads.map(lead => ({
        id: lead.id,
        customerFirstName: lead.customerFirstName,
        customerLastName: lead.customerLastName,
        email: lead.email,
        phoneNumber: lead.phoneNumber
      }))),
      smsLogs: generateDataHash(smsLogs.map(sms => ({
        id: sms.id,
        phoneNumber: sms.phoneNumber,
        smsStatus: sms.smsStatus,
        messageContent: sms.messageContent
      }))),
      generatedDocuments: generateDataHash(generatedDocuments.map(doc => ({
        id: doc.id,
        filename: doc.filename,
        templateId: doc.templateId
      })))
    }

    const backupData: ComprehensiveBackupData = {
      timestamp: new Date().toISOString(),
      version: '3.0.0',
      backupType: 'comprehensive',
      createdBy: session.user.email,
      reason: reason,
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
        },
        dataIntegrityHashes,
        communicationSummary: {
          totalSMS,
          totalDocuments: documentsGenerated,
          smsSuccessRate: Math.round(smsSuccessRate * 100) / 100,
          documentsGenerated
        }
      }
    }
    
    // Write backup file
    const backupFileName = `comprehensive-backup-${timestamp}.json`
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
    
    console.log('✅ COMPREHENSIVE BACKUP COMPLETE')
    console.log('================================')
    console.log(`📁 Backup file: ${backupFileName}`)
    console.log(`💾 File size: ${fileSizeInMB}MB`)
    console.log(`📊 Total records: ${backupData.metadata.totalRecords}`)
    console.log('')
    console.log('📋 Table breakdown:')
    Object.entries(backupData.metadata.tables).forEach(([table, count]) => {
      console.log(`  - ${table}: ${count} records`)
    })
    console.log('')
    console.log('📞 Communication Summary:')
    console.log(`  - SMS Messages: ${totalSMS} (${smsSuccessRate.toFixed(1)}% success rate)`)
    console.log(`  - Documents Generated: ${documentsGenerated}`)
    console.log('')
    console.log('🔒 All customer data and communication history backed up safely')

    return NextResponse.json({
      success: true,
      message: 'Comprehensive backup created successfully',
      backupFileName,
      backupPath,
      fileSize: fileSizeInMB + 'MB',
      totalRecords: backupData.metadata.totalRecords,
      communicationSummary: backupData.metadata.communicationSummary,
      tables: backupData.metadata.tables,
      timestamp: backupData.timestamp
    })

  } catch (error) {
    console.error('❌ Comprehensive backup failed:', error)
    
    return NextResponse.json({
      error: 'Comprehensive backup creation failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  } finally {
    await prisma.$disconnect()
  }
}

export async function GET() {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    console.log('📋 Listing comprehensive backups...')
    
    const backupDir = join(process.cwd(), 'backups', 'comprehensive')
    
    if (!existsSync(backupDir)) {
      return NextResponse.json({
        success: true,
        backups: [],
        message: 'No comprehensive backups found - directory does not exist'
      })
    }

    const fs = require('fs')
    const files = fs.readdirSync(backupDir)
      .filter((file: string) => file.startsWith('comprehensive-backup-') && file.endsWith('.json'))
      .sort()
      .reverse() // Most recent first

    const backups = []

    for (const file of files) {
      try {
        const filePath = join(backupDir, file)
        const content = fs.readFileSync(filePath, 'utf-8')
        const backupData = JSON.parse(content)
        
        backups.push({
          filename: file,
          timestamp: backupData.timestamp,
          size: backupData.metadata?.backupSize || 'Unknown',
          records: backupData.metadata?.totalRecords || 0,
          tables: backupData.metadata?.tables || {},
          communicationSummary: backupData.metadata?.communicationSummary || {},
          createdBy: backupData.createdBy || 'Unknown',
          reason: backupData.reason || 'No reason provided'
        })
      } catch (error) {
        console.warn(`Error reading backup file ${file}:`, error)
        // Add as corrupted backup
        backups.push({
          filename: file,
          timestamp: 'Unknown',
          size: 'Unknown',
          records: 0,
          corrupted: true
        })
      }
    }

    return NextResponse.json({
      success: true,
      backups,
      count: backups.length
    })

  } catch (error) {
    console.error('Error listing comprehensive backups:', error)
    
    return NextResponse.json({
      error: 'Failed to list comprehensive backups',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}