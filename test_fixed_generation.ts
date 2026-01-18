import { PrismaClient } from '@prisma/client'
import { EnhancedTemplateService } from './src/lib/paperwork/enhanced-template-service'

const prisma = new PrismaClient()

async function testFixedDocumentGeneration() {
  try {
    console.log('🧪 Testing FIXED document generation...')

    // Get the first sale (Kenan's sale with totalPlanCost: 31.48)
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

    console.log('📊 Using sale data:', {
      id: sale.id,
      customer: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      totalPlanCost: sale.totalPlanCost // This should be monthly cost
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

    console.log('📄 Using template:', {
      id: template.id,
      name: template.name,
      type: template.templateType
    })

    // Transform sale data for template with CORRECT calculations
    const templateData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
      coverageStartDate: new Date().toLocaleDateString('en-GB'),
      policyNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`, // Format: TFT0123
      totalCost: (sale.totalPlanCost * 12).toFixed(2), // Annual cost = monthly * 12
      monthlyCost: sale.totalPlanCost.toFixed(2), // Monthly cost
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }

    console.log('📝 FIXED Template data:', {
      customerName: templateData.customerName,
      policyNumber: templateData.policyNumber,
      monthlyPlanCost: sale.totalPlanCost, // Original monthly cost
      calculatedMonthlyCost: templateData.monthlyCost, // What we show as monthly
      calculatedAnnualCost: templateData.totalCost, // What we show as annual (monthly * 12)
    })

    console.log('✅ Cost calculations:')
    console.log(`  Monthly cost in DB: £${sale.totalPlanCost}`)
    console.log(`  Document monthly cost: £${templateData.monthlyCost}`)  
    console.log(`  Document annual cost: £${templateData.totalCost} (${sale.totalPlanCost} × 12)`)
    console.log(`  Policy number: ${templateData.policyNumber}`)

    // Test the enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService()
    const result = await enhancedTemplateService.generateDocument('welcome-letter', templateData)

    // Generate filename and file path
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const fileName = `welcome-letter-FIXED-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`
    const filePath = `storage/documents/${fileName}`

    console.log('💾 File details:', { fileName, filePath })

    // Save the document content to file
    const fs = await import('fs/promises')
    const path = await import('path')
    
    // Ensure storage directory exists
    const fullStoragePath = path.join(process.cwd(), 'storage/documents')
    await fs.mkdir(fullStoragePath, { recursive: true })
    
    // Write the document content to file
    const fullFilePath = path.join(process.cwd(), filePath)
    await fs.writeFile(fullFilePath, result, 'utf8')
    console.log('💾 FIXED document saved to:', fullFilePath)

    // Create GeneratedDocument record in database
    const generatedDocument = await prisma.generatedDocument.create({
      data: {
        saleId: sale.id,
        templateId: template.id,
        filename: fileName,
        filePath: filePath,
        fileSize: Buffer.byteLength(result, 'utf8'),
        mimeType: 'text/html',
        metadata: {
          templateType: 'welcome_letter',
          customerName: templateData.customerName,
          generationMethod: 'fixed-cost-calculation',
          policyNumber: templateData.policyNumber,
          monthlyCost: templateData.monthlyCost,
          annualCost: templateData.totalCost
        }
      }
    })

    console.log('✅ Created FIXED GeneratedDocument record:', generatedDocument.id)

  } catch (error) {
    console.error('❌ Error in fixed test:', error)
  } finally {
    await prisma.$disconnect()
  }
}

testFixedDocumentGeneration()