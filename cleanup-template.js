// Clean up template name and ensure it's ready
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function cleanupTemplate() {
  try {
    console.log('🧹 Cleaning up template name...');
    
    const result = await prisma.documentTemplate.updateMany({
      where: {
        templateType: 'welcome-letter',
        isActive: true
      },
      data: {
        name: 'Flash Team Welcome Letter',
        description: 'Professional welcome letter with Flash Team branding and styling'
      }
    });
    
    console.log('✅ Updated', result.count, 'template(s)');
    
    // Final verification
    const template = await prisma.documentTemplate.findFirst({
      where: {
        templateType: 'welcome-letter',
        isActive: true
      }
    });
    
    if (template) {
      console.log('📄 Final template status:');
      console.log(`  - Name: ${template.name}`);
      console.log(`  - Type: ${template.templateType}`);
      console.log(`  - Active: ${template.isActive}`);
      console.log(`  - Content length: ${template.htmlContent.length}`);
      console.log(`  - Contains Flash Team: ${template.htmlContent.includes('Flash Team')}`);
      console.log(`  - Contains CSS: ${template.htmlContent.includes('linear-gradient')}`);
      console.log('✅ Template is ready for use!');
    } else {
      console.log('❌ Template not found');
    }
    
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

cleanupTemplate();