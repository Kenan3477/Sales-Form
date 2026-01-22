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
            line-height: 1.3;
            color: #333;
            background: white;
            font-size: 12px;
        }
        
        .document-container {
            max-width: 100%;
            background: white;
        }
        
        .header {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 30%, #1e4c72 70%, #1a365d 100%);
            color: white;
            padding: 15px 20px;
            position: relative;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ff4500 0%, #ff6500 50%, #ff4500 100%);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .lightning-icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(45deg, #ff6500, #ffa500);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: white;
        }
        
        .lightning-icon::before {
            content: '⚡';
        }
        
        .logo-text {
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        
        .tagline {
            font-size: 11px;
            opacity: 0.9;
            margin-top: 1px;
            font-style: italic;
        }
        
        .content {
            padding: 15px 20px;
        }
        
        .main-title {
            font-size: 20px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 12px;
            border-bottom: 2px solid #ff6500;
            padding-bottom: 5px;
        }
        
        .intro-text {
            font-size: 12px;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        
        .activation-banner {
            background: linear-gradient(135deg, #ff6500 0%, #ff8500 100%);
            color: white;
            padding: 12px 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            text-align: center;
            font-size: 14px;
            font-weight: bold;
        }
        
        .three-column {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            background: #fafbfc;
        }
        
        .card-header {
            background: #1a365d;
            color: white;
            padding: 8px 12px;
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
        }
        
        .card-content {
            padding: 10px 12px;
            background: white;
            font-size: 10px;
        }
        
        .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 3px 0;
            border-bottom: 1px solid #f0f4f7;
        }
        
        .detail-row:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
            font-size: 9px;
            letter-spacing: 0.3px;
            width: 45%;
        }
        
        .detail-value {
            font-weight: bold;
            color: #1a365d;
            text-align: right;
            width: 50%;
            font-size: 10px;
        }
        
        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 6px;
            margin-bottom: 5px;
            font-size: 9px;
            line-height: 1.2;
        }
        
        .checklist-item:last-child {
            margin-bottom: 0;
        }
        
        .check-icon {
            width: 12px;
            height: 12px;
            background: #ff6500;
            border-radius: 50%;
            position: relative;
            flex-shrink: 0;
            margin-top: 1px;
        }
        
        .check-icon::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 8px;
            font-weight: bold;
        }
        
        .two-column-bottom {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .compact-list {
            list-style: none;
            font-size: 9px;
            line-height: 1.3;
        }
        
        .compact-list li {
            margin-bottom: 4px;
            padding-left: 12px;
            position: relative;
        }
        
        .compact-list li::before {
            content: '•';
            color: #ff6500;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .numbered-steps {
            font-size: 10px;
        }
        
        .numbered-steps div {
            margin-bottom: 4px;
            padding-left: 15px;
            position: relative;
        }
        
        .numbered-steps div::before {
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            background: #1a365d;
            color: white;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 8px;
            font-weight: bold;
            top: 1px;
        }
        
        .numbered-steps {
            counter-reset: step-counter;
        }
        
        .important-section {
            background: #f8fafc;
            border-left: 3px solid #ff6500;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 0 4px 4px 0;
        }
        
        .important-title {
            font-size: 12px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 8px;
        }
        
        .footer {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
            color: white;
            padding: 10px 20px;
            text-align: center;
            font-size: 10px;
            margin-top: 0;
        }
        
        .footer-content {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
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
                page-break-inside: avoid;
            }
            
            * {
                page-break-inside: avoid;
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
            <h1 class="main-title">Protection Plan Confirmation</h1>
            
            <div class="intro-text">
                <strong>Dear {{customerName}},</strong><br>
                Thank you for choosing Flash Team. Your <strong>Protection Plan</strong> is now active.
            </div>
            
            <div class="activation-banner">
                ⚡ Your Protection Plan is Active - Plan Ref: {{policyNumber}}
            </div>
            
            <div class="three-column">
                <div class="card">
                    <div class="card-header">Customer Details</div>
                    <div class="card-content">
                        <div class="detail-row">
                            <span class="detail-label">Name</span>
                            <span class="detail-value">{{customerName}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Email</span>
                            <span class="detail-value">{{email}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Phone</span>
                            <span class="detail-value">{{phone}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Address</span>
                            <span class="detail-value">{{address}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Start Date</span>
                            <span class="detail-value">{{coverageStartDate}}</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">Plan Benefits</div>
                    <div class="card-content">
                        <div class="detail-row" style="border-bottom: 2px solid #ff6500; margin-bottom: 8px; padding-bottom: 8px;">
                            <span class="detail-label">Monthly:</span>
                            <span class="detail-value">£{{monthlyCost}}</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Qualified engineers for covered breakdowns</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Repairs or replacement where applicable</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Fixed pricing - no call-out charges</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Subject to engineer availability</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">Request Assistance</div>
                    <div class="card-content">
                        <div class="numbered-steps">
                            <div>Call 0330 822 7695</div>
                            <div>Quote plan ref {{policyNumber}}</div>
                            <div>Describe the issue</div>
                            <div>Book appointment</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="two-column-bottom">
                <div class="card">
                    <div class="card-header">Direct Debit Guarantee</div>
                    <div class="card-content">
                        <div style="font-weight: bold; margin-bottom: 6px; font-size: 9px;">
                            Payments appear as "Warmcare" on your bank statement.
                        </div>
                        <ul class="compact-list">
                            <li>10 working days notice for payment changes</li>
                            <li>Full refund if payment errors occur</li>
                            <li>Cancel anytime via your bank</li>
                            <li>Offered by all banks and building societies</li>
                        </ul>
                    </div>
                </div>
                
                <div class="important-section">
                    <div class="important-title">Important Information</div>
                    <ul class="compact-list">
                        <li>This is a <strong>service agreement</strong> (not insurance)</li>
                        <li>Subject to <strong>plan terms, conditions and exclusions</strong></li>
                        <li><strong>Annual boiler service:</strong> Contact us to book</li>
                        <li>All repairs subject to availability and assessment</li>
                    </ul>
                </div>
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