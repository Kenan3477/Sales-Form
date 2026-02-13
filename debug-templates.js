const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function checkTemplateDetails() {
  try {
    console.log('Checking detailed template information...')
    
    const templates = await prisma.documentTemplate.findMany({
      select: {
        id: true,
        name: true,
        templateType: true,
        version: true,
        isActive: true,
        description: true
      },
      orderBy: {
        createdAt: 'desc'
      }
    })

    console.log('\nDatabase templates:')
    templates.forEach(template => {
      console.log(`- ID: ${template.id}`)
      console.log(`  Name: ${template.name}`)
      console.log(`  Type: ${template.templateType}`)
      console.log(`  Description: ${template.description || 'No description'}`)
      console.log(`  Active: ${template.isActive}`)
      console.log(`  Version: ${template.version}`)
      console.log(`  ---`)
    })

  } catch (error) {
    console.error('❌ Error checking templates:', error)
  } finally {
    await prisma.$disconnect()
  }
}

checkTemplateDetails()