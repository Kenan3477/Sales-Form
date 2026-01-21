import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';

export async function GET(request: NextRequest) {
  try {
    // Rate limiting
    const clientIP = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    const rateLimitCheck = await checkApiRateLimit(clientIP);
    if (!rateLimitCheck.success) {
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { status: 429 }
      );
    }

    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get query parameters
    const url = new URL(request.url);
    const saleId = url.searchParams.get('saleId');
    const customerStatus = url.searchParams.get('customerStatus');
    const userId = session.user.role === 'AGENT' ? session.user.id : undefined;
    
    // Pagination parameters
    const page = parseInt(url.searchParams.get('page') || '1');
    const limit = parseInt(url.searchParams.get('limit') || '100');
    const skip = (page - 1) * limit;

    // Query generated documents from database
    const { prisma } = await import('@/lib/prisma');
    
    const whereClause: any = {
      isDeleted: false
    };

    // If specific sale ID is requested
    if (saleId) {
      whereClause.saleId = saleId;
    }

    // If agent user, only show their own sales' documents
    if (userId) {
      whereClause.sale = {
        createdById: userId
      };
    }

    // If customer status filter is requested
    if (customerStatus && customerStatus !== 'all') {
      whereClause.sale = {
        ...whereClause.sale,
        status: customerStatus.toUpperCase()
      };
    }

    console.log('📋 Fetching documents with where clause:', JSON.stringify(whereClause, null, 2));
    console.log('📋 Pagination: page', page, 'limit', limit, 'skip', skip);

    // Get total count for pagination
    const totalCount = await prisma.generatedDocument.count({
      where: whereClause
    });

    const documents = await prisma.generatedDocument.findMany({
      where: whereClause,
      include: {
        sale: {
          select: {
            id: true,
            customerFirstName: true,
            customerLastName: true,
            email: true,
            status: true,
            createdBy: {
              select: {
                email: true
              }
            }
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
      skip: skip,
      take: limit
    });

    console.log('📋 Found documents from database:', documents.length);
    if (documents.length > 0) {
      console.log('📋 First document:', JSON.stringify(documents[0], null, 2));
    }

    // Transform the data for frontend consumption
    const transformedDocuments = documents.map((doc: any) => ({
      id: doc.id,
      saleId: doc.saleId,
      templateId: doc.templateId,
      templateName: doc.template?.name || 'Unknown Template',
      fileName: doc.filename,
      downloadCount: doc.downloadCount,
      createdAt: doc.generatedAt.toISOString(),
      sale: {
        id: doc.sale?.id || '',
        customer: {
          fullName: `${doc.sale?.customerFirstName || ''} ${doc.sale?.customerLastName || ''}`.trim(),
          email: doc.sale?.email || ''
        },
        status: doc.sale?.status || 'ACTIVE'
      }
    }));

    console.log('📋 Returning transformed documents:', transformedDocuments.length);

    return NextResponse.json({
      success: true,
      documents: transformedDocuments,
      pagination: {
        page: page,
        limit: limit,
        total: totalCount,
        totalPages: Math.ceil(totalCount / limit),
        hasMore: skip + documents.length < totalCount
      }
    });

  } catch (error) {
    console.error('Get documents error:', error);

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}