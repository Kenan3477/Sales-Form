const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function checkRecentPricingChanges() {
  console.log('🔍 Checking for recent pricing changes that need to be reverted...\n');
  
  try {
    // Based on the previous output, these were the customers that were "fixed"
    // Let me check their current status
    
    const customersToCheck = [
      { firstName: 'Mary', lastName: 'Roberts', email: 'robertsm19@sky.com' },
      { firstName: 'Pauline', lastName: 'Carr', email: 'pollycarr11@gmail.com' },
      { firstName: 'Shirley', lastName: 'Robertson', email: 'shirley.robertson@placeholder.com' },
      { firstName: 'Thomas', lastName: 'Passey', email: 'tfPassey36@gmail.com' }
    ];
    
    console.log('👥 Checking the 4 customers that were previously "fixed" from £1 pricing:\n');
    
    for (const customer of customersToCheck) {
      const sale = await prisma.sale.findFirst({
        where: {
          customerFirstName: customer.firstName,
          customerLastName: customer.lastName,
          email: customer.email
        },
        include: {
          appliances: true
        }
      });
      
      if (sale) {
        const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
        const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
        
        console.log(`👤 ${sale.customerFirstName} ${sale.customerLastName} (${sale.email})`);
        console.log(`   💰 Current total: £${sale.totalPlanCost}`);
        console.log(`   🔧 Appliances: £${applianceTotal} (${sale.appliances.length} items)`);
        console.log(`   🏠 Boiler: £${boilerPrice} (selected: ${sale.boilerCoverSelected})`);
        console.log(`   🏷️ Sale ID: ${sale.id}`);
        console.log(`   📅 Last updated: ${sale.updatedAt}`);
        
        if (sale.appliances.length > 0) {
          console.log(`   📦 Appliances:`);
          sale.appliances.forEach((app, index) => {
            console.log(`      ${index + 1}. ${app.appliance}${app.otherText ? ` (${app.otherText})` : ''} - £${app.cost}`);
          });
        }
        
        // Determine if this looks like it was changed from £1
        if (sale.totalPlanCost === 29.99 && sale.appliances.length === 0 && sale.boilerCoverSelected) {
          console.log(`   ⚠️  This appears to have been changed from £1 to £29.99 (boiler only)`);
        } else if (sale.totalPlanCost === 114.98 && applianceTotal === 84.99 && boilerPrice === 29.99) {
          console.log(`   ⚠️  This appears to have been changed from £1 to calculated total`);
        }
        
        console.log('');
      } else {
        console.log(`❌ Could not find sale for ${customer.firstName} ${customer.lastName}`);
      }
    }
    
    // Also check if there are any customers with suspiciously round numbers that might indicate recent changes
    console.log('\n🔍 Checking for other potential recent pricing changes...\n');
    
    const recentlyUpdated = await prisma.sale.findMany({
      where: {
        updatedAt: {
          gte: new Date('2026-01-23') // Today's changes
        }
      },
      include: {
        appliances: true
      },
      orderBy: {
        updatedAt: 'desc'
      }
    });
    
    if (recentlyUpdated.length > 0) {
      console.log(`📅 Found ${recentlyUpdated.length} sales updated today:`);
      recentlyUpdated.forEach(sale => {
        const appTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
        const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
        console.log(`   ${sale.customerFirstName} ${sale.customerLastName}: £${sale.totalPlanCost} (updated: ${sale.updatedAt.toLocaleTimeString()})`);
      });
    } else {
      console.log('✅ No sales were updated today');
    }
    
  } catch (error) {
    console.error('❌ Error checking pricing changes:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkRecentPricingChanges();