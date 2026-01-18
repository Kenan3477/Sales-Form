import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';
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
    const activeOnly = url.searchParams.get('activeOnly') !== 'false'; // Default to true

    // Initialize Enhanced Template Service and get templates
    const enhancedTemplateService = new EnhancedTemplateService();
    const availableTemplates = enhancedTemplateService.getAvailableTemplates();
    
    // Convert to expected format
    const templates = availableTemplates.map(template => ({
      id: template.id,
      name: template.name,
      description: template.description,
      templateType: 'welcome_letter', // Since we only have welcome letter now
      htmlContent: template.html,
      isActive: true,
      version: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      createdBy: {
        name: 'Flash Team System',
        email: 'system@theflashteam.co.uk'
      },
      _count: {
        generatedDocuments: 0
      }
    }));

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
    // Authentication - only admins can create templates
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Template creation is disabled - using Flash Team template only
    return NextResponse.json({
      error: 'Template creation is disabled. Using Flash Team template only.',
    }, { status: 400 });

  } catch (error) {
    console.error('Create template error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest) {
  try {
    // Authentication - only admins can update templates
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Template update is disabled - using Flash Team template only
    return NextResponse.json({
      error: 'Template editing is disabled. Using Flash Team template only.',
    }, { status: 400 });

  } catch (error) {
    console.error('Update template error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}