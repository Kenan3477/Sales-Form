import { PrismaClient } from '@prisma/client';
import { TemplateService } from '../src/lib/paperwork/template-service';

const prisma = new PrismaClient();
const templateService = new TemplateService();

async function seedPaperworkTemplates() {
  try {
    console.log('🌱 Seeding paperwork templates...');

    // Check if we have any admin users
    const adminUser = await prisma.user.findFirst({
      where: { role: 'ADMIN' },
    });

    if (!adminUser) {
      console.log('❌ No admin user found. Please create an admin user first.');
      return;
    }

    console.log(`✅ Using admin user: ${adminUser.email}`);

    // Template types to create
    const templateTypes = [
      'welcome_letter',
      'service_agreement', 
      'direct_debit_form',
      'coverage_summary'
    ] as const;

    for (const templateType of templateTypes) {
      // Check if template already exists
      const existingTemplate = await prisma.documentTemplate.findFirst({
        where: { templateType, isActive: true },
      });

      if (existingTemplate) {
        console.log(`⏩ Template "${templateType}" already exists, skipping`);
        continue;
      }

      // Get default HTML content
      const htmlContent = templateService.getDefaultTemplate(templateType);

      // Create template
      const template = await prisma.documentTemplate.create({
        data: {
          name: `Default ${templateType.replace('_', ' ')} Template`,
          description: `Auto-generated default template for ${templateType.replace('_', ' ')}`,
          templateType,
          htmlContent,
          version: 1,
          isActive: true,
          createdById: adminUser.id,
        },
      });

      console.log(`✅ Created template: ${template.name} (ID: ${template.id})`);
    }

    console.log('🎉 Paperwork templates seeded successfully!');

  } catch (error) {
    console.error('❌ Error seeding paperwork templates:', error);
    throw error;
  }
}

async function main() {
  await seedPaperworkTemplates();
}

if (require.main === module) {
  main()
    .catch((e) => {
      console.error(e);
      process.exit(1);
    })
    .finally(async () => {
      await prisma.$disconnect();
    });
}

export { seedPaperworkTemplates };