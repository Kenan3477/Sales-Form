import { prisma } from '@/lib/prisma'
import { LeadStatus } from '@prisma/client'

// Campaign configuration types
export interface CampaignSettings {
  id?: string
  name: string
  description?: string
  isActive: boolean
  
  // Dialing strategy configuration
  dialingStrategy: 'ROUND_ROBIN' | 'PRIORITY_BASED' | 'SKILL_BASED' | 'LOAD_BALANCED'
  
  // Priority rules
  priorityRules: {
    callbackPriority: number // 1-10 (10 = highest)
    newLeadPriority: number
    noAnswerRetryPriority: number
    timeSinceLastContactWeight: number // Hours multiplier
    maxContactAttempts: number
  }
  
  // Frequency controls
  frequencySettings: {
    minTimeBetweenCalls: number // Minutes
    maxDailyAttempts: number
    retrySchedule: {
      firstRetry: number // Hours
      subsequentRetries: number[] // Hours array
    }
    respectDoNotCallTimes: boolean
    doNotCallHours: {
      start: string // "09:00"
      end: string   // "17:00"
    }
  }
  
  // Agent assignment rules
  agentAssignment: {
    useSkillMatching: boolean
    maxSimultaneousLeads: number
    allowReassignment: boolean
    reassignmentCriteria: {
      noContactAfterHours: number
      maxAttemptsBeforeReassign: number
    }
  }
  
  // Lead filtering
  leadFilters: {
    includeStatuses: LeadStatus[]
    excludeStatuses: LeadStatus[]
    timezoneRespect: boolean
    leadAgeLimit: number // Days
  }
  
  createdAt?: Date
  updatedAt?: Date
  createdBy: string
}

// Campaign metrics and analytics
export interface CampaignMetrics {
  campaignId: string
  periodStart: Date
  periodEnd: Date
  
  totalLeadsProcessed: number
  successfulConnections: number
  salesMade: number
  callbacksScheduled: number
  doNotCallRequests: number
  
  averageCallsPerLead: number
  conversionRate: number
  averageTimeToContact: number // Hours
  
  agentPerformance: {
    agentId: string
    leadsProcessed: number
    salesMade: number
    averageCallDuration: number
    conversionRate: number
  }[]
}

// Queue optimization result
export interface QueueOptimizationResult {
  optimizedQueue: {
    leadId: string
    agentId: string
    priority: number
    scheduledTime: Date
    reason: string
  }[]
  
  metrics: {
    totalLeadsQueued: number
    averagePriority: number
    estimatedCompletionTime: Date
    agentDistribution: Record<string, number>
  }
}

export class CampaignManagementService {
  /**
   * Create or update campaign settings
   */
  async saveCampaignSettings(settings: CampaignSettings): Promise<CampaignSettings> {
    const campaignData = {
      name: settings.name,
      description: settings.description,
      isActive: settings.isActive,
      settings: settings as any, // Store entire settings object as JSON
      createdBy: settings.createdBy,
      updatedAt: new Date()
    }

    if (settings.id) {
      // Update existing campaign
      const campaign = await prisma.campaignSettings.update({
        where: { id: settings.id },
        data: campaignData
      })
      return { ...settings, id: campaign.id, updatedAt: campaign.updatedAt }
    } else {
      // Create new campaign
      const campaign = await prisma.campaignSettings.create({
        data: {
          ...campaignData,
          createdAt: new Date()
        }
      })
      return { ...settings, id: campaign.id, createdAt: campaign.createdAt, updatedAt: campaign.updatedAt }
    }
  }

  /**
   * Get campaign settings
   */
  async getCampaignSettings(campaignId?: string): Promise<CampaignSettings | null> {
    let campaign

    if (campaignId) {
      campaign = await prisma.campaignSettings.findUnique({
        where: { id: campaignId }
      })
    } else {
      // Get active campaign
      campaign = await prisma.campaignSettings.findFirst({
        where: { isActive: true },
        orderBy: { updatedAt: 'desc' }
      })
    }

    if (!campaign) return null

    return {
      id: campaign.id,
      ...(campaign.settings as any),
      createdAt: campaign.createdAt,
      updatedAt: campaign.updatedAt
    }
  }

