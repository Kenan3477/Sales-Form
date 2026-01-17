// Main exports for the paperwork module
export { PaperworkService } from './paperwork-service';
export { PDFService } from './pdf-service';
export { TemplateService } from './template-service';
export { ContextBuilder } from './context-builder';

// Type exports
export type {
  DocumentGenerationRequest,
  GeneratedDocumentResult,
  TemplateContext,
  CustomerContext,
  AddressContext,
  AgreementContext,
  ApplianceContext,
  CoverageContext,
  MetadataContext,
  TemplateType,
  TemplateVariable,
  TemplateInfo,
  DocumentGenerationError,
  PDFGenerationOptions,
  SaleWithRelations,
  DocumentTemplateWithRelations,
} from './types';

export { DEFAULT_PDF_OPTIONS } from './types';