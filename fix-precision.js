const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function fixFloatingPointPrecision() {
  console.log('🔧 Fixing floating point precision issues...');
  
  try {
    // Find Pauline Carr's specific record that we know has precision issues
    const precisionSale = await prisma.sale.findFirst({
      where: {
        customerFirstName: 'Pauline',
        customerLastName: 'Carr',
        totalPlanCost: { gt: 114.9, lt: 115 }
      },
      include: {
        appliances: true
      }
    });
    
    if (precisionSale) {
      const applianceTotal = precisionSale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = precisionSale.boilerPriceSelected || 0;
      const correctTotal = Math.round((applianceTotal + boilerPrice) * 100) / 100;
      
      console.log(`👤 Found precision issue: ${precisionSale.customerFirstName} ${precisionSale.customerLastName}`);
      console.log(`   💰 Current: £${precisionSale.totalPlanCost}`);
      console.log(`   🔧 Appliances: £${applianceTotal}`);
      console.log(`   🏠 Boiler: £${boilerPrice}`);
      console.log(`   ✅ Corrected: £${correctTotal}`);
      
      await prisma.sale.update({
        where: { id: precisionSale.id },
        data: { totalPlanCost: correctTotal }
      });
      
      console.log('✅ Fixed precision issue!');
    }
    
    // Final verification - check for any remaining £1 or very low prices
    console.log('\n🔍 Final verification check...');
    
    const remainingIssues = await prisma.sale.findMany({
      where: {
        totalPlanCost: { lt: 5 }
      },
      include: {
        appliances: true
      },
      orderBy: {
        totalPlanCost: 'asc'
      }
    });
    
    console.log(`📊 Found ${remainingIssues.length} sales with total cost < £5:`);
    
    for (const sale of remainingIssues) {
      const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = sale.boilerPriceSelected || 0;
      const calculatedTotal = applianceTotal + boilerPrice;
      
      console.log(`\n👤 ${sale.customerFirstName} ${sale.customerLastName} (${sale.email})`);
      console.log(`   💰 Current: £${sale.totalPlanCost}`);
      console.log(`   🔧 Appliances: £${applianceTotal} (${sale.appliances.length} items)`);
      console.log(`   🏠 Boiler: £${boilerPrice} (selected: ${sale.boilerCoverSelected})`);
      console.log(`   ⚡ Calculated: £${calculatedTotal}`);
      console.log(`   📅 Created: ${sale.createdAt.toLocaleDateString()}`);
      
      if (calculatedTotal > sale.totalPlanCost && calculatedTotal > 0) {
        console.log(`   ⚠️  Needs fixing: Should be £${calculatedTotal}`);
      } else {
        console.log(`   ✅ Appears correct or needs manual review`);
      }
    }
    
  } catch (error) {
    console.error('❌ Error fixing precision:', error);
  } finally {
    await prisma.$disconnect();
  }
}

fixFloatingPointPrecision();