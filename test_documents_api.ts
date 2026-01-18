import { getServerSession } from 'next-auth'
import { authOptions } from './src/lib/auth'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Simulate the documents API call
async function testDocumentsAPI() {
  try {
    console.log('🧪 Testing documents API simulation...')
    
    // Simulate authenticated request
    const whereClause = {
      isDeleted: false
    }
    
    console.log('📋 Fetching documents with where clause:', JSON.stringify(whereClause, null, 2))
    
    const documents = await prisma.generatedDocument.findMany({
      where: whereClause,
      include: {
        sale: {
          select: {
            id: true,
            customerFirstName: true,
            customerLastName: true,
            email: true,
            createdBy: {
              select: {
                email: true
              }
            }
          }
        },
        template: {
          select: {
            name: true,
            templateType: true
          }
        }
      },
      orderBy: {
        generatedAt: 'desc'
      }
    })
    
    console.log('📋 Found documents from database:', documents.length)
    if (documents.length > 0) {
      console.log('📋 First document raw:', JSON.stringify(documents[0], null, 2))
    }
    
    // Transform the data for frontend consumption
    const transformedDocuments = documents.map(doc => ({
      id: doc.id,
      saleId: doc.saleId,
      templateId: doc.templateId,
      templateName: doc.template.name,
      fileName: doc.filename,
      downloadCount: doc.downloadCount,
      createdAt: doc.generatedAt.toISOString(),
      sale: {
        id: doc.sale.id,
        customer: {
          fullName: `${doc.sale.customerFirstName} ${doc.sale.customerLastName}`,
          email: doc.sale.email
        }
      }
    }))
    
    console.log('📋 Transformed documents:', transformedDocuments.length)
    console.log('📋 Transformed document data:', JSON.stringify(transformedDocuments, null, 2))
    
    const response = {
      success: true,
      documents: transformedDocuments
    }
    
    console.log('✅ API would return:', JSON.stringify(response, null, 2))
    
  } catch (error) {
    console.error('❌ Error in test:', error)
  } finally {
    await prisma.$disconnect()
  }
}

testDocumentsAPI()