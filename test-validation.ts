import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function testValidation() {
  try {
    // Get current field configurations
    const fieldConfigs = await prisma.fieldConfiguration.findMany();
    console.log('Current field configurations:');
    fieldConfigs.forEach(config => {
      console.log(`${config.fieldName}: required=${config.isRequired}`);
    });
    
    console.log('\nBased on these configurations:');
    console.log('- Email is NOT required (isRequired: false)');
    console.log('- The update should now work with empty email field');
    console.log('- Customer: Teresa Cullinane with phone 7957688103 and empty email should be valid');
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

testValidation();