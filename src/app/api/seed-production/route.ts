import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export async function POST(request: NextRequest) {
  // SECURITY: Disable production seeding entirely
  if (process.env.NODE_ENV === 'production') {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  // Only allow in development with environment variable
  if (!process.env.ALLOW_PRODUCTION_SEED) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  try {
    console.log('🌱 Starting development database seed...');

    // Check if admin already exists
    const existingAdmin = await prisma.user.findFirst({ 
      where: { role: 'ADMIN' } 
    });

    if (existingAdmin) {
      return NextResponse.json({
        status: 'already_exists',
        message: 'Admin user already exists',
        admin: { email: existingAdmin.email, role: existingAdmin.role }
      });
    }

    // Hash passwords
    const adminPassword = await bcrypt.hash('admin123', 12);
    const agentPassword = await bcrypt.hash('agent123', 12);

    // Create users
    const admin = await prisma.user.create({
      data: {
        email: 'admin@salesportal.com',
        password: adminPassword,
        role: 'ADMIN',
      },
    });

    const agent = await prisma.user.create({
      data: {
        email: 'agent@salesportal.com',
        password: agentPassword,
        role: 'AGENT',
      },
    });

    // Create default field configurations
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
      skipDuplicates: true,
    });

    return NextResponse.json({
      status: 'success',
      message: 'Production database seeded successfully',
      users: {
        admin: { email: admin.email, role: admin.role },
        agent: { email: agent.email, role: agent.role }
      }
    });

  } catch (error) {
    console.error('❌ Error seeding production database:', error);
    return NextResponse.json(
      { 
        status: 'error',
        message: 'Database seeding failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}