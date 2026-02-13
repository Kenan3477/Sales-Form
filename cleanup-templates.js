const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function cleanupDuplicateTemplates() {
  try {
    console.log('Cleaning up duplicate Coverage Continuation Notice templates...')
    
    // Delete the template with the wrong template type
    const deleteResult = await prisma.documentTemplate.deleteMany({
      where: {
        templateType: 'coverage_continuation',
        name: 'Coverage Continuation Notice'
      }
    });

    console.log(`✅ Deleted ${deleteResult.count} duplicate template(s)`)
    
    // Show remaining templates
    const remainingTemplates = await prisma.documentTemplate.findMany({
      select: {
        id: true,
        name: true,
        templateType: true,
        isActive: true
      },
      where: {
        isActive: true
      }
    });

    console.log('\nRemaining active templates:')
    remainingTemplates.forEach(template => {
      console.log(`- ${template.name} (${template.templateType})`)
    });

  } catch (error) {
    console.error('❌ Error cleaning templates:', error)
  } finally {
    await prisma.$disconnect()
  }
}

cleanupDuplicateTemplates()