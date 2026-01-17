import { TemplateService } from './template-service';
import { TemplateType } from './types';

/**
 * Enhanced template service with multiple template variations and professional styling
 */
export class EnhancedTemplateService {
  private baseService: TemplateService;

  constructor() {
    this.baseService = new TemplateService();
  }

  /**
   * Get professional welcome letter template (enhanced version)
   */
  private getProfessionalWelcomeLetterTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">
        <div class="logo-icon">🏠</div>
        <div class="company-info">
            <h1 class="company-name">SalesPortal Coverage</h1>
            <p class="company-tagline">Professional Home Protection Services</p>
        </div>
    </div>
    <div class="header-right">
        <div class="document-title">Welcome Letter</div>
        <div class="document-date">{{date metadata.generationDate 'long'}}</div>
        <div class="reference-number">Ref: {{metadata.saleId}}</div>
    </div>
</div>

<div class="content">
    <div class="welcome-section">
        <h1 class="welcome-title">Welcome to Your New Home Coverage Plan</h1>
        
        <div class="greeting">
            <p class="greeting-text">Dear {{#if customer.title}}{{customer.title}} {{/if}}{{customer.lastName}},</p>
            
            <p class="welcome-message">
                Thank you for choosing SalesPortal Coverage for your home protection needs. 
                We're delighted to confirm your new coverage plan and welcome you to our family 
                of satisfied customers who trust us to protect their most valuable investment.
            </p>
        </div>
    </div>

    <div class="section-grid">
        <div class="customer-section">
            <div class="section-header">
                <h2 class="section-title">Customer Information</h2>
                <div class="section-icon">👤</div>
            </div>
            <div class="info-card">
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

        <div class="agreement-section">
            <div class="section-header">
                <h2 class="section-title">Agreement Summary</h2>
                <div class="section-icon">📋</div>
            </div>
            <div class="info-card">
                <div class="info-row featured">
                    <span class="label">Monthly Payment:</span>
                    <span class="value price">{{agreement.monthlyPaymentFormatted}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Annual Total:</span>
                    <span class="value">{{agreement.totalCostFormatted}}</span>
                </div>
                <div class="info-row">
                    <span class="label">First Payment:</span>
                    <span class="value">{{date agreement.directDebitDate 'long'}}</span>
                </div>
                <div class="info-row">
                    <span class="label">Payment Method:</span>
                    <span class="value">Direct Debit</span>
                </div>
            </div>
        </div>
    </div>

    {{#if appliances}}
    <div class="coverage-section">
        <div class="section-header">
            <h2 class="section-title">Appliance Coverage Details</h2>
            <div class="section-icon">🔧</div>
            <div class="item-count">{{appliances.length}} items covered</div>
        </div>
        
        <div class="appliance-grid">
            {{#each appliances}}
            <div class="appliance-card">
                <div class="appliance-header">
                    <h3 class="appliance-name">{{this.name}}</h3>
                    <div class="appliance-cost">{{this.costFormatted}}/year</div>
                </div>
                {{#if this.otherText}}
                <div class="appliance-details">{{this.otherText}}</div>
                {{/if}}
                <div class="coverage-info">
                    <span class="coverage-label">Coverage Limit:</span>
                    <span class="coverage-value">{{this.coverLimitFormatted}}</span>
                </div>
            </div>
            {{/each}}
        </div>
    </div>
    {{/if}}

    {{#if agreement.coverage.hasBoilerCover}}
    <div class="boiler-section">
        <div class="section-header">
            <h2 class="section-title">Boiler Coverage</h2>
            <div class="section-icon">🔥</div>
        </div>
        <div class="boiler-card">
            <div class="boiler-info">
                <h3>Central Heating Boiler Cover</h3>
                <p>Comprehensive protection for your boiler and heating system</p>
                {{#if agreement.coverage.boilerPriceFormatted}}
                <div class="boiler-cost">{{agreement.coverage.boilerPriceFormatted}}/year</div>
                {{/if}}
            </div>
            <div class="boiler-benefits">
                <div class="benefit">✓ Annual boiler service</div>
                <div class="benefit">✓ Emergency repairs</div>
                <div class="benefit">✓ Parts and labour included</div>
                <div class="benefit">✓ 24/7 helpline</div>
            </div>
        </div>
    </div>
    {{/if}}

    <div class="total-section">
        <div class="total-card">
            <h2 class="total-title">Total Coverage Investment</h2>
            <div class="total-breakdown">
                <div class="total-line">
                    <span>Annual Premium:</span>
                    <span>{{agreement.totalCostFormatted}}</span>
                </div>
                <div class="total-line main-total">
                    <span>Monthly Payment:</span>
                    <span class="total-amount">{{agreement.monthlyPaymentFormatted}}</span>
                </div>
            </div>
            <div class="payment-info">
                <p>Payments will be collected via Direct Debit starting {{date agreement.directDebitDate 'month-year'}}</p>
            </div>
        </div>
    </div>

    <div class="next-steps">
        <h2 class="steps-title">What Happens Next?</h2>
        <div class="steps-grid">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>Immediate Coverage</h3>
                    <p>Your coverage begins immediately upon completion of this agreement</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>Policy Documents</h3>
                    <p>You'll receive your detailed policy documents within 5-7 business days</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>Customer Portal</h3>
                    <p>Access your account online to manage your coverage and submit claims</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h3>Support Available</h3>
                    <p>Our customer service team is here to help with any questions</p>
                </div>
            </div>
        </div>
    </div>

    <div class="contact-section">
        <h2 class="contact-title">Need Help? We're Here for You</h2>
        <div class="contact-grid">
            <div class="contact-item">
                <div class="contact-icon">📞</div>
                <div class="contact-info">
                    <h3>Customer Service</h3>
                    <p>1-800-COVERAGE</p>
                    <p class="contact-hours">Mon-Fri 8AM-6PM</p>
                </div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">⚡</div>
                <div class="contact-info">
                    <h3>Emergency Claims</h3>
                    <p>1-800-EMERGENCY</p>
                    <p class="contact-hours">24/7 Available</p>
                </div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">💻</div>
                <div class="contact-info">
                    <h3>Online Portal</h3>
                    <p>portal.salesportal.com</p>
                    <p class="contact-hours">Always Available</p>
                </div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">✉️</div>
                <div class="contact-info">
                    <h3>Email Support</h3>
                    <p>support@salesportal.com</p>
                    <p class="contact-hours">24-48hr Response</p>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="footer">
    <div class="footer-content">
        <div class="footer-left">
            <p class="footer-text">
                Thank you for choosing SalesPortal Coverage for your home protection needs.
            </p>
            <p class="footer-agent">
                {{#if metadata.agentName}}
                Your dedicated agent: <strong>{{metadata.agentName}}</strong>
                {{/if}}
            </p>
        </div>
        <div class="footer-right">
            <p class="footer-reference">Document ID: {{metadata.documentId}}</p>
            <p class="footer-date">Generated: {{date metadata.generationDate 'long'}}</p>
        </div>
    </div>
</div>

<style>
/* Enhanced Professional Styling */
.header {
    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
    color: white;
    padding: 24px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 8px 8px 0 0;
}

.company-logo {
    display: flex;
    align-items: center;
    gap: 16px;
}

.logo-icon {
    width: 48px;
    height: 48px;
    background: #ff6b35;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.company-name {
    font-size: 28px;
    font-weight: 700;
    line-height: 1.1;
}

.company-tagline {
    font-size: 14px;
    opacity: 0.9;
}

.header-right {
    text-align: right;
}

.document-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 4px;
}

.document-date, .reference-number {
    font-size: 14px;
    opacity: 0.9;
}

.content {
    padding: 32px;
}

.welcome-section {
    text-align: center;
    margin-bottom: 40px;
    padding: 24px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 12px;
    border-left: 4px solid #0ea5e9;
}

.welcome-title {
    font-size: 32px;
    font-weight: 700;
    color: #0c4a6e;
    margin-bottom: 16px;
    line-height: 1.2;
}

.greeting-text {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 16px;
}

.welcome-message {
    font-size: 16px;
    line-height: 1.6;
    color: #6b7280;
    max-width: 600px;
    margin: 0 auto;
}

.section-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 32px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e5e7eb;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #374151;
}

.section-icon {
    font-size: 24px;
}

.item-count {
    background: #dbeafe;
    color: #1e40af;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.info-card {
    background: #f8fafc;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #e2e8f0;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #e2e8f0;
}

.info-row:last-child {
    border-bottom: none;
}

.info-row.featured {
    background: #dbeafe;
    margin: -8px -12px 8px;
    padding: 12px;
    border-radius: 6px;
    border-bottom: 2px solid #2563eb;
}

.label {
    font-weight: 500;
    color: #6b7280;
}

.value {
    font-weight: 600;
    color: #374151;
}

.value.price {
    font-size: 18px;
    color: #1e40af;
}

.coverage-section {
    margin-bottom: 32px;
}

.appliance-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
}

.appliance-card {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    transition: all 0.2s ease;
}

.appliance-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.appliance-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.appliance-name {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
}

.appliance-cost {
    font-size: 14px;
    font-weight: 600;
    color: #059669;
    background: #d1fae5;
    padding: 2px 8px;
    border-radius: 4px;
}

.appliance-details {
    font-size: 14px;
    color: #6b7280;
    font-style: italic;
    margin-bottom: 8px;
}

.coverage-info {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    padding-top: 8px;
    border-top: 1px solid #e5e7eb;
}

.coverage-label {
    color: #6b7280;
}

.coverage-value {
    font-weight: 600;
    color: #374151;
}

.boiler-section {
    margin-bottom: 32px;
}

.boiler-card {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    background: #fef3c7;
    border-radius: 12px;
    padding: 24px;
    border: 2px solid #f59e0b;
}

.boiler-info h3 {
    font-size: 20px;
    font-weight: 600;
    color: #92400e;
    margin-bottom: 8px;
}

.boiler-info p {
    color: #78350f;
    margin-bottom: 12px;
}

.boiler-cost {
    font-size: 18px;
    font-weight: 700;
    color: #92400e;
}

.boiler-benefits {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.benefit {
    font-size: 14px;
    color: #78350f;
    font-weight: 500;
}

.total-section {
    margin: 40px 0;
}

.total-card {
    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
    color: white;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
}

.total-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
}

.total-breakdown {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

.total-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 16px;
}

.total-line.main-total {
    border-top: 2px solid rgba(255, 255, 255, 0.3);
    padding-top: 12px;
    margin-top: 12px;
    font-size: 20px;
    font-weight: 600;
}

.total-amount {
    font-size: 24px;
    font-weight: 700;
}

.payment-info {
    font-size: 14px;
    opacity: 0.9;
}

.next-steps {
    margin: 40px 0;
}

.steps-title {
    font-size: 24px;
    font-weight: 700;
    color: #374151;
    margin-bottom: 24px;
    text-align: center;
}

.steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
}

.step {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.2s ease;
}

.step:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
}

.step-number {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    color: white;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 18px;
    margin: 0 auto 12px;
}

.step-content h3 {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}

.step-content p {
    font-size: 14px;
    color: #6b7280;
    line-height: 1.4;
}

.contact-section {
    margin: 40px 0;
}

.contact-title {
    font-size: 24px;
    font-weight: 700;
    color: #374151;
    margin-bottom: 24px;
    text-align: center;
}

.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
}

.contact-item {
    background: #f8fafc;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid #e2e8f0;
}

.contact-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.contact-info h3 {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 4px;
}

.contact-info p {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 2px;
}

.contact-hours {
    font-size: 12px;
    color: #9ca3af;
    font-style: italic;
}

.footer {
    background: #f8fafc;
    padding: 24px 32px;
    border-radius: 0 0 8px 8px;
    border-top: 1px solid #e2e8f0;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-text {
    color: #6b7280;
    font-size: 14px;
}

.footer-agent {
    color: #374151;
    font-size: 14px;
    margin-top: 4px;
}

.footer-right {
    text-align: right;
}

.footer-reference, .footer-date {
    font-size: 12px;
    color: #9ca3af;
    font-family: monospace;
}

@media (max-width: 768px) {
    .section-grid {
        grid-template-columns: 1fr;
    }
    
    .boiler-card {
        grid-template-columns: 1fr;
    }
    
    .steps-grid {
        grid-template-columns: 1fr;
    }
    
    .contact-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .footer-content {
        flex-direction: column;
        text-align: center;
        gap: 12px;
    }
}

@media (max-width: 480px) {
    .contact-grid {
        grid-template-columns: 1fr;
    }
    
    .header {
        flex-direction: column;
        text-align: center;
        gap: 16px;
    }
    
    .content {
        padding: 16px;
    }
}
</style>`;
  }

  /**
   * Get comprehensive service agreement template
   */
  private getComprehensiveServiceAgreementTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">
        <div class="logo-icon">📋</div>
        <div class="company-info">
            <h1 class="company-name">SalesPortal Coverage</h1>
            <p class="company-tagline">Home Protection Service Agreement</p>
        </div>
    </div>
    <div class="header-right">
        <div class="document-title">Service Agreement</div>
        <div class="document-date">{{date metadata.generationDate 'long'}}</div>
        <div class="reference-number">Agreement: {{metadata.saleId}}</div>
    </div>
</div>

<div class="content">
    <div class="agreement-intro">
        <h1 class="agreement-title">Home Coverage Service Agreement</h1>
        <div class="agreement-parties">
            <p><strong>This Agreement is between:</strong></p>
            <div class="parties-grid">
                <div class="party">
                    <h3>Service Provider</h3>
                    <p><strong>SalesPortal Coverage Inc.</strong></p>
                    <p>Professional Home Protection Services</p>
                    <p>support@salesportal.com</p>
                    <p>1-800-COVERAGE</p>
                </div>
                <div class="party">
                    <h3>Customer</h3>
                    <p><strong>{{customer.fullName}}</strong></p>
                    <p>{{customer.address.fullAddress}}</p>
                    <p>{{customer.phoneNumber}}</p>
                    <p>{{customer.email}}</p>
                </div>
            </div>
            <p class="agreement-date"><strong>Agreement Date:</strong> {{date metadata.generationDate 'long'}}</p>
        </div>
    </div>

    <div class="terms-section">
        <h2>1. Coverage Details</h2>
        
        <div class="coverage-summary">
            <h3>Summary of Coverage</h3>
            <table class="coverage-table">
                <thead>
                    <tr>
                        <th>Coverage Type</th>
                        <th>Details</th>
                        <th>Annual Premium</th>
                    </tr>
                </thead>
                <tbody>
                    {{#if agreement.coverage.hasApplianceCover}}
                    {{#each appliances}}
                    <tr>
                        <td>{{this.name}}</td>
                        <td>Coverage up to {{this.coverLimitFormatted}}{{#if this.otherText}} - {{this.otherText}}{{/if}}</td>
                        <td>{{this.costFormatted}}</td>
                    </tr>
                    {{/each}}
                    {{/if}}
                    {{#if agreement.coverage.hasBoilerCover}}
                    <tr>
                        <td>Central Heating Boiler</td>
                        <td>Comprehensive boiler and heating system coverage</td>
                        <td>{{agreement.coverage.boilerPriceFormatted}}</td>
                    </tr>
                    {{/if}}
                </tbody>
                <tfoot>
                    <tr class="total-row">
                        <td colspan="2"><strong>Total Annual Premium</strong></td>
                        <td><strong>{{agreement.totalCostFormatted}}</strong></td>
                    </tr>
                </tfoot>
            </table>
        </div>

        <h3>Payment Terms</h3>
        <div class="payment-terms">
            <p><strong>Monthly Payment:</strong> {{agreement.monthlyPaymentFormatted}}</p>
            <p><strong>Payment Method:</strong> Direct Debit</p>
            <p><strong>Account Holder:</strong> {{agreement.accountDetails.accountName}}</p>
            <p><strong>Sort Code:</strong> {{agreement.accountDetails.sortCodeFormatted}}</p>
            <p><strong>Account Number:</strong> {{agreement.accountDetails.accountNumberMasked}}</p>
            <p><strong>First Payment Date:</strong> {{date agreement.directDebitDate 'long'}}</p>
        </div>
    </div>

    <div class="terms-section">
        <h2>2. Terms and Conditions</h2>

        <div class="terms-subsection">
            <h3>2.1 Coverage Period</h3>
            <p>This agreement provides coverage for a period of twelve (12) months from the date of this agreement. The coverage will automatically renew annually unless terminated by either party with thirty (30) days written notice.</p>
        </div>

        <div class="terms-subsection">
            <h3>2.2 What's Covered</h3>
            <ul class="terms-list">
                <li>Repair or replacement of covered appliances due to mechanical breakdown</li>
                <li>Parts and labour costs for covered repairs</li>
                <li>Annual maintenance service for covered items</li>
                <li>24/7 emergency helpline support</li>
                <li>No call-out charges for covered items</li>
            </ul>
        </div>

        <div class="terms-subsection">
            <h3>2.3 What's Not Covered</h3>
            <ul class="terms-list">
                <li>Pre-existing faults known at the start of coverage</li>
                <li>Damage due to misuse, neglect, or normal wear and tear</li>
                <li>Cosmetic damage that doesn't affect functionality</li>
                <li>Items over 15 years old (unless specifically agreed)</li>
                <li>Commercial or business use of covered appliances</li>
            </ul>
        </div>

        <div class="terms-subsection">
            <h3>2.4 Claims Process</h3>
            <p>To make a claim:</p>
            <ol class="terms-list">
                <li>Contact our claims helpline on 1-800-EMERGENCY</li>
                <li>Provide your agreement reference number: {{metadata.saleId}}</li>
                <li>Describe the problem and affected appliance</li>
                <li>Our team will arrange an engineer visit within 24-48 hours</li>
                <li>The engineer will diagnose and repair the fault if covered</li>
            </ol>
        </div>

        <div class="terms-subsection">
            <h3>2.5 Payment Terms</h3>
            <p>Payments are collected monthly by Direct Debit on or around the date specified above. If a payment fails, we will attempt collection three times. If payment remains outstanding after 30 days, coverage may be suspended.</p>
        </div>

        <div class="terms-subsection">
            <h3>2.6 Cancellation Rights</h3>
            <p>You have the right to cancel this agreement within 14 days of receiving this document for a full refund. After this period, you may cancel with 30 days notice. Any refund will be calculated on a pro-rata basis.</p>
        </div>
    </div>

    <div class="terms-section">
        <h2>3. Customer Rights and Responsibilities</h2>

        <div class="rights-grid">
            <div class="rights-column">
                <h3>Your Rights</h3>
                <ul class="rights-list">
                    <li>Prompt repair service within agreed timescales</li>
                    <li>Professional qualified engineers</li>
                    <li>Clear communication about repair progress</li>
                    <li>Right to cancel as outlined above</li>
                    <li>Access to our complaints procedure</li>
                    <li>Data protection under GDPR</li>
                </ul>
            </div>
            <div class="rights-column">
                <h3>Your Responsibilities</h3>
                <ul class="rights-list">
                    <li>Allow reasonable access for engineers</li>
                    <li>Maintain appliances in good working order</li>
                    <li>Report faults promptly</li>
                    <li>Ensure payment details remain current</li>
                    <li>Notify us of any changes to your circumstances</li>
                    <li>Use appliances in accordance with manufacturer instructions</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="signatures-section">
        <h2>4. Agreement Signatures</h2>
        <p>By proceeding with this service agreement, both parties acknowledge they have read, understood, and agree to be bound by these terms and conditions.</p>
        
        <div class="signature-boxes">
            <div class="signature-box">
                <h3>Customer Acceptance</h3>
                <p><strong>Name:</strong> {{customer.fullName}}</p>
                <p><strong>Date:</strong> {{date metadata.generationDate 'long'}}</p>
                <div class="signature-line"></div>
                <p class="signature-label">Customer Signature</p>
            </div>
            <div class="signature-box">
                <h3>Company Representative</h3>
                <p><strong>Name:</strong> {{#if metadata.agentName}}{{metadata.agentName}}{{else}}SalesPortal Team{{/if}}</p>
                <p><strong>Date:</strong> {{date metadata.generationDate 'long'}}</p>
                <div class="signature-line"></div>
                <p class="signature-label">Authorized Signature</p>
            </div>
        </div>
    </div>
</div>

<div class="footer">
    <div class="footer-content">
        <div class="footer-left">
            <p>SalesPortal Coverage Inc. | Professional Home Protection Services</p>
            <p>Regulated by the Home Protection Authority | Registration No: HPA-12345</p>
        </div>
        <div class="footer-right">
            <p>Agreement Reference: {{metadata.saleId}}</p>
            <p>Generated: {{date metadata.generationDate 'long'}}</p>
        </div>
    </div>
</div>

<style>
/* Service Agreement Styling */
.agreement-intro {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border-radius: 12px;
    padding: 32px;
    margin-bottom: 32px;
    border-left: 4px solid #3b82f6;
}

.agreement-title {
    font-size: 28px;
    font-weight: 700;
    color: #1e40af;
    margin-bottom: 24px;
    text-align: center;
}

.parties-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin: 24px 0;
}

.party {
    background: white;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #d1d5db;
}

.party h3 {
    color: #374151;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 4px;
}

.party p {
    margin-bottom: 4px;
    color: #6b7280;
}

.agreement-date {
    text-align: center;
    font-size: 16px;
    color: #374151;
    margin-top: 16px;
}

.terms-section {
    margin-bottom: 32px;
    background: white;
    border-radius: 8px;
    padding: 24px;
    border: 1px solid #e5e7eb;
}

.terms-section h2 {
    color: #1e40af;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 20px;
    border-bottom: 2px solid #dbeafe;
    padding-bottom: 8px;
}

.coverage-summary {
    margin-bottom: 24px;
}

.coverage-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
}

.coverage-table th,
.coverage-table td {
    border: 1px solid #d1d5db;
    padding: 12px;
    text-align: left;
}

.coverage-table th {
    background: #f3f4f6;
    font-weight: 600;
    color: #374151;
}

.coverage-table tbody tr:nth-child(even) {
    background: #f9fafb;
}

.total-row {
    background: #dbeafe;
    font-weight: 600;
}

.payment-terms {
    background: #f0f9ff;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #0ea5e9;
}

.payment-terms p {
    margin-bottom: 8px;
    color: #374151;
}

.terms-subsection {
    margin-bottom: 24px;
}

.terms-subsection h3 {
    color: #374151;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
}

.terms-list {
    margin-left: 20px;
    color: #6b7280;
}

.terms-list li {
    margin-bottom: 8px;
    line-height: 1.5;
}

.rights-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.rights-column h3 {
    color: #059669;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
}

.rights-list {
    margin-left: 16px;
    color: #374151;
}

.rights-list li {
    margin-bottom: 6px;
}

.signatures-section {
    background: #f8fafc;
    border-radius: 12px;
    padding: 32px;
    border: 2px solid #e5e7eb;
}

.signatures-section h2 {
    color: #1e40af;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
}

.signature-boxes {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    margin-top: 24px;
}

.signature-box {
    background: white;
    padding: 24px;
    border-radius: 8px;
    border: 1px solid #d1d5db;
}

.signature-box h3 {
    color: #374151;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
}

.signature-line {
    height: 2px;
    background: #d1d5db;
    margin: 24px 0 8px;
}

.signature-label {
    text-align: center;
    font-size: 12px;
    color: #6b7280;
    font-style: italic;
}

@media (max-width: 768px) {
    .parties-grid,
    .rights-grid,
    .signature-boxes {
        grid-template-columns: 1fr;
    }
    
    .coverage-table {
        font-size: 12px;
    }
    
    .coverage-table th,
    .coverage-table td {
        padding: 8px;
    }
}
</style>`;
  }

  /**
   * Get enhanced direct debit form template
   */
  private getEnhancedDirectDebitFormTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">
        <div class="logo-icon">🏦</div>
        <div class="company-info">
            <h1 class="company-name">SalesPortal Coverage</h1>
            <p class="company-tagline">Direct Debit Authorization Form</p>
        </div>
    </div>
    <div class="header-right">
        <div class="document-title">Direct Debit Mandate</div>
        <div class="document-date">{{date metadata.generationDate 'long'}}</div>
        <div class="reference-number">Ref: {{metadata.saleId}}</div>
    </div>
</div>

<div class="content">
    <div class="mandate-intro">
        <h1 class="mandate-title">Direct Debit Instruction</h1>
        <p class="mandate-subtitle">
            This Instruction authorizes SalesPortal Coverage to collect payments from your account by Direct Debit
        </p>
    </div>

    <div class="mandate-details">
        <div class="detail-section">
            <h2>Service User Details</h2>
            <div class="service-user-info">
                <div class="info-row">
                    <span class="label">Service User Name:</span>
                    <span class="value">SalesPortal Coverage Inc.</span>
                </div>
                <div class="info-row">
                    <span class="label">Service User Number:</span>
                    <span class="value">123456</span>
                </div>
                <div class="info-row">
                    <span class="label">Service Address:</span>
                    <span class="value">Professional Home Protection Services<br>
                    Coverage House, Protection Street<br>
                    Customer Service, CS1 2DD</span>
                </div>
            </div>
        </div>

        <div class="detail-section">
            <h2>Payer Details</h2>
            <div class="payer-info">
                <div class="form-row">
                    <span class="label">Account Holder Name:</span>
                    <span class="value">{{agreement.accountDetails.accountName}}</span>
                </div>
                <div class="form-row">
                    <span class="label">Address:</span>
                    <span class="value">{{customer.address.fullAddress}}</span>
                </div>
                <div class="form-row">
                    <span class="label">Phone Number:</span>
                    <span class="value">{{customer.phoneNumber}}</span>
                </div>
                <div class="form-row">
                    <span class="label">Email Address:</span>
                    <span class="value">{{customer.email}}</span>
                </div>
            </div>
        </div>

        <div class="detail-section">
            <h2>Bank/Building Society Details</h2>
            <div class="bank-details">
                <div class="bank-row">
                    <span class="label">Bank/Building Society Name:</span>
                    <div class="value-box"></div>
                </div>
                <div class="bank-row">
                    <span class="label">Address:</span>
                    <div class="value-box large"></div>
                </div>
                <div class="account-details">
                    <div class="account-row">
                        <span class="label">Sort Code:</span>
                        <div class="sort-code-boxes">
                            {{#each (split agreement.accountDetails.sortCode "-")}}
                            <div class="code-box">{{this}}</div>
                            {{/each}}
                        </div>
                    </div>
                    <div class="account-row">
                        <span class="label">Account Number:</span>
                        <div class="account-boxes">
                            {{#each (split agreement.accountDetails.accountNumber "")}}
                            <div class="digit-box">{{this}}</div>
                            {{/each}}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="detail-section">
            <h2>Payment Information</h2>
            <div class="payment-info">
                <div class="payment-row">
                    <span class="label">Monthly Payment Amount:</span>
                    <span class="value amount">{{agreement.monthlyPaymentFormatted}}</span>
                </div>
                <div class="payment-row">
                    <span class="label">Payment Frequency:</span>
                    <span class="value">Monthly</span>
                </div>
                <div class="payment-row">
                    <span class="label">First Payment Date:</span>
                    <span class="value">{{date agreement.directDebitDate 'long'}}</span>
                </div>
                <div class="payment-row">
                    <span class="label">Reference Number:</span>
                    <span class="value">{{metadata.saleId}}</span>
                </div>
            </div>
        </div>
    </div>

    <div class="instruction-text">
        <h2>Instruction to Your Bank or Building Society</h2>
        <p class="instruction-paragraph">
            Please pay SalesPortal Coverage Direct Debits from the account detailed in this Instruction 
            subject to the safeguards assured by the Direct Debit Guarantee. I understand that this 
            Instruction may remain with SalesPortal Coverage and, if so, details will be passed electronically 
            to my Bank/Building Society.
        </p>
    </div>

    <div class="signature-section">
        <h2>Authorization</h2>
        <div class="signature-grid">
            <div class="signature-box">
                <span class="signature-label">Signature(s):</span>
                <div class="signature-line"></div>
            </div>
            <div class="date-box">
                <span class="date-label">Date:</span>
                <div class="date-line">{{date metadata.generationDate 'short'}}</div>
            </div>
        </div>
    </div>

    <div class="guarantee-section">
        <h2>The Direct Debit Guarantee</h2>
        <div class="guarantee-content">
            <div class="guarantee-logo">
                <div class="dd-logo">DD</div>
                <span class="guarantee-text">Direct Debit Guarantee</span>
            </div>
            <ul class="guarantee-list">
                <li>This Guarantee is offered by all banks and building societies that accept instructions to pay Direct Debits</li>
                <li>If there are any changes to the amount, date or frequency of your Direct Debit, SalesPortal Coverage will notify you 10 working days in advance of your account being debited or as otherwise agreed. If you request SalesPortal Coverage to collect a payment, confirmation of the amount and date will be given to you at the time of the request</li>
                <li>If an error is made in the payment of your Direct Debit, by SalesPortal Coverage or your bank or building society, you are entitled to a full and immediate refund of the amount paid from your bank or building society</li>
                <li>If you receive a refund you are not entitled to, you must pay it back when SalesPortal Coverage asks you to</li>
                <li>You can cancel a Direct Debit at any time by simply contacting your bank or building society. Written confirmation may be required. Please also notify us</li>
            </ul>
        </div>
    </div>
</div>

<div class="footer">
    <div class="footer-content">
        <div class="footer-left">
            <p>For office use only:</p>
            <p>Service User Number: 123456 | Reference: {{metadata.saleId}}</p>
        </div>
        <div class="footer-right">
            <p>SalesPortal Coverage Inc.</p>
            <p>Generated: {{date metadata.generationDate 'long'}}</p>
        </div>
    </div>
</div>

<style>
/* Direct Debit Form Styling */
.mandate-intro {
    background: linear-gradient(135deg, #065f46 0%, #047857 100%);
    color: white;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 32px;
}

.mandate-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
}

.mandate-subtitle {
    font-size: 16px;
    opacity: 0.9;
}

.mandate-details {
    display: grid;
    gap: 24px;
}

.detail-section {
    background: #f8fafc;
    border-radius: 8px;
    padding: 24px;
    border: 1px solid #e2e8f0;
}

.detail-section h2 {
    color: #374151;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 16px;
    border-bottom: 2px solid #d1d5db;
    padding-bottom: 8px;
}

.info-row, .form-row, .payment-row {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 16px;
    margin-bottom: 12px;
    align-items: center;
}

.label {
    font-weight: 500;
    color: #6b7280;
}

.value {
    color: #374151;
    font-weight: 600;
}

.value.amount {
    font-size: 20px;
    color: #059669;
    font-weight: 700;
}

.bank-row {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 16px;
    margin-bottom: 16px;
    align-items: center;
}

.value-box {
    border: 2px solid #d1d5db;
    height: 40px;
    border-radius: 4px;
    background: white;
}

.value-box.large {
    height: 80px;
}

.account-details {
    margin-top: 20px;
}

.account-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}

.sort-code-boxes {
    display: flex;
    gap: 8px;
}

.code-box {
    width: 40px;
    height: 40px;
    border: 2px solid #374151;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 600;
    background: white;
}

.account-boxes {
    display: flex;
    gap: 4px;
}

.digit-box {
    width: 32px;
    height: 40px;
    border: 2px solid #374151;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 600;
    background: white;
}

.instruction-text {
    background: #fef3c7;
    border-radius: 8px;
    padding: 24px;
    border-left: 4px solid #f59e0b;
    margin: 24px 0;
}

.instruction-text h2 {
    color: #92400e;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 12px;
}

.instruction-paragraph {
    color: #78350f;
    line-height: 1.6;
    font-size: 14px;
}

.signature-section {
    background: white;
    border-radius: 8px;
    padding: 24px;
    border: 2px solid #d1d5db;
    margin: 24px 0;
}

.signature-section h2 {
    color: #374151;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 16px;
}

.signature-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 32px;
    align-items: end;
}

.signature-line {
    border-bottom: 2px solid #374151;
    height: 40px;
    margin-top: 8px;
}

.date-line {
    border-bottom: 2px solid #374151;
    height: 40px;
    margin-top: 8px;
    display: flex;
    align-items: center;
    padding: 0 8px;
    font-weight: 600;
}

.guarantee-section {
    background: #f0f9ff;
    border-radius: 12px;
    padding: 24px;
    border: 2px solid #0ea5e9;
    margin-top: 24px;
}

.guarantee-section h2 {
    color: #0c4a6e;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 16px;
}

.guarantee-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.dd-logo {
    background: #0ea5e9;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
}

.guarantee-text {
    font-size: 16px;
    font-weight: 600;
    color: #0c4a6e;
}

.guarantee-list {
    margin-left: 20px;
    color: #1e40af;
}

.guarantee-list li {
    margin-bottom: 8px;
    line-height: 1.5;
    font-size: 12px;
}

@media (max-width: 768px) {
    .info-row, .form-row, .payment-row {
        grid-template-columns: 1fr;
        gap: 4px;
    }
    
    .bank-row {
        grid-template-columns: 1fr;
    }
    
    .signature-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }
    
    .account-boxes, .sort-code-boxes {
        flex-wrap: wrap;
        gap: 2px;
    }
    
    .digit-box, .code-box {
        width: 28px;
        height: 32px;
        font-size: 14px;
    }
}
</style>`;
  }

  /**
   * Get enhanced coverage summary template
   */
  private getCoverageSummaryTemplate(): string {
    return `
<div class="header">
    <div class="company-logo">
        <div class="logo-icon">📊</div>
        <div class="company-info">
            <h1 class="company-name">SalesPortal Coverage</h1>
            <p class="company-tagline">Coverage Summary Report</p>
        </div>
    </div>
    <div class="header-right">
        <div class="document-title">Coverage Summary</div>
        <div class="document-date">{{date metadata.generationDate 'long'}}</div>
        <div class="reference-number">Ref: {{metadata.saleId}}</div>
    </div>
</div>

<div class="content">
    <div class="summary-intro">
        <h1 class="summary-title">Your Home Coverage Summary</h1>
        <div class="customer-details">
            <h2>Customer Information</h2>
            <div class="details-grid">
                <div class="detail-item">
                    <span class="detail-label">Name:</span>
                    <span class="detail-value">{{customer.fullName}}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Address:</span>
                    <span class="detail-value">{{customer.address.fullAddress}}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Phone:</span>
                    <span class="detail-value">{{customer.phoneNumber}}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value">{{customer.email}}</span>
                </div>
            </div>
        </div>
    </div>

    <div class="coverage-overview">
        <h2 class="section-title">Coverage Overview</h2>
        <div class="overview-cards">
            <div class="overview-card main">
                <h3>Total Annual Premium</h3>
                <p class="premium-amount">{{agreement.totalCostFormatted}}</p>
                <p class="premium-monthly">{{agreement.monthlyPaymentFormatted}} per month</p>
            </div>
            <div class="overview-card">
                <h3>Coverage Start Date</h3>
                <p class="coverage-date">{{date agreement.directDebitDate 'long'}}</p>
            </div>
        </div>
    </div>

    {{#if agreement.coverage.hasApplianceCover}}
    <div class="appliance-coverage">
        <h2 class="section-title">Appliance Coverage</h2>
        <div class="appliance-summary">
            <p class="coverage-description">
                Your appliances are protected against mechanical breakdown and electrical faults. 
                We provide repair or replacement service with qualified engineers and genuine parts.
            </p>
            <div class="appliance-list">
                {{#each appliances}}
                <div class="appliance-item">
                    <div class="appliance-header">
                        <h4 class="appliance-name">{{this.name}}</h4>
                        <span class="appliance-premium">{{this.costFormatted}}/year</span>
                    </div>
                    <div class="appliance-details">
                        <div class="detail-row">
                            <span class="detail-label">Coverage Limit:</span>
                            <span class="detail-value">{{this.coverLimitFormatted}}</span>
                        </div>
                        {{#if this.otherText}}
                        <div class="detail-row">
                            <span class="detail-label">Notes:</span>
                            <span class="detail-value">{{this.otherText}}</span>
                        </div>
                        {{/if}}
                    </div>
                    <div class="coverage-benefits">
                        <h5>What's Included:</h5>
                        <ul>
                            <li>Repair or replacement due to mechanical breakdown</li>
                            <li>Parts and labour costs covered</li>
                            <li>Annual maintenance service</li>
                            <li>24/7 emergency helpline</li>
                        </ul>
                    </div>
                </div>
                {{/each}}
            </div>
        </div>
    </div>
    {{/if}}

    {{#if agreement.coverage.hasBoilerCover}}
    <div class="boiler-coverage">
        <h2 class="section-title">Boiler Coverage</h2>
        <div class="boiler-summary">
            <div class="boiler-overview">
                <h3>Central Heating Boiler Protection</h3>
                <p class="boiler-description">
                    Complete protection for your boiler and central heating system, including annual service 
                    and emergency repairs.
                </p>
                {{#if agreement.coverage.boilerPriceFormatted}}
                <p class="boiler-premium">Annual Premium: {{agreement.coverage.boilerPriceFormatted}}</p>
                {{/if}}
            </div>
            
            <div class="boiler-features">
                <h4>Coverage Features</h4>
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">🔧</div>
                        <div class="feature-text">
                            <h5>Annual Service</h5>
                            <p>Professional boiler service to maintain efficiency and safety</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">⚡</div>
                        <div class="feature-text">
                            <h5>Emergency Repairs</h5>
                            <p>24/7 emergency callout for boiler breakdowns</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🔩</div>
                        <div class="feature-text">
                            <h5>Parts & Labour</h5>
                            <p>All parts and labour costs included in coverage</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">📞</div>
                        <div class="feature-text">
                            <h5>Expert Support</h5>
                            <p>Access to qualified Gas Safe registered engineers</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {{/if}}

    <div class="important-information">
        <h2 class="section-title">Important Information</h2>
        
        <div class="info-grid">
            <div class="info-section">
                <h3>Claims Process</h3>
                <ol>
                    <li>Call our 24/7 helpline: 1-800-EMERGENCY</li>
                    <li>Provide your reference number: {{metadata.saleId}}</li>
                    <li>Describe the fault or problem</li>
                    <li>We'll arrange an engineer visit within 24-48 hours</li>
                </ol>
            </div>
            
            <div class="info-section">
                <h3>Policy Exclusions</h3>
                <ul>
                    <li>Pre-existing faults known before coverage started</li>
                    <li>Damage due to misuse or neglect</li>
                    <li>Cosmetic damage that doesn't affect function</li>
                    <li>Items over 15 years old (unless specifically covered)</li>
                </ul>
            </div>
            
            <div class="info-section">
                <h3>Payment Information</h3>
                <p><strong>Monthly Payment:</strong> {{agreement.monthlyPaymentFormatted}}</p>
                <p><strong>Payment Method:</strong> Direct Debit</p>
                <p><strong>Next Payment:</strong> {{date agreement.directDebitDate 'long'}}</p>
                <p><strong>Account:</strong> {{agreement.accountDetails.sortCodeFormatted}} {{agreement.accountDetails.accountNumberMasked}}</p>
            </div>
            
            <div class="info-section">
                <h3>Contact Information</h3>
                <p><strong>Customer Service:</strong> 1-800-COVERAGE</p>
                <p><strong>Emergency Claims:</strong> 1-800-EMERGENCY</p>
                <p><strong>Email:</strong> support@salesportal.com</p>
                <p><strong>Online:</strong> portal.salesportal.com</p>
            </div>
        </div>
    </div>
</div>

<div class="footer">
    <div class="footer-content">
        <div class="footer-left">
            <p>Thank you for choosing SalesPortal Coverage for your home protection needs.</p>
            <p>This summary provides an overview of your coverage. Full terms and conditions apply.</p>
        </div>
        <div class="footer-right">
            <p>Document ID: {{metadata.documentId}}</p>
            <p>Generated: {{date metadata.generationDate 'long'}}</p>
            {{#if metadata.agentName}}
            <p>Agent: {{metadata.agentName}}</p>
            {{/if}}
        </div>
    </div>
</div>

<style>
/* Coverage Summary Styling */
.summary-intro {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 32px;
    border-left: 4px solid #0ea5e9;
}

.summary-title {
    font-size: 28px;
    font-weight: 700;
    color: #0c4a6e;
    margin-bottom: 24px;
    text-align: center;
}

.customer-details h2 {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 16px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 4px;
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 12px;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 12px;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
}

.detail-label {
    font-weight: 500;
    color: #6b7280;
}

.detail-value {
    font-weight: 600;
    color: #374151;
}

.coverage-overview {
    margin-bottom: 32px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 20px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 8px;
}

.overview-cards {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
}

.overview-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    border: 2px solid #e5e7eb;
    text-align: center;
}

.overview-card.main {
    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
    color: white;
    border-color: #3b82f6;
}

.overview-card h3 {
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 8px;
}

.premium-amount {
    font-size: 32px;
    font-weight: 700;
    margin: 8px 0;
    line-height: 1;
}

.premium-monthly {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
}

.coverage-date {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin: 8px 0 0;
}

.appliance-coverage, .boiler-coverage, .important-information {
    margin-bottom: 32px;
}

.coverage-description, .boiler-description {
    color: #6b7280;
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 24px;
    text-align: center;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.appliance-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
}

.appliance-item {
    background: white;
    border-radius: 12px;
    padding: 20px;
    border: 2px solid #e5e7eb;
    transition: all 0.2s ease;
}

.appliance-item:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.appliance-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #e5e7eb;
}

.appliance-name {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin: 0;
}

.appliance-premium {
    background: #dbeafe;
    color: #1e40af;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
}

.appliance-details {
    margin-bottom: 16px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
}

.coverage-benefits h5 {
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 8px;
}

.coverage-benefits ul {
    margin: 0;
    padding-left: 16px;
    color: #6b7280;
    font-size: 14px;
}

.coverage-benefits li {
    margin-bottom: 4px;
}

.boiler-overview {
    text-align: center;
    margin-bottom: 24px;
}

.boiler-overview h3 {
    font-size: 20px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 12px;
}

.boiler-premium {
    font-size: 18px;
    font-weight: 600;
    color: #f59e0b;
    margin-top: 16px;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #f8fafc;
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid #f59e0b;
}

.feature-icon {
    font-size: 24px;
    width: 40px;
    text-align: center;
}

.feature-text h5 {
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 4px;
}

.feature-text p {
    font-size: 12px;
    color: #6b7280;
    margin: 0;
    line-height: 1.4;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.info-section {
    background: white;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #e5e7eb;
}

.info-section h3 {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
    margin: 0 0 12px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 4px;
}

.info-section ol, .info-section ul {
    margin: 0;
    padding-left: 20px;
    color: #6b7280;
    font-size: 14px;
}

.info-section li {
    margin-bottom: 4px;
    line-height: 1.4;
}

.info-section p {
    margin-bottom: 8px;
    font-size: 14px;
    color: #6b7280;
}

@media (max-width: 768px) {
    .overview-cards {
        grid-template-columns: 1fr;
    }
    
    .appliance-list {
        grid-template-columns: 1fr;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
    
    .info-grid {
        grid-template-columns: 1fr;
    }
    
    .details-grid {
        grid-template-columns: 1fr;
    }
    
    .appliance-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    
    .detail-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
}
</style>`;
  }

  /**
   * Get default template with enhanced versions
   */
  getDefaultTemplate(templateType: string): string {
    switch (templateType) {
      case 'welcome_letter':
        return this.getProfessionalWelcomeLetterTemplate();
      case 'service_agreement':
        return this.getComprehensiveServiceAgreementTemplate();
      case 'direct_debit_form':
        return this.getEnhancedDirectDebitFormTemplate();
      case 'coverage_summary':
        return this.getCoverageSummaryTemplate();
      default:
        return this.baseService.getDefaultTemplate(templateType as TemplateType);
    }
  }

  /**
   * Render template using base service
   */
  renderTemplate(htmlContent: string, context: any): string {
    return this.baseService.renderTemplate(htmlContent, context);
  }
}