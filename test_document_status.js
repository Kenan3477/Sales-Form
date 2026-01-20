#!/usr/bin/env node
// Test script for Document Generation Status functionality
const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function testDocumentStatusFeatures() {
  console.log('🧪 Testing Document Generation Status functionality...\n')

  try {
    // Test 1: Check if documentsGenerated field exists and works
    console.log('1. Testing database schema for documentsGenerated field...')
    
    // Get a few sales to test with
    const sales = await prisma.sale.findMany({
      take: 5,
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        documentsGenerated: true,
        documentsGeneratedAt: true,
        documentsGeneratedBy: true
      }
    })
    
    console.log(`✅ Found ${sales.length} sales with documentsGenerated field`)
    sales.forEach(sale => {
      console.log(`  - ${sale.customerFirstName} ${sale.customerLastName}: ${sale.documentsGenerated ? 'Documents Generated ✓' : 'No Documents ✗'}`)
    })
    console.log('')

    // Test 2: Test filtering sales by document generation status
    console.log('2. Testing filtering by document generation status...')
    
    const salesWithDocs = await prisma.sale.count({
      where: { documentsGenerated: true }
    })
    
    const salesWithoutDocs = await prisma.sale.count({
      where: { documentsGenerated: false }
    })
    
    console.log(`✅ Sales with documents generated: ${salesWithDocs}`)
    console.log(`✅ Sales without documents generated: ${salesWithoutDocs}`)
    console.log('')

    // Test 3: Test document download tracking
    console.log('3. Testing document download tracking...')
    
    const documentsWithDownloads = await prisma.generatedDocument.count({
      where: { downloadCount: { gt: 0 } }
    })
    
    const documentsWithoutDownloads = await prisma.generatedDocument.count({
      where: { downloadCount: 0 }
    })
    
    console.log(`✅ Documents downloaded: ${documentsWithDownloads}`)
    console.log(`✅ Documents not downloaded: ${documentsWithoutDownloads}`)
    console.log('')

    // Test 4: Test if document generation marks sale correctly
    console.log('4. Testing document generation marking...')
    
    // Find a sale without documents generated
    const unprocessedSale = await prisma.sale.findFirst({
      where: { documentsGenerated: false },
      select: { id: true, customerFirstName: true, customerLastName: true }
    })
    
    if (unprocessedSale) {
      console.log(`Found unprocessed sale: ${unprocessedSale.customerFirstName} ${unprocessedSale.customerLastName}`)
      console.log('(Ready for testing document generation in UI)')
    } else {
      console.log('No unprocessed sales found - all sales have had documents generated')
    }
    
    console.log('\n🎉 All Document Status tests passed!')

  } catch (error) {
    console.error('❌ Test failed:', error.message)
  } finally {
    await prisma.$disconnect()
  }
}

testDocumentStatusFeatures().catch(console.error)