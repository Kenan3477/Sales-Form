import { PrismaClient } from '@prisma/client'
import { EnhancedTemplateService } from './src/lib/paperwork/enhanced-template-service'

const prisma = new PrismaClient()

async function testDocumentGenerationWithAppliances() {
  try {
    console.log('🧪 Testing document generation with appliance details...')

    // Get the first sale with appliances
    const sale = await prisma.sale.findFirst({
      include: {
        appliances: true,
        createdBy: {
          select: {
            email: true,
          }
        }
      }
    })

    if (!sale) {
      console.error('No sale found!')
      return
    }

    console.log('📊 Using sale:', {
      id: sale.id,
      customer: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      appliances: sale.appliances
    })

    // Get the first active template
    const template = await prisma.documentTemplate.findFirst({
      where: {
        templateType: 'welcome_letter',
        isActive: true
      }
    })

    if (!template) {
      console.error('No template found!')
      return
    }

    // Transform sale data for template (same as API)
    const templateData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
      coverageStartDate: new Date().toLocaleDateString('en-GB'),
      policyNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      totalCost: (sale.totalPlanCost * 12).toFixed(2), // Annual cost = monthly * 12
      monthlyCost: sale.totalPlanCost.toFixed(2), // Monthly cost
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      appliances: sale.appliances.map(appliance => ({
        name: appliance.appliance + (appliance.otherText ? ` (${appliance.otherText})` : ''),
        coverLimit: `£${appliance.coverLimit.toFixed(2)}`,
        monthlyCost: `£${appliance.cost.toFixed(2)}`
      })),
      boilerCost: sale.boilerPriceSelected ? `£${sale.boilerPriceSelected.toFixed(2)}` : null,
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }

    console.log('📝 Template data:', JSON.stringify(templateData, null, 2))

    // Test the enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService()
    const result = await enhancedTemplateService.generateDocument('welcome-letter', templateData)

    console.log('✅ Generated content length:', result.length)

    // Generate filename and save to test
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const fileName = `welcome-letter-FIXED-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`
    const filePath = `storage/documents/${fileName}`

    // Save the document content to file
    const fs = await import('fs/promises')
    const path = await import('path')
    
    const fullStoragePath = path.join(process.cwd(), 'storage/documents')
    await fs.mkdir(fullStoragePath, { recursive: true })
    
    const fullFilePath = path.join(process.cwd(), filePath)
    await fs.writeFile(fullFilePath, result, 'utf8')
    console.log('💾 File saved to:', fullFilePath)

    // Check if appliance section is included
    if (result.includes('Covered Appliances')) {
      console.log('✅ Appliance section found in document')
    } else {
      console.log('❌ Appliance section NOT found in document')
    }

    if (result.includes('Washing machine')) {
      console.log('✅ Washing machine appliance found in document')
    } else {
      console.log('❌ Washing machine appliance NOT found in document')
    }

  } catch (error) {
    console.error('❌ Error in test:', error)
  } finally {
    await prisma.$disconnect()
  }
}

testDocumentGenerationWithAppliances()