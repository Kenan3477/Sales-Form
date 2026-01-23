import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function identifyPricingDiscrepancies() {
  console.log('Identifying pricing discrepancies...');
  
  try {
    const sales = await prisma.sale.findMany({
      include: {
        appliances: true
      }
    });

    console.log(`Checking ${sales.length} sales for discrepancies...`);
    
    let discrepancies = [];
    let correctTotalSum = 0;
    let currentTotalSum = 0;
    let adjustmentNeeded = 0;

    for (const sale of sales) {
      // Calculate what the total SHOULD be
      let correctTotal = 0;
      
      // Add boiler cost if selected
      if (sale.boilerCoverSelected && sale.boilerPriceSelected) {
        correctTotal += parseFloat(sale.boilerPriceSelected.toString());
      }
      
      // Add appliance costs
      if (sale.appliances && sale.appliances.length > 0) {
        for (const appliance of sale.appliances) {
          correctTotal += appliance.cost;
        }
      }
      
      correctTotal = Math.round(correctTotal * 100) / 100;
      const currentTotal = parseFloat(sale.totalPlanCost?.toString() || '0');
      
      correctTotalSum += correctTotal;
      currentTotalSum += currentTotal;
      
      // Check for discrepancy
      if (Math.abs(currentTotal - correctTotal) > 0.01) {
        discrepancies.push({
          name: `${sale.customerFirstName} ${sale.customerLastName}`,
          current: currentTotal,
          correct: correctTotal,
          difference: currentTotal - correctTotal
        });
        adjustmentNeeded += (correctTotal - currentTotal);
      }
    }

    console.log(`\n=== PRICING ANALYSIS ===`);
    console.log(`Current total system value: £${currentTotalSum.toFixed(2)}`);
    console.log(`Correct total system value: £${correctTotalSum.toFixed(2)}`);
    console.log(`Total adjustment needed: £${adjustmentNeeded.toFixed(2)}`);
    console.log(`Sales with discrepancies: ${discrepancies.length}`);

    if (discrepancies.length > 0) {
      console.log(`\n=== TOP 10 DISCREPANCIES ===`);
      discrepancies
        .sort((a, b) => Math.abs(b.difference) - Math.abs(a.difference))
        .slice(0, 10)
        .forEach(d => {
          console.log(`${d.name}: £${d.current} → £${d.correct} (${d.difference > 0 ? '+' : ''}${d.difference.toFixed(2)})`);
        });
    }

    // What would the total be if we target £70K?
    const targetTotal = 70000;
    const reductionNeeded = currentTotalSum - targetTotal;
    
    console.log(`\n=== TARGET ANALYSIS ===`);
    console.log(`Target total: £${targetTotal.toFixed(2)}`);
    console.log(`Current total: £${currentTotalSum.toFixed(2)}`);
    console.log(`Reduction needed: £${reductionNeeded.toFixed(2)}`);
    console.log(`Average reduction per sale: £${(reductionNeeded / sales.length).toFixed(2)}`);
    
  } catch (error) {
    console.error('Error identifying discrepancies:', error);
  } finally {
    await prisma.$disconnect();
  }
}

identifyPricingDiscrepancies();