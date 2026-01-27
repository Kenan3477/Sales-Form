import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Simple test of the import normalization logic
const testRow = {
  'Customer First Name': 'John',
  'Customer Last Name': 'Doe',
  'Phone Number': '1234567890',
  'Email': 'john.doe@test.com',
  'Account Name': 'John Doe',
  'Sort Code': '123456',
  'Account Number': '12345678',
  'Direct Debit Date': '2026-01-24',
  'Single App Price (Internal)': '30.00',  // £30 total for appliances
  'Appliance 1': 'Washing Machine',
  'Appliance 2': 'Fridge Freezer',
  'Appliance 3': 'Dishwasher',
  'Customer Premium': '55.00'  // £30 appliances + £25 boiler
}

// Test the normalizeDataRow function logic for per-appliance calculation
function testPerApplianceCalculation() {
  console.log('🧪 Testing per-appliance calculation logic...')
  console.log('Input data:', testRow)
  
  // Simulate the calculation that should happen
  const singleAppPrice = 30.00
  const appliances = ['Washing Machine', 'Fridge Freezer', 'Dishwasher']
  const perAppCost = singleAppPrice / appliances.length
  
  console.log(`📊 Single App Price: £${singleAppPrice}`)
  console.log(`🏠 Number of appliances: ${appliances.length}`)
  console.log(`💰 Expected per-appliance cost: £${perAppCost.toFixed(2)}`)
  console.log(`✅ Each appliance should cost: £${perAppCost.toFixed(2)}`)
  
  // This should result in £10.00 per appliance (£30 ÷ 3 = £10)
  console.log('\nExpected result: Each appliance costs £10.00')
}

testPerApplianceCalculation()

export {}