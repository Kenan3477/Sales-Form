import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function checkCurrentPricing() {
  console.log('Checking current pricing structure...');
  
  try {
    // Get a sample of sales to understand the current pricing
    const sampleSales = await prisma.sale.findMany({
      take: 10,
      include: {
        appliances: true
      },
      orderBy: {
        totalPlanCost: 'desc'
      }
    });

    console.log('\n=== TOP 10 HIGHEST COST SALES ===');
    let totalSystemValue = 0;
    
    for (const sale of sampleSales) {
      console.log(`${sale.customerFirstName} ${sale.customerLastName}: £${sale.totalPlanCost}`);
      console.log(`  Boiler: ${sale.boilerCoverSelected ? 'Yes' : 'No'} (£${sale.boilerPriceSelected || 0})`);
      console.log(`  Appliances: ${sale.appliances.length} items`);
      if (sale.appliances.length > 0) {
        sale.appliances.forEach(app => {
          console.log(`    - ${app.appliance}: £${app.cost}`);
        });
      }
      console.log('---');
      totalSystemValue += parseFloat(sale.totalPlanCost?.toString() || '0');
    }

    // Get total system value
    const allSales = await prisma.sale.findMany({
      select: {
        totalPlanCost: true
      }
    });

    const totalValue = allSales.reduce((sum, sale) => {
      return sum + parseFloat(sale.totalPlanCost?.toString() || '0');
    }, 0);

    console.log(`\n=== SYSTEM TOTALS ===`);
    console.log(`Total Sales: ${allSales.length}`);
    console.log(`Total System Value: £${totalValue.toFixed(2)}`);
    console.log(`Average Sale Value: £${(totalValue / allSales.length).toFixed(2)}`);
    
    // Check for any suspiciously high individual costs
    const expensiveAppliances = await prisma.appliance.findMany({
      where: {
        cost: {
          gt: 50
        }
      },
      include: {
        sale: {
          select: {
            customerFirstName: true,
            customerLastName: true
          }
        }
      }
    });

    if (expensiveAppliances.length > 0) {
      console.log(`\n=== EXPENSIVE APPLIANCES (>£50) ===`);
      expensiveAppliances.forEach(app => {
        console.log(`${app.sale.customerFirstName} ${app.sale.customerLastName}: ${app.appliance} - £${app.cost}`);
      });
    } else {
      console.log(`\n✅ No appliances over £50 found`);
    }
    
  } catch (error) {
    console.error('Error checking pricing:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkCurrentPricing();