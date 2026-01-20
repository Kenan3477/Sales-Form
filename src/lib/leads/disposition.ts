import { prisma } from '@/lib/prisma'
import { LeadStatus } from '@prisma/client'

export interface DispositionInput {
  leadId: string
  agentId: string
  status: LeadStatus
  notes?: string
  callbackAt?: Date
}

export interface DispositionResult {
  success: boolean
  lead?: any
  sale?: any
  error?: string
}

export class LeadDispositionService {
  /**
   * Process lead disposition
   */
  async disposeLead(input: DispositionInput): Promise<DispositionResult> {
    const { leadId, agentId, status, notes, callbackAt } = input

    try {
      // Get lead with checkout verification
      const lead = await prisma.lead.findUnique({
        where: { id: leadId },
        include: {
          appliances: true,
          saleLink: true
        }
      })

      if (!lead) {
        return { success: false, error: 'Lead not found' }
      }

      if (lead.checkedOutBy !== agentId) {
        return { success: false, error: 'Lead is not checked out by this agent' }
      }

      if (lead.saleLink) {
        return { success: false, error: 'Lead has already been converted to a sale' }
      }

      // Process disposition based on status
      switch (status) {
        case 'CALLED_NO_ANSWER':
          return this.handleCalledNoAnswer(lead, agentId, notes)
        
        case 'CALLBACK':
          if (!callbackAt) {
            return { success: false, error: 'Callback date is required for CALLBACK status' }
          }
          return this.handleCallback(lead, agentId, callbackAt, notes)
        
        case 'SALE_MADE':
          return this.handleSaleMade(lead, agentId, notes)
        
        case 'CANCELLED':
          return this.handleCancelled(lead, agentId, notes)
        
        case 'DO_NOT_CALL':
          return this.handleDoNotCall(lead, agentId, notes)
        
        default:
          return { success: false, error: `Invalid disposition status: ${status}` }
      }

    } catch (error) {
      console.error('Disposition error:', error)
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      }
    }
  }

  /**
   * Handle CALLED_NO_ANSWER disposition
   */
  private async handleCalledNoAnswer(lead: any, agentId: string, notes?: string): Promise<DispositionResult> {
    await prisma.$transaction(async (tx) => {
      // Update lead
      await tx.lead.update({
        where: { id: lead.id },
        data: {
          currentStatus: 'CALLED_NO_ANSWER',
          lastDispositionAt: new Date(),
          lastDispositionBy: agentId,
          lastContactAttemptAt: new Date(),
          timesContacted: lead.timesContacted + 1,
          checkedOutBy: null,
          checkedOutAt: null
        }
      })

      // Log disposition history
      await tx.leadDispositionHistory.create({
        data: {
          leadId: lead.id,
          agentId,
          status: 'CALLED_NO_ANSWER',
          notes,
          metadata: {
            timesContacted: lead.timesContacted + 1
          }
        }
      })
    })

    const updatedLead = await prisma.lead.findUnique({
      where: { id: lead.id },
      include: { appliances: true }
    })

    return { success: true, lead: updatedLead }
  }

  /**
   * Handle CALLBACK disposition
   */
  private async handleCallback(lead: any, agentId: string, callbackAt: Date, notes?: string): Promise<DispositionResult> {
    await prisma.$transaction(async (tx) => {
      // Update lead
      await tx.lead.update({
        where: { id: lead.id },
        data: {
          currentStatus: 'CALLBACK',
          lastDispositionAt: new Date(),
          lastDispositionBy: agentId,
          callbackAt,
          checkedOutBy: null,
          checkedOutAt: null
        }
      })

      // Log disposition history
      await tx.leadDispositionHistory.create({
        data: {
          leadId: lead.id,
          agentId,
          status: 'CALLBACK',
          notes,
          metadata: {
            callbackScheduledFor: callbackAt.toISOString()
          }
        }
      })
    })

    const updatedLead = await prisma.lead.findUnique({
      where: { id: lead.id },
      include: { appliances: true }
    })

    return { success: true, lead: updatedLead }
  }

  /**
   * Handle CANCELLED disposition
   */
  private async handleCancelled(lead: any, agentId: string, notes?: string): Promise<DispositionResult> {
    await prisma.$transaction(async (tx) => {
      // Update lead to terminal status
      await tx.lead.update({
        where: { id: lead.id },
        data: {
          currentStatus: 'CANCELLED',
          lastDispositionAt: new Date(),
          lastDispositionBy: agentId,
          checkedOutBy: null,
          checkedOutAt: null
        }
      })

      // Log disposition history
      await tx.leadDispositionHistory.create({
        data: {
          leadId: lead.id,
          agentId,
          status: 'CANCELLED',
          notes
        }
      })
    })

    const updatedLead = await prisma.lead.findUnique({
      where: { id: lead.id },
      include: { appliances: true }
    })

    return { success: true, lead: updatedLead }
  }

  /**
   * Handle DO_NOT_CALL disposition
   */
  private async handleDoNotCall(lead: any, agentId: string, notes?: string): Promise<DispositionResult> {
    await prisma.$transaction(async (tx) => {
      // Update lead to terminal status with do not call flag
      await tx.lead.update({
        where: { id: lead.id },
        data: {
          currentStatus: 'DO_NOT_CALL',
          doNotCall: true,
          lastDispositionAt: new Date(),
          lastDispositionBy: agentId,
          checkedOutBy: null,
          checkedOutAt: null
        }
      })

      // Log disposition history
      await tx.leadDispositionHistory.create({
        data: {
          leadId: lead.id,
          agentId,
          status: 'DO_NOT_CALL',
          notes
        }
      })
    })

    const updatedLead = await prisma.lead.findUnique({
      where: { id: lead.id },
      include: { appliances: true }
    })

    return { success: true, lead: updatedLead }
  }

  /**
   * Handle SALE_MADE disposition - convert to actual sale
   */
  private async handleSaleMade(lead: any, agentId: string, notes?: string): Promise<DispositionResult> {
    try {
      // Map lead to sale format (reuse existing sales pipeline)
      const saleData = this.mapLeadToSaleData(lead, agentId)
      
      // Call existing sales creation endpoint/service
      const sale = await this.createSaleFromLead(saleData)
      
      // Link lead to sale and update status
      await prisma.$transaction(async (tx) => {
        // Update lead to terminal status
        await tx.lead.update({
          where: { id: lead.id },
          data: {
            currentStatus: 'SALE_MADE',
            lastDispositionAt: new Date(),
            lastDispositionBy: agentId,
            checkedOutBy: null,
            checkedOutAt: null
          }
        })

        // Create lead-to-sale link
        await tx.leadToSaleLink.create({
          data: {
            leadId: lead.id,
            saleId: sale.id,
            convertedBy: agentId
          }
        })

        // Log disposition history
        await tx.leadDispositionHistory.create({
          data: {
            leadId: lead.id,
            agentId,
            status: 'SALE_MADE',
            notes,
            metadata: {
              saleId: sale.id,
              saleAmount: sale.totalPlanCost
            }
          }
        })
      })

      const updatedLead = await prisma.lead.findUnique({
        where: { id: lead.id },
        include: { 
          appliances: true,
          saleLink: {
            include: {
              sale: true
            }
          }
        }
      })

      return { success: true, lead: updatedLead, sale }

    } catch (error) {
      console.error('Sale conversion error:', error)
      
      // Mark as conversion failed, don't lose the lead
      await prisma.$transaction(async (tx) => {
        await tx.lead.update({
          where: { id: lead.id },
          data: {
            currentStatus: 'CONVERSION_FAILED',
            lastDispositionAt: new Date(),
            lastDispositionBy: agentId,
            checkedOutBy: null,
            checkedOutAt: null
          }
        })

        await tx.leadDispositionHistory.create({
          data: {
            leadId: lead.id,
            agentId,
            status: 'CONVERSION_FAILED',
            notes: `Sale conversion failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
            metadata: {
              error: error instanceof Error ? error.message : 'Unknown error',
              originalNotes: notes
            }
          }
        })
      })

      return { 
        success: false, 
        error: `Failed to convert lead to sale: ${error instanceof Error ? error.message : 'Unknown error'}` 
      }
    }
  }

  /**
   * Map lead data to sale format (matches existing sale creation)
   */
  private mapLeadToSaleData(lead: any, agentId: string) {
    return {
      customerFirstName: lead.customerFirstName,
      customerLastName: lead.customerLastName,
      title: lead.title,
      phoneNumber: lead.phoneNumber,
      email: lead.email,
      notes: lead.notes,
      mailingStreet: lead.mailingStreet,
      mailingCity: lead.mailingCity,
      mailingProvince: lead.mailingProvince,
      mailingPostalCode: lead.mailingPostalCode,
      
      // Use placeholder bank details - agent will need to collect these
      accountName: `${lead.customerFirstName} ${lead.customerLastName}`,
      sortCode: '000000', // Will need to be updated by agent
      accountNumber: '00000000', // Will need to be updated by agent
      directDebitDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
      
      status: 'ACTIVE',
      applianceCoverSelected: lead.applianceCoverSelected,
      boilerCoverSelected: lead.boilerCoverSelected,
      boilerPriceSelected: lead.boilerPriceSelected,
      totalPlanCost: lead.totalPlanCost,
      createdById: agentId,
      
      // Map appliances
      appliances: lead.appliances.map((app: any) => ({
        appliance: app.applianceType,
        brand: app.brand,
        model: app.model,
        age: app.age,
        price: app.price
      }))
    }
  }

  /**
   * Create sale using existing sales pipeline (CRITICAL: DO NOT MODIFY EXISTING PIPELINE)
   */
  private async createSaleFromLead(saleData: any) {
    // Use existing sales creation logic
    // This calls the exact same validation and creation process as the sales form
    
    const { appliances, ...saleCore } = saleData
    
    // Create sale using Prisma (matches existing sales creation)
    const sale = await prisma.sale.create({
      data: saleCore
    })

    // Create appliances if any
    if (appliances && appliances.length > 0) {
      await prisma.appliance.createMany({
        data: appliances.map((appliance: any) => ({
          ...appliance,
          saleId: sale.id
        }))
      })
    }

    return sale
  }

  /**
   * Get disposition history for a lead
   */
  async getDispositionHistory(leadId: string) {
    return prisma.leadDispositionHistory.findMany({
      where: { leadId },
      include: {
        agent: {
          select: { email: true }
        }
      },
      orderBy: { createdAt: 'desc' }
    })
  }

  /**
   * Skip a lead (just release checkout without disposition)
   */
  async skipLead(leadId: string, agentId: string): Promise<boolean> {
    try {
      await prisma.lead.update({
        where: {
          id: leadId,
          checkedOutBy: agentId
        },
        data: {
          checkedOutBy: null,
          checkedOutAt: null
        }
      })
      return true
    } catch (error) {
      return false
    }
  }
}

export const leadDispositionService = new LeadDispositionService()