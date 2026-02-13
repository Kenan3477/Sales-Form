const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function updateTemplateText() {
  try {
    console.log('Updating Coverage Continuation Notice text...')
    
    // Get the current template
    const template = await prisma.documentTemplate.findUnique({
      where: { id: 'cml6e85p70005tsey7avbhm90' }
    });

    if (!template) {
      console.log('❌ Template not found');
      return;
    }

    // Update the text content
    let updatedContent = template.htmlContent
      // Remove "Despite our recent attempts to contact you" text
      .replace(/Despite our recent attempts to contact you,\s*/g, '')
      .replace(/We are writing to inform you that despite our recent attempts to contact you,\s*/g, 'We are writing to inform you that ')
      // Change "Warmcare Ltd" to just "Warmcare"
      .replace(/Warmcare Ltd/g, 'Warmcare');

    await prisma.documentTemplate.update({
      where: { id: 'cml6e85p70005tsey7avbhm90' },
      data: {
        htmlContent: updatedContent,
        updatedAt: new Date()
      }
    });

    console.log('✅ Updated Coverage Continuation Notice:');
    console.log('- Removed "Despite our recent attempts to contact you" text');
    console.log('- Changed "Warmcare Ltd" to "Warmcare"');

  } catch (error) {
    console.error('❌ Error updating template:', error);
  } finally {
    await prisma.$disconnect();
  }
}

updateTemplateText();