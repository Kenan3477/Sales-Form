import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function deleteAllGeneratedDocuments() {
  console.log('🗑️  DELETING ALL GENERATED DOCUMENTS')
  console.log('===================================')
  
  try {
    // First, count how many documents we have
    const totalCount = await prisma.generatedDocument.count()
    console.log(`📊 Total generated documents found: ${totalCount}`)
    
    if (totalCount === 0) {
      console.log('✅ No generated documents found to delete')
      return
    }
    
    // Get some sample documents before deletion
    console.log('\n📋 Sample documents to be deleted:')
    const samples = await prisma.generatedDocument.findMany({
      take: 10,
      select: {
        id: true,
        filename: true,
        generatedAt: true,
        sale: {
          select: {
            customerFirstName: true,
            customerLastName: true
          }
        },
        template: {
          select: {
            name: true
          }
        }
      }
    })
    
    samples.forEach((doc, index) => {
      console.log(`  ${index + 1}. ${doc.template.name} for ${doc.sale.customerFirstName} ${doc.sale.customerLastName} (${doc.generatedAt.toLocaleDateString()})`)
    })
    
    if (totalCount > 10) {
      console.log(`  ... and ${totalCount - 10} more documents`)
    }
    
    console.log('\n⚠️  WARNING: This will permanently delete ALL generated documents!')
    console.log('⚠️  This action cannot be undone!')
    
    // Proceed with deletion
    console.log('\n🔄 Deleting all generated documents...')
    
    const deleteResult = await prisma.generatedDocument.deleteMany({})
    
    console.log(`✅ Successfully deleted ${deleteResult.count} generated documents`)
    
    // Verify deletion
    const remainingCount = await prisma.generatedDocument.count()
    console.log(`📊 Remaining documents: ${remainingCount}`)
    
    if (remainingCount === 0) {
      console.log('✅ All generated documents have been successfully deleted')
    } else {
      console.log(`⚠️  Warning: ${remainingCount} documents still remain`)
    }
    
  } catch (error) {
    console.error('❌ Error deleting generated documents:', error)
  } finally {
    await prisma.$disconnect()
  }
}

deleteAllGeneratedDocuments().catch(console.error)