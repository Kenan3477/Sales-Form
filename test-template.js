import { EnhancedTemplateService } from '../src/lib/paperwork/enhanced-template-service';

// Test the template generation locally
const testData = {
  customerName: 'Giuseppe Raccio',
  email: 'Racciofamily@hotmail.com',
  phone: '7836517717',
  address: '34 Lomond Cresent, , , KA15 2EA',
  coverageStartDate: '18/01/2026',
  policyNumber: 'TFT3182',
  totalCost: '671.76',
  monthlyCost: '55.98',
  hasApplianceCover: true,
  hasBoilerCover: true,
  appliances: [
    {
      name: 'Washing Machine',
      coverLimit: '£500.00',
      monthlyCost: '£8.50'
    }
  ],
  boilerCost: '£24.99',
  currentDate: '18th January 2026'
};

async function testTemplate() {
  try {
    console.log('🧪 Testing template generation...');
    const service = new EnhancedTemplateService();
    const result = await service.generateDocument('welcome-letter', testData);
    
    console.log('✅ Generated template length:', result.length);
    console.log('\n📄 First 1000 characters:');
    console.log(result.substring(0, 1000));
    console.log('\n📄 Last 500 characters:');
    console.log(result.substring(result.length - 500));
    
    // Check if it contains the expected styling
    if (result.includes('Flash Team')) {
      console.log('✅ Contains Flash Team branding');
    } else {
      console.log('❌ Missing Flash Team branding');
    }
    
    if (result.includes('linear-gradient')) {
      console.log('✅ Contains CSS styling');
    } else {
      console.log('❌ Missing CSS styling');
    }
    
    if (result.includes('Giuseppe Raccio')) {
      console.log('✅ Variables are being replaced');
    } else {
      console.log('❌ Variables not being replaced');
    }

  } catch (error) {
    console.error('❌ Error testing template:', error);
  }
}

testTemplate();