import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export async function GET(request: NextRequest) {
  try {
    // Check if this is a setup request
    const url = new URL(request.url);
    const setup = url.searchParams.get('setup');
    
    if (setup === 'init') {
      // Check if already initialized
      const existingAdmin = await prisma.user.findFirst({ where: { role: 'ADMIN' } });
      if (existingAdmin) {
        return NextResponse.json({
          status: 'already_initialized',
          message: 'Database already has admin users',
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
      });

      return NextResponse.json({
        status: 'initialized',
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
    }

    // Regular health check
    return NextResponse.json(
      { 
        status: 'healthy',
        service: 'Sales Form Portal',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      },
      { status: 200 }
    );
  } catch (error) {
    console.error('Health check error:', error);
    return NextResponse.json(
      { 
        status: 'unhealthy',
        error: 'Service unavailable',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 503 }
    );
  }
}