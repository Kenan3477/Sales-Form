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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.2;
            color: #2d3748;
            background: white;
            font-size: 10px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .document-container {
            max-width: 100%;
            background: white;
        }
        
        .header {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 30%, #1e4c72 70%, #1a365d 100%);
            color: white;
            padding: 8px 15px;
            position: relative;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #ff4500 0%, #ff6500 50%, #ff4500 100%);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .lightning-icon {
            width: 18px;
            height: 18px;
            background: linear-gradient(45deg, #ff6500, #ffa500);
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        
        .lightning-icon::before {
            content: '⚡';
        }
        
        .logo-text {
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        
        .tagline {
            font-size: 9px;
            opacity: 0.9;
            margin-top: 1px;
            font-style: italic;
        }
        
        .content {
            padding: 18px 15px 30px 15px;
        }
        
        .main-title {
            font-size: 16px;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 14px;
            border-bottom: 2px solid #ff6500;
            padding-bottom: 7px;
            letter-spacing: -0.25px;
        }
        
        .intro-text {
            font-size: 10px;
            margin-bottom: 18px;
            line-height: 1.45;
        }
        
        .activation-banner {
            background: linear-gradient(135deg, #ff6500 0%, #ff8500 100%);
            color: white;
            padding: 14px 18px;
            margin-bottom: 22px;
            border-radius: 4px;
            text-align: center;
            font-size: 11px;
            font-weight: 600;
            box-shadow: 0 2px 6px rgba(255, 101, 0, 0.2);
            letter-spacing: 0.25px;
        }
        
        .three-column {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 14px;
            margin-bottom: 24px;
        }
        
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            background: #fafbfc;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: box-shadow 0.2s ease;
        }
        
        .card-header {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
            color: white;
            padding: 12px 8px;
            font-weight: 600;
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .card-content {
            padding: 14px 8px;
            background: white;
            font-size: 8px;
            line-height: 1.45;
        }
        
        .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 4px 0;
            border-bottom: 1px solid #f0f4f7;
        }
        
        .detail-row:last-child {
            border-bottom: none;
            padding-bottom: 3px;
        }
        
        .detail-label {
            font-weight: 600;
            color: #4a5568;
            text-transform: uppercase;
            font-size: 7px;
            letter-spacing: 0.5px;
            width: 45%;
        }
        
        .detail-value {
            font-weight: 600;
            color: #1a365d;
            text-align: right;
            width: 50%;
            font-size: 8px;
        }
        
        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 5px;
            margin-bottom: 7px;
            font-size: 8px;
            line-height: 1.45;
        }
        
        .checklist-item:last-child {
            margin-bottom: 3px;
        }
        
        .check-icon {
            width: 10px;
            height: 10px;
            background: linear-gradient(135deg, #ff6500, #ff8500);
            border-radius: 50%;
            position: relative;
            flex-shrink: 0;
            margin-top: 1px;
            box-shadow: 0 1px 2px rgba(255, 101, 0, 0.3);
        }
        
        .check-icon::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 7px;
            font-weight: bold;
        }
        
        .two-column-bottom {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin-bottom: 24px;
        }
        
        .compact-list {
            list-style: none;
            font-size: 8px;
            line-height: 1.45;
        }
        
        .compact-list li {
            margin-bottom: 6px;
            padding-left: 10px;
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
            font-size: 8px;
        }
        
        .numbered-steps div {
            margin-bottom: 6px;
            padding-left: 12px;
            position: relative;
            line-height: 1.45;
        }
        
        .numbered-steps div::before {
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            background: linear-gradient(135deg, #1a365d, #2c5282);
            color: white;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 6px;
            font-weight: 600;
            top: 1px;
            box-shadow: 0 1px 2px rgba(26, 54, 93, 0.3);
        }
        
        .numbered-steps {
            counter-reset: step-counter;
        }
        
        .important-section {
            background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
            border-left: 3px solid #ff6500;
            padding: 14px;
            margin-bottom: 22px;
            border-radius: 0 4px 4px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .important-title {
            font-size: 9px;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 10px;
            letter-spacing: 0.25px;
        }
        
        .additional-info {
            background: linear-gradient(135deg, #e8f4fd 0%, #bee3f8 100%);
            border: 1px solid #90cdf4;
            border-radius: 4px;
            padding: 14px;
            margin-bottom: 22px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .additional-info h3 {
            color: #1a365d;
            font-size: 9px;
            font-weight: 700;
            margin-bottom: 10px;
            border-bottom: 1px solid #90cdf4;
            padding-bottom: 4px;
            letter-spacing: 0.25px;
        }
        
        .coverage-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin-bottom: 24px;
        }
        
        .coverage-section {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .coverage-section h4 {
            color: #1a365d;
            font-size: 8px;
            font-weight: 700;
            margin-bottom: 7px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .footer {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
            color: white;
            padding: 14px 15px;
            text-align: center;
            font-size: 8px;
            margin-top: 18px;
            box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
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
                        <div style="font-weight: bold; margin-bottom: 8px; font-size: 10px;">
                            Payments appear as "Warmcare" on your bank statement.
                        </div>
                        <ul class="compact-list">
                            <li>10 working days notice for payment changes</li>
                            <li>Full refund if payment errors occur</li>
                            <li>Cancel anytime via your bank</li>
                            <li>Offered by all banks and building societies</li>
                            <li>Confirmation given when payment requested</li>
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
                        <li>Emergency cover available for qualifying issues</li>
                    </ul>
                </div>
            </div>
            
            <div class="coverage-grid">
                <div class="coverage-section">
                    <h4>What's Covered</h4>
                    <ul class="compact-list">
                        <li>Central heating system repairs</li>
                        <li>Boiler breakdown and servicing</li>
                        <li>Radiator and pipework issues</li>
                        <li>Thermostat and control faults</li>
                        <li>Kitchen appliance breakdowns</li>
                        <li>Washing machine and dishwasher</li>
                    </ul>
                </div>
                
                <div class="coverage-section">
                    <h4>Exclusions & Limitations</h4>
                    <ul class="compact-list">
                        <li>Pre-existing conditions</li>
                        <li>Damage due to neglect or misuse</li>
                        <li>External pipework and drainage</li>
                        <li>Cosmetic damage or wear</li>
                        <li>Appliances over 15 years old</li>
                        <li>Full terms available on request</li>
                    </ul>
                </div>
            </div>
            
            <div class="additional-info">
                <h3>Your Rights & Peace of Mind</h3>
                <div class="coverage-grid">
                    <div>
                        <p style="font-size: 10px; margin-bottom: 6px;"><strong>Cooling Off Period:</strong> You have 14 days to cancel this agreement for a full refund.</p>
                    </div>
                    <div>
                        <p style="font-size: 10px; margin-bottom: 6px;"><strong>Quality Guarantee:</strong> All work carried out by Gas Safe registered engineers.</p>
                    </div>
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