const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function fixAllPricingIssues() {
  console.log('🛠️  Comprehensive pricing fix - identifying and correcting calculation errors...\n');
  
  try {
    // Find all sales where the current totalPlanCost doesn't match the calculated total
    const allSales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });
    
    const salesToFix = [];
    
    console.log(`📊 Analyzing ${allSales.length} total sales for pricing inconsistencies...\n`);
    
    for (const sale of allSales) {
      const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
      const calculatedTotal = applianceTotal + boilerPrice;
      
      // Round to avoid floating point precision issues
      const roundedCalculated = Math.round(calculatedTotal * 100) / 100;
      const roundedCurrent = Math.round(sale.totalPlanCost * 100) / 100;
      
      // Check if there's a significant difference (more than 1 penny)
      if (Math.abs(roundedCalculated - roundedCurrent) > 0.01) {
        // Skip obvious test data or placeholder entries
        if (sale.customerFirstName === 'Test' || 
            sale.email === '' || 
            sale.customerFirstName === '' ||
            (calculatedTotal === 0 && sale.totalPlanCost < 5)) {
          continue;
        }
        
        salesToFix.push({
          sale,
          currentTotal: roundedCurrent,
          calculatedTotal: roundedCalculated,
          applianceTotal,
          boilerPrice,
          difference: roundedCalculated - roundedCurrent
        });
      }
    }
    
    console.log(`🔍 Found ${salesToFix.length} sales with pricing inconsistencies:\n`);
    
    // Sort by largest difference first
    salesToFix.sort((a, b) => Math.abs(b.difference) - Math.abs(a.difference));
    
    let totalRevenueCorrected = 0;
    const actualFixes = [];
    
    for (const fix of salesToFix) {
      const { sale, currentTotal, calculatedTotal, applianceTotal, boilerPrice, difference } = fix;
      
      console.log(`👤 ${sale.customerFirstName} ${sale.customerLastName} (${sale.email})`);
      console.log(`   💰 Current total: £${currentTotal}`);
      console.log(`   🔧 Appliances: £${applianceTotal} (${sale.appliances.length} items)`);
      console.log(`   🏠 Boiler: £${boilerPrice} (cover: ${sale.boilerCoverSelected}, price: ${sale.boilerPriceSelected})`);
      console.log(`   ⚡ Should be: £${calculatedTotal}`);
      console.log(`   📊 Difference: ${difference > 0 ? '+' : ''}£${difference.toFixed(2)}`);
      console.log(`   📅 Created: ${sale.createdAt.toLocaleDateString()}`);
      
      if (sale.appliances.length > 0) {
        console.log(`   📦 Appliances breakdown:`);
        sale.appliances.forEach((app, index) => {
          console.log(`      ${index + 1}. ${app.appliance}${app.otherText ? ` (${app.otherText})` : ''} - £${app.cost}`);
        });
      }
      
      // Only fix if the calculated total makes sense (greater than 0 or has valid data)
      if (calculatedTotal > 0 || (calculatedTotal === 0 && sale.appliances.length === 0 && !sale.boilerCoverSelected)) {
        console.log(`   ✅ Will fix: £${currentTotal} → £${calculatedTotal}`);
        actualFixes.push(fix);
        totalRevenueCorrected += difference;
      } else {
        console.log(`   ⚠️  Skipping - insufficient data to determine correct price`);
      }
      console.log('');
    }
    
    if (actualFixes.length === 0) {
      console.log('✅ No pricing fixes needed!');
      return;
    }
    
    console.log(`\n📋 Summary before applying fixes:`);
    console.log(`   🛠️  Sales to fix: ${actualFixes.length}`);
    console.log(`   💰 Total revenue correction: ${totalRevenueCorrected >= 0 ? '+' : ''}£${totalRevenueCorrected.toFixed(2)}`);
    console.log(`   📊 Average correction: ${totalRevenueCorrected >= 0 ? '+' : ''}£${(totalRevenueCorrected / actualFixes.length).toFixed(2)} per sale`);
    
    console.log('\n⚡ Applying fixes...\n');
    
    // Apply the fixes
    for (const fix of actualFixes) {
      const { sale, calculatedTotal } = fix;
      
      await prisma.sale.update({
        where: { id: sale.id },
        data: { totalPlanCost: calculatedTotal }
      });
      
      console.log(`✅ Fixed ${sale.customerFirstName} ${sale.customerLastName}: £${fix.currentTotal} → £${calculatedTotal}`);
    }
    
    console.log(`\n🎉 Successfully fixed ${actualFixes.length} sales with correct pricing!`);
    console.log(`💰 Total revenue properly accounted for: ${totalRevenueCorrected >= 0 ? '+' : ''}£${totalRevenueCorrected.toFixed(2)}`);
    
    // Final verification
    console.log('\n🔍 Running final verification...');
    
    const verificationSales = await prisma.sale.findMany({
      where: {
        totalPlanCost: { gt: 0, lt: 5 } // Check for remaining suspicious prices
      },
      include: {
        appliances: true
      }
    });
    
    const stillNeedFix = verificationSales.filter(sale => {
      const applianceTotal = sale.appliances.reduce((sum, app) => sum + app.cost, 0);
      const boilerPrice = sale.boilerCoverSelected && sale.boilerPriceSelected ? sale.boilerPriceSelected : 0;
      const calculatedTotal = applianceTotal + boilerPrice;
      return Math.abs(calculatedTotal - sale.totalPlanCost) > 0.01 && calculatedTotal > 5;
    });
    
    if (stillNeedFix.length === 0) {
      console.log('✅ All pricing issues resolved!');
    } else {
      console.log(`⚠️  ${stillNeedFix.length} sales may still need manual review`);
    }
    
  } catch (error) {
    console.error('❌ Error fixing pricing issues:', error);
  } finally {
    await prisma.$disconnect();
  }
}

fixAllPricingIssues();