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
    // Handle multiple field name variations (export format, simple format, etc.)
    const getFieldValue = (row: any, ...fieldNames: string[]) => {
      for (const fieldName of fieldNames) {
        if (row[fieldName] !== undefined && row[fieldName] !== null && row[fieldName] !== '') {
          return row[fieldName];
        }
      }
      return undefined;
    };

    // Extract basic customer information with multiple field variations
    const firstName = getFieldValue(row, 
      'First Name', 'customer_first_name', 'first_name', 'customerFirstName', 'firstName'
    );
    const lastName = getFieldValue(row, 
      'Last Name', 'customer_last_name', 'last_name', 'customerLastName', 'lastName'
    );
    const email = getFieldValue(row, 
      'Email', 'email'
    );
    const phoneNumber = getFieldValue(row, 
      'Phone', 'Plain Phone', 'phone_number', 'phone', 'phoneNumber'
    );

    // Basic validation
    if (!firstName) {
      throw new Error('First name is required');
    }
    if (!lastName) {
      throw new Error('Last name is required');
    }
    if (!phoneNumber) {
      throw new Error('Phone number is required');
    }
    if (!email) {
      throw new Error('Email is required');
    }

    // Normalize phone number (basic)
    const normalizedPhone = phoneNumber.toString().trim();
    if (!normalizedPhone || normalizedPhone.length < 10) {
      throw new Error('Valid phone number is required');
    }

    // Extract address information
    const mailingStreet = getFieldValue(row, 
      'Mailing Street', 'First Line Add', 'mailing_street', 'address', 'street', 'mailingStreet'
    );
    const mailingCity = getFieldValue(row, 
      'Mailing City', 'mailing_city', 'city', 'mailingCity'
    );
    const mailingProvince = getFieldValue(row, 
      'Mailing Province', 'mailing_province', 'province', 'state', 'mailingProvince'
    );
    const mailingPostalCode = getFieldValue(row, 
      'Mailing Postal Code', 'mailing_postal_code', 'postal_code', 'zip', 'mailingPostalCode'
    );

    // Extract title and other customer details
    const title = getFieldValue(row, 'Title', 'title');
    const notes = getFieldValue(row, 'Description', 'Call Notes', 'notes');

    // Handle assigned agent
    let assignedAgentId: string | undefined;
    const agentEmail = getFieldValue(row, 
      'Lead Sales Agent', 'Customers Owner', 'assigned_agent_email', 'assignedAgentEmail'
    );
    if (agentEmail && agentEmail !== 'Kenan') {
      const agent = agents.find(a => a.email === agentEmail);
      if (agent) {
        assignedAgentId = agent.id;
      }
    }

    // Parse appliances from multiple sources
    let appliances: LeadData['appliances'] = [];
    
    // First try JSON format (simple import)
    if (row.appliances) {
      try {
        appliances = JSON.parse(row.appliances);
      } catch {
        // Ignore JSON parse errors and try other methods
      }
    }

    // If no appliances yet, try individual appliance fields (simple format)
    if (appliances.length === 0 && row.appliance_type && row.appliance_price) {
      appliances = [{
        applianceType: row.appliance_type,
        brand: row.appliance_brand,
        model: row.appliance_model,
        age: row.appliance_age ? parseInt(row.appliance_age) : undefined,
        price: parseFloat(row.appliance_price)
      }];
    }

    // If still no appliances, extract from export format (up to 10 appliances)
    if (appliances.length === 0) {
      for (let i = 1; i <= 10; i++) {
        const applianceType = getFieldValue(row, `Appliance ${i} Type`);
        const applianceBrand = getFieldValue(row, `Appliance ${i} Brand`);
        const applianceAge = getFieldValue(row, `Appliance ${i} Age`);
        const applianceValue = getFieldValue(row, `Appliance ${i} Value`);

        if (applianceType) {
          // Parse price from string like "£25.99" or "25.99"
          let price = 0;
          if (applianceValue) {
            const priceString = applianceValue.toString().replace(/[£$,]/g, '');
            price = parseFloat(priceString) || 0;
          }

          appliances.push({
            applianceType,
            brand: applianceBrand,
            model: undefined, // Export doesn't include model
            age: applianceAge ? parseInt(applianceAge.toString()) : undefined,
            price
          });
        }
      }
    }

    // Extract boiler information
    let boilerCoverSelected = false;
    let boilerPriceSelected: number | undefined;

    // Try export format first
    const customerPremium = getFieldValue(row, 'Customer Premium');
    const boilerPrice = getFieldValue(row, 'boiler_price', 'Boiler Package Price (Internal)');

    if (boilerPrice) {
      const priceString = boilerPrice.toString().replace(/[£$,]/g, '');
      boilerPriceSelected = parseFloat(priceString) || undefined;
      boilerCoverSelected = !!boilerPriceSelected;
    }

    // Calculate total plan cost
    const applianceCost = appliances.reduce((sum, app) => sum + (app.price || 0), 0);
    const boilerCost = boilerPriceSelected || 0;
    
    // Try to get total from export format first
    let totalPlanCost = 0;
    if (customerPremium) {
      const premiumString = customerPremium.toString().replace(/[£$,]/g, '');
      totalPlanCost = parseFloat(premiumString) || 0;
    } else {
      // Calculate from individual components
      totalPlanCost = applianceCost + boilerCost;
    }

    // Ensure we have some coverage selected
    const applianceCoverSelected = appliances.length > 0;
    if (!applianceCoverSelected && !boilerCoverSelected) {
      // Default to appliance cover if no specific coverage found
      appliances.push({
        applianceType: 'UNKNOWN',
        brand: undefined,
        model: undefined,
        age: undefined,
        price: totalPlanCost || 25 // Default price if nothing specified
      });
    }

    // Recalculate total if we added default appliance
    if (!totalPlanCost) {
      totalPlanCost = appliances.reduce((sum, app) => sum + (app.price || 0), 0) + boilerCost;
    }

    return {
      customerFirstName: firstName,
      customerLastName: lastName,
      title: title || undefined,
      phoneNumber: normalizedPhone,
      email,
      mailingStreet: mailingStreet || undefined,
      mailingCity: mailingCity || undefined,
      mailingProvince: mailingProvince || undefined,
      mailingPostalCode: mailingPostalCode || undefined,
      notes: notes || undefined,
      applianceCoverSelected,
      boilerCoverSelected,
      boilerPriceSelected,
      totalPlanCost,
      appliances,
      assignedAgentId
    };
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