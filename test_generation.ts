import { PrismaClient } from '@prisma/client'
import { EnhancedTemplateService } from './src/lib/paperwork/enhanced-template-service'

const prisma = new PrismaClient()

async function testDocumentGeneration() {
  try {
    console.log('🧪 Testing document generation...')

    // Get the first sale
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
      email: sale.email
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

    // Transform sale data for template
    const templateData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
      coverageStartDate: new Date().toLocaleDateString('en-GB'),
      policyNumber: `FT-2025-${sale.id.slice(-6)}`,
      totalCost: sale.totalPlanCost.toString(),
      monthlyCost: (sale.totalPlanCost / 12).toFixed(2),
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    }

    console.log('📝 Template data:', templateData)

    // Test the enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService()
    const result = await enhancedTemplateService.generateDocument('welcome-letter', templateData)

    console.log('✅ Generated content preview:', result.substring(0, 200) + '...')

    // Generate filename and file path
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const fileName = `welcome-letter-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`
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
    console.log('💾 File saved to:', fullFilePath)

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
          generationMethod: 'test-script'
        }
      }
    })

    console.log('✅ Created GeneratedDocument record:', generatedDocument.id)

    // Verify it was created
    const verificationDoc = await prisma.generatedDocument.findUnique({
      where: { id: generatedDocument.id },
      include: {
        sale: {
          select: {
            customerFirstName: true,
            customerLastName: true,
            email: true
          }
        },
        template: {
          select: {
            name: true,
            templateType: true
          }
        }
      }
    })

    console.log('🔍 Verification - Document found in database:', {
      id: verificationDoc?.id,
      filename: verificationDoc?.filename,
      customer: verificationDoc?.sale ? `${verificationDoc.sale.customerFirstName} ${verificationDoc.sale.customerLastName}` : 'Unknown',
      template: verificationDoc?.template?.name
    })

  } catch (error) {
    console.error('❌ Error in test:', error)
  } finally {
    await prisma.$disconnect()
  }
}

testDocumentGeneration()