  /**
   * List all campaigns
   */
  async listCampaigns(): Promise<CampaignSettings[]> {
    const campaigns = await prisma.campaignSettings.findMany({
      orderBy: { updatedAt: 'desc' }
    })

    return campaigns.map(campaign => ({
      id: campaign.id,
      ...(campaign.settings as any),
      createdAt: campaign.createdAt,
      updatedAt: campaign.updatedAt
    }))
  }

  /**
   * Optimize queue based on campaign settings
   */
  async optimizeQueue(campaignId?: string, agentIds?: string[]): Promise<QueueOptimizationResult> {
    const campaign = await this.getCampaignSettings(campaignId)
    if (!campaign) {
      throw new Error('No active campaign found')
    }

    // Get available agents
    const agents = await prisma.user.findMany({
      where: {
        role: 'AGENT',
        ...(agentIds ? { id: { in: agentIds } } : {})
      }
    })

    // Get leads that need to be processed
    const leads = await this.getLeadsForProcessing(campaign)

    // Apply optimization algorithm
    const optimizedQueue = this.applyOptimizationStrategy(leads, agents, campaign)

    // Calculate metrics
    const metrics = this.calculateQueueMetrics(optimizedQueue, agents)

    return {
      optimizedQueue,
      metrics
    }
  }

  /**
   * Get leads ready for processing based on campaign rules
   */
  private async getLeadsForProcessing(campaign: CampaignSettings) {
    const now = new Date()
    const leadAgeLimit = new Date(now.getTime() - (campaign.leadFilters.leadAgeLimit * 24 * 60 * 60 * 1000))

    return prisma.lead.findMany({
      where: {
        currentStatus: {
          in: campaign.leadFilters.includeStatuses,
          notIn: campaign.leadFilters.excludeStatuses
        },
        doNotCall: false,
        createdAt: { gte: leadAgeLimit },
        checkedOutBy: null,
        OR: [
          // New leads
          { currentStatus: 'NEW' },
          // Callbacks that are due
          {
            currentStatus: 'CALLBACK',
            callbackAt: { lte: now }
          },
          // No answer leads ready for retry
          {
            currentStatus: 'CALLED_NO_ANSWER',
            lastContactAttemptAt: {
              lte: new Date(now.getTime() - (campaign.frequencySettings.minTimeBetweenCalls * 60 * 1000))
            },
            timesContacted: { lt: campaign.priorityRules.maxContactAttempts }
          }
        ]
      },
      include: {
        appliances: true,
        dispositionHistory: {
          orderBy: { createdAt: 'desc' },
          take: 5
        }
      },
      orderBy: { createdAt: 'asc' }
    })
  }

  /**
   * Apply optimization strategy to leads and agents
   */
  private applyOptimizationStrategy(leads: any[], agents: any[], campaign: CampaignSettings) {
    const queue: QueueOptimizationResult['optimizedQueue'] = []
    const now = new Date()

    // Calculate priority for each lead
    const prioritizedLeads = leads.map(lead => ({
      ...lead,
      calculatedPriority: this.calculateLeadPriority(lead, campaign, now)
    }))

    // Sort by priority
    prioritizedLeads.sort((a, b) => b.calculatedPriority - a.calculatedPriority)

    // Assign leads to agents based on strategy
    switch (campaign.dialingStrategy) {
      case 'ROUND_ROBIN':
        this.assignRoundRobin(prioritizedLeads, agents, campaign, queue, now)
        break
      case 'PRIORITY_BASED':
        this.assignPriorityBased(prioritizedLeads, agents, campaign, queue, now)
        break
      case 'SKILL_BASED':
        this.assignSkillBased(prioritizedLeads, agents, campaign, queue, now)
        break
      case 'LOAD_BALANCED':
        this.assignLoadBalanced(prioritizedLeads, agents, campaign, queue, now)
        break
    }

    return queue
  }

