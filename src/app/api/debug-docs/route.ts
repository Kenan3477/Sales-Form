import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    console.log('🔍 Testing document count...');
    
    // Test database connection
    const session = await getServerSession(authOptions);
    console.log('🔐 Session:', { hasSession: !!session, role: session?.user?.role });
    
    if (!session?.user || (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    
    // Count total documents
    const totalDocs = await prisma.generatedDocument.count({
      where: { isDeleted: false }
    });
    
    console.log(`📊 Total documents: ${totalDocs}`);
    
    // Get first 5 documents to test the query
    const sampleDocs = await prisma.generatedDocument.findMany({
      where: { isDeleted: false },
      include: {
        sale: {
          select: {
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
      },
      take: 5,
      orderBy: {
        generatedAt: 'desc'
      }
    });
    
    console.log(`📄 Sample docs retrieved: ${sampleDocs.length}`);
    
    // Check if documents have metadata
    const docsWithMetadata = sampleDocs.filter(doc => 
      doc.metadata && 
      typeof doc.metadata === 'object' && 
      'documentContent' in doc.metadata
    );
    
    console.log(`📋 Docs with PDF content: ${docsWithMetadata.length}`);
    
    return NextResponse.json({
      status: 'success',
      totalDocuments: totalDocs,
      sampleCount: sampleDocs.length,
      docsWithContent: docsWithMetadata.length,
      sampleFilenames: sampleDocs.map(d => d.filename)
    });
    
  } catch (error) {
    console.error('❌ Debug test error:', error);
    return NextResponse.json({ 
      error: 'Debug test failed',
      details: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    }, { status: 500 });
  }
}