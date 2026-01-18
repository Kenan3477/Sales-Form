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

    // Get both Enhanced Template Service templates and database templates
    const { prisma } = await import('@/lib/prisma');
    
    // Initialize Enhanced Template Service and get templates
    const enhancedTemplateService = new EnhancedTemplateService();
    const availableTemplates = enhancedTemplateService.getAvailableTemplates();
    
    // Get database templates
    const dbTemplates = await prisma.documentTemplate.findMany({
      where: activeOnly ? { isActive: true } : {},
      include: {
        createdBy: {
          select: {
            email: true
          }
        },
        _count: {
          select: {
            generatedDocuments: true
          }
        }
      },
      orderBy: {
        updatedAt: 'desc'
      }
    });

    // Convert EnhancedTemplateService templates to expected format
    const enhancedServiceTemplates = availableTemplates.map(template => ({
      id: template.id,
      name: template.name,
      description: template.description,
      templateType: template.id.replace('-', '_'), // Convert ID to template type
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

    // Combine both template sources - database templates already have the correct format
    const allTemplates = [
      ...enhancedServiceTemplates, 
      ...dbTemplates.map(dbTemplate => ({
        ...dbTemplate,
        createdBy: dbTemplate.createdBy || { email: 'system@theflashteam.co.uk' }
      }))
    ];
    
    console.log('📄 Available templates:', {
      enhancedService: enhancedServiceTemplates.length,
      database: dbTemplates.length,
      total: allTemplates.length,
      templateIds: allTemplates.map(t => t.id)
    });

    return NextResponse.json({
      success: true,
      templates: allTemplates,
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

    // Parse request body
    const body = await request.json();
    const { name, description, templateType, htmlContent } = body;

    // Validation
    if (!name || !templateType || !htmlContent) {
      return NextResponse.json({
        error: 'Missing required fields: name, templateType, and htmlContent are required'
      }, { status: 400 });
    }

    // Import Prisma
    const { prisma } = await import('@/lib/prisma');

    // Check if template type already exists
    const existingTemplate = await prisma.documentTemplate.findFirst({
      where: {
        templateType: templateType,
        isActive: true
      }
    });

    if (existingTemplate) {
      return NextResponse.json({
        error: `Template with type '${templateType}' already exists`
      }, { status: 409 });
    }

    // Create new template
    const newTemplate = await prisma.documentTemplate.create({
      data: {
        name: name.trim(),
        description: description?.trim() || null,
        templateType: templateType.trim(),
        htmlContent: htmlContent.trim(),
        isActive: true,
        version: 1,
        createdById: session.user.id
      },
      include: {
        createdBy: {
          select: {
            email: true
          }
        },
        _count: {
          select: {
            generatedDocuments: true
          }
        }
      }
    });

    console.log(`✅ Created new template: ${newTemplate.name} (${newTemplate.templateType})`);

    return NextResponse.json({
      success: true,
      template: newTemplate,
      message: 'Template created successfully'
    }, { status: 201 });

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
    // Rate limiting
    const clientIP = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    const rateLimitCheck = await checkApiRateLimit(clientIP);
    if (!rateLimitCheck.success) {
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { status: 429 }
      );
    }

    // Authentication - only admins can update templates
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Parse request body
    const body = await request.json();
    const { id, name, description, templateType, htmlContent, isActive } = body;

    // Validation
    if (!id) {
      return NextResponse.json({
        error: 'Template ID is required'
      }, { status: 400 });
    }

    if (!name || !templateType || !htmlContent) {
      return NextResponse.json({
        error: 'Missing required fields: name, templateType, and htmlContent are required'
      }, { status: 400 });
    }

    // Import Prisma
    const { prisma } = await import('@/lib/prisma');

    // Check if template exists
    const existingTemplate = await prisma.documentTemplate.findUnique({
      where: { id }
    });

    if (!existingTemplate) {
      return NextResponse.json({
        error: 'Template not found'
      }, { status: 404 });
    }

    // Prevent editing of EnhancedTemplateService templates (they have specific IDs)
    if (['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'].includes(id)) {
      return NextResponse.json({
        error: 'Cannot edit system templates. Create a new custom template instead.'
      }, { status: 403 });
    }

    // Check if templateType already exists for a different template
    if (templateType !== existingTemplate.templateType) {
      const duplicateTemplate = await prisma.documentTemplate.findFirst({
        where: {
          templateType: templateType,
          isActive: true,
          id: { not: id }
        }
      });

      if (duplicateTemplate) {
        return NextResponse.json({
          error: `Template with type '${templateType}' already exists`
        }, { status: 409 });
      }
    }

    // Update template
    const updatedTemplate = await prisma.documentTemplate.update({
      where: { id },
      data: {
        name: name.trim(),
        description: description?.trim() || null,
        templateType: templateType.trim(),
        htmlContent: htmlContent.trim(),
        isActive: isActive !== undefined ? isActive : existingTemplate.isActive,
        version: existingTemplate.version + 1
      },
      include: {
        createdBy: {
          select: {
            email: true
          }
        },
        _count: {
          select: {
            generatedDocuments: true
          }
        }
      }
    });

    console.log(`✅ Updated template: ${updatedTemplate.name} (${updatedTemplate.templateType})`);

    return NextResponse.json({
      success: true,
      template: updatedTemplate,
      message: 'Template updated successfully'
    });

  } catch (error) {
    console.error('Update template error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}