  /**
   * Calculate lead priority based on campaign rules
   */
  private calculateLeadPriority(lead: any, campaign: CampaignSettings, now: Date): number {
    let priority = 0

    // Base priority by status
    switch (lead.currentStatus) {
      case 'CALLBACK':
        priority += campaign.priorityRules.callbackPriority * 10
        break
      case 'NEW':
        priority += campaign.priorityRules.newLeadPriority * 10
        break
      case 'CALLED_NO_ANSWER':
        priority += campaign.priorityRules.noAnswerRetryPriority * 10
        break
    }

    // Time since last contact weight
    if (lead.lastContactAttemptAt) {
      const hoursSinceLastContact = (now.getTime() - lead.lastContactAttemptAt.getTime()) / (1000 * 60 * 60)
      priority += hoursSinceLastContact * campaign.priorityRules.timeSinceLastContactWeight
    }

    // Callback urgency (overdue callbacks get higher priority)
    if (lead.currentStatus === 'CALLBACK' && lead.callbackAt) {
      const hoursOverdue = (now.getTime() - lead.callbackAt.getTime()) / (1000 * 60 * 60)
      if (hoursOverdue > 0) {
        priority += hoursOverdue * 5 // Bonus for overdue callbacks
      }
    }

    // Lead age factor (older leads get slight priority boost)
    const leadAgeHours = (now.getTime() - lead.createdAt.getTime()) / (1000 * 60 * 60)
    priority += leadAgeHours * 0.1

    return Math.max(0, priority)
  }

  /**
   * Round Robin assignment strategy
   */
  private assignRoundRobin(leads: any[], agents: any[], campaign: CampaignSettings, queue: any[], now: Date) {
    let agentIndex = 0
    const agentLoadCount = agents.reduce((acc, agent) => {
      acc[agent.id] = 0
      return acc
    }, {} as Record<string, number>)

    for (const lead of leads) {
      const agent = agents[agentIndex % agents.length]
      
      if (agentLoadCount[agent.id] < campaign.agentAssignment.maxSimultaneousLeads) {
        queue.push({
          leadId: lead.id,
          agentId: agent.id,
          priority: lead.calculatedPriority,
          scheduledTime: this.calculateScheduledTime(lead, campaign, now),
          reason: `Round robin assignment (Priority: ${lead.calculatedPriority.toFixed(1)})`
        })
        agentLoadCount[agent.id]++
      }
      
      agentIndex++
    }
  }

  /**
   * Priority-based assignment strategy
   */
  private assignPriorityBased(leads: any[], agents: any[], campaign: CampaignSettings, queue: any[], now: Date) {
    const agentLoadCount = agents.reduce((acc, agent) => {
      acc[agent.id] = 0
      return acc
    }, {} as Record<string, number>)

    // Assign highest priority leads first
    for (const lead of leads) {
      // Find agent with lowest current load
      const availableAgent = agents
        .filter(agent => agentLoadCount[agent.id] < campaign.agentAssignment.maxSimultaneousLeads)
        .sort((a, b) => agentLoadCount[a.id] - agentLoadCount[b.id])[0]

      if (availableAgent) {
        queue.push({
          leadId: lead.id,
          agentId: availableAgent.id,
          priority: lead.calculatedPriority,
          scheduledTime: this.calculateScheduledTime(lead, campaign, now),
          reason: `Priority-based assignment (Priority: ${lead.calculatedPriority.toFixed(1)})`
        })
        agentLoadCount[availableAgent.id]++
      }
    }
  }

