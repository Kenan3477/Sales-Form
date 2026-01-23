const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function findAndFixPricingIssues() {
  console.log('🔍 Searching for customers with £1 monthly premiums...');
  
  try {
    // Find sales with £1 total plan cost
    const salesWithOnePrice = await prisma.sale.findMany({
      where: {
        totalPlanCost: 1
      },
      include: {
        appliances: true
      },
      orderBy: {
        createdAt: 'desc'
      }
    });
    
    console.log(`\n📊 Found ${salesWithOnePrice.length} sales with £1 monthly premium`);
    
    if (salesWithOnePrice.length === 0) {
      console.log('✅ No customers found with £1 pricing. Checking for other suspicious prices...');
      
      // Check for other suspiciously low prices
      const suspiciouslyLowPrices = await prisma.sale.findMany({
        where: {
          totalPlanCost: {
            lt: 5 // Less than £5
          }
        },
        include: {
          appliances: true
        },
        orderBy: {
          totalPlanCost: 'asc'
        },
        take: 20
      });
      
      console.log(`\n📊 Found ${suspiciouslyLowPrices.length} sales with suspiciously low prices (< £5):`);
      
      for (const sale of suspiciouslyLowPrices) {
        const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
        const boilerPrice = sale.boilerPriceSelected || 0;
        const calculatedTotal = applianceTotal + boilerPrice;
        
        console.log(`\n👤 ${sale.customerFirstName} ${sale.customerLastName}`);
        console.log(`   📧 ${sale.email}`);
        console.log(`   💰 Current total: £${sale.totalPlanCost}`);
        console.log(`   🔧 Appliance total: £${applianceTotal} (${sale.appliances.length} appliances)`);
        console.log(`   🏠 Boiler price: £${boilerPrice} (selected: ${sale.boilerCoverSelected})`);
        console.log(`   ⚡ Calculated total: £${calculatedTotal}`);
        console.log(`   🏷️ Sale ID: ${sale.id}`);
        console.log(`   📅 Created: ${sale.createdAt.toLocaleDateString()}`);
        
        if (sale.appliances.length > 0) {
          console.log(`   📦 Appliances:`);
          sale.appliances.forEach((app, index) => {
            console.log(`      ${index + 1}. ${app.appliance}${app.otherText ? ` (${app.otherText})` : ''} - £${app.cost}`);
          });
        }
      }
      
      return;
    }
    
    // Analyze and fix £1 pricing issues
    const fixedSales = [];
    
    for (const sale of salesWithOnePrice) {
      const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = sale.boilerPriceSelected || 0;
      const calculatedTotal = applianceTotal + boilerPrice;
      
      console.log(`\n👤 ${sale.customerFirstName} ${sale.customerLastName}`);
      console.log(`   📧 ${sale.email}`);
      console.log(`   💰 Current total: £${sale.totalPlanCost}`);
      console.log(`   🔧 Appliance total: £${applianceTotal} (${sale.appliances.length} appliances)`);
      console.log(`   🏠 Boiler price: £${boilerPrice} (selected: ${sale.boilerCoverSelected})`);
      console.log(`   ⚡ Calculated total: £${calculatedTotal}`);
      console.log(`   🏷️ Sale ID: ${sale.id}`);
      
      if (sale.appliances.length > 0) {
        console.log(`   📦 Appliances:`);
        sale.appliances.forEach((app, index) => {
          console.log(`      ${index + 1}. ${app.appliance}${app.otherText ? ` (${app.otherText})` : ''} - £${app.cost}`);
        });
      }
      
      // Only fix if we can calculate a proper total from existing data
      if (calculatedTotal > 1) {
        console.log(`   ✅ Will fix: £${sale.totalPlanCost} → £${calculatedTotal}`);
        fixedSales.push({
          id: sale.id,
          oldTotal: sale.totalPlanCost,
          newTotal: calculatedTotal,
          customer: `${sale.customerFirstName} ${sale.customerLastName}`,
          email: sale.email
        });
      } else {
        console.log(`   ⚠️  Cannot auto-fix: No valid appliance/boiler data`);
      }
    }
    
    if (fixedSales.length === 0) {
      console.log('\n❌ No sales can be auto-fixed (missing appliance/boiler data)');
      return;
    }
    
    console.log(`\n🛠️  Ready to fix ${fixedSales.length} sales:`);
    fixedSales.forEach(fix => {
      console.log(`   - ${fix.customer} (${fix.email}): £${fix.oldTotal} → £${fix.newTotal}`);
    });
    
    // Ask for confirmation (in a real scenario, we'd add user input)
    console.log('\n⚡ Applying fixes...');
    
    // Apply the fixes
    for (const fix of fixedSales) {
      await prisma.sale.update({
        where: { id: fix.id },
        data: { totalPlanCost: fix.newTotal }
      });
      console.log(`   ✅ Fixed ${fix.customer}: £${fix.oldTotal} → £${fix.newTotal}`);
    }
    
    console.log(`\n🎉 Successfully fixed ${fixedSales.length} sales with correct pricing!`);
    
    // Summary statistics
    console.log('\n📈 Summary:');
    const totalFixed = fixedSales.reduce((sum, fix) => sum + (fix.newTotal - fix.oldTotal), 0);
    console.log(`   💰 Total revenue corrected: £${totalFixed.toFixed(2)}`);
    console.log(`   📊 Average correction: £${(totalFixed / fixedSales.length).toFixed(2)} per sale`);
    
  } catch (error) {
    console.error('❌ Error finding/fixing pricing issues:', error);
  } finally {
    await prisma.$disconnect();
  }
}

// Run the function
findAndFixPricingIssues();