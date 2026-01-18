import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function checkTemplateContent() {
  try {
    const template = await prisma.documentTemplate.findFirst({
      where: {
        templateType: 'welcome_letter',
        isActive: true
      }
    });

    if (template) {
      console.log('Template content preview:');
      
      // Look for boiler-related sections
      const lines = template.htmlContent.split('\n');
      let foundBoilerSection = false;
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.toLowerCase().includes('boiler') || line.includes('{{#if') || line.includes('{{/if}}')) {
          console.log(`Line ${i + 1}: ${line}`);
          foundBoilerSection = true;
        }
      }
      
      if (!foundBoilerSection) {
        console.log('❌ No boiler conditional section found in template');
        
        // Look for where appliance section ends to see where we should add boiler section
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (line.includes('{{/each}}') || line.includes('Appliance') || line.includes('cover')) {
            console.log(`Context line ${i + 1}: ${line}`);
          }
        }
      }
      
    } else {
      console.log('Template not found');
    }

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkTemplateContent();