import { prisma } from '@/lib/prisma';
import { PDFService } from './pdf-service';
import { TemplateService } from './template-service';
import { ContextBuilder } from './context-builder';
import { 
  DocumentGenerationRequest, 
  GeneratedDocumentResult, 
  SaleWithRelations,
  TemplateType,
  DocumentGenerationError,
  DEFAULT_PDF_OPTIONS 
} from './types';

/**
 * Main paperwork service that orchestrates document generation
 */
export class PaperworkService {
  private templateService: TemplateService;

  constructor() {
    this.templateService = new TemplateService();
  }

  /**
   * Generate a document for a sale
   */
  async generateDocument(request: DocumentGenerationRequest): Promise<GeneratedDocumentResult> {
    try {
      // 1. Fetch sale with all relations
      const sale = await this.getSaleWithRelations(request.saleId);
      if (!sale) {
        throw new Error(`Sale not found: ${request.saleId}`);
      }

      // 2. Get or find template
      const template = await this.getTemplate(request.templateType, request.templateId);

      // 3. Build template context
      const documentId = this.generateDocumentId();
      const context = ContextBuilder.buildTemplateContext(sale, documentId);

      // 4. Render HTML from template
      const htmlContent = this.templateService.renderTemplate(template.htmlContent, context);

      // 5. Generate filename and path
      const filename = PDFService.generateFilename(sale.id, template.templateType);
      const filePath = PDFService.getFilePath(filename);

      // 6. Generate PDF
      const pdfResult = await PDFService.generatePDF(htmlContent, filePath);

      // 7. Save document record to database
      const generatedDocument = await prisma.generatedDocument.create({
        data: {
          id: documentId,
          saleId: sale.id,
          templateId: template.id,
          filename,
          filePath: pdfResult.filePath,
          fileSize: pdfResult.fileSize,
          metadata: context as any, // Store context for reference
        },
        include: {
          template: true,
          sale: true,
        },
      });

      // 8. Return result
      return {
        id: generatedDocument.id,
        saleId: generatedDocument.saleId,
        templateId: generatedDocument.templateId,
        filename: generatedDocument.filename,
        filePath: generatedDocument.filePath,
        fileSize: generatedDocument.fileSize,
        downloadUrl: `/api/paperwork/download/${generatedDocument.id}`,
        metadata: context,
      };

    } catch (error) {
      const docError: DocumentGenerationError = {
        code: 'DOCUMENT_GENERATION_FAILED',
        message: `Document generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        details: error,
      };
      throw docError;
    }
  }

  /**
   * Generate document preview (return HTML or PDF buffer)
   */
  async generatePreview(
    request: DocumentGenerationRequest,
    format: 'html' | 'pdf' = 'html'
  ): Promise<{ content: string | Buffer; mimeType: string }> {
    try {
      // 1. Fetch sale with all relations
      const sale = await this.getSaleWithRelations(request.saleId);
      if (!sale) {
        throw new Error(`Sale not found: ${request.saleId}`);
      }

      // 2. Get or find template
      const template = await this.getTemplate(request.templateType, request.templateId);

      // 3. Build template context
      const documentId = 'preview-' + Date.now();
      const context = ContextBuilder.buildTemplateContext(sale, documentId);

      // 4. Render HTML from template
      const htmlContent = this.templateService.renderTemplate(template.htmlContent, context);

      if (format === 'html') {
        return {
          content: htmlContent,
          mimeType: 'text/html',
        };
      } else {
        // Generate PDF buffer
        const pdfBuffer = await PDFService.generatePDFBuffer(htmlContent);
        return {
          content: pdfBuffer,
          mimeType: 'application/pdf',
        };
      }

    } catch (error) {
      const docError: DocumentGenerationError = {
        code: 'PREVIEW_GENERATION_FAILED',
        message: `Preview generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        details: error,
      };
      throw docError;
    }
  }

  /**
   * Get all documents for a sale
   */
  async getDocumentsForSale(saleId: string): Promise<GeneratedDocumentResult[]> {
    const documents = await prisma.generatedDocument.findMany({
      where: {
        saleId,
        isDeleted: false,
      },
      include: {
        template: true,
      },
      orderBy: {
        generatedAt: 'desc',
      },
    });

    return documents.map(doc => ({
      id: doc.id,
      saleId: doc.saleId,
      templateId: doc.templateId,
      filename: doc.filename,
      filePath: doc.filePath,
      fileSize: doc.fileSize,
      downloadUrl: `/api/paperwork/download/${doc.id}`,
      metadata: doc.metadata as any,
    }));
  }

  /**
   * Delete a generated document
   */
  async deleteDocument(documentId: string): Promise<void> {
    const document = await prisma.generatedDocument.findUnique({
      where: { id: documentId },
    });

    if (!document) {
      throw new Error(`Document not found: ${documentId}`);
    }

    // Mark as deleted in database
    await prisma.generatedDocument.update({
      where: { id: documentId },
      data: { isDeleted: true },
    });

    // Optionally delete physical file (for now, keep it for audit purposes)
    // await fs.unlink(document.filePath).catch(() => {});
  }

  /**
   * Get document by ID for download
   */
  async getDocumentForDownload(documentId: string): Promise<{
    filePath: string;
    filename: string;
    mimeType: string;
  } | null> {
    const document = await prisma.generatedDocument.findUnique({
      where: { 
        id: documentId,
        isDeleted: false,
      },
    });

    if (!document) {
      return null;
    }

    // Update download count and timestamp
    await prisma.generatedDocument.update({
      where: { id: documentId },
      data: {
        downloadCount: { increment: 1 },
        lastDownloadAt: new Date(),
      },
    });

    return {
      filePath: document.filePath,
      filename: document.filename,
      mimeType: document.mimeType,
    };
  }