  /**
   * Skill-based assignment strategy (placeholder - would need agent skills data)
   */
  private assignSkillBased(leads: any[], agents: any[], campaign: CampaignSettings, queue: any[], now: Date) {
    // For now, fall back to priority-based assignment
    // In a full implementation, this would match agent skills to lead requirements
    this.assignPriorityBased(leads, agents, campaign, queue, now)
  }

  /**
   * Load-balanced assignment strategy
   */
  private assignLoadBalanced(leads: any[], agents: any[], campaign: CampaignSettings, queue: any[], now: Date) {
    const targetLeadsPerAgent = Math.ceil(leads.length / agents.length)
    const agentLoadCount = agents.reduce((acc, agent) => {
      acc[agent.id] = 0
      return acc
    }, {} as Record<string, number>)

    for (const lead of leads) {
      // Find agent with most room for additional leads
      const availableAgent = agents
        .filter(agent => agentLoadCount[agent.id] < Math.min(targetLeadsPerAgent, campaign.agentAssignment.maxSimultaneousLeads))
        .sort((a, b) => agentLoadCount[a.id] - agentLoadCount[b.id])[0]

      if (availableAgent) {
        queue.push({
          leadId: lead.id,
          agentId: availableAgent.id,
          priority: lead.calculatedPriority,
          scheduledTime: this.calculateScheduledTime(lead, campaign, now),
          reason: `Load-balanced assignment (Priority: ${lead.calculatedPriority.toFixed(1)})`
        })
        agentLoadCount[availableAgent.id]++
      }
    }
  }

  /**
   * Calculate when a lead should be scheduled for contact
   */
  private calculateScheduledTime(lead: any, campaign: CampaignSettings, now: Date): Date {
    let scheduledTime = new Date(now)

    // For callbacks, respect the callback time if not overdue
    if (lead.currentStatus === 'CALLBACK' && lead.callbackAt && lead.callbackAt > now) {
      return lead.callbackAt
    }

    // For retry calls, respect minimum time between calls
    if (lead.lastContactAttemptAt) {
      const minNextContact = new Date(
        lead.lastContactAttemptAt.getTime() + (campaign.frequencySettings.minTimeBetweenCalls * 60 * 1000)
      )
      if (minNextContact > scheduledTime) {
        scheduledTime = minNextContact
      }
    }

    // Respect do not call hours if configured
    if (campaign.frequencySettings.respectDoNotCallTimes) {
      scheduledTime = this.adjustForDoNotCallHours(scheduledTime, campaign.frequencySettings.doNotCallHours)
    }

    return scheduledTime
  }

  /**
   * Adjust scheduled time to respect do not call hours
   */
  private adjustForDoNotCallHours(scheduledTime: Date, doNotCallHours: { start: string; end: string }): Date {
    const timeStr = scheduledTime.toTimeString().slice(0, 5) // "HH:MM"
    
    if (timeStr < doNotCallHours.start) {
      // Before allowed hours - schedule for start time
      const [hours, minutes] = doNotCallHours.start.split(':').map(Number)
      scheduledTime.setHours(hours, minutes, 0, 0)
    } else if (timeStr >= doNotCallHours.end) {
      // After allowed hours - schedule for next day start time
      const nextDay = new Date(scheduledTime)
      nextDay.setDate(nextDay.getDate() + 1)
      const [hours, minutes] = doNotCallHours.start.split(':').map(Number)
      nextDay.setHours(hours, minutes, 0, 0)
      return nextDay
    }

    return scheduledTime
  }

  /**
   * Calculate queue metrics
   */
  private calculateQueueMetrics(queue: any[], agents: any[]) {
    const agentDistribution = queue.reduce((acc, item) => {
      acc[item.agentId] = (acc[item.agentId] || 0) + 1
      return acc
    }, {} as Record<string, number>)

    const totalPriority = queue.reduce((sum, item) => sum + item.priority, 0)
    const averagePriority = queue.length > 0 ? totalPriority / queue.length : 0

    // Estimate completion time based on average call duration
    const estimatedMinutesPerCall = 15 // Configurable
    const maxSimultaneousLeads = Math.max(...agents.map(() => 5)) // From campaign settings
    const parallelCapacity = agents.length * maxSimultaneousLeads
    const estimatedCompletionMinutes = Math.ceil(queue.length / parallelCapacity) * estimatedMinutesPerCall
    const estimatedCompletionTime = new Date(Date.now() + (estimatedCompletionMinutes * 60 * 1000))

    return {
      totalLeadsQueued: queue.length,
      averagePriority,
      estimatedCompletionTime,
      agentDistribution
    }
  }

