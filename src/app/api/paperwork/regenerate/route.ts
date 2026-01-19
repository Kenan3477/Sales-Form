import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import fs from 'fs/promises';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'admin') {
      return NextResponse.json(
        { error: 'Unauthorized - Admin access required' },
        { status: 401 }
      );
    }

    const { documentId, saleId, templateId } = await request.json();

    // Validate required fields
    if (!documentId || !saleId || !templateId) {
      return NextResponse.json(
        { error: 'Missing required fields: documentId, saleId, and templateId are required' },
        { status: 400 }
      );
    }

    // Find the existing document
    const existingDocument = await prisma.generatedDocument.findUnique({
      where: { id: documentId },
      include: {
        sale: {
          include: {
            createdBy: true
          }
        },
        template: true
      }
    });

    if (!existingDocument) {
      return NextResponse.json(
        { error: 'Document not found' },
        { status: 404 }
      );
    }

    // Get the template and sale data
    const template = await prisma.documentTemplate.findUnique({
      where: { id: templateId }
    });

    if (!template) {
      return NextResponse.json(
        { error: 'Template not found' },
        { status: 404 }
      );
    }

    const sale = existingDocument.sale;

    // Generate new document content using the template's htmlContent
    let content = template.htmlContent;

    // Replace variables in the content
    const variables = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      firstName: sale.customerFirstName,
      lastName: sale.customerLastName,
      email: sale.email,
      phoneNumber: sale.phoneNumber,
      address: sale.mailingStreet || '',
      postcode: sale.mailingPostalCode || '',
      applianceCover: sale.applianceCoverSelected ? 'Yes' : 'No',
      boilerCover: sale.boilerCoverSelected ? 'Yes' : 'No',
      totalCost: sale.totalPlanCost?.toString() || '0',
      agentName: sale.agentName || sale.createdBy.email || 'Unknown Agent',
      adminName: sale.createdBy.email || 'Unknown Admin',
      saleDate: sale.createdAt.toLocaleDateString('en-GB'),
      currentDate: new Date().toLocaleDateString('en-GB'),
      year: new Date().getFullYear().toString()
    };

    // Replace all variables in content
    for (const [key, value] of Object.entries(variables)) {
      const regex = new RegExp(`{{\\s*${key}\\s*}}`, 'g');
      content = content.replace(regex, value);
    }

    // Generate new filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${template.name}-REGENERATED-${sale.customerFirstName}-${sale.customerLastName}-${timestamp}.html`;
    const relativePath = `storage/documents/${filename}`;
    const fullPath = path.join(process.cwd(), relativePath);

    // Ensure directory exists
    await fs.mkdir(path.dirname(fullPath), { recursive: true });

    // Write the new content to file
    await fs.writeFile(fullPath, content, 'utf-8');

    // Delete old file if it exists
    if (existingDocument.filePath) {
      try {
        const oldFullPath = path.join(process.cwd(), existingDocument.filePath);
        await fs.unlink(oldFullPath);
      } catch (fileError) {
        console.warn('Failed to delete old file:', fileError);
      }
    }

    // Update the document in database (remove content field and include relations)
    const updatedDocument = await prisma.generatedDocument.update({
      where: { id: documentId },
      data: {
        filePath: relativePath,
        filename: filename
      },
      include: {
        template: true,
        sale: {
          include: {
            createdBy: true
          }
        }
      }
    });

    return NextResponse.json({
      success: true,
      document: updatedDocument,
      message: 'Document regenerated successfully'
    });

  } catch (error) {
    console.error('Error regenerating document:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}