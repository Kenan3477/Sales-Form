import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export async function GET() {
  // SECURITY: Only allow setup check in development or if explicitly enabled
  if (process.env.NODE_ENV === 'production' && process.env.ALLOW_SETUP !== 'true') {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  try {
    // Check database connection
    await prisma.$connect();
    
    // Check if users exist
    const adminCount = await prisma.user.count({ where: { role: 'ADMIN' } });
    const agentCount = await prisma.user.count({ where: { role: 'AGENT' } });
    
    // Check if settings exist
    const settingsCount = await prisma.fieldConfiguration.count();
    
    return NextResponse.json({
      status: 'connected',
      database: 'PostgreSQL connected',
      users: {
        admins: adminCount,
        agents: agentCount,
        total: adminCount + agentCount
      },
      settings: settingsCount > 0 ? 'configured' : 'not configured',
      message: adminCount > 0 ? 'Database already initialized' : 'Database needs initialization'
    });
  } catch (error) {
    console.error('Database check error:', error);
    return NextResponse.json(
      { 
        status: 'error',
        message: 'Database connection failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}

export async function POST() {
  // SECURITY: Completely disable setup in production unless explicitly allowed
  if (process.env.NODE_ENV === 'production' && process.env.ALLOW_SETUP !== 'true') {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  try {
    // Check if already initialized
    const existingAdmin = await prisma.user.findFirst({ where: { role: 'ADMIN' } });
    if (existingAdmin) {
      return NextResponse.json({
        status: 'already_initialized',
        message: 'Database already has admin users'
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
    });

    return NextResponse.json({
      status: 'success',
      message: 'Database initialized successfully',
      users: {
        admin: { email: admin.email, role: admin.role },
        agent: { email: agent.email, role: agent.role }
      },
      defaultCredentials: {
        admin: 'admin@salesportal.com / admin123',
        agent: 'agent@salesportal.com / agent123'
      }
    });

  } catch (error) {
    console.error('Database initialization error:', error);
    return NextResponse.json(
      { 
        status: 'error',
        message: 'Database initialization failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 
      { status: 500 }
    );
  }
}