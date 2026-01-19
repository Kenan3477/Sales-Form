import Handlebars from 'handlebars';
import { TemplateContext, TemplateType, DocumentTemplateWithRelations } from './types';
import { ContextBuilder } from './context-builder';

/**
 * Template service for managing Handlebars templates and rendering
 */
export class TemplateService {
  
  constructor() {
    this.registerHelpers();
  }

  /**
   * Render template with context data
   */
  renderTemplate(
    htmlContent: string, 
    context: TemplateContext
  ): string {
    try {
      const template = Handlebars.compile(htmlContent);
      const rendered = template(context);
      
      return this.addDocumentWrapper(rendered);
    } catch (error) {
      throw new Error(`Template rendering failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Get default template content for a given type
   */
  getDefaultTemplate(templateType: TemplateType): string {
    switch (templateType) {
      case 'welcome_letter':
        return this.getWelcomeLetterTemplate();
      case 'service_agreement':
        return this.getServiceAgreementTemplate();
      case 'direct_debit_form':
        return this.getDirectDebitFormTemplate();
      case 'coverage_summary':
        return this.getCoverageSummaryTemplate();
      default:
        throw new Error(`Unknown template type: ${templateType}`);
    }
  }

  /**
   * Validate template syntax
   */
  validateTemplate(htmlContent: string): { valid: boolean; error?: string } {
    try {
      Handlebars.compile(htmlContent);
      return { valid: true };
    } catch (error) {
      return { 
        valid: false, 
        error: error instanceof Error ? error.message : 'Unknown template error'
      };
    }
  }

  /**
   * Get template variables used in HTML content
   */
  extractTemplateVariables(htmlContent: string): string[] {
    const variableRegex = /\{\{\s*([^}]+)\s*\}\}/g;
    const variables = new Set<string>();
    let match;

    while ((match = variableRegex.exec(htmlContent)) !== null) {
      const variable = match[1].trim();
      // Remove Handlebars helpers and just get variable names
      const cleanVariable = variable.replace(/^(if|unless|each|with)\s+/, '');
      variables.add(cleanVariable);
    }

    return Array.from(variables);
  }

  /**
   * Register custom Handlebars helpers
   */
  private registerHelpers() {
    // Currency formatting helper
    Handlebars.registerHelper('currency', function(value: number) {
      if (typeof value !== 'number') return value;
      return new Intl.NumberFormat('en-CA', {
        style: 'currency',
        currency: 'CAD',
      }).format(value);
    });

    // Date formatting helper
    Handlebars.registerHelper('date', function(value: string | Date, format?: string) {
      const date = value instanceof Date ? value : new Date(value);
      
      switch (format) {
        case 'short':
          return new Intl.DateTimeFormat('en-CA').format(date);
        case 'long':
          return new Intl.DateTimeFormat('en-CA', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          }).format(date);
        case 'month-year':
          return new Intl.DateTimeFormat('en-CA', {
            year: 'numeric',
            month: 'long',
          }).format(date);
        default:
          return new Intl.DateTimeFormat('en-CA', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          }).format(date);
      }
    });

    // Uppercase helper
    Handlebars.registerHelper('upper', function(str: string) {
      return typeof str === 'string' ? str.toUpperCase() : str;
    });

    // Conditional equality helper
    Handlebars.registerHelper('eq', function(a: any, b: any) {
      return a === b;
    });

    // Mathematical operations
    Handlebars.registerHelper('add', function(a: number, b: number) {
      return (a || 0) + (b || 0);
    });

    Handlebars.registerHelper('multiply', function(a: number, b: number) {
      return (a || 0) * (b || 0);
    });
  }

  /**
   * Add document wrapper with base styles
   */
  private addDocumentWrapper(content: string): string {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 12px;
            line-height: 1.6;
            color: #333;
            background: white;
        }
        
        .document {
            max-width: 210mm;
            margin: 0 auto;
            padding: 20mm;
            background: white;
            min-height: 297mm;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #007bff;
            padding-bottom: 20px;
        }
        
        .company-logo {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 10px;
        }
        
        .company-details {
            font-size: 10px;
            color: #666;
        }
        
        .content {
            margin-bottom: 30px;
        }
        
        .section {
            margin-bottom: 25px;
        }
        
        .section-title {
            font-size: 14px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 15px;
            border-left: 4px solid #007bff;
            padding-left: 10px;
        }
        
        .customer-info, .agreement-details, .appliance-list {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 3px 0;
        }
        
        .info-row:nth-child(even) {
            background: rgba(0, 123, 255, 0.05);
            margin: 8px -15px;
            padding: 8px 15px;
        }
        
        .label {
            font-weight: bold;
            width: 40%;
        }
        
        .value {
            width: 60%;
            text-align: right;
        }
        
        .appliance-item {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 3px;
            padding: 10px;
            margin-bottom: 10px;
        }
        
        .appliance-name {
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }
        
        .total-section {
            background: #e3f2fd;
            border: 2px solid #007bff;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
        }
        
        .total-amount {
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 10px;
            color: #666;
            border-top: 1px solid #dee2e6;
            padding-top: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        
        th, td {
            border: 1px solid #dee2e6;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background: #007bff;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        @media print {
            body {
                margin: 0;
                padding: 0;
            }
            
            .document {
                margin: 0;
                padding: 15mm;
                box-shadow: none;
                min-height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="document">
        ${content}
    </div>
</body>
</html>`;
  }

  /**
   * Welcome letter template
   */
  private getWelcomeLetterTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">SalesPortal Coverage</div>
    <div class="company-details">
        Professional Home Coverage Services<br>
        Phone: 1-800-COVERAGE | Email: support@salesportal.com
    </div>
</div>

<div class="content">
    <div class="section">
        <h1 style="color: #007bff; margin-bottom: 20px;">Welcome to Your New Coverage Plan</h1>
        
        <p>Dear {{customer.title}} {{customer.lastName}},</p>
        
        <p>Welcome! We're delighted to confirm your new home coverage plan. Below are the details of your agreement and coverage selection.</p>
    </div>

    <div class="section">
        <div class="section-title">Customer Information</div>
        <div class="customer-info">
            <div class="info-row">
                <span class="label">Full Name:</span>
                <span class="value">{{customer.fullName}}</span>
            </div>
            <div class="info-row">
                <span class="label">Phone Number:</span>
                <span class="value">{{customer.phoneNumber}}</span>
            </div>
            <div class="info-row">
                <span class="label">Email Address:</span>
                <span class="value">{{customer.email}}</span>
            </div>
            <div class="info-row">
                <span class="label">Service Address:</span>
                <span class="value">{{customer.address.fullAddress}}</span>
            </div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">Agreement Summary</div>
        <div class="agreement-details">
            <div class="info-row">
                <span class="label">Monthly Payment:</span>
                <span class="value">{{agreement.monthlyPaymentFormatted}}</span>
            </div>
            <div class="info-row">
                <span class="label">Annual Total:</span>
                <span class="value">{{agreement.monthlyPaymentFormatted}} monthly</span>
            </div>
            <div class="info-row">
                <span class="label">Direct Debit Date:</span>
                <span class="value">{{date agreement.directDebitDate 'long'}}</span>
            </div>
            <div class="info-row">
                <span class="label">Payment Account:</span>
                <span class="value">{{agreement.accountDetails.accountNumberMasked}}</span>
            </div>
        </div>
    </div>

    {{#if appliances}}
    <div class="section">
        <div class="section-title">Appliance Coverage ({{appliances.length}} items)</div>
        <div class="appliance-list">
            {{#each appliances}}
            <div class="appliance-item">
                <div class="appliance-name">{{this.name}}</div>
                {{#if this.otherText}}
                <div style="font-style: italic; color: #666; margin-bottom: 5px;">{{this.otherText}}</div>
                {{/if}}
                <div class="info-row">
                    <span class="label">Coverage Limit:</span>
                    <span class="value">{{this.coverLimitFormatted}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Monthly Cost:</span>
                    <span class="value">{{this.costFormatted}}</span>
                </div>
            </div>
            {{/each}}
        </div>
    </div>
    {{/if}}

    {{#if agreement.coverage.hasBoilerCover}}
    <div class="section">
        <div class="section-title">Boiler Coverage</div>
        <div class="agreement-details">
            <div class="info-row">
                <span class="label">Boiler Coverage:</span>
                <span class="value">Included</span>
            </div>
            {{#if agreement.coverage.boilerPriceFormatted}}
            <div class="info-row">
                <span class="label">Monthly Cost:</span>
                <span class="value">{{agreement.coverage.boilerPriceFormatted}}</span>
            </div>
            {{/if}}
        </div>
    </div>
    {{/if}}

    <div class="section">
        <div class="total-section">
            <h3>Total Monthly Coverage Cost</h3>
            <div class="total-amount">{{agreement.monthlyPaymentFormatted}}</div>
            <div style="margin-top: 10px; font-size: 12px;">
                Monthly payments of {{agreement.monthlyPaymentFormatted}} beginning {{date agreement.directDebitDate 'month-year'}}
            </div>
        </div>
    </div>

    <div class="section">
        <h3>What's Next?</h3>
        <ul style="margin-left: 20px; margin-top: 10px;">
            <li>Your coverage begins immediately upon completion of this agreement</li>
            <li>You will receive your plan documents within 5-7 business days</li>
            <li>For claims or service, contact us at 1-800-COVERAGE</li>
            <li>Questions? Reach out to your agent {{#if metadata.agentName}}{{metadata.agentName}}{{else}}or our support team{{/if}}</li>
        </ul>
    </div>
</div>

<div class="footer">
    <p>Thank you for choosing SalesPortal Coverage for your home protection needs.</p>
    <p>Document generated on {{date metadata.generationDate 'long'}} | Reference: {{metadata.saleId}}</p>
</div>`;
  }

  /**
   * Service agreement template
   */
  private getServiceAgreementTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">SalesPortal Coverage</div>
    <div class="company-details">Home Coverage Service Agreement</div>
</div>

<div class="content">
    <div class="section">
        <h1 style="color: #007bff; margin-bottom: 20px;">Home Coverage Service Agreement</h1>
        
        <p><strong>Agreement Date:</strong> {{date metadata.generationDate 'long'}}</p>
        <p><strong>Customer:</strong> {{customer.fullName}}</p>
        <p><strong>Service Address:</strong> {{customer.address.fullAddress}}</p>
    </div>

    <!-- Agreement content would continue here -->
    <div class="section">
        <h3>Terms and Conditions</h3>
        <p>This service agreement outlines the terms of coverage for the above customer...</p>
    </div>
</div>`;
  }

  /**
   * Direct debit form template  
   */
  private getDirectDebitFormTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">SalesPortal Coverage</div>
    <div class="company-details">Direct Debit Authorization</div>
</div>

<div class="content">
    <div class="section">
        <h1 style="color: #007bff; margin-bottom: 20px;">Direct Debit Authorization</h1>
        
        <div class="customer-info">
            <div class="info-row">
                <span class="label">Account Holder:</span>
                <span class="value">{{agreement.accountDetails.accountName}}</span>
            </div>
            <div class="info-row">
                <span class="label">Sort Code:</span>
                <span class="value">{{agreement.accountDetails.sortCodeFormatted}}</span>
            </div>
            <div class="info-row">
                <span class="label">Account Number:</span>
                <span class="value">{{agreement.accountDetails.accountNumber}}</span>
            </div>
            <div class="info-row">
                <span class="label">Monthly Amount:</span>
                <span class="value">{{agreement.monthlyPaymentFormatted}}</span>
            </div>
        </div>
    </div>
</div>`;
  }

  /**
   * Coverage summary template
   */
  private getCoverageSummaryTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">SalesPortal Coverage</div>
    <div class="company-details">Coverage Summary Report</div>
</div>

<div class="content">
    <div class="section">
        <h1 style="color: #007bff; margin-bottom: 20px;">Coverage Summary</h1>
        
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Coverage Limit</th>
                    <th>Monthly Cost</th>
                </tr>
            </thead>
            <tbody>
                {{#each appliances}}
                <tr>
                    <td>{{this.name}}</td>
                    <td>{{this.coverLimitFormatted}}</td>
                    <td>{{this.costFormatted}}</td>
                </tr>
                {{/each}}
            </tbody>
        </table>
    </div>
</div>`;
  }
}