  /**
   * Get campaign metrics for analytics
   */
  async getCampaignMetrics(campaignId: string, startDate: Date, endDate: Date): Promise<CampaignMetrics> {
    // Query disposition history within date range
    const dispositions = await prisma.leadDispositionHistory.findMany({
      where: {
        createdAt: {
          gte: startDate,
          lte: endDate
        }
      },
      include: {
        lead: true,
        agent: true
      }
    })

    // Calculate metrics from disposition history
    const totalLeadsProcessed = new Set(dispositions.map(d => d.leadId)).size
    const successfulConnections = dispositions.filter(d => d.status === 'SALE_MADE' || d.status === 'CALLBACK').length
    const salesMade = dispositions.filter(d => d.status === 'SALE_MADE').length
    const callbacksScheduled = dispositions.filter(d => d.status === 'CALLBACK').length
    const doNotCallRequests = dispositions.filter(d => d.status === 'DO_NOT_CALL').length

    // Calculate agent performance
    const agentStats = new Map()
    dispositions.forEach(d => {
      const agentId = d.agentId
      if (!agentStats.has(agentId)) {
        agentStats.set(agentId, {
          agentId,
          leadsProcessed: new Set(),
          salesMade: 0,
          totalDispositions: 0
        })
      }
      
      const stats = agentStats.get(agentId)
      stats.leadsProcessed.add(d.leadId)
      stats.totalDispositions++
      if (d.status === 'SALE_MADE') stats.salesMade++
    })

    const agentPerformance = Array.from(agentStats.values()).map(stats => ({
      agentId: stats.agentId,
      leadsProcessed: stats.leadsProcessed.size,
      salesMade: stats.salesMade,
      averageCallDuration: 0, // Would need call duration data
      conversionRate: stats.leadsProcessed.size > 0 ? stats.salesMade / stats.leadsProcessed.size : 0
    }))

    return {
      campaignId,
      periodStart: startDate,
      periodEnd: endDate,
      totalLeadsProcessed,
      successfulConnections,
      salesMade,
      callbacksScheduled,
      doNotCallRequests,
      averageCallsPerLead: totalLeadsProcessed > 0 ? dispositions.length / totalLeadsProcessed : 0,
      conversionRate: totalLeadsProcessed > 0 ? salesMade / totalLeadsProcessed : 0,
      averageTimeToContact: 0, // Would need time tracking data
      agentPerformance
    }
  }

  /**
   * Apply queue optimization in real-time
   */
  async applyQueueOptimization(campaignId?: string): Promise<{ applied: number; errors: string[] }> {
    const optimization = await this.optimizeQueue(campaignId)
    const errors: string[] = []
    let applied = 0

    // Apply the optimization by updating lead assignments and priorities
    for (const item of optimization.optimizedQueue) {
      try {
        await prisma.lead.update({
          where: { id: item.leadId },
          data: {
            assignedAgentId: item.agentId,
            // Could store calculated priority and scheduled time in lead metadata
            metadata: {
              ...(await prisma.lead.findUnique({ where: { id: item.leadId } }))?.metadata,
              campaignPriority: item.priority,
              scheduledTime: item.scheduledTime,
              assignmentReason: item.reason
            }
          }
        })
        applied++
      } catch (error) {
        errors.push(`Failed to update lead ${item.leadId}: ${error}`)
      }
    }

    return { applied, errors }
  }
}