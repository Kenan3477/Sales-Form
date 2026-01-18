// Simple test script to check document generation
const { default: fetch } = require('node-fetch');

async function testDocumentGeneration() {
  try {
    // First, let's check what sales exist
    console.log('Checking available sales...');
    const salesResponse = await fetch('http://localhost:3000/api/sales');
    
    if (!salesResponse.ok) {
      console.error('Failed to fetch sales:', await salesResponse.text());
      return;
    }
    
    const salesData = await salesResponse.json();
    const sales = Array.isArray(salesData) ? salesData : salesData.sales || [];
    
    console.log(`Found ${sales.length} sales`);
    if (sales.length > 0) {
      console.log('First sale:', JSON.stringify(sales[0], null, 2));
    }
    
    // Check templates
    console.log('\nChecking templates...');
    const templatesResponse = await fetch('http://localhost:3000/api/paperwork/templates');
    
    if (!templatesResponse.ok) {
      console.error('Failed to fetch templates:', await templatesResponse.text());
      return;
    }
    
    const templatesData = await templatesResponse.json();
    console.log('Templates response:', JSON.stringify(templatesData, null, 2));
    
    // Check documents
    console.log('\nChecking existing documents...');
    const documentsResponse = await fetch('http://localhost:3000/api/paperwork/documents');
    
    if (!documentsResponse.ok) {
      console.error('Failed to fetch documents:', await documentsResponse.text());
      return;
    }
    
    const documentsData = await documentsResponse.json();
    console.log('Documents response:', JSON.stringify(documentsData, null, 2));
    
  } catch (error) {
    console.error('Error in test:', error);
  }
}

testDocumentGeneration();