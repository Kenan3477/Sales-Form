/**
 * Create default Flash Team template
 */
console.log('🔧 Creating default Flash Team template...')

async function createDefaultTemplate() {
  try {
    // Import prisma client
    const { PrismaClient } = await import('@prisma/client')
    const prisma = new PrismaClient()
    
    // Check if template already exists
    const existing = await prisma.documentTemplate.findUnique({
      where: { id: 'flash-team-default' }
    })
    
    if (existing) {
      console.log('✅ Template already exists:', existing.name)
      return
    }
    
    // Get first admin user for createdBy
    const admin = await prisma.user.findFirst({
      where: { role: 'ADMIN' }
    })
    
    if (!admin) {
      console.error('❌ No admin user found! Need admin user to create template.')
      return
    }
    
    // Create the template
    const template = await prisma.documentTemplate.create({
      data: {
        id: 'flash-team-default',
        name: 'Flash Team Protection Plan',
        description: 'Default Flash Team protection plan document template',
        templateType: 'flash-team-protection',
        htmlContent: '<html><body><h1>Flash Team Protection Plan</h1><p>Auto-generated template for Flash Team documents.</p></body></html>',
        isActive: true,
        version: 1,
        createdById: admin.id
      }
    })
    
    console.log('✅ Created template:', template.name)
    console.log('📄 Template ID:', template.id)
    
  } catch (error) {
    console.error('❌ Error creating template:', error.message)
  }
}

createDefaultTemplate()