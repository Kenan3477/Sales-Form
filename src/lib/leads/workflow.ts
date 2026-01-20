import { prisma } from '@/lib/prisma'
import { LeadStatus } from '@prisma/client'

export interface LeadWorkflowOptions {
  agentId: string
  includeCallbacks?: boolean
  prioritizeCallbacks?: boolean
}

export interface NextLeadResult {
  lead: any | null
  hasMore: boolean
  totalAssigned: number
  totalCallbacks: number
}

export class LeadWorkflowService {
  /**
   * Get the next lead for an agent to work on
   */
  async getNextLead(options: LeadWorkflowOptions): Promise<NextLeadResult> {
    const { agentId, includeCallbacks = true, prioritizeCallbacks = true } = options

    // Clean up stale checkouts (older than 30 minutes)
    await this.cleanupStaleCheckouts()

    // Get counts for dashboard
    const [totalAssigned, totalCallbacks] = await Promise.all([
      this.getTotalAssignedLeads(agentId),
      this.getTotalCallbacks(agentId)
    ])

    let lead = null

    // Try to get callback leads first if prioritized
    if (includeCallbacks && prioritizeCallbacks) {
      lead = await this.getNextCallbackLead(agentId)
    }

    // If no callback lead, get next regular lead
    if (!lead) {
      lead = await this.getNextRegularLead(agentId)
    }

    // If still no lead and callbacks not prioritized, try callbacks
    if (!lead && includeCallbacks && !prioritizeCallbacks) {
      lead = await this.getNextCallbackLead(agentId)
    }

    // Check if there are more leads available
    const hasMore = await this.hasMoreLeads(agentId)

    return {
      lead,
      hasMore,
      totalAssigned,
      totalCallbacks
    }
  }

  /**
   * Get a callback lead that's due
   */
  private async getNextCallbackLead(agentId: string) {
    const now = new Date()
    
    return prisma.lead.findFirst({
      where: {
        assignedAgentId: agentId,
        currentStatus: 'CALLBACK',
        callbackAt: {
          lte: now
        },
        checkedOutBy: null,
        doNotCall: false
      },
      include: {
        appliances: true,
        dispositionHistory: {
          orderBy: { createdAt: 'desc' },
          take: 3
        }
      },
      orderBy: {
        callbackAt: 'asc'
      }
    })
  }

  /**
   * Get next regular lead (non-callback)
   */
  private async getNextRegularLead(agentId: string) {
    const nonTerminalStatuses: LeadStatus[] = ['NEW', 'CALLED_NO_ANSWER']
    
    return prisma.lead.findFirst({
      where: {
        assignedAgentId: agentId,
        currentStatus: {
          in: nonTerminalStatuses
        },
        checkedOutBy: null,
        doNotCall: false
      },
      include: {
        appliances: true,
        dispositionHistory: {
          orderBy: { createdAt: 'desc' },
          take: 3
        }
      },
      orderBy: [
        { lastContactAttemptAt: 'asc' }, // Older attempts first
        { createdAt: 'asc' } // Older leads first
      ]
    })
  }

  /**
   * Check out a lead for an agent
   */
  async checkoutLead(leadId: string, agentId: string): Promise<boolean> {
    try {
      await prisma.lead.update({
        where: {
          id: leadId,
          checkedOutBy: null // Only checkout if not already checked out
        },
        data: {
          checkedOutBy: agentId,
          checkedOutAt: new Date()
        }
      })
      return true
    } catch (error) {
      // Lead was already checked out by someone else
      return false
    }
  }

