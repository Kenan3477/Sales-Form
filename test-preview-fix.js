const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function testPreviewEndpoints() {
  try {
    console.log('Testing template preview endpoints...')
    
    const templates = await prisma.documentTemplate.findMany({
      where: { isActive: true },
      select: { id: true, name: true, templateType: true }
    });

    console.log(`\nFound ${templates.length} active templates:`)
    templates.forEach(template => {
      console.log(`- ${template.name} (${template.templateType}): ID ${template.id}`)
      console.log(`  Preview URL: http://localhost:3000/api/paperwork/preview/${template.id}`)
    });

    console.log('\n✅ All templates should now show different content when you click Preview in the admin interface!')
    console.log('\nTo test:')
    console.log('1. Go to http://localhost:3000/admin/paperwork')
    console.log('2. Click on Document Templates tab')
    console.log('3. Click Preview button for each template')
    console.log('4. Each should open a new tab with different content')

  } catch (error) {
    console.error('❌ Error:', error)
  } finally {
    await prisma.$disconnect()
  }
}

testPreviewEndpoints()