import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';

// Bulk generation schema
const bulkGenerateSchema = z.object({
  saleIds: z.array(z.string().min(1)).min(1),
  templateIds: z.array(z.string().min(1)).min(1),
});

export async function POST(request: NextRequest) {
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

    // Authentication - only admins can bulk generate
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Parse and validate request body
    const body = await request.json();
    const { saleIds, templateIds } = bulkGenerateSchema.parse(body);

    // Initialize enhanced template service
    const enhancedTemplateService = new EnhancedTemplateService();
    
    // Track results
    const results: {
      generated: number;
      failed: number;
      errors: string[];
      documents: any[];
    } = {
      generated: 0,
      failed: 0,
      errors: [],
      documents: []
    };

    // Load database connection
    const { prisma } = await import('@/lib/prisma');

    // Generate documents for each sale (using Flash Team welcome letter template)
    for (const saleId of saleIds) {
      try {
        // Load sale data
        const sale = await prisma.sale.findUnique({
          where: { id: saleId },
          include: {
            appliances: true,
            createdBy: {
              select: { email: true }
            }
          }
        });

        if (!sale) {
          results.failed++;
          results.errors.push(`Sale ${saleId.slice(-6)}: Sale not found`);
          continue;
        }

        // Transform sale data for template
        const templateData = {
          customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
          email: sale.email,
          phone: sale.phoneNumber,
          address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
          coverageStartDate: new Date().toLocaleDateString('en-GB'),
          policyNumber: `FT-2025-${sale.id.slice(-6)}`,
          totalCost: sale.totalPlanCost.toString(),
          monthlyCost: (sale.totalPlanCost / 12).toFixed(2),
          hasApplianceCover: sale.applianceCoverSelected,
          hasBoilerCover: sale.boilerCoverSelected,
          currentDate: new Date().toLocaleDateString('en-GB', { 
            day: 'numeric',
            month: 'long',
            year: 'numeric'
          })
        };

        // Generate document using enhanced service
        const documentContent = await enhancedTemplateService.generateDocument('welcome-letter', templateData);
        
        const document = {
          id: `doc-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          content: documentContent,
          fileName: `welcome-letter-${sale.customerFirstName}-${sale.customerLastName}.html`,
          templateName: 'Flash Team Welcome Letter',
          saleId: sale.id,
          customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
          customerEmail: sale.email,
          generatedAt: new Date().toISOString(),
          downloadUrl: `/api/paperwork/download/${sale.id}`
        };

        results.documents.push(document);
        results.generated++;
      } catch (error) {
        results.failed++;
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        results.errors.push(`Sale ${saleId.slice(-6)}: ${errorMessage}`);
        console.error(`Bulk generation error for sale ${saleId}:`, error);
      }
    }

    return NextResponse.json({
      success: true,
      ...results,
      total: saleIds.length
    });

  } catch (error) {
    console.error('Bulk generate documents error:', error);

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid request data', details: error.issues },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}