  /**
   * Create a new document template
   */
  async createTemplate(data: {
    name: string;
    description?: string;
    templateType: TemplateType;
    htmlContent: string;
    createdById: string;
  }): Promise<any> {
    // Validate template syntax
    const validation = this.templateService.validateTemplate(data.htmlContent);
    if (!validation.valid) {
      throw new Error(`Invalid template syntax: ${validation.error}`);
    }

    // Get next version number for this template type
    const latestTemplate = await prisma.documentTemplate.findFirst({
      where: { templateType: data.templateType },
      orderBy: { version: 'desc' },
    });

    const nextVersion = (latestTemplate?.version || 0) + 1;

    // Deactivate previous versions
    await prisma.documentTemplate.updateMany({
      where: { 
        templateType: data.templateType,
        isActive: true,
      },
      data: { isActive: false },
    });

    // Create new template
    return await prisma.documentTemplate.create({
      data: {
        ...data,
        version: nextVersion,
        isActive: true,
      },
      include: {
        createdBy: true,
      },
    });
  }

  /**
   * Get all templates
   */
  async getTemplates(activeOnly: boolean = true): Promise<any[]> {
    return await prisma.documentTemplate.findMany({
      where: activeOnly ? { isActive: true } : undefined,
      include: {
        createdBy: true,
        _count: {
          select: {
            generatedDocuments: true,
          },
        },
      },
      orderBy: [
        { templateType: 'asc' },
        { version: 'desc' },
      ],
    });
  }

  /**
   * Update template
   */
  async updateTemplate(templateId: string, data: {
    name?: string;
    description?: string;
    htmlContent?: string;
    isActive?: boolean;
  }): Promise<any> {
    if (data.htmlContent) {
      // Validate template syntax
      const validation = this.templateService.validateTemplate(data.htmlContent);
      if (!validation.valid) {
        throw new Error(`Invalid template syntax: ${validation.error}`);
      }
    }

    return await prisma.documentTemplate.update({
      where: { id: templateId },
      data,
      include: {
        createdBy: true,
      },
    });
  }

  /**
   * Private helper methods
   */

  private async getSaleWithRelations(saleId: string): Promise<SaleWithRelations | null> {
    return await prisma.sale.findUnique({
      where: { id: saleId },
      include: {
        appliances: true,
        createdBy: {
          select: {
            id: true,
            email: true,
          },
        },
      },
    });
  }

  private async getTemplate(templateType: string, templateId?: string) {
    if (templateId) {
      const template = await prisma.documentTemplate.findUnique({
        where: { id: templateId },
      });
      
      if (!template) {
        throw new Error(`Template not found: ${templateId}`);
      }
      
      return template;
    }

    // Find latest active template for the type
    const template = await prisma.documentTemplate.findFirst({
      where: {
        templateType,
        isActive: true,
      },
      orderBy: {
        version: 'desc',
      },
    });

    if (!template) {
      // Create default template if none exists
      return await this.createDefaultTemplate(templateType as TemplateType);
    }

    return template;
  }

  private async createDefaultTemplate(templateType: TemplateType) {
    const defaultHtml = this.templateService.getDefaultTemplate(templateType);
    
    // Get first admin user or create system entry
    const adminUser = await prisma.user.findFirst({
      where: { role: 'ADMIN' },
    });

    if (!adminUser) {
      throw new Error('No admin user found to create default template');
    }
    
    return await prisma.documentTemplate.create({
      data: {
        name: `Default ${templateType.replace('_', ' ')} Template`,
        description: `Auto-generated default template for ${templateType}`,
        templateType,
        htmlContent: defaultHtml,
        version: 1,
        isActive: true,
        createdById: adminUser.id,
      },
    });
  }

  private generateDocumentId(): string {
    return `doc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Service health check
   */
  async healthCheck(): Promise<{ healthy: boolean; services: Record<string, boolean>; errors?: string[] }> {
    const results = {
      healthy: true,
      services: {
        database: false,
        pdfService: false,
        templateService: false,
        storage: false,
      },
      errors: [] as string[],
    };

    try {
      // Test database connection
      await prisma.$queryRaw`SELECT 1`;
      results.services.database = true;
    } catch (error) {
      results.services.database = false;
      results.errors.push(`Database: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    try {
      // Test PDF service
      const pdfHealth = await PDFService.healthCheck();
      results.services.pdfService = pdfHealth.healthy;
      if (!pdfHealth.healthy && pdfHealth.error) {
        results.errors.push(`PDF Service: ${pdfHealth.error}`);
      }
    } catch (error) {
      results.services.pdfService = false;
      results.errors.push(`PDF Service: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    try {
      // Test template service
      this.templateService.validateTemplate('<html><body>Test</body></html>');
      results.services.templateService = true;
    } catch (error) {
      results.services.templateService = false;
      results.errors.push(`Template Service: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    try {
      // Test storage directory
      const storageDir = PDFService.getStorageDirectory();
      await import('fs/promises').then(fs => fs.access(storageDir));
      results.services.storage = true;
    } catch (error) {
      results.services.storage = false;
      results.errors.push(`Storage: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    // Overall health
    results.healthy = Object.values(results.services).every(Boolean);

    return results;
  }
}