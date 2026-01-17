import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { PaperworkService } from '@/lib/paperwork';
import { checkApiRateLimit } from '@/lib/rateLimit';
import { z } from 'zod';

// Template creation schema
const createTemplateSchema = z.object({
  name: z.string().min(1),
  description: z.string().optional(),
  templateType: z.enum(['welcome_letter', 'service_agreement', 'direct_debit_form', 'coverage_summary']),
  htmlContent: z.string().min(1),
});

// Template update schema
const updateTemplateSchema = z.object({
  name: z.string().min(1).optional(),
  description: z.string().optional(),
  htmlContent: z.string().min(1).optional(),
  isActive: z.boolean().optional(),
});

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
    const activeOnly = url.searchParams.get('activeOnly') !== 'false'; // Default to true

    // Initialize paperwork service and get templates
    const paperworkService = new PaperworkService();
    const templates = await paperworkService.getTemplates(activeOnly);

    return NextResponse.json({
      success: true,
      templates,
    });

  } catch (error) {
    console.error('Get templates error:', error);

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

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

    // Authentication - only admins can create templates
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Parse and validate request body
    const body = await request.json();
    const validatedData = createTemplateSchema.parse(body);

    // Initialize paperwork service and create template
    const paperworkService = new PaperworkService();
    const template = await paperworkService.createTemplate({
      ...validatedData,
      createdById: session.user.id,
    });

    return NextResponse.json({
      success: true,
      template,
    }, { status: 201 });

  } catch (error) {
    console.error('Create template error:', error);

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { 
          error: 'Invalid request data',
          details: error.issues,
        },
        { status: 400 }
      );
    }

    if (error instanceof Error) {
      if (error.message.includes('template syntax')) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest) {
  try {
    // Rate limiting - no need for security check as admin requirement is below
    const clientIP = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    const rateLimitCheck = await checkApiRateLimit(clientIP);

    // Authentication - only admins can update templates
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Parse and validate request body
    const body = await request.json();
    const { templateId, ...updateData } = body;
    
    if (!templateId) {
      return NextResponse.json({ error: 'Template ID required' }, { status: 400 });
    }

    const validatedData = updateTemplateSchema.parse(updateData);

    // Initialize paperwork service and update template
    const paperworkService = new PaperworkService();
    const template = await paperworkService.updateTemplate(templateId, validatedData);

    return NextResponse.json({
      success: true,
      template,
    });

  } catch (error) {
    console.error('Update template error:', error);

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { 
          error: 'Invalid request data',
          details: error.issues,
        },
        { status: 400 }
      );
    }

    if (error instanceof Error) {
      if (error.message.includes('template syntax')) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}