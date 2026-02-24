const { z } = require('zod');

// Test the exact validation logic we're using
const emailValidation = z.string()
  .refine((val) => val === '' || z.string().email().safeParse(val).success, {
    message: 'Please enter a valid email address or leave empty'
  })
  .optional();

// Test cases
const testCases = [
  '',
  'valid@email.com', 
  'invalid-email',
  null,
  undefined,
  'joanna.kolasinska@example.com'
];

console.log('🧪 Testing Email Validation Logic:');
console.log('=====================================');

testCases.forEach((testCase, index) => {
  console.log(`\n📧 Test ${index + 1}: ${JSON.stringify(testCase)}`);
  try {
    const result = emailValidation.parse(testCase);
    console.log(`✅ SUCCESS: ${JSON.stringify(result)}`);
  } catch (error) {
    console.log(`❌ ERROR: ${error.message}`);
    console.log(`📋 Error Details:`, error.issues || error);
  }
});

// Also test the required version
const emailValidationRequired = z.string()
  .refine((val) => val === '' || z.string().email().safeParse(val).success, {
    message: 'Please enter a valid email address'
  });

console.log('\n\n🧪 Testing Required Email Validation:');
console.log('=====================================');

testCases.forEach((testCase, index) => {
  console.log(`\n📧 Test ${index + 1}: ${JSON.stringify(testCase)}`);
  try {
    const result = emailValidationRequired.parse(testCase);
    console.log(`✅ SUCCESS: ${JSON.stringify(result)}`);
  } catch (error) {
    console.log(`❌ ERROR: ${error.message}`);
  }
});