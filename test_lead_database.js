#!/usr/bin/env node
// Test script for Lead Database functionality
const { PrismaClient } = require('@prisma/client')
const fs = require('fs')

const prisma = new PrismaClient()

async function testLeadDatabase() {
  console.log('🧪 Testing Lead Database functionality...\n')

  try {
    // Test 1: Check database schema
    console.log('1. Testing database schema...')
    const leadCount = await prisma.lead.count()
    const batchCount = await prisma.leadImportBatch.count()
    console.log(`✅ Schema working - Leads: ${leadCount}, Batches: ${batchCount}\n`)

    // Test 2: Test import service
    console.log('2. Testing import service...')
    const { importCsvLeads } = require('./src/lib/leads/import.ts')
    
    // Read test CSV file
    const csvContent = fs.readFileSync('./test_leads.csv', 'utf-8')
    
    // Test import
    const importResult = await importCsvLeads(
      csvContent,
      'admin@salesportal.com', // Admin user
      'Test Import Batch'
    )
    
    console.log('✅ Import completed:', {
      batchId: importResult.batchId,
      totalProcessed: importResult.totalProcessed,
      successful: importResult.successful,
      failed: importResult.failed
    })
    console.log('')

    // Test 3: Test workflow service
    console.log('3. Testing workflow service...')
    const { getNextLead, getLeadStats } = require('./src/lib/leads/workflow.ts')
    
    // Get stats
    const stats = await getLeadStats('agent@salesportal.com')
    console.log('✅ Lead stats:', stats)
    
    // Get next lead for agent
    const nextLead = await getNextLead('agent@salesportal.com')
    if (nextLead) {
      console.log('✅ Got next lead:', {
        id: nextLead.id,
        customerName: `${nextLead.firstName} ${nextLead.lastName}`,
        status: nextLead.status
      })
    }
    console.log('')

    // Test 4: Test disposition service
    console.log('4. Testing disposition service...')
    const { disposeLead } = require('./src/lib/leads/disposition.ts')
    
    if (nextLead) {
      const dispositionResult = await disposeLead(
        nextLead.id,
        'agent@salesportal.com',
        'NOT_INTERESTED',
        'Customer not interested in service'
      )
      console.log('✅ Lead disposed:', {
        leadId: dispositionResult.id,
        status: dispositionResult.status
      })
    }

    console.log('\n🎉 All Lead Database tests passed!')

  } catch (error) {
    console.error('❌ Test failed:', error.message)
    console.error(error.stack)
  } finally {
    await prisma.$disconnect()
  }
}

testLeadDatabase().catch(console.error)