  /**
   * Release a checked-out lead
   */
  async releaseLead(leadId: string, agentId: string): Promise<boolean> {
    try {
      await prisma.lead.update({
        where: {
          id: leadId,
          checkedOutBy: agentId // Only release if checked out by this agent
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

  /**
   * Get lead with checkout attempt
   */
  async getLeadWithCheckout(leadId: string, agentId: string) {
    const lead = await prisma.lead.findUnique({
      where: { id: leadId },
      include: {
        appliances: true,
        dispositionHistory: {
          orderBy: { createdAt: 'desc' },
          take: 5
        },
        assignedAgent: {
          select: { email: true }
        }
      }
    })

    if (!lead) return null

    // Check if lead is available for checkout
    if (lead.checkedOutBy && lead.checkedOutBy !== agentId) {
      // Check if checkout is stale (older than 30 minutes)
      const checkoutAge = lead.checkedOutAt ? 
        Date.now() - lead.checkedOutAt.getTime() : 
        Infinity

      if (checkoutAge < 30 * 60 * 1000) { // 30 minutes
        throw new Error('Lead is currently being worked on by another agent')
      }
    }

    // Attempt checkout
    const checkedOut = await this.checkoutLead(leadId, agentId)
    if (!checkedOut) {
      throw new Error('Unable to checkout lead')
    }

    return lead
  }

  /**
   * Get total assigned leads for agent
   */
  async getTotalAssignedLeads(agentId: string): Promise<number> {
    return prisma.lead.count({
      where: {
        assignedAgentId: agentId,
        currentStatus: {
          notIn: ['SALE_MADE', 'CANCELLED', 'DO_NOT_CALL']
        },
        doNotCall: false
      }
    })
  }

  /**
   * Get total callbacks due for agent
   */
  async getTotalCallbacks(agentId: string): Promise<number> {
    return prisma.lead.count({
      where: {
        assignedAgentId: agentId,
        currentStatus: 'CALLBACK',
        callbackAt: {
          lte: new Date()
        },
        doNotCall: false
      }
    })
  }

  /**
   * Check if agent has more leads available
   */
  async hasMoreLeads(agentId: string): Promise<boolean> {
    const count = await prisma.lead.count({
      where: {
        assignedAgentId: agentId,
        currentStatus: {
          notIn: ['SALE_MADE', 'CANCELLED', 'DO_NOT_CALL']
        },
        checkedOutBy: null,
        doNotCall: false
      },
      take: 1
    })

    return count > 0
  }

  /**
   * Clean up stale checkouts (older than 30 minutes)
   */
  async cleanupStaleCheckouts(): Promise<number> {
    const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000)
    
    const result = await prisma.lead.updateMany({
      where: {
        checkedOutAt: {
          lt: thirtyMinutesAgo
        },
        checkedOutBy: {
          not: null
        }
      },
      data: {
        checkedOutBy: null,
        checkedOutAt: null
      }
    })

    return result.count
  }

  /**
   * Get lead statistics for agent dashboard
   */
  async getLeadStats(agentId: string) {
    const [
      totalAssigned,
      newLeads,
      callbacksDue,
      callbacksScheduled,
      noAnswers,
      totalContacted
    ] = await Promise.all([
      this.getTotalAssignedLeads(agentId),
      prisma.lead.count({
        where: {
          assignedAgentId: agentId,
          currentStatus: 'NEW',
          doNotCall: false
        }
      }),
      this.getTotalCallbacks(agentId),
      prisma.lead.count({
        where: {
          assignedAgentId: agentId,
          currentStatus: 'CALLBACK',
          callbackAt: {
            gt: new Date()
          },
          doNotCall: false
        }
      }),
      prisma.lead.count({
        where: {
          assignedAgentId: agentId,
          currentStatus: 'CALLED_NO_ANSWER',
          doNotCall: false
        }
      }),
      prisma.lead.count({
        where: {
          assignedAgentId: agentId,
          currentStatus: {
            in: ['CALLED_NO_ANSWER', 'CALLBACK', 'SALE_MADE', 'CANCELLED']
          }
        }
      })
    ])

    return {
      totalAssigned,
      newLeads,
      callbacksDue,
      callbacksScheduled,
      noAnswers,
      totalContacted
    }
  }
}

export const leadWorkflowService = new LeadWorkflowService()