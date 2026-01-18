// Activate and fix the template
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function activateTemplate() {
  try {
    console.log('🔄 Activating the welcome letter template...');
    
    const result = await prisma.documentTemplate.updateMany({
      where: {
        OR: [
          { templateType: 'welcome_letter' },
          { templateType: 'welcome-letter' }
        ]
      },
      data: {
        isActive: true,
        templateType: 'welcome-letter' // Standardize on dash format
      }
    });
    
    console.log('✅ Updated', result.count, 'template(s)');
    
    // Verify the update
    const templates = await prisma.documentTemplate.findMany({
      where: {
        templateType: 'welcome-letter',
        isActive: true
      }
    });
    
    console.log('📋 Active welcome letter templates:', templates.length);
    templates.forEach(t => console.log(`  - ${t.name} (ID: ${t.id})`));
    
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

activateTemplate();