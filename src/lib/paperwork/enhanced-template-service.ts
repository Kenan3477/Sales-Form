// Self-contained type definitions
type TemplateType = 'welcome-letter' | 'service-agreement' | 'direct-debit-form' | 'coverage-summary' | string;

/**
 * Enhanced template service with Flash Team branding
 */
export class EnhancedTemplateService {
  private static templates = [
    {
      id: 'welcome-letter',
      name: 'Welcome Letter',
      description: 'Flash Team welcome letter for new customers',
      category: 'Customer Communications',
      html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flash Team Protection Plan</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.4;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .document-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .header {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 30%, #1e4c72 70%, #1a365d 100%);
            color: white;
            padding: 30px 40px;
            position: relative;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 8px;
            background: linear-gradient(90deg, #ff4500 0%, #ff6500 50%, #ff4500 100%);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .lightning-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(45deg, #ff6500, #ffa500);
            clip-path: polygon(25% 0%, 75% 0%, 50% 45%, 85% 45%, 50% 100%, 15% 55%, 50% 55%);
            box-shadow: 0 0 10px rgba(255,101,0,0.4);
        }
        
        .logo-text {
            font-size: 36px;
            font-weight: bold;
            letter-spacing: 2px;
        }
        
        .tagline {
            font-size: 14px;
            opacity: 0.95;
            margin-top: 2px;
            font-style: italic;
            letter-spacing: 0.5px;
        }
        
        .content {
            padding: 40px;
        }
        
        .main-title {
            font-size: 28px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 25px;
            border-bottom: 3px solid #ff6500;
            padding-bottom: 10px;
        }
        
        .intro-text {
            font-size: 15px;
            margin-bottom: 25px;
            line-height: 1.6;
        }
        
        .activation-banner {
            background: linear-gradient(135deg, #ff6500 0%, #ff8500 100%);
            color: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .activation-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        }
        
        .activation-banner .lightning-small {
            width: 20px;
            height: 20px;
            background: white;
            clip-path: polygon(25% 0%, 75% 0%, 50% 45%, 85% 45%, 50% 100%, 15% 55%, 50% 55%);
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        .activation-text {
            font-size: 18px;
            font-weight: bold;
            position: relative;
            z-index: 1;
        }
        
        .activation-subtext {
            background: #1a365d;
            margin: 15px -20px -20px -20px;
            padding: 12px 20px;
            font-size: 14px;
            position: relative;
            z-index: 1;
        }
        
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 25px;
        }
        
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            overflow: hidden;
            background: #fafbfc;
        }
        
        .card-header {
            background: #1a365d;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 16px;
        }
        
        .card-content {
            padding: 20px;
            background: white;
        }
        
        .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 10px 0;
            border-bottom: 1px solid #f0f4f7;
        }
        
        .detail-row:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
            width: 35%;
        }
        
        .detail-value {
            font-weight: bold;
            color: #1a365d;
            text-align: right;
            width: 60%;
            font-size: 14px;
        }
        
        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .checklist-item:last-child {
            margin-bottom: 0;
        }
        
        .check-icon {
            width: 18px;
            height: 18px;
            background: #ff6500;
            border-radius: 50%;
            position: relative;
            flex-shrink: 0;
            margin-top: 2px;
        }
        
        .check-icon::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 12px;
            font-weight: bold;
        }
        
        .single-column-card {
            margin-bottom: 25px;
        }
        
        .numbered-list {
            counter-reset: step-counter;
        }
        
        .numbered-item {
            display: flex;
            align-items: flex-start;
            gap: 15px;
            margin-bottom: 12px;
            counter-increment: step-counter;
            font-size: 14px;
        }
        
        .numbered-item::before {
            content: counter(step-counter);
            background: #1a365d;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .guarantee-intro {
            font-weight: bold;
            margin-bottom: 15px;
            color: #1a365d;
            font-size: 14px;
        }
        
        .guarantee-list {
            list-style: none;
            counter-reset: item-counter;
        }
        
        .guarantee-list li {
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
            font-size: 14px;
            counter-increment: item-counter;
        }
        
        .guarantee-list li::before {
            content: counter(item-counter);
            position: absolute;
            left: 0;
            background: #1a365d;
            color: white;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
        }
        
        .important-section {
            background: #f8fafc;
            border-left: 4px solid #ff6500;
            padding: 25px;
            margin-bottom: 0;
            border-radius: 0 8px 8px 0;
        }
        
        .important-title {
            font-size: 18px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 15px;
        }
        
        .important-list {
            list-style: none;
        }
        
        .important-list li {
            margin-bottom: 12px;
            padding-left: 20px;
            position: relative;
            font-size: 14px;
        }
        
        .important-list li::before {
            content: '•';
            color: #ff6500;
            font-weight: bold;
            position: absolute;
            left: 0;
            font-size: 16px;
        }
        
        .footer {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
            color: white;
            padding: 20px 40px;
            text-align: center;
            font-size: 14px;
            margin-top: 0;
        }
        
        .footer-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .footer-divider {
            color: #ff6500;
            font-weight: bold;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .document-container {
                max-width: none;
                margin: 0;
                box-shadow: none;
            }
            
            .card {
                break-inside: avoid;
            }
        }
        
