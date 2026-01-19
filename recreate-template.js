const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function deleteAndRecreateTemplate() {
  try {
    console.log('🗑️ Deleting all generated documents first...');
    
    // Delete all generated documents first to avoid foreign key constraints
    await prisma.generatedDocument.deleteMany({});
    
    console.log('✅ All generated documents deleted');
    
    console.log('🗑️ Deleting all existing templates...');
    
    // Delete all existing document templates
    await prisma.documentTemplate.deleteMany({});
    
    console.log('✅ All templates deleted successfully');
    
    // Get a real user ID for the template
    const firstUser = await prisma.user.findFirst();
    if (!firstUser) {
      throw new Error('No users found in database');
    }
    
    console.log('📝 Creating new template with exact ChatGPT match...');
    
    const EXACT_CHATGPT_TEMPLATE = `<!DOCTYPE html>
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
            background: white;
        }
        
        .document-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 20%, #3b82f6 40%, #1e40af 80%, #1e3a8a 100%);
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(255,255,255,0.2) 1px, transparent 1px),
                radial-gradient(circle at 75% 75%, rgba(255,255,255,0.15) 1px, transparent 1px),
                radial-gradient(circle at 50% 50%, rgba(255,255,255,0.1) 2px, transparent 2px),
                linear-gradient(45deg, rgba(255,255,255,0.05) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.05) 75%),
                linear-gradient(-45deg, rgba(255,255,255,0.05) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.05) 75%);
            background-size: 60px 60px, 40px 40px, 100px 100px, 30px 30px, 30px 30px;
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
            height: 10px;
            background: linear-gradient(90deg, #ff4500 0%, #ff6500 50%, #ff4500 100%);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .lightning-icon {
            width: 35px;
            height: 35px;
            background: linear-gradient(45deg, #ff6500, #ffa500);
            clip-path: polygon(25% 0%, 75% 0%, 50% 45%, 85% 45%, 50% 100%, 15% 55%, 50% 55%);
            box-shadow: 0 0 15px rgba(255,101,0,0.5);
        }
        
        .logo-text {
            font-size: 38px;
            font-weight: bold;
            letter-spacing: 2px;
        }
        
        .tagline {
            font-size: 14px;
            opacity: 0.95;
            margin-top: 3px;
            font-style: italic;
            letter-spacing: 0.5px;
        }
        
        .content {
            padding: 40px;
        }
        
        .main-title {
            font-size: 32px;
            font-weight: bold;
            color: #1e3a8a;
            margin-bottom: 25px;
        }
        
        .intro-text {
            font-size: 16px;
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
            width: 22px;
            height: 22px;
            background: white;
            clip-path: polygon(25% 0%, 75% 0%, 50% 45%, 85% 45%, 50% 100%, 15% 55%, 50% 55%);
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        .activation-text {
            font-size: 20px;
            font-weight: bold;
            position: relative;
            z-index: 1;
        }
        
        .activation-subtext {
            background: #1e3a8a;
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
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            overflow: hidden;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .card-header {
            background: #1e3a8a;
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
            border-bottom: 1px solid #f3f4f6;
        }
        
        .detail-row:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
            width: 40%;
        }
        
        .detail-value {
            font-weight: bold;
            color: #1e3a8a;
            text-align: right;
            width: 55%;
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
            background: #1e3a8a;
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
            color: #1e3a8a;
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
        }
        
        .guarantee-list li::before {
            content: counter(item-counter);
            counter-increment: item-counter;
            position: absolute;
            left: 0;
            background: #1e3a8a;
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
            font-size: 20px;
            font-weight: bold;
            color: #1e3a8a;
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
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
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
                <strong>Dear {{customerName}},</strong><br><br>
                Thank you for choosing Flash Team. This document confirms that your Protection Plan is now active, subject to the plan terms, conditions and exclusions.
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
                            <span class="detail-value">{{customerName}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">EMAIL</span>
                            <span class="detail-value">{{email}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">PHONE</span>
                            <span class="detail-value">{{phoneNumber}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">ADDRESS</span>
                            <span class="detail-value">{{address}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">START DATE</span>
                            <span class="detail-value">{{coverageStartDate}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">POLICY REF</span>
                            <span class="detail-value">{{policyNumber}}</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">What Your Plan Provides</div>
                    <div class="card-content">
                        {{#if monthlyCost}}
                        <div class="detail-row" style="border-bottom: 2px solid #ff6500; margin-bottom: 15px; padding-bottom: 15px;">
                            <span class="detail-label">Monthly Payment:</span>
                            <span class="detail-value">£{{monthlyCost}}</span>
                        </div>
                        {{/if}}
                        
                        {{#if hasApplianceCover}}
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Access to qualified engineers for covered appliance breakdowns</span>
                        </div>
                        {{/if}}
                        
                        {{#if hasBoilerCover}}
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Access to qualified engineers for covered boiler and central heating breakdowns</span>
                        </div>
                        {{/if}}
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Repairs to covered appliances or systems, where repair is possible</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>If a repair is not economically viable, we may, at our discretion, offer a replacement of equivalent specification</span>
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
                            <span>Quote your policy reference {{policyNumber}}</span>
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
                        <li>Quote your policy reference {{policyNumber}}</li>
                        <li>Describe the issue so we can assess eligibility</li>
                        <li>You may cancel your Direct Debit at any time via your bank or building society</li>
                    </ul>
                </div>
            </div>
            
            <div class="important-section">
                <div class="important-title">Important Information</div>
                <ul class="important-list">
                    <li>This Protection Plan is a <strong>service agreement</strong> and is not an insurance policy</li>
                    <li>All services are provided subject to <strong>plan terms, conditions and exclusions</strong></li>
                    <li><strong>Annual boiler service:</strong> Please contact us to book your annual boiler service</li>
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
</html>`;

    // Create new template
    const newTemplate = await prisma.documentTemplate.create({
      data: {
        name: 'Welcome Letter',
        description: 'Flash Team Protection Plan - Exact ChatGPT Match',
        templateType: 'welcome-letter',
        htmlContent: EXACT_CHATGPT_TEMPLATE,
        isActive: true,
        version: 1,
        createdById: firstUser.id
      }
    });

    console.log('✅ New template created successfully!');
    console.log('Template details:', {
      id: newTemplate.id,
      name: newTemplate.name,
      length: newTemplate.htmlContent.length,
      isActive: newTemplate.isActive,
      templateType: newTemplate.templateType
    });

    return newTemplate;

  } catch (error) {
    console.error('❌ Error recreating template:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

if (require.main === module) {
  deleteAndRecreateTemplate()
    .then(() => {
      console.log('🎉 Template recreation completed successfully!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Failed to recreate template:', error);
      process.exit(1);
    });
}

module.exports = { deleteAndRecreateTemplate };