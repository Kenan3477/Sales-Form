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
      html: `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Flash Team's Protection Plan</title>

  <style>
    :root{
      /* Brand palette (dark blue + orange) */
      --navy:#0b2a4a;
      --navy-dark:#081f36;
      --orange:#ff6b35;
      --orange-soft:#ff8c42;

      --bg:#f4f6fa;
      --text:#223043;
      --muted:#6b7787;
      --line:#e4e9f1;
      --card:#ffffff;
      --soft:#f0f5ff;
    }

    *{box-sizing:border-box}

    body{
      margin:0;
      padding:24px;
      background:var(--bg);
      font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;
      color:var(--text);
      line-height:1.55;
    }

    .container{
      max-width:860px;
      margin:0 auto;
      background:var(--card);
      border-radius:14px;
      overflow:hidden;
      box-shadow:0 8px 18px rgba(12, 24, 39, 0.10);
      border:1px solid rgba(11,42,74,.08);
    }

    /* Header */
    .header{
      background:linear-gradient(135deg,var(--navy) 0%,var(--navy-dark) 100%);
      color:#fff;
      padding:36px 28px 28px;
      position:relative;
    }
    .header::after{
      content:"";
      position:absolute;
      bottom:0;
      left:0;
      right:0;
      height:6px;
      background:linear-gradient(90deg,var(--orange),var(--orange-soft));
    }

    .brand{
      display:flex;
      align-items:center;
      justify-content:center;
      gap:14px;
      text-align:center;
      flex-wrap:wrap;
    }

    .bolt{
      width:42px;
      height:42px;
      border-radius:12px;
      background:linear-gradient(135deg,var(--orange),var(--orange-soft));
      display:grid;
      place-items:center;
      font-size:22px;
      font-weight:900;
      box-shadow:0 6px 14px rgba(255,107,53,.35);
    }

    .brand h1{
      margin:0;
      font-size:42px;
      font-weight:800;
      letter-spacing:.4px;
      line-height:1;
    }

    .tagline{
      margin:10px 0 0 0;
      text-align:center;
      font-weight:500;
      opacity:.95;
    }

    /* Content */
    .content{padding:32px}

    h2{
      margin:0 0 14px 0;
      font-size:22px;
      color:var(--navy);
      border-bottom:3px solid var(--orange);
      padding-bottom:8px;
    }

    .hero{
      background:linear-gradient(135deg,var(--orange),var(--orange-soft));
      color:#fff;
      border-radius:12px;
      padding:18px 20px;
      text-align:center;
      margin:22px 0;
      box-shadow:0 8px 18px rgba(255,107,53,.28);
    }
    .hero strong{
      display:block;
      font-size:18px;
      margin-bottom:6px;
    }

    .grid{
      display:grid;
      grid-template-columns:1.1fr .9fr;
      gap:20px;
      margin:24px 0;
      align-items:start;
    }
    @media(max-width:800px){
      .grid{grid-template-columns:1fr}
      body{padding:12px}
      .content{padding:22px 16px}
      .brand h1{font-size:38px}
    }

    /* Cards */
    .card{
      border:1px solid var(--line);
      border-radius:12px;
      overflow:hidden;
      background:#fff;
    }
    .card-header{
      background:linear-gradient(180deg, rgba(11,42,74,.06) 0%, rgba(11,42,74,.02) 100%);
      padding:14px 16px;
      font-weight:900;
      color:var(--navy);
      border-bottom:1px solid var(--line);
    }

    .row{
      display:flex;
      justify-content:space-between;
      gap:14px;
      padding:10px 16px;
      border-bottom:1px solid var(--line);
    }
    .row:last-child{border-bottom:none}

    .label{
      text-transform:uppercase;
      font-size:12px;
      letter-spacing:.4px;
      color:var(--muted);
      font-weight:800;
      min-width:160px;
    }

    .value{
      font-weight:800;
      text-align:right;
      max-width:420px;
    }

    .body-pad{padding:16px}

    ul{margin:10px 0 0 0; padding-left:18px}
    li{margin:8px 0}

    /* Steps */
    .steps{
      border:1px solid var(--line);
      border-radius:12px;
      padding:16px;
      background:#fbfcff;
    }
    .steps ol{margin:0; padding-left:18px}
    .steps li{margin:10px 0}

    .phone{
      color:var(--navy);
      font-weight:900;
      text-decoration:none;
    }

    /* Direct Debit */
    .dd{
      margin-top:18px;
      border-radius:12px;
      border:1px solid var(--line);
      overflow:hidden;
      background:#fff;
    }
    .dd-header{
      background:linear-gradient(90deg,#eef2f9,#fff3eb);
      padding:14px 16px;
      font-weight:900;
      color:var(--navy);
      border-bottom:1px solid var(--line);
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:10px;
    }
    .dd-badge{
      font-size:12px;
      font-weight:900;
      color:var(--orange);
      border:2px solid rgba(255,107,53,.35);
      padding:4px 10px;
      border-radius:999px;
      background:#fff;
      white-space:nowrap;
    }
    .dd-body{padding:14px 16px}

    .note{
      margin-top:12px;
      padding:10px 12px;
      border-radius:10px;
      background:var(--soft);
      border:1px solid rgba(11,42,74,.10);
      color:var(--navy);
      font-weight:800;
    }

    /* Footer */
    .footer{
      background:linear-gradient(135deg,var(--navy),var(--navy-dark));
      color:#fff;
      padding:24px 26px;
      margin-top:26px;
      position:relative;
    }
    .footer::before{
      content:"";
      position:absolute;
      top:0;
      left:0;
      right:0;
      height:6px;
      background:linear-gradient(90deg,var(--orange),var(--orange-soft));
    }
    .footer-grid{
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
      gap:12px;
      margin-top:12px;
    }
    .footer-card{
      background:rgba(255,255,255,.08);
      border:1px solid rgba(255,255,255,.10);
      padding:12px;
      border-radius:10px;
    }
    .footer-card strong{display:block;margin-bottom:6px}
    .small{opacity:.9;margin-top:14px;font-size:13px}

    /* Print tweaks */
    @media print{
      body{background:#fff;padding:0}
      .container{box-shadow:none;border:none;border-radius:0;max-width:100%}
      .footer{page-break-inside:avoid}
    }
  </style>
</head>

<body>
<div class="container">

  <div class="header">
    <div class="brand">
      <div class="bolt">⚡</div>
      <div>
        <h1>Flash Team</h1>
        <div class="tagline">Fast, Friendly Repairs You Can Trust</div>
      </div>
    </div>
  </div>

  <div class="content">

    <h2>The Flash Team's Protection Plan</h2>

    <p>Dear <strong>{{customerName}}</strong>,</p>

    <p>
      Thank you for choosing Flash Team. This document confirms that your
      <strong>Protection Plan</strong> is now active, subject to the plan terms,
      conditions and exclusions.
    </p>

    <div class="hero">
      <strong>Your Protection Plan is now active</strong>
      This letter explains your cover and how to request assistance.
    </div>

    <div class="grid">

      <!-- Account Details -->
      <div class="card">
        <div class="card-header">Your Account Details</div>
        <div class="row"><div class="label">Customer</div><div class="value">{{customerName}}</div></div>
        <div class="row"><div class="label">Email</div><div class="value">{{email}}</div></div>
        <div class="row"><div class="label">Phone</div><div class="value">{{phone}}</div></div>
        <div class="row"><div class="label">Address</div><div class="value">{{address}}</div></div>
        <div class="row"><div class="label">Start Date</div><div class="value">{{coverageStartDate}}</div></div>
        <div class="row"><div class="label">Plan Ref</div><div class="value">{{policyNumber}}</div></div>
      </div>

      <!-- Plan Summary -->
      <div class="card">
        <div class="card-header">What Your Plan Provides</div>
        <div class="body-pad">
          <p><strong>Annual Cost:</strong> £{{totalCost}}</p>
          {{#if monthlyCost}}<p><strong>Monthly Payment:</strong> £{{monthlyCost}}</p>{{/if}}

          <ul>
            {{#if hasApplianceCover}}<li>Access to qualified engineers for covered appliance breakdowns</li>{{/if}}
            {{#if hasBoilerCover}}<li>Access to qualified engineers for covered boiler and central heating breakdowns</li>{{/if}}
            <li>Repairs to covered appliances or systems, where repair is possible</li>
            <li>
              If a repair is not economically viable, we may, at our discretion,
              offer a replacement of equivalent specification (new for old where applicable),
              subject to availability and the plan terms.
            </li>
            <li>Fixed pricing with no call-out charge for covered faults</li>
            <li>Appointments offered subject to engineer availability</li>
          </ul>
        </div>
      </div>

    </div>

    <h2>Requesting Assistance</h2>
    <div class="steps">
      <ol>
        <li>Call <a class="phone" href="tel:03308227695">0330 822 7695</a></li>
        <li>Quote your plan reference <strong>{{policyNumber}}</strong></li>
        <li>Describe the issue so we can assess eligibility under the plan</li>
        <li>Book an appointment subject to availability</li>
      </ol>
    </div>

    <div class="dd">
      <div class="dd-header">
        <span>Direct Debit Guarantee</span>
        <span class="dd-badge">Payments show as "Warmcare"</span>
      </div>
      <div class="dd-body">
        <p style="margin-top:0">
          If you pay by Direct Debit, your payment will appear on your bank statement as <strong>Warmcare</strong>.
        </p>
        <ul>
          <li>The Direct Debit Guarantee is offered by all banks and building societies that accept instructions to pay Direct Debits.</li>
          <li>If there are any changes to the amount, date or frequency of your Direct Debit, we will notify you in advance.</li>
          <li>If an error is made in the payment of your Direct Debit, you are entitled to a full and immediate refund from your bank or building society.</li>
          <li>You can cancel a Direct Debit at any time by contacting your bank or building society. Written confirmation may be required.</li>
        </ul>
        <div class="note">
          Keep this letter safe — you'll need your plan reference <strong>{{policyNumber}}</strong> when contacting us.
        </div>
      </div>
    </div>

    <h2>Important Information</h2>
    <ul>
      <li>This Protection Plan is a <strong>service agreement</strong> and is not an insurance policy.</li>
      <li>All services are provided subject to the plan <strong>terms, conditions and exclusions</strong>.</li>
      <li><strong>Annual boiler service:</strong> Please contact us to book your annual boiler service.</li>
    </ul>

  </div>

  <div class="footer">
    <div class="footer-grid">
      <div class="footer-card"><strong>Phone</strong>0330 822 7695</div>
      <div class="footer-card"><strong>Email</strong>info@theflashteam.co.uk</div>
      <div class="footer-card"><strong>Website</strong>theflashteam.co.uk</div>
      <div class="footer-card"><strong>Coverage</strong>Nationwide UK</div>
    </div>
    <div class="small">
      Flash Team — Customer assistance is provided subject to plan terms, conditions and exclusions.
    </div>
  </div>

</div>
</body>
</html>`
    }
  ];
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