import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function debugSaleUpdate() {
  try {
    const saleId = "cmkqxmzd600177r0vvtulc3fx";
    
    // First, check if this sale exists
    const existingSale = await prisma.sale.findUnique({
      where: { id: saleId },
      include: { appliances: true }
    });

    if (!existingSale) {
      console.log(`❌ Sale ${saleId} not found`);
      return;
    }

    console.log('✅ Found existing sale:');
    console.log('Customer:', existingSale.customerFirstName, existingSale.customerLastName);
    console.log('Email:', existingSale.email || '(empty)');
    console.log('Phone:', existingSale.phoneNumber);
    console.log('Appliances:', existingSale.appliances.length);
    console.log('');

    // Test the field configuration logic
    const fieldConfigs = await prisma.fieldConfiguration.findMany();
    const isFieldRequired = (fieldName: string): boolean => {
      const config = fieldConfigs.find(c => c.fieldName === fieldName)
      return config?.isRequired || false
    }

    console.log('Field requirements:');
    const fieldsToCheck = ['customerFirstName', 'customerLastName', 'email', 'phoneNumber'];
    fieldsToCheck.forEach(field => {
      console.log(`${field}: ${isFieldRequired(field) ? 'required' : 'optional'}`);
    });
    console.log('');

    // Test validation with the problematic data
    const testData = {
      customerFirstName: "Teresa",
      customerLastName: "Cullinane",
      email: "", // Empty email
      phoneNumber: "7957688103"
    };

    console.log('Testing validation with data:', testData);
    
    const missingFields: string[] = []
    
    if (isFieldRequired('customerFirstName') && !testData.customerFirstName) {
      missingFields.push('firstName')
    }
    if (isFieldRequired('customerLastName') && !testData.customerLastName) {
      missingFields.push('lastName')
    }
    if (isFieldRequired('email') && !testData.email) {
      missingFields.push('email')
    }
    if (isFieldRequired('phoneNumber') && !testData.phoneNumber) {
      missingFields.push('phoneNumber')
    }

    if (missingFields.length > 0) {
      console.log(`❌ Validation failed: Missing required fields: ${missingFields.join(', ')}`);
    } else {
      console.log('✅ Validation passed - no missing required fields');
    }

  } catch (error) {
    console.error('Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

debugSaleUpdate();