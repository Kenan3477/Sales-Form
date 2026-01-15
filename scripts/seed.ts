import { prisma } from '../src/lib/prisma';
import bcrypt from 'bcryptjs';

async function seedDatabase() {
  try {
    console.log('🌱 Starting database seed...');

    // Check if admin already exists
    const existingAdmin = await prisma.user.findFirst({ 
      where: { role: 'ADMIN' } 
    });

    if (existingAdmin) {
      console.log('✅ Admin user already exists:', existingAdmin.email);
      return;
    }

    console.log('📝 Creating admin and agent users...');

    // Hash passwords
    const adminPassword = await bcrypt.hash('admin123', 12);
    const agentPassword = await bcrypt.hash('agent123', 12);

    // Create users
    const admin = await prisma.user.create({
      data: {
        email: 'admin@salesportal.com',
        password: adminPassword,
        name: 'Admin User',
        role: 'ADMIN',
      },
    });

    const agent = await prisma.user.create({
      data: {
        email: 'agent@salesportal.com',
        password: agentPassword,
        name: 'Sales Agent',
        role: 'AGENT',
      },
    });

    console.log('👤 Created admin user:', admin.email);
    console.log('👤 Created agent user:', agent.email);

    // Create default field configurations
    console.log('⚙️ Creating field configurations...');
    const defaultConfigs = [
      { fieldName: 'customerName', mandatory: true },
      { fieldName: 'customerEmail', mandatory: true },
      { fieldName: 'customerPhone', mandatory: true },
      { fieldName: 'customerAddress', mandatory: true },
      { fieldName: 'customerPostcode', mandatory: true },
      { fieldName: 'energySupplier', mandatory: false },
      { fieldName: 'accountNumber', mandatory: false },
      { fieldName: 'propertyType', mandatory: true },
      { fieldName: 'numBedrooms', mandatory: true },
      { fieldName: 'boilerAge', mandatory: false },
      { fieldName: 'applianceBreakdown', mandatory: false },
      { fieldName: 'boilerBreakdown', mandatory: false },
    ];

    await prisma.fieldConfiguration.createMany({
      data: defaultConfigs,
    });

    console.log('✅ Database seeded successfully!');
    console.log('🔐 Login credentials:');
    console.log('   Admin: admin@salesportal.com / admin123');
    console.log('   Agent: agent@salesportal.com / agent123');

  } catch (error) {
    console.error('❌ Error seeding database:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

if (require.main === module) {
  seedDatabase();
}

export default seedDatabase;