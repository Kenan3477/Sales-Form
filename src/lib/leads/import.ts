import { prisma } from '@/lib/prisma'
import { LeadStatus } from '@prisma/client'

export interface LeadData {
  customerFirstName: string
  customerLastName: string
  title?: string
  phoneNumber: string
  email: string
  mailingStreet?: string
  mailingCity?: string
  mailingProvince?: string
  mailingPostalCode?: string
  notes?: string
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected?: number
  totalPlanCost: number
  appliances: Array<{
    applianceType: string
    brand?: string
    model?: string
    age?: number
    price: number
  }>
  assignedAgentEmail?: string
  assignedAgentId?: string
}

export interface ImportResult {
  success: boolean
  batchId: string
  totalRows: number
  successfulRows: number
  failedRows: number
  errors: Array<{
    row: number
    data: any
    reason: string
  }>
}

export class LeadImportService {
  /**
   * Import leads from CSV data
   */
  async importLeads(
    csvData: any[],
    filename: string,
    importedBy: string
  ): Promise<ImportResult> {
    const batchId = `batch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    const errors: ImportResult['errors'] = []
    const successfulLeads: any[] = []

    // Create import batch
    const importBatch = await prisma.leadImportBatch.create({
      data: {
        id: batchId,
        filename,
        importedBy,
        totalRows: csvData.length,
        successfulRows: 0,
        failedRows: 0
      }
    })

    // Get all agents for round-robin assignment
    const agents = await prisma.user.findMany({
      where: { role: 'AGENT' },
      orderBy: { createdAt: 'asc' }
    })

    let agentIndex = 0

    for (let i = 0; i < csvData.length; i++) {
      const row = csvData[i]
      
      try {
        // Validate required fields
        const leadData = await this.validateAndTransformRow(row, agents)
        
        // Assign agent (round-robin if not specified)
        if (!leadData.assignedAgentId && agents.length > 0) {
          leadData.assignedAgentId = agents[agentIndex % agents.length].id
          agentIndex++
        }

        successfulLeads.push({
          ...leadData,
          importBatchId: batchId,
          createdBy: importedBy,
          source: `import:${filename}`
        })

      } catch (error) {
        errors.push({
          row: i + 1,
          data: row,
          reason: error instanceof Error ? error.message : 'Unknown error'
        })
      }
    }

    // Bulk insert successful leads
    if (successfulLeads.length > 0) {
      await prisma.$transaction(async (tx) => {
        for (const leadData of successfulLeads) {
          const { appliances, ...lead } = leadData
          
          const createdLead = await tx.lead.create({
            data: lead
          })

          if (appliances && appliances.length > 0) {
            await tx.leadAppliance.createMany({
              data: appliances.map((appliance: any) => ({
                ...appliance,
                leadId: createdLead.id
              }))
            })
          }
        }
      })
    }

    // Update batch with final counts
    await prisma.leadImportBatch.update({
      where: { id: batchId },
      data: {
        successfulRows: successfulLeads.length,
        failedRows: errors.length,
        errorReportLocation: errors.length > 0 ? `errors/${batchId}.json` : null
      }
    })

    // Store error report if needed
    if (errors.length > 0) {
      // In production, save to file storage (S3, local storage, etc.)
      console.log(`Import errors for batch ${batchId}:`, errors)
    }

    return {
      success: true,
      batchId,
      totalRows: csvData.length,
      successfulRows: successfulLeads.length,
      failedRows: errors.length,
      errors
    }
  }

  /**
   * Validate and transform a CSV row into LeadData
   */
  private async validateAndTransformRow(row: any, agents: any[]): Promise<LeadData> {
    // Basic validation
    if (!row.customer_first_name && !row.first_name && !row.customerFirstName) {
      throw new Error('First name is required')
    }
    if (!row.customer_last_name && !row.last_name && !row.customerLastName) {
      throw new Error('Last name is required')
    }
    if (!row.phone_number && !row.phone && !row.phoneNumber) {
      throw new Error('Phone number is required')
    }
    if (!row.email) {
      throw new Error('Email is required')
    }

    // Normalize phone number (basic)
    const phoneNumber = (row.phone_number || row.phone || row.phoneNumber || '').toString().trim()
    if (!phoneNumber || phoneNumber.length < 10) {
      throw new Error('Valid phone number is required')
    }

    // Handle assigned agent
    let assignedAgentId: string | undefined
    if (row.assigned_agent_email || row.assignedAgentEmail) {
      const agent = agents.find(a => a.email === (row.assigned_agent_email || row.assignedAgentEmail))
      if (!agent) {
        throw new Error(`Agent with email ${row.assigned_agent_email || row.assignedAgentEmail} not found`)
      }
      assignedAgentId = agent.id
    }

    // Parse appliances (expect JSON string or individual fields)
    let appliances: LeadData['appliances'] = []
    if (row.appliances) {
      try {
        appliances = JSON.parse(row.appliances)
      } catch {
        // Fallback to individual appliance fields
        if (row.appliance_type && row.appliance_price) {
          appliances = [{
            applianceType: row.appliance_type,
            brand: row.appliance_brand,
            model: row.appliance_model,
            age: row.appliance_age ? parseInt(row.appliance_age) : undefined,
            price: parseFloat(row.appliance_price)
          }]
        }
      }
    }

    // Calculate total plan cost
    const applianceCost = appliances.reduce((sum, app) => sum + (app.price || 0), 0)
    const boilerCost = row.boiler_price ? parseFloat(row.boiler_price) : 0
    const totalPlanCost = applianceCost + boilerCost

    return {
      customerFirstName: row.customer_first_name || row.first_name || row.customerFirstName,
      customerLastName: row.customer_last_name || row.last_name || row.customerLastName,
      title: row.title,
      phoneNumber,
      email: row.email,
      mailingStreet: row.mailing_street || row.address || row.street,
      mailingCity: row.mailing_city || row.city,
      mailingProvince: row.mailing_province || row.province || row.state,
      mailingPostalCode: row.mailing_postal_code || row.postal_code || row.zip,
      notes: row.notes,
      applianceCoverSelected: appliances.length > 0,
      boilerCoverSelected: !!row.boiler_cover || !!row.boiler_price,
      boilerPriceSelected: boilerCost || undefined,
      totalPlanCost,
      appliances,
      assignedAgentId
    }
  }

  /**
   * Get import batch details
   */
  async getImportBatch(batchId: string) {
    return prisma.leadImportBatch.findUnique({
      where: { id: batchId },
      include: {
        importedByUser: {
          select: { email: true }
        },
        _count: {
          select: { leads: true }
        }
      }
    })
  }

  /**
   * Get all import batches
   */
  async getImportBatches(page: number = 1, limit: number = 20) {
    const offset = (page - 1) * limit

    const [batches, total] = await Promise.all([
      prisma.leadImportBatch.findMany({
        include: {
          importedByUser: {
            select: { email: true }
          },
          _count: {
            select: { leads: true }
          }
        },
        orderBy: { importedAt: 'desc' },
        skip: offset,
        take: limit
      }),
      prisma.leadImportBatch.count()
    ])

    return {
      batches,
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit)
    }
  }
}

export const leadImportService = new LeadImportService()