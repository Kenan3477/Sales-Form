// Test the getNestedValue function behavior
const testData = {
  boilerCost: '£24.99',
  hasBoilerCover: true,
  appliances: [
    { name: 'Washing Machine', cost: '8.50' }
  ]
};

function getNestedValue(obj, path) {
  return path.split('.').reduce((current, key) => current && current[key], obj);
}

console.log('🧪 Testing getNestedValue:');
console.log('boilerCost:', getNestedValue(testData, 'boilerCost'));
console.log('hasBoilerCover:', getNestedValue(testData, 'hasBoilerCover')); 
console.log('appliances.length:', getNestedValue(testData, 'appliances.length'));

// Test truthiness
console.log('');
console.log('🧪 Testing truthiness:');
console.log('Boolean(boilerCost):', Boolean(getNestedValue(testData, 'boilerCost')));
console.log('Boolean(hasBoilerCover):', Boolean(getNestedValue(testData, 'hasBoilerCover')));
console.log('Boolean(appliances.length):', Boolean(getNestedValue(testData, 'appliances.length')));

// Test conditional that might be failing
const boilerCostValue = getNestedValue(testData, 'boilerCost');
console.log('');
console.log('🔧 Specific test for boilerCost conditional:');
console.log('Raw value:', boilerCostValue);
console.log('Type:', typeof boilerCostValue);
console.log('Truthy?:', !!boilerCostValue);
console.log('Conditional result:', boilerCostValue ? 'SHOW' : 'HIDE');