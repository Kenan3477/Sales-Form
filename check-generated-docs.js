const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function checkGeneratedDocuments() {
  try {
    console.log('Checking recently generated documents...')
    
    const recentDocuments = await prisma.generatedDocument.findMany({
      select: {
        id: true,
        filename: true,
        generatedAt: true,
        metadata: true,
        sale: {
          select: {
            customerFirstName: true,
            customerLastName: true
          }
        },
        template: {
          select: {
            name: true,
            templateType: true
          }
        }
      },
      orderBy: {
        generatedAt: 'desc'
      },
      take: 5
    });

    console.log(`\n📋 Found ${recentDocuments.length} recent documents:\n`);

    recentDocuments.forEach((doc, index) => {
      const customer = `${doc.sale.customerFirstName} ${doc.sale.customerLastName}`;
      const template = doc.template ? doc.template.name : 'Unknown Template';
      const templateType = doc.template ? doc.template.templateType : doc.metadata?.templateType || 'Unknown Type';
      const generationMethod = doc.metadata?.generationMethod || 'Unknown Method';
      
      console.log(`${index + 1}. ${customer}`);
      console.log(`   Template: ${template} (${templateType})`);
      console.log(`   Filename: ${doc.filename}`);
      console.log(`   Method: ${generationMethod}`);
      console.log(`   Created: ${new Date(doc.generatedAt).toLocaleString()}`);
      console.log('');
    });

    // Check specifically for Coverage Continuation Notice documents
    const coverageNotices = recentDocuments.filter(doc => 
      doc.template?.templateType === 'uncontacted_customer_notice' ||
      doc.metadata?.templateType === 'uncontacted_customer_notice'
    );

    if (coverageNotices.length > 0) {
      console.log(`✅ Found ${coverageNotices.length} Coverage Continuation Notice document(s)!`);
      console.log('✅ The uncontacted customer template is generating correctly.');
    } else {
      console.log('❌ No Coverage Continuation Notice documents found recently.');
    }

  } catch (error) {
    console.error('❌ Error checking documents:', error);
  } finally {
    await prisma.$disconnect();
  }
}

checkGeneratedDocuments();