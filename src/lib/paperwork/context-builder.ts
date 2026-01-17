import { SaleWithRelations, TemplateContext, CustomerContext, AddressContext, AgreementContext, ApplianceContext, CoverageContext, MetadataContext } from './types';

/**
 * Builds template context from sale data for document generation
 */
export class ContextBuilder {
  
  /**
   * Build complete template context from sale data
   */
  static buildTemplateContext(
    sale: SaleWithRelations, 
    documentId: string
  ): TemplateContext {
    return {
      customer: this.buildCustomerContext(sale),
      agreement: this.buildAgreementContext(sale),
      appliances: this.buildApplianceContexts(sale),
      metadata: this.buildMetadataContext(sale, documentId),
    };
  }

  /**
   * Build customer context
   */
  private static buildCustomerContext(sale: SaleWithRelations): CustomerContext {
    const fullName = [sale.title, sale.customerFirstName, sale.customerLastName]
      .filter(Boolean)
      .join(' ');

    return {
      fullName,
      firstName: sale.customerFirstName,
      lastName: sale.customerLastName,
      title: sale.title || undefined,
      phoneNumber: sale.phoneNumber,
      email: sale.email,
      address: this.buildAddressContext(sale),
    };
  }

  /**
   * Build address context
   */
  private static buildAddressContext(sale: SaleWithRelations): AddressContext {
    const addressParts = [
      sale.mailingStreet,
      sale.mailingCity,
      sale.mailingProvince,
      sale.mailingPostalCode
    ].filter(Boolean);

    return {
      street: sale.mailingStreet || '',
      city: sale.mailingCity || '',
      province: sale.mailingProvince || '',
      postalCode: sale.mailingPostalCode || '',
      fullAddress: addressParts.join(', '),
    };
  }

  /**
   * Build agreement context
   */
  private static buildAgreementContext(sale: SaleWithRelations): AgreementContext {
    const monthlyPayment = sale.totalPlanCost / 12; // Assuming annual cost

    return {
      totalCost: sale.totalPlanCost,
      totalCostFormatted: this.formatCurrency(sale.totalPlanCost),
      monthlyPayment,
      monthlyPaymentFormatted: this.formatCurrency(monthlyPayment),
      directDebitDate: sale.directDebitDate.toISOString(),
      directDebitDateFormatted: this.formatDate(sale.directDebitDate),
      accountDetails: {
        accountName: sale.accountName,
        sortCode: sale.sortCode,
        accountNumber: sale.accountNumber,
        sortCodeFormatted: this.formatSortCode(sale.sortCode),
        accountNumberMasked: this.maskAccountNumber(sale.accountNumber),
      },
      coverage: this.buildCoverageContext(sale),
    };
  }

  /**
   * Build coverage context
   */
  private static buildCoverageContext(sale: SaleWithRelations): CoverageContext {
    return {
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      boilerPrice: sale.boilerPriceSelected || undefined,
      boilerPriceFormatted: sale.boilerPriceSelected 
        ? this.formatCurrency(sale.boilerPriceSelected)
        : undefined,
      totalItems: sale.appliances.length + (sale.boilerCoverSelected ? 1 : 0),
    };
  }

  /**
   * Build appliance contexts
   */
  private static buildApplianceContexts(sale: SaleWithRelations): ApplianceContext[] {
    return sale.appliances.map(appliance => ({
      id: appliance.id,
      name: appliance.appliance,
      otherText: appliance.otherText || undefined,
      coverLimit: appliance.coverLimit,
      coverLimitFormatted: this.formatCurrency(appliance.coverLimit),
      cost: appliance.cost,
      costFormatted: this.formatCurrency(appliance.cost),
    }));
  }

  /**
   * Build metadata context
   */
  private static buildMetadataContext(
    sale: SaleWithRelations, 
    documentId: string
  ): MetadataContext {
    const now = new Date();
    
    return {
      agentName: sale.agentName || undefined,
      generationDate: now.toISOString(),
      generationDateFormatted: this.formatDate(now),
      saleId: sale.id,
      documentId,
    };
  }

  // Utility formatting methods
  
  /**
   * Format currency values
   */
  private static formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-CA', {
      style: 'currency',
      currency: 'CAD',
    }).format(value);
  }

  /**
   * Format dates in a readable format
   */
  private static formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-CA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(date);
  }

  /**
   * Format sort code with dashes
   */
  private static formatSortCode(sortCode: string): string {
    // Remove any existing formatting
    const clean = sortCode.replace(/\D/g, '');
    
    // Format as XX-XX-XX
    if (clean.length === 6) {
      return `${clean.slice(0, 2)}-${clean.slice(2, 4)}-${clean.slice(4, 6)}`;
    }
    
    return sortCode; // Return original if not 6 digits
  }

  /**
   * Mask account number for security
   */
  private static maskAccountNumber(accountNumber: string): string {
    // Remove any existing formatting
    const clean = accountNumber.replace(/\D/g, '');
    
    if (clean.length >= 8) {
      // Show last 4 digits, mask the rest
      const lastFour = clean.slice(-4);
      const masked = 'X'.repeat(clean.length - 4);
      
      // Format as XXXX-XXXX-1234 for 8+ digit accounts
      if (clean.length === 8) {
        return `${masked.slice(0, 4)}-${masked.slice(4)}-${lastFour}`;
      } else {
        return `${masked}-${lastFour}`;
      }
    }
    
    return accountNumber; // Return original if too short
  }

  /**
   * Get available template variables for documentation/UI
   */
  static getAvailableVariables(): Record<string, string[]> {
    return {
      customer: [
        'customer.fullName',
        'customer.firstName', 
        'customer.lastName',
        'customer.title',
        'customer.phoneNumber',
        'customer.email',
        'customer.address.street',
        'customer.address.city',
        'customer.address.province',
        'customer.address.postalCode',
        'customer.address.fullAddress',
      ],
      agreement: [
        'agreement.totalCost',
        'agreement.totalCostFormatted',
        'agreement.monthlyPayment',
        'agreement.monthlyPaymentFormatted',
        'agreement.directDebitDate',
        'agreement.directDebitDateFormatted',
        'agreement.accountDetails.accountName',
        'agreement.accountDetails.sortCode',
        'agreement.accountDetails.accountNumber',
        'agreement.accountDetails.sortCodeFormatted',
        'agreement.accountDetails.accountNumberMasked',
        'agreement.coverage.hasApplianceCover',
        'agreement.coverage.hasBoilerCover',
        'agreement.coverage.boilerPrice',
        'agreement.coverage.boilerPriceFormatted',
        'agreement.coverage.totalItems',
      ],
      appliances: [
        'appliances.length',
        'appliances[0].name',
        'appliances[0].otherText',
        'appliances[0].coverLimit',
        'appliances[0].coverLimitFormatted',
        'appliances[0].cost',
        'appliances[0].costFormatted',
      ],
      metadata: [
        'metadata.agentName',
        'metadata.generationDate',
        'metadata.generationDateFormatted',
        'metadata.saleId',
        'metadata.documentId',
      ],
    };
  }
}