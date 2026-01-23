import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    // Authentication
    const session = await getServerSession(authOptions);
    if (!session?.user || (session.user.role !== 'ADMIN' && session.user.role !== 'AGENT')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('🧪 Testing PDF processing with minimal documents...');

    // Get just the first 5 documents to test
    const testDocs = await prisma.generatedDocument.findMany({
      where: { 
        isDeleted: false
      },
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

    console.log(`📊 Found ${testDocs.length} test documents`);

    if (testDocs.length === 0) {
      return NextResponse.json({
        status: 'error',
        message: 'No documents with PDF content found for testing'
      }, { status: 404 });
    }

    // Try to process just the first document
    const testDoc = testDocs[0];
    console.log(`🧪 Testing single document: ${testDoc.filename}`);

    try {
      // Dynamic import of PDF-lib
      const PDFLib = await import('pdf-lib');
      const { PDFDocument } = PDFLib;

      // Get PDF content
      if (testDoc.metadata && typeof testDoc.metadata === 'object' && 'documentContent' in testDoc.metadata) {
        const pdfContent = testDoc.metadata.documentContent as string;
        console.log(`📄 PDF content length: ${pdfContent.length} characters`);

        // Convert to buffer
        const pdfBuffer = Buffer.from(pdfContent, 'base64');
        console.log(`📄 PDF buffer size: ${pdfBuffer.length} bytes`);

        // Try to load the PDF
        const pdf = await PDFDocument.load(pdfBuffer);
        const pageCount = pdf.getPageCount();
        console.log(`📖 PDF loaded successfully: ${pageCount} pages`);

        return NextResponse.json({
          status: 'success',
          message: 'Single PDF processing test passed',
          testDocument: {
            filename: testDoc.filename,
            customer: `${testDoc.sale.customerFirstName} ${testDoc.sale.customerLastName}`,
            contentLength: pdfContent.length,
            bufferSize: pdfBuffer.length,
            pageCount: pageCount
          },
          totalTestDocuments: testDocs.length,
          allDocuments: testDocs.map(doc => ({
            filename: doc.filename,
            customer: `${doc.sale.customerFirstName} ${doc.sale.customerLastName}`,
            hasContent: !!(doc.metadata && typeof doc.metadata === 'object' && doc.metadata !== null && 'documentContent' in doc.metadata)
          }))
        });

      } else {
        throw new Error('No PDF content found in metadata');
      }

    } catch (pdfError) {
      console.error(`❌ PDF processing failed:`, pdfError);
      return NextResponse.json({
        status: 'pdf_error',
        message: 'PDF processing failed',
        error: pdfError instanceof Error ? pdfError.message : 'Unknown PDF error',
        testDocument: {
          filename: testDoc.filename,
          customer: `${testDoc.sale.customerFirstName} ${testDoc.sale.customerLastName}`
        }
      }, { status: 500 });
    }

  } catch (error) {
    console.error('❌ Test PDF processing error:', error);
    return NextResponse.json({
      status: 'test_error',
      message: 'Test failed',
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack?.split('\n').slice(0, 5) : []
    }, { status: 500 });
  }
}