import { TemplateService } from './template-service';
import { TemplateType } from './types';

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
      html: `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Flash Team</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            line-height: 1.6;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 3em;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .header .tagline {
            margin: 15px 0 0 0;
            font-size: 1.3em;
            font-weight: 300;
            opacity: 0.95;
        }
        .content {
            padding: 40px;
        }
        .welcome-section {
            margin-bottom: 35px;
        }
        .welcome-section h2 {
            color: #2c3e50;
            border-bottom: 3px solid #FF6B35;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        .highlight-box {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            color: white;
            padding: 25px;
            margin: 25px 0;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
        }
        .highlight-box strong {
            font-size: 1.2em;
            display: block;
            margin-bottom: 10px;
        }
        .customer-details {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
        }
        .details-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .detail-item {
            border-bottom: 1px solid #dee2e6;
            padding-bottom: 12px;
        }
        .detail-label {
            font-weight: 600;
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .detail-value {
            color: #2c3e50;
            font-size: 1.1em;
            margin-top: 8px;
            font-weight: 500;
        }
        .coverage-summary {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin: 25px 0;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }
        .benefits-section {
            background-color: #f0f8ff;
            border-left: 5px solid #FF6B35;
            padding: 25px;
            margin: 25px 0;
            border-radius: 0 8px 8px 0;
        }
        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .benefit-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        .benefit-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .footer h3 {
            margin-top: 0;
            color: #FF6B35;
            font-size: 1.8em;
        }
        .contact-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin: 25px 0;
        }
        .contact-item {
            text-align: center;
            padding: 15px;
            background-color: rgba(255, 107, 53, 0.1);
            border-radius: 8px;
        }
        .contact-item strong {
            display: block;
            color: #FF6B35;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        .cta-section {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            color: white;
            padding: 30px;
            margin: 30px 0;
            border-radius: 10px;
            text-align: center;
        }
        .steps-list {
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .steps-list ol {
            margin: 0;
            padding-left: 20px;
        }
        .steps-list li {
            margin-bottom: 15px;
            line-height: 1.6;
        }
        .rating-badge {
            background: #ffc107;
            color: #2c3e50;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            display: inline-block;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Flash Team</h1>
            <div class="tagline">Fast, Friendly Repairs You Can Trust</div>
            <div class="rating-badge">⭐⭐⭐⭐⭐ 4.9/5 Rating</div>
        </div>
        
        <div class="content">
            <div class="welcome-section">
                <h2>Welcome to Flash Team Coverage!</h2>
                <p>Dear {{customerName}},</p>
                <p>Thank you for choosing Flash Team for your home protection needs. We're delighted to welcome you to our family of thousands of satisfied customers across the UK who trust us to keep their appliances and heating systems running smoothly.</p>
                <p>As part of our commitment to <strong>fast, friendly repairs you can trust</strong>, your coverage is now active and ready to protect your home with our same-day service and 6-month guarantee.</p>
            </div>

            <div class="highlight-box">
                <strong>🎉 Your Flash Team coverage is now ACTIVE!</strong>
                <p>This letter confirms your coverage details and provides everything you need to know about your protection plan.</p>
            </div>

            <div class="customer-details">
                <h3 style="color: #2c3e50; margin-top: 0;">Your Account Details</h3>
                <div class="details-grid">
                    <div class="detail-item">
                        <div class="detail-label">Customer Name</div>
                        <div class="detail-value">{{customerName}}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Email Address</div>
                        <div class="detail-value">{{email}}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Phone Number</div>
                        <div class="detail-value">{{phone}}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Property Address</div>
                        <div class="detail-value">{{address}}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Coverage Start Date</div>
                        <div class="detail-value">{{coverageStartDate}}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Policy Reference</div>
                        <div class="detail-value">{{policyNumber}}</div>
                    </div>
                </div>
            </div>

            <div class="coverage-summary">
                <h3 style="margin-top: 0;">Your Flash Team Protection</h3>
                <p><strong>Annual Premium:</strong> £{{totalCost}}</p>
                {{#if monthlyCost}}<p><strong>Monthly Payment:</strong> £{{monthlyCost}}</p>{{/if}}
                <div style="margin-top: 20px;">
                    <p><strong>What's Protected:</strong></p>
                    <ul style="margin: 15px 0; padding-left: 25px; text-align: left;">
                        {{#if hasApplianceCover}}<li>✅ Washing Machines, Dishwashers, Ovens, Fridges & More</li>{{/if}}
                        {{#if hasBoilerCover}}<li>✅ Boiler & Central Heating System</li>{{/if}}
                        <li>✅ Same-Day Service Available</li>
                        <li>✅ Fixed Prices - No Hidden Costs</li>
                        <li>✅ Gas Safe Registered Engineers</li>
                        <li>✅ 6-Month Guarantee on Every Repair</li>
                    </ul>
                </div>
            </div>

            <div class="benefits-section">
                <h2 style="color: #2c3e50; margin-top: 0;">Why You Chose Flash Team</h2>
                <div class="benefits-grid">
                    <div class="benefit-card">
                        <div class="benefit-icon">🚀</div>
                        <h4 style="color: #2c3e50; margin: 10px 0;">Same Day Service</h4>
                        <p>Need it fixed fast? We offer same-day and next-day appointments across our nationwide coverage.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="benefit-icon">💷</div>
                        <h4 style="color: #2c3e50; margin: 10px 0;">Fixed Prices</h4>
                        <p>Know exactly what you'll pay upfront. No hidden fees, no call-out charges, no surprises.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="benefit-icon">🔧</div>
                        <h4 style="color: #2c3e50; margin: 10px 0;">Trusted Engineers</h4>
                        <p>All engineers are fully trained, DBS checked, and Gas Safe registered where applicable.</p>
                    </div>
                    <div class="benefit-card">
                        <div class="benefit-icon">🛡️</div>
                        <h4 style="color: #2c3e50; margin: 10px 0;">6-Month Guarantee</h4>
                        <p>Every repair comes with our comprehensive 6-month guarantee on parts and labour.</p>
                    </div>
                </div>
            </div>

            <div class="cta-section">
                <h2 style="margin-top: 0;">Need a Repair? It's Simple!</h2>
                <div class="steps-list">
                    <ol style="text-align: left; color: #2c3e50;">
                        <li><strong>Call us on 0330 822 7695</strong> - Our friendly team is available 7 days a week</li>
                        <li><strong>Quote your policy reference:</strong> {{policyNumber}}</li>
                        <li><strong>Describe the problem</strong> - We'll provide instant diagnosis over the phone</li>
                        <li><strong>Book your appointment</strong> - Same-day service available in most areas</li>
                        <li><strong>Expert repair</strong> - Our Gas Safe engineer will fix it with our 6-month guarantee</li>
                    </ol>
                </div>
            </div>

            <div class="welcome-section">
                <h2>Important Information</h2>
                <ul>
                    <li><strong>Keep This Letter Safe:</strong> Your policy reference number is {{policyNumber}} - you'll need this for any claims</li>
                    <li><strong>Emergency Repairs:</strong> Call 0330 822 7695 for 24/7 emergency support</li>
                    <li><strong>Online Account:</strong> Visit www.theflashteam.co.uk to manage your account and book repairs</li>
                    <li><strong>Annual Service:</strong> We'll contact you about your annual boiler service to keep your warranty valid</li>
                </ul>
            </div>

            <div class="highlight-box">
                <strong>💡 Pro Tip:</strong> 95% of our repairs are completed on the first visit! Our expert diagnosis and comprehensive van stock means we fix it right, first time.
            </div>
        </div>

        <div class="footer">
            <h3>Contact Flash Team</h3>
            <div class="contact-info">
                <div class="contact-item">
                    <strong>📞 24/7 Repair Helpline</strong>
                    0330 822 7695
                </div>
                <div class="contact-item">
                    <strong>📧 Customer Support</strong>
                    info@theflashteam.co.uk
                </div>
                <div class="contact-item">
                    <strong>🌐 Online Portal</strong>
                    www.theflashteam.co.uk
                </div>
                <div class="contact-item">
                    <strong>📍 Coverage Area</strong>
                    Nationwide UK
                </div>
            </div>
            <p style="margin-top: 30px; font-size: 0.95em; opacity: 0.9;">
                <strong>Flash Team - Fast, Friendly Repairs You Can Trust</strong><br>
                Thank you for choosing us to protect your home. We're here whenever you need us!
            </p>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
                <small>⭐⭐⭐⭐⭐ Trusted by thousands of UK homeowners • Gas Safe Registered • Same-Day Service Available</small>
            </div>
        </div>
    </div>
</body>
</html>`
    }
  ];

  private baseService: TemplateService;

  constructor() {
    this.baseService = new TemplateService();
  }

  /**
   * Get all available templates
   */
  getAvailableTemplates() {
    return EnhancedTemplateService.templates;
  }

  /**
   * Get template by ID
   */
  getTemplate(templateId: string) {
    const template = EnhancedTemplateService.templates.find(t => t.id === templateId);
    if (!template) {
      throw new Error(`Template ${templateId} not found`);
    }
    return template;
  }

  /**
   * Generate document from template with Flash Team branding
   */
  async generateDocument(templateId: string, data: any): Promise<string> {
    const template = this.getTemplate(templateId);
    
    // Process template with Handlebars-like syntax
    let html = template.html;
    
    // Replace simple variables
    const replaceVariables = (text: string, obj: any, prefix = ''): string => {
      return text.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
        const cleanKey = key.trim();
        const value = this.getNestedValue(obj, cleanKey);
        return value !== undefined ? String(value) : match;
      });
    };
    
    // Replace conditional blocks
    html = this.processConditionals(html, data);
    
    // Replace variables
    html = replaceVariables(html, data);
    
    return html;
  }

  /**
   * Process conditional blocks like {{#if condition}}...{{/if}}
   */
  private processConditionals(html: string, data: any): string {
    const conditionalRegex = /\{\{#if\s+([^}]+)\}\}([\s\S]*?)\{\{\/if\}\}/g;
    
    return html.replace(conditionalRegex, (match, condition, content) => {
      const conditionValue = this.getNestedValue(data, condition.trim());
      return conditionValue ? content : '';
    });
  }

  /**
   * Get nested object value by dot notation path
   */
  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => {
      return current && current[key] !== undefined ? current[key] : undefined;
    }, obj);
  }

  /**
   * Preview template with sample data
   */
  async previewTemplate(templateId: string): Promise<string> {
    const sampleData = {
      customerName: 'John Smith',
      email: 'john.smith@email.com',
      phone: '07700 900123',
      address: '123 High Street, London, SW1A 1AA',
      coverageStartDate: '1st January 2025',
      policyNumber: 'FT-2025-001234',
      totalCost: '299',
      monthlyCost: '24.99',
      hasApplianceCover: true,
      hasBoilerCover: true,
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
      })
    };

    return this.generateDocument(templateId, sampleData);
  }

  /**
   * Get default template content for backward compatibility
   */
  getDefaultTemplate(templateType: string): string {
    // For backward compatibility, always return the welcome letter template
    // since we now only have one template
    const template = this.getTemplate('welcome-letter');
    return template.html;
  }

  /**
   * Render template using base service for backward compatibility
   */
  renderTemplate(htmlContent: string, context: any): string {
    return this.baseService.renderTemplate(htmlContent, context);
  }
}