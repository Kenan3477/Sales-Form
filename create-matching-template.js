const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function createMatchingTemplate() {
  try {
    console.log('Creating Coverage Continuation Notice to match Flash Team Protection Plan exactly...')
    
    const matchingTemplate = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Continuation Notice</title>
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
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
            box-shadow: 0 0 10px rgba(255,101,0,0.4);
        }
        
        .lightning-icon::before {
            content: '⚡';
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
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        .activation-text {
            font-size: 18px;
        }
        .lightning-small::before {
            content: "⚡";
            font-size: 16px;
            color: #3498db;
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
            <h1 class="main-title">Coverage Continuation Notice</h1>
            
            <div class="intro-text">
                <strong>Dear {{customerFirstName}} {{customerLastName}},</strong><br><br>
                We are writing to inform you about your <strong>Protection Plan coverage</strong>. Despite our recent attempts to contact you, your plan remains active and will continue as normal.
            </div>
            
            <div class="activation-banner">
                <div class="activation-text">
                    <span class="lightning-small"></span>
                    Your Protection Plan remains fully active
                </div>
                <div class="activation-subtext">
                    No action is required - your coverage continues automatically
                </div>
            </div>
            
            <div class="two-column">
                <div class="card">
                    <div class="card-header">Your Account Details</div>
                    <div class="card-content">
                        <div class="detail-row">
                            <span class="detail-label">CUSTOMER</span>
                            <span class="detail-value">{{customerFirstName}} {{customerLastName}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">EMAIL</span>
                            <span class="detail-value">{{email}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">PHONE</span>
                            <span class="detail-value">{{phone}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">ADDRESS</span>
                            <span class="detail-value">{{address}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">NOTICE DATE</span>
                            <span class="detail-value">{{currentDate}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">PLAN REF</span>
                            <span class="detail-value">{{policyNumber}}</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">Coverage Status</div>
                    <div class="card-content">
                        <div class="detail-row" style="border-bottom: 2px solid #ff6500; margin-bottom: 15px; padding-bottom: 15px;">
                            <span class="detail-label">Monthly Payment:</span>
                            <span class="detail-value">£{{monthlyCost}}</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Your coverage is still fully active</span>
                        </div>
                        
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>No interruption to your protection</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>All terms remain the same</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Service will commence within 7-14 working days</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Payments processed by Warmcare as before</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card single-column-card">
                <div class="card-header">What Happens Next</div>
                <div class="card-content">
                    <div class="numbered-list">
                        <div class="numbered-item">
                            <span>Your plan will continue automatically</span>
                        </div>
                        <div class="numbered-item">
                            <span>Services will commence within 7-14 working days</span>
                        </div>
                        <div class="numbered-item">
                            <span>Monthly payments continue via Warmcare</span>
                        </div>
                        <div class="numbered-item">
                            <span>Call 0330 822 7695 if you need assistance</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card single-column-card">
                <div class="card-header">Payment Information</div>
                <div class="card-content">
                    <div class="guarantee-intro">
                        Your monthly payments will continue to be processed by Warmcare Ltd.
                    </div>
                    <ul class="guarantee-list">
                        <li>Monthly cost: £{{monthlyCost}} per month</li>
                        <li>Payment processor: Warmcare Ltd (as previously arranged)</li>
                        <li>No changes to your existing payment schedule</li>
                        <li>No action required from you regarding payments</li>
                        <li>Your Direct Debit will continue as normal</li>
                    </ul>
                </div>
            </div>
            
            <div class="important-section">
                <div class="important-title">Important Information</div>
                <ul class="important-list">
                    <li>Your <strong>Protection Plan remains fully active</strong> and will continue without interruption</li>
                    <li>Service commencement is scheduled for <strong>7-14 working days</strong> from this notice</li>
                    <li><strong>No action required:</strong> Everything will proceed automatically</li>
                    <li>For any questions, contact us on <strong>0330 822 7695</strong></li>
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

    await prisma.documentTemplate.update({
      where: {
        id: 'cml6e85p70005tsey7avbhm90'
      },
      data: {
        htmlContent: matchingTemplate,
        description: 'Coverage continuation notice using exact Flash Team protection plan design and branding',
        updatedAt: new Date()
      }
    });

    console.log('✅ Coverage Continuation Notice updated to match Flash Team Protection Plan exactly!');
    console.log('- Uses identical layout, colors, and styling');
    console.log('- Same header design with lightning icon and gradient');  
    console.log('- Identical card structure and typography');
    console.log('- Same activation banner and footer design');
    console.log('- Content adapted for coverage continuation messaging');

  } catch (error) {
    console.error('❌ Error updating template:', error);
  } finally {
    await prisma.$disconnect();
  }
}

createMatchingTemplate();