        @media (max-width: 768px) {
            .content {
                padding: 20px;
            }
            
            .header {
                padding: 20px;
            }
            
            .two-column {
                grid-template-columns: 1fr;
            }
            
            .footer-content {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <div class="header">
            <div class="logo-section">
                <div class="lightning-icon"></div>
                <div>
                    <div class="logo-text">Flash Team</div>
                    <div class="tagline">Fast, Friendly Repairs You Can Trust</div>
                </div>
            </div>
        </div>
        
        <div class="content">
            <h1 class="main-title">The Flash Team's Protection Plan</h1>
            
            <div class="intro-text">
                <strong>Dear {{customer.name}},</strong><br><br>
                Thank you for choosing Flash Team. This document confirms that your <strong>Protection Plan</strong> is now active, subject to the plan terms, conditions and exclusions.
            </div>
            
            <div class="activation-banner">
                <div class="activation-text">
                    <span class="lightning-small"></span>
                    Your Protection Plan is now active
                </div>
                <div class="activation-subtext">
                    This letter explains your cover and how to request assistance
                </div>
            </div>
            
            <div class="two-column">
                <div class="card">
                    <div class="card-header">Your Account Details</div>
                    <div class="card-content">
                        <div class="detail-row">
                            <span class="detail-label">CUSTOMER</span>
                            <span class="detail-value">{{customer.name}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">EMAIL</span>
                            <span class="detail-value">{{customer.email}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">PHONE</span>
                            <span class="detail-value">{{customer.phone}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">ADDRESS</span>
                            <span class="detail-value">{{customer.address}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">START DATE</span>
                            <span class="detail-value">{{agreement.startDate}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">PLAN REF</span>
                            <span class="detail-value">{{agreement.planNumber}}</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">What Your Plan Provides</div>
                    <div class="card-content">
                        <div class="detail-row" style="border-bottom: 2px solid #ff6500; margin-bottom: 15px; padding-bottom: 15px;">
                            <span class="detail-label">Monthly Payment:</span>
                            <span class="detail-value">£{{agreement.monthlyCost}}</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Access to qualified engineers for covered breakdowns</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Repairs to covered appliances or systems, where repair is possible.</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>If a repair is not economically viable, we may, at our discretion, offer a replacement of equivalent specification (now for old wree ahere applicable), subject to availability.</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Fixed pricing with no call-out charge for covered faults</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Appointments offered subject to engineer availability</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card single-column-card">
                <div class="card-header">Requesting Assistance</div>
                <div class="card-content">
                    <div class="numbered-list">
                        <div class="numbered-item">
                            <span>Call 0330 822 7695</span>
                        </div>
                        <div class="numbered-item">
                            <span>Quote your plan reference {{agreement.planNumber}}</span>
                        </div>
                        <div class="numbered-item">
                            <span>Describe the issue so we can assess eligibility</span>
                        </div>
                        <div class="numbered-item">
                            <span>Book an appointment subject to availability</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card single-column-card">
                <div class="card-header">Direct Debit Guarantee</div>
                <div class="card-content">
                    <div class="guarantee-intro">
                        If you pay by Direct Debit, payments will appear on your bank statement as Warmcare.
                    </div>
                    <ul class="guarantee-list">
                        <li>Call 0330 822 7695</li>
                        <li>Quote your plan reference {{agreement.planNumber}}</li>
                        <li>Describe the issue so we can assess eligibility</li>
                        <li>You may cancel your Direct Debit at any time via your bank or building society</li>
                    </ul>
                </div>
            </div>
            
            <div class="important-section">
                <div class="important-title">Important Information</div>
                <ul class="important-list">
                    <li>This Protection Plan is a <strong>service agreement</strong> and is not an insurance plan</li>
                    <li>All services are provided subject to <strong>plan terms, conditions and exclusions</strong></li>
                    <li><strong>Annual boiler service:</strong> Please contact us to <strong>book your annual boiler service</strong></li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-content">
                <span>Flash Team</span>
                <span class="footer-divider">•</span>
                <span>Nationwide UK</span>
                <span class="footer-divider">•</span>
                <span>0330 822 7695</span>
                <span class="footer-divider">•</span>
                <span>theflashteam.co.uk</span>
            </div>
        </div>
    </div>
</body>
</html>`
    }
  ];

  constructor() {
    // No dependencies needed - self-contained template service
  }

  /**
   * Get all available templates
   */
  getAvailableTemplates() {
    return EnhancedTemplateService.templates;
  }

  /**
   * Get a specific template by ID
   */
  getTemplate(templateId: TemplateType) {
    const template = EnhancedTemplateService.templates.find(t => t.id === templateId);
    if (!template) {
      throw new Error(`Template not found: ${templateId}`);
    }
    return template;
  }

  /**
   * Generate a document using the specified template
   */
  async generateDocument(templateId: TemplateType, data: any): Promise<string> {
    try {
      const template = this.getTemplate(templateId);
      let html = template.html;

      // Replace template variables with actual data
      html = html.replace(/\{\{([^}]+)\}\}/g, (match: string, key: string) => {
        const cleanKey = key.trim();
        
        // Handle nested properties like customer.name, agreement.monthlyCost
        const value = cleanKey.split('.').reduce((obj: any, prop: string) => {
          return obj && obj[prop] !== undefined ? obj[prop] : undefined;
        }, data);
        
        return value !== undefined ? String(value) : match;
      });

      return html;

    } catch (error) {
      console.error('Error generating document:', error);
      throw error;
    }
  }

  /**
   * Preview a template with sample data
   */
  async previewTemplate(templateId: TemplateType): Promise<string> {
    // Sample data for preview
    const sampleData = {
      customer: {
        name: 'John Smith',
        email: 'john.smith@example.com',
        phone: '01234 567890',
        address: '123 Main Street, City, Postcode'
      },
      agreement: {
        startDate: '2024-01-15',
        planNumber: 'TFT0123',
        monthlyCost: '29.99'
      }
    };

    return this.generateDocument(templateId, sampleData);
  }
}