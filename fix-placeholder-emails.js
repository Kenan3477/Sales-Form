import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function fixPlaceholderEmails() {
  console.log('🔧 FIXING PLACEHOLDER EMAIL DATA CORRUPTION')
  console.log('============================================')
  
  try {
    // First, count affected records
    const affectedRecords = await prisma.sale.count({
      where: {
        email: {
          contains: '@placeholder.com'
        }
      }
    })
    
    console.log(`📊 Found ${affectedRecords} sales with placeholder emails`)
    
    if (affectedRecords === 0) {
      console.log('✅ No placeholder emails found in production database')
      return
    }
    
    // Get sample of affected records
    const sampleRecords = await prisma.sale.findMany({
      where: {
        email: {
          contains: '@placeholder.com'
        }
      },
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        phoneNumber: true,
        createdAt: true
      },
      take: 10
    })
    
    console.log('📋 Sample affected customers:')
    sampleRecords.forEach(record => {
      console.log(`  - ${record.customerFirstName} ${record.customerLastName}: ${record.email} (Phone: ${record.phoneNumber})`)
    })
    
    console.log('')
    console.log('🚨 CRITICAL DATA CORRUPTION DETECTED!')
    console.log('=====================================')
    console.log('❌ Customer email addresses were artificially generated')
    console.log('❌ This violates data integrity principles')
    console.log('❌ Real customer contact information has been lost')
    console.log('')
    
    // Mark these records for manual review by setting email to empty
    console.log('⚡ Applying emergency fix: Setting placeholder emails to empty...')
    
    const updateResult = await prisma.sale.updateMany({
      where: {
        email: {
          contains: '@placeholder.com'
        }
      },
      data: {
        email: '' // Set to empty rather than keeping fake email
      }
    })
    
    console.log(`✅ Updated ${updateResult.count} records - placeholder emails removed`)
    console.log('')
    console.log('📝 NEXT STEPS REQUIRED:')
    console.log('1. Review these customers manually')
    console.log('2. Attempt to recover original email addresses from source data')
    console.log('3. Contact customers via phone to obtain correct email addresses')
    console.log('4. Implement data validation to prevent future corruption')
    console.log('')
    console.log('🔒 Emergency fix complete - manual review required')
    
  } catch (error) {
    console.error('❌ Error fixing placeholder emails:', error)
  } finally {
    await prisma.$disconnect()
  }
}

fixPlaceholderEmails().catch(console.error)