const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function testWiseguysTemplate() {
  try {
    console.log('🔍 Checking Wiseguys template in database...');

    // Find the Wiseguys template
    const wiseguysTemplate = await prisma.documentTemplate.findFirst({
      where: {
        OR: [
          { templateType: 'wiseguys-welcome-letter' },
          { name: { contains: 'Wiseguys', mode: 'insensitive' } }
        ]
      }
    });

    if (wiseguysTemplate) {
      console.log('✅ Wiseguys template found!');
      console.log('📋 Template details:', {
        id: wiseguysTemplate.id,
        name: wiseguysTemplate.name,
        templateType: wiseguysTemplate.templateType,
        isActive: wiseguysTemplate.isActive,
        contentLength: wiseguysTemplate.htmlContent.length
      });

      // Check if it has the authentic branding
      const hasGreenColor = wiseguysTemplate.htmlContent.includes('#7ED321');
      const hasCharcoalBg = wiseguysTemplate.htmlContent.includes('#3a3a3a');
      const hasRealPhone = wiseguysTemplate.htmlContent.includes('01202 806060');
      const hasRealQuote = wiseguysTemplate.htmlContent.includes('Lindsay Tara');
      
      console.log('🎨 Branding check:');
      console.log(`  - Has lime green (#7ED321): ${hasGreenColor}`);
      console.log(`  - Has charcoal background (#3a3a3a): ${hasCharcoalBg}`);
      console.log(`  - Has real phone (01202 806060): ${hasRealPhone}`);
      console.log(`  - Has real customer quote (Lindsay Tara): ${hasRealQuote}`);
      
      if (hasGreenColor && hasCharcoalBg && hasRealPhone && hasRealQuote) {
        console.log('🎉 Template has authentic Wiseguys branding!');
      } else {
        console.log('⚠️ Template needs branding updates');
      }

    } else {
      console.log('❌ Wiseguys template not found in database');
    }

  } catch (error) {
    console.error('❌ Error checking template:', error);
  } finally {
    await prisma.$disconnect();
  }
}

testWiseguysTemplate();