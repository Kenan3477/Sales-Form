#!/usr/bin/env node

import { PrismaClient } from '@prisma/client';
import { WiseguysProfessionalTemplateService } from './src/lib/paperwork/wiseguys-professional-template.ts';

const prisma = new PrismaClient();

async function updateWiseguysTemplate() {
  try {
    console.log('🎨 Updating Wiseguys template with enhanced professional branding...');
    
    // Get the enhanced template content
    const template = WiseguysProfessionalTemplateService.getTemplate('wiseguys-tech-plan');
    
    if (!template) {
      throw new Error('Wiseguys template not found in service');
    }

    // Update the database template
    const result = await prisma.documentTemplate.update({
      where: {
        id: 'cmn6g6j330003sgoct0m540gm'
      },
      data: {
        name: template.name,
        description: template.description,
        htmlContent: template.html,
        updatedAt: new Date()
      }
    });

    console.log('✅ Wiseguys template updated successfully with professional branding! 🎨');
    console.log(`📝 Template ID: ${result.id}`);
    console.log(`🎭 New features: Enhanced Wiseguys branding, premium visual elements`);
    console.log(`📏 Template size: ${result.htmlContent.length} characters`);
    console.log('🚀 Enhanced features:');
    console.log('   • Premium logo with notification badge');
    console.log('   • Enhanced color gradients and shadows');
    console.log('   • Subtle Wiseguys watermark pattern');
    console.log('   • Professional hover effects');
    console.log('   • Enhanced typography and spacing');
    console.log('   • Premium visual polish and branding');

  } catch (error) {
    console.error('❌ Error updating Wiseguys template:', error);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

updateWiseguysTemplate();