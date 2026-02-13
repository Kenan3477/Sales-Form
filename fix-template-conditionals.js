const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function fixTemplateConditionals() {
  try {
    console.log('Fixing conditional logic in Coverage Continuation Notice...')
    
    // Get the current template
    const template = await prisma.documentTemplate.findUnique({
      where: { id: 'cml6e85p70005tsey7avbhm90' }
    });

    if (!template) {
      console.log('❌ Template not found');
      return;
    }

    // Replace Handlebars conditionals with simple HTML since we don't have conditional processing
    let updatedContent = template.htmlContent
      .replace(/{{#if hasApplianceCover}}/g, '')
      .replace(/{{\/if}}/g, '')
      .replace(/{{#if hasBoilerCover}}/g, '');

    await prisma.documentTemplate.update({
      where: { id: 'cml6e85p70005tsey7avbhm90' },
      data: {
        htmlContent: updatedContent,
        updatedAt: new Date()
      }
    });

    console.log('✅ Fixed conditional logic in template - now shows all coverage sections');

  } catch (error) {
    console.error('❌ Error fixing template:', error);
  } finally {
    await prisma.$disconnect();
  }
}

fixTemplateConditionals();