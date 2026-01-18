const fetch = require('node-fetch');

async function testDocumentGeneration() {
  try {
    console.log('🧪 Testing document generation API...');
    
    // Create a test sale data
    const testSale = {
      id: 'test-123',
      customerFirstName: 'John',
      customerLastName: 'Doe',
      phoneNumber: '01234567890',
      email: 'john.doe@test.com',
      mailingStreet: '123 Test St',
      mailingCity: 'Test City', 
      mailingProvince: 'Test Province',
      mailingPostalCode: 'TE1 2ST',
      totalPlanCost: 46.48,
      boilerCoverSelected: true,
      boilerPriceSelected: 24.99,
      applianceCoverSelected: true,
      appliances: [
        {
          appliance: 'Washing Machine',
          coverLimit: 500.00,
          cost: 8.50
        }
      ]
    };

    const response = await fetch('http://localhost:3000/api/paperwork/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token' // This might be needed
      },
      body: JSON.stringify({
        saleId: 'test-123',
        templateId: 'welcome-letter',
        testData: testSale // Pass test data directly
      })
    });

    const text = await response.text();
    console.log('📝 Response status:', response.status);
    console.log('📝 Response:', text.substring(0, 200), '...');
    
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

testDocumentGeneration();