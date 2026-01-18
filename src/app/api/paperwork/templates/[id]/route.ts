import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { checkApiRateLimit } from '@/lib/rateLimit';

export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
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

    const { id } = params;

    // Import Prisma
    const { prisma } = await import('@/lib/prisma');

    // Get template by ID
    const template = await prisma.documentTemplate.findUnique({
      where: { id },
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

    if (!template) {
      return NextResponse.json({
        error: 'Template not found'
      }, { status: 404 });
    }

    return NextResponse.json({
      success: true,
      template
    });

  } catch (error) {
    console.error('Get template error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
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

    const { id } = params;

    // Parse request body
    const body = await request.json();
    const { name, description, templateType, htmlContent, isActive } = body;

    // Validation
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

    // Prevent editing of EnhancedTemplateService templates
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

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
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

    // Authentication - only admins can delete templates
    const session = await getServerSession(authOptions);
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    const { id } = params;

    // Import Prisma
    const { prisma } = await import('@/lib/prisma');

    // Check if template exists
    const existingTemplate = await prisma.documentTemplate.findUnique({
      where: { id },
      include: {
        _count: {
          select: {
            generatedDocuments: true
          }
        }
      }
    });

    if (!existingTemplate) {
      return NextResponse.json({
        error: 'Template not found'
      }, { status: 404 });
    }

    // Prevent deletion of EnhancedTemplateService templates
    if (['welcome-letter', 'service-agreement', 'direct-debit-form', 'coverage-summary'].includes(id)) {
      return NextResponse.json({
        error: 'Cannot delete system templates.'
      }, { status: 403 });
    }

    // Check if template has generated documents
    if (existingTemplate._count.generatedDocuments > 0) {
      // Soft delete - mark as inactive instead of hard delete
      const deactivatedTemplate = await prisma.documentTemplate.update({
        where: { id },
        data: {
          isActive: false,
          name: `[DELETED] ${existingTemplate.name}`
        }
      });

      console.log(`🗑️ Soft deleted template: ${existingTemplate.name} (had ${existingTemplate._count.generatedDocuments} generated documents)`);

      return NextResponse.json({
        success: true,
        message: `Template deactivated successfully. Template had ${existingTemplate._count.generatedDocuments} generated documents, so it was marked as inactive instead of permanently deleted.`,
        template: deactivatedTemplate
      });
    } else {
      // Hard delete - template has no generated documents
      await prisma.documentTemplate.delete({
        where: { id }
      });

      console.log(`🗑️ Hard deleted template: ${existingTemplate.name} (no generated documents)`);

      return NextResponse.json({
        success: true,
        message: 'Template deleted successfully'
      });
    }

  } catch (error) {
    console.error('Delete template error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}