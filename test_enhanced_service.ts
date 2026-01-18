import { EnhancedTemplateService } from './src/lib/paperwork/enhanced-template-service';

async function testConditionalProcessing() {
  console.log('🧪 Testing conditional processing with EnhancedTemplateService...');
  
  const templateService = new EnhancedTemplateService();
  
  // Test data with both appliances and boiler coverage
  const testData = {
    customerName: 'John Smith',
    email: 'john.smith@email.com',
    phone: '07700 900123',
    address: '123 High Street, London, SW1A 1AA',
    coverageStartDate: '1st January 2025',
    policyNumber: 'TFT0123',
    totalCost: '455.52',
    monthlyCost: '37.96',
    hasApplianceCover: true,
    hasBoilerCover: true,
    appliances: [
      {
        name: 'Washing Machine',
        coverLimit: '£500.00',
        monthlyCost: '£8.50'
      }
    ],
    boilerCost: '£24.99', // This should trigger the conditional
    currentDate: new Date().toLocaleDateString('en-GB', { 
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  };
  
  console.log('📊 Test data:', JSON.stringify({ 
    appliances: testData.appliances, 
    boilerCost: testData.boilerCost,
    hasBoilerCover: testData.hasBoilerCover 
  }, null, 2));
  
  try {
    console.log('\n🔄 Generating document...');
    const result = await templateService.generateDocument('welcome-letter', testData);
    
    console.log('\n✅ Document generated successfully!');
    console.log('📝 Length:', result.length, 'characters');
    
    // Check if boilerCost conditional was processed
    const hasUnprocessedConditional = result.includes('{{#if boilerCost}}');
    const hasBoilerSection = result.includes('Boiler & Central Heating');
    
    console.log('\n🔍 Conditional Processing Results:');
    console.log('❌ Unprocessed conditional found:', hasUnprocessedConditional);
    console.log('✅ Boiler section found:', hasBoilerSection);
    
    if (hasUnprocessedConditional) {
      console.log('\n🚨 ERROR: Conditional processing failed!');
      console.log('Raw conditional still present in output');
    } else {
      console.log('\n🎉 SUCCESS: All conditionals processed correctly!');
    }
    
  } catch (error) {
    console.error('❌ Error generating document:', error);
  }
}

testConditionalProcessing();