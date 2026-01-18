// Self-contained type definitions
type TemplateType = 'welcome-letter' | 'service-agreement' | 'direct-debit-form' | 'coverage-summary';

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
          <p><strong>Monthly Payment:</strong> £{{monthlyCost}}</p>
          {{#if appliancesCount}}<p><strong>Appliances Covered:</strong> {{appliancesCount}}</p>{{/if}}

          <ul>
            <li>Access to qualified engineers for covered appliance breakdowns</li>
            <li>Access to qualified engineers for covered boiler and central heating breakdowns</li>
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

    {{#if appliances.length}}
    <h2>Covered Appliances</h2>
    <div class="card">
      <div class="card-header">Your Appliance Cover Details</div>
      {{#each appliances}}
      <div class="row">
        <div class="label">{{name}}</div>
        <div class="value">Up to {{coverLimit}} cover - {{monthlyCost}}/month</div>
      </div>
      {{/each}}
      {{#if boilerCost}}
      <div class="row">
        <div class="label">Boiler & Central Heating</div>
        <div class="value">Full system cover - {{boilerCost}}/month</div>
      </div>
      {{/if}}
    </div>
    {{/if}}

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
    
    // First process {{#each}} blocks (they may contain conditionals)
    html = this.processEachBlocks(html, data);
    
    // Then process remaining {{#if}} conditionals
    html = this.processConditionals(html, data);
    
    // Finally replace simple variables
    html = this.replaceVariables(html, data);
    
    return html;
  }

  /**
   * Replace simple variables in template
   */
  private replaceVariables(html: string, data: any): string {
    return html.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
      const cleanKey = key.trim();
      const value = this.getNestedValue(data, cleanKey);
      return value !== undefined ? String(value) : match;
    });
  }

  /**
   * Process {{#each}} blocks separately 
   */
  private processEachBlocks(html: string, data: any): string {
    return html.replace(/\{\{#each ([^}]+)\}\}([\s\S]*?)\{\{\/each\}\}/g, 
      (match, arrayName, blockContent) => {
        const arrayValue = this.getNestedValue(data, arrayName.trim());
        if (Array.isArray(arrayValue)) {
          return arrayValue.map((item, index) => {
            let itemHtml = blockContent;
            
            // First, process any nested conditionals within the each block
            itemHtml = itemHtml.replace(/\{\{#if ([^}]+)\}\}([\s\S]*?)(?:\{\{else\}\}([\s\S]*?))?\{\{\/if\}\}/g, 
              (nestedMatch: string, nestedCondition: string, nestedIfContent: string, nestedElseContent = '') => {
                const cleanCondition = nestedCondition.trim();
                let conditionValue;
                
                // Handle parent context references like ../boilerCost
                if (cleanCondition.startsWith('../')) {
                  const parentKey = cleanCondition.substring(3);
                  conditionValue = this.getNestedValue(data, parentKey);
                } else {
                  conditionValue = this.getNestedValue(item, cleanCondition);
                }
                
                return conditionValue ? nestedIfContent : nestedElseContent;
              }
            );
            
            // Then replace variables
            itemHtml = itemHtml.replace(/\{\{([^}]+)\}\}/g, (varMatch: string, varKey: string) => {
              const cleanKey = varKey.trim();
              
              // Handle parent context references like ../boilerCost
              if (cleanKey.startsWith('../')) {
                const parentKey = cleanKey.substring(3);
                const parentValue = this.getNestedValue(data, parentKey);
                return parentValue !== undefined ? String(parentValue) : varMatch;
              }
              
              // Handle current item properties
              const value = this.getNestedValue(item, cleanKey);
              return value !== undefined ? String(value) : varMatch;
            });
            
            return itemHtml;
          }).join('');
        }
        return '';
      }
    );
  }

  /**
   * Get nested value from object using dot notation
   */
  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current && current[key], obj);
  }

  /**
   * Process conditional blocks in template
   */
  private processConditionals(html: string, data: any): string {
    let processedHtml = html;
    let attempts = 0;
    const maxAttempts = 20;
    
    while (attempts < maxAttempts) {
      const initialHtml = processedHtml;
      
      // Count conditionals before processing
      const conditionalsBefore = (processedHtml.match(/\{\{#if/g) || []).length;
      if (conditionalsBefore === 0) {
        break;
      }
      
      // Process one conditional at a time, starting with the innermost ones
      // Look for conditionals that don't contain other conditionals
      const simpleConditionalRegex = /\{\{#if ([^}]+)\}\}([^{]*(?:\{(?!#if)[^}]*\}[^{]*)*)\{\{\/if\}\}/;
      const match = processedHtml.match(simpleConditionalRegex);
      
      if (match) {
        const [fullMatch, condition, content] = match;
        const conditionValue = this.getNestedValue(data, condition.trim());
        const result = conditionValue ? content : '';
        processedHtml = processedHtml.replace(fullMatch, result);
      } else {
        // Fallback: process any conditional using non-greedy matching
        const fallbackProcessed = processedHtml.replace(/\{\{#if ([^}]+)\}\}([\s\S]*?)\{\{\/if\}\}/, 
          (match, condition, content) => {
            const conditionValue = this.getNestedValue(data, condition.trim());
            return conditionValue ? content : '';
          }
        );
        
        if (fallbackProcessed !== processedHtml) {
          processedHtml = fallbackProcessed;
        } else {
          break;
        }
      }
      
      attempts++;
      
      if (processedHtml === initialHtml) {
        break;
      }
    }
    
    return processedHtml;
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
      policyNumber: 'TFT0123', // Updated format
      totalCost: '455.52', // Annual cost
      monthlyCost: '37.96', // Monthly cost
      hasApplianceCover: true,
      hasBoilerCover: true,
      appliances: [
        {
          name: 'Washing Machine',
          coverLimit: '£500.00',
          monthlyCost: '£8.50'
        },
        {
          name: 'Dishwasher',
          coverLimit: '£400.00',
          monthlyCost: '£5.46'
        }
      ],
      boilerCost: '£24.99', // This is the key field for testing
      currentDate: new Date().toLocaleDateString('en-GB', { 
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    };

    return this.generateDocument(templateId, sampleData);
  }

  /**
   * Get default template content for a given type
   */
  getDefaultTemplate(templateType: string): string {
    const template = EnhancedTemplateService.templates.find(t => t.id === 'welcome-letter');
    return template ? template.html : '';
  }

  /**
   * Render template with given content and data
   */
  renderTemplate(content: string, data: any): string {
    let html = content;
    
    // Replace conditional blocks
    html = this.processConditionals(html, data);
    
    // Replace variables
    html = html.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
      const cleanKey = key.trim();
      const value = this.getNestedValue(data, cleanKey);
      return value !== undefined ? String(value) : match;
    });
    
    return html;
  }
}