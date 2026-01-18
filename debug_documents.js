const { PrismaClient } = require('@prisma/client');

async function checkDocuments() {
  const prisma = new PrismaClient();
  
  try {
    console.log('Checking GeneratedDocument records...');
    
    const documents = await prisma.generatedDocument.findMany({
      include: {
        sale: {
          select: {
            id: true,
            customerFirstName: true,
            customerLastName: true,
            email: true
          }
        },
        template: {
          select: {
            name: true,
            templateType: true
          }
        }
      }
    });
    
    console.log(`Found ${documents.length} documents in database:`);
    console.log(JSON.stringify(documents, null, 2));
    
    console.log('\nChecking DocumentTemplate records...');
    const templates = await prisma.documentTemplate.findMany();
    console.log(`Found ${templates.length} templates:`);
    console.log(JSON.stringify(templates.map(t => ({ id: t.id, name: t.name, type: t.templateType, active: t.isActive })), null, 2));
    
    console.log('\nChecking Sales records...');
    const sales = await prisma.sale.findMany({
      select: {
        id: true,
        customerFirstName: true,
        customerLastName: true,
        email: true,
        createdAt: true
      },
      take: 5
    });
    console.log(`Found ${sales.length} sales (showing first 5):`);
    console.log(JSON.stringify(sales, null, 2));
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkDocuments();