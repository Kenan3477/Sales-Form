const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function testTemplateContent() {
  try {
    console.log('Testing template content differentiation...')
    
    const templates = await prisma.documentTemplate.findMany({
      where: { isActive: true }
    });

    console.log(`\nFound ${templates.length} active templates:\n`)

    templates.forEach((template, index) => {
      console.log(`${index + 1}. ${template.name}`)
      console.log(`   Type: ${template.templateType}`)
      console.log(`   ID: ${template.id}`)
      console.log(`   Content preview: ${template.htmlContent.substring(0, 100).replace(/\s+/g, ' ')}...`)
      console.log(`   Variables: ${template.variables}`)
      console.log('')
    });

    // Test if Coverage Continuation Notice has unique content
    const continuationTemplate = templates.find(t => t.templateType === 'uncontacted_customer_notice');
    if (continuationTemplate) {
      const hasWarmcare = continuationTemplate.htmlContent.toLowerCase().includes('warmcare');
      const hasContinuation = continuationTemplate.htmlContent.toLowerCase().includes('continuation');
      const has7to14Days = continuationTemplate.htmlContent.toLowerCase().includes('7-14');
      
      console.log('✅ Coverage Continuation Notice validation:')
      console.log(`   - Contains "Warmcare": ${hasWarmcare ? '✅' : '❌'}`)
      console.log(`   - Contains "continuation": ${hasContinuation ? '✅' : '❌'}`)
      console.log(`   - Contains "7-14": ${has7to14Days ? '✅' : '❌'}`)
    }

  } catch (error) {
    console.error('❌ Error testing templates:', error)
  } finally {
    await prisma.$disconnect()
  }
}

testTemplateContent()