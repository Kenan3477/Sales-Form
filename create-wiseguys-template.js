import { PrismaClient } from '@prisma/client';
import { WiseguysTemplateService } from './src/lib/paperwork/wiseguys-template-service.js';

const prisma = new PrismaClient();

async function createWiseguysTemplate() {
  try {
    console.log('🎨 Creating Wiseguys branded welcome letter template...');

    // Check if we have any admin users
    const adminUser = await prisma.user.findFirst({
      where: { role: 'ADMIN' },
    });

    if (!adminUser) {
      console.log('❌ No admin user found. Please create an admin user first.');
      return;
    }

    console.log(`✅ Using admin user: ${adminUser.email}`);

    // Check if the template already exists
    const existingTemplate = await prisma.documentTemplate.findFirst({
      where: { 
        templateType: 'wiseguys-welcome-letter',
        isActive: true 
      },
    });

    if (existingTemplate) {
      console.log('⚠️ Wiseguys template already exists. Updating...');
      
      const wiseguysTemplate = WiseguysTemplateService.getTemplate('wiseguys-welcome-letter');
      if (!wiseguysTemplate) {
        throw new Error('Wiseguys template not found in service');
      }

      await prisma.documentTemplate.update({
        where: { id: existingTemplate.id },
        data: {
          name: wiseguysTemplate.name,
          description: wiseguysTemplate.description,
          htmlContent: wiseguysTemplate.html,
        }
      });

      console.log('✅ Updated existing Wiseguys template successfully!');
      return existingTemplate;
    }

    // Create new Wiseguys template
    const wiseguysTemplate = WiseguysTemplateService.getTemplate('wiseguys-welcome-letter');
    if (!wiseguysTemplate) {
      throw new Error('Wiseguys template not found in service');
    }

    const newTemplate = await prisma.documentTemplate.create({
      data: {
        name: wiseguysTemplate.name,
        description: wiseguysTemplate.description,
        templateType: 'wiseguys-welcome-letter',
        htmlContent: wiseguysTemplate.html,
        isActive: true,
        version: 1,
        createdById: adminUser.id
      }
    });

    console.log('✅ Created Wiseguys template successfully!');
    console.log('📋 Template details:', {
      id: newTemplate.id,
      name: newTemplate.name,
      templateType: newTemplate.templateType,
      isActive: newTemplate.isActive,
      htmlLength: newTemplate.htmlContent.length
    });

    // Also create a standard welcome-letter version for compatibility
    const compatTemplate = await prisma.documentTemplate.upsert({
      where: {
        templateType_version: {
          templateType: 'welcome-letter',
          version: 1
        }
      },
      update: {
        htmlContent: wiseguysTemplate.html,
        name: 'Wiseguys Welcome Letter (Compat)',
        description: 'Wiseguys branded welcome letter (compatibility version)',
        isActive: true
      },
      create: {
        name: 'Wiseguys Welcome Letter (Compat)',
        description: 'Wiseguys branded welcome letter (compatibility version)',
        templateType: 'welcome-letter',
        htmlContent: wiseguysTemplate.html,
        isActive: true,
        version: 1,
        createdById: adminUser.id
      }
    });

    console.log('✅ Created/updated compatibility template!');
    
    return newTemplate;

  } catch (error) {
    console.error('❌ Error creating Wiseguys template:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

// Test template generation
async function testTemplateGeneration() {
  try {
    console.log('🧪 Testing Wiseguys template generation...');
    
    const testData = {
      customerName: 'John Smith',
      email: 'john.smith@example.com',
      phone: '01202 123 456',
      serviceDate: new Date().toLocaleDateString('en-GB'),
      establishedYear: '2020'
    };

    const renderedTemplate = WiseguysTemplateService.renderTemplate('wiseguys-welcome-letter', testData);
    
    console.log('✅ Template rendered successfully!');
    console.log('📊 Template stats:');
    console.log(`  - Length: ${renderedTemplate.length} characters`);
    console.log(`  - Contains customer name: ${renderedTemplate.includes(testData.customerName)}`);
    console.log(`  - Contains email: ${renderedTemplate.includes(testData.email)}`);
    console.log(`  - Contains phone: ${renderedTemplate.includes(testData.phone)}`);
    
    return true;
  } catch (error) {
    console.error('❌ Template generation test failed:', error);
    return false;
  }
}

// Main execution
async function main() {
  console.log('🚀 Starting Wiseguys template setup...');
  
  // Test template generation first
  const testPassed = await testTemplateGeneration();
  if (!testPassed) {
    console.error('❌ Template generation test failed. Stopping...');
    return;
  }
  
  // Create the template in database
  await createWiseguysTemplate();
  
  console.log('🎉 Wiseguys template setup complete!');
  console.log('');
  console.log('📋 Next steps:');
  console.log('1. Update the contact information in the template with actual Wiseguys details');
  console.log('2. Add the Wiseguys logo image to the public/images/ directory');
  console.log('3. Customize the services section based on actual Wiseguys services');
  console.log('4. Add quotes from the Wiseguys Facebook page');
  console.log('5. Test the template generation from the admin panel');
}

// Run the script
main().catch(console.error);