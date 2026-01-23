import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function checkEmailFieldConfig() {
  try {
    // Check field configuration for email
    const emailConfig = await prisma.fieldConfiguration.findUnique({
      where: { fieldName: 'email' }
    });
    
    console.log('Email field configuration:', emailConfig);
    
    // Also check all field configurations
    const allConfigs = await prisma.fieldConfiguration.findMany();
    console.log('\nAll field configurations:');
    allConfigs.forEach(config => {
      console.log(`${config.fieldName}: required=${config.isRequired}`);
    });
    
  } catch (error) {
    console.error('Error checking field config:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkEmailFieldConfig();