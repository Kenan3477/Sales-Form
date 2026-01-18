import { Sale, Appliance, DocumentTemplate } from '@prisma/client';

// Core Types
export interface DocumentGenerationRequest {
  saleId: string;
  templateType: string;
  templateId?: string; // If not provided, uses latest active template
}

export interface TemplateContext {
  customer: CustomerContext;
  agreement: AgreementContext;
  appliances: ApplianceContext[];
  appliancesCount: number;
  metadata: MetadataContext;
}

export interface CustomerContext {
  fullName: string;
  firstName: string;
  lastName: string;
  title?: string;
  phoneNumber: string;
  email: string;
  address: AddressContext;
}

export interface AddressContext {
  street: string;
  city: string;
  province: string;
  postalCode: string;
  fullAddress: string;
}

export interface AgreementContext {
  totalCost: number;
  totalCostFormatted: string;
  monthlyPayment: number;
  monthlyPaymentFormatted: string;
  directDebitDate: string;
  directDebitDateFormatted: string;
  accountDetails: {
    accountName: string;
    sortCode: string;
    accountNumber: string;
    sortCodeFormatted: string; // XX-XX-XX format
    accountNumberMasked: string; // XXXX-XXXX-1234 format
  };
  coverage: CoverageContext;
}

export interface CoverageContext {
  hasApplianceCover: boolean;
  hasBoilerCover: boolean;
  boilerPrice?: number;
  boilerPriceFormatted?: string;
  totalItems: number;
}

export interface ApplianceContext {
  id: string;
  name: string;
  otherText?: string;
  coverLimit: number;
  coverLimitFormatted: string;
  cost: number;
  costFormatted: string;
}

export interface MetadataContext {
  agentName?: string;
  generationDate: string;
  generationDateFormatted: string;
  saleId: string;
  documentId: string;
}

// Template Types
export type TemplateType = 
  | 'welcome_letter'
  | 'service_agreement' 
  | 'direct_debit_form'
  | 'coverage_summary';

export interface TemplateVariable {
  name: string;
  description: string;
  type: 'string' | 'number' | 'boolean' | 'date' | 'currency' | 'array';
  required: boolean;
  defaultValue?: any;
  example: string;
}

export interface TemplateInfo {
  type: TemplateType;
  name: string;
  description: string;
  variables: TemplateVariable[];
}

// Document Generation Types
export interface GeneratedDocumentResult {
  id: string;
  saleId: string;
  templateId: string;
  filename: string;
  filePath: string;
  fileSize: number;
  downloadUrl: string;
  metadata: TemplateContext;
}

export interface DocumentGenerationError {
  code: string;
  message: string;
  details?: any;
}

// PDF Generation Configuration
export interface PDFGenerationOptions {
  format: 'A4' | 'Letter';
  margin: {
    top: string;
    right: string;
    bottom: string;
    left: string;
  };
  displayHeaderFooter: boolean;
  headerTemplate?: string;
  footerTemplate?: string;
  printBackground: boolean;
  timeout: number;
}

export const DEFAULT_PDF_OPTIONS: PDFGenerationOptions = {
  format: 'A4',
  margin: {
    top: '2cm',
    right: '2cm',
    bottom: '2cm',
    left: '2cm',
  },
  displayHeaderFooter: false,
  printBackground: true,
  timeout: 30000,
};

// Extended types with relations
export type SaleWithRelations = Sale & {
  appliances: Appliance[];
  createdBy: {
    id: string;
    email: string;
  };
};

export type DocumentTemplateWithRelations = DocumentTemplate & {
  createdBy: {
    id: string;
    email: string;
  };
};