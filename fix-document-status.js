#!/usr/bin/env node
// Migration script to fix documentsGenerated status
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function fixDocumentGenerationStatus() {
  console.log('🔧 Starting document generation status fix...');
  
  try {
    // Get unique sale IDs that have documents but are not marked as documentsGenerated
    const saleIdsWithDocs = await prisma.generatedDocument.findMany({
      where: {
        isDeleted: false
      },
      select: {
        saleId: true
      },
      distinct: ['saleId']
    });
    
    const saleIds = saleIdsWithDocs.map(doc => doc.saleId);
    console.log(`📋 Found ${saleIds.length} unique sales with documents`);
    
    if (saleIds.length === 0) {
      console.log('✅ No sales to update');
      return;
    }
    
    // Update all sales that have documents but are not marked as documentsGenerated
    const result = await prisma.sale.updateMany({
      where: {
        id: { in: saleIds },
        documentsGenerated: false
      },
      data: {
        documentsGenerated: true,
        documentsGeneratedAt: new Date(),
        documentsGeneratedBy: null // Historical documents don't have this info
      }
    });
    
    console.log(`✅ Updated ${result.count} sales to documentsGenerated: true`);
    
    // Verify the fix
    const finalCount = await prisma.sale.count({
      where: { documentsGenerated: true }
    });
    const totalDocs = await prisma.generatedDocument.count({
      where: { isDeleted: false }
    });
    
    console.log(`📊 Verification:`);
    console.log(`   - Sales marked as having documents: ${finalCount}`);
    console.log(`   - Total documents in database: ${totalDocs}`);
    console.log(`✅ Document generation status fix completed successfully!`);
    
  } catch (error) {
    console.error('❌ Error fixing document generation status:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

if (require.main === module) {
  fixDocumentGenerationStatus().catch(console.error);
}

module.exports = { fixDocumentGenerationStatus };