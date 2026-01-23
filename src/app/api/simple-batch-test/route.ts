import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

export async function GET(request: NextRequest) {
  console.log('🔄 Starting SIMPLE batch PDF download...');
  
  try {
    // Step 1: Authentication
    console.log('Step 1: Checking authentication...');
    const session = await getServerSession(authOptions);
    
    if (!session?.user) {
      console.log('❌ No session found');
      return NextResponse.json({ error: 'Unauthorized', step: 'session' }, { status: 401 });
    }
    
    if (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT') {
      console.log('❌ Insufficient role:', session.user.role);
      return NextResponse.json({ error: 'Unauthorized', step: 'role', role: session.user.role }, { status: 403 });
    }
    
    console.log('✅ Authentication passed for user:', session.user.email);

    // Step 2: Parse parameters
    console.log('Step 2: Parsing URL parameters...');
    const url = new URL(request.url);
    const batch = parseInt(url.searchParams.get('batch') || '1');
    const totalBatches = parseInt(url.searchParams.get('totalBatches') || '1');
    const batchSize = parseInt(url.searchParams.get('batchSize') || '50');
    const downloadAll = url.searchParams.get('downloadAll') === 'true';
    
    console.log('✅ Parameters parsed:', { batch, totalBatches, batchSize, downloadAll });

    // Step 3: Simple database test
    console.log('Step 3: Testing database connection...');
    const docCount = await prisma.generatedDocument.count({
      where: { isDeleted: false }
    });
    
    console.log('✅ Database connection working, total docs:', docCount);

    // For now, just return success without processing PDFs
    return NextResponse.json({
      status: 'simple_test_success',
      message: `Simple batch ${batch}/${totalBatches} test completed`,
      parameters: { batch, totalBatches, batchSize, downloadAll },
      documentCount: docCount,
      user: session.user.email,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('❌ Simple batch error:', error);
    
    // Detailed error response
    const errorInfo = {
      error: 'Simple batch test failed',
      message: error instanceof Error ? error.message : 'Unknown error',
      type: typeof error,
      name: error instanceof Error ? error.name : 'Unknown',
      stack: error instanceof Error ? error.stack?.split('\n').slice(0, 5) : []
    };
    
    console.error('Error details:', errorInfo);
    
    return NextResponse.json(errorInfo, { status: 500 });
  }
}