// Test the specific API call that's failing
const saleId = "cmkqxmzd600177r0vvtulc3fx";

// Sample data based on the error message
const testData = {
  customerFirstName: "Teresa",
  customerLastName: "Cullinane",
  email: "", // This is empty which was causing the original error
  phoneNumber: "7957688103"
};

console.log('Testing API call with data:', testData);
console.log('Sale ID:', saleId);
console.log('');
console.log('To test this manually:');
console.log('1. Go to http://localhost:3000');
console.log('2. Login as admin');
console.log('3. Navigate to the sales page');
console.log('4. Try to edit the customer with the above data');
console.log('');
console.log('Or use curl:');
console.log(`curl -X PUT http://localhost:3000/api/sales/${saleId} \\`);
console.log('  -H "Content-Type: application/json" \\');
console.log(`  -d '${JSON.stringify(testData, null, 2).replace(/\n/g, '\\n').replace(/"/g, '\\"')}'`);