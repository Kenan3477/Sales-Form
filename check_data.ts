import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function checkData() {
  try {
    console.log('🔍 Checking database content...')

    // Check sales
    const sales = await prisma.sale.findMany({
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        totalPlanCost: true,
        createdAt: true
      },
      take: 5
    })
    console.log(`📊 Found ${sales.length} sales:`)
    console.log(JSON.stringify(sales, null, 2))

    // Check templates
    const templates = await prisma.documentTemplate.findMany({
      select: {
        id: true,
        name: true,
        templateType: true,
        isActive: true
      }
    })
    console.log(`📄 Found ${templates.length} templates:`)
    console.log(JSON.stringify(templates, null, 2))

    // Check existing documents
    const documents = await prisma.generatedDocument.findMany({
      select: {
        id: true,
        saleId: true,
        filename: true,
        generatedAt: true,
        isDeleted: true
      }
    })
    console.log(`📑 Found ${documents.length} generated documents:`)
    console.log(JSON.stringify(documents, null, 2))

  } catch (error) {
    console.error('Error:', error)
  } finally {
    await prisma.$disconnect()
  }
}

checkData()