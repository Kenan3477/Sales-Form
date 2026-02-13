const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function updateCoverageTemplate() {
  try {
    console.log('Updating Coverage Continuation Notice with Flash Team branding...')
    
    const professionalTemplate = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Continuation Notice - The Flash Team</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.5;
            color: #333;
            background: #f8f9fa;
            padding: 20px;
        }
        
        .document-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid #e0e0e0;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6500 0%, #ff8500 50%, #ffb000 100%);
            color: white;
            padding: 30px 40px;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }
        
        @keyframes shimmer {
            0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
            50% { transform: translate(-50%, -50%) rotate(180deg); }
        }
        
        .company-name {
            font-size: 32px;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 2;
        }
        
        .tagline {
            font-size: 16px;
            opacity: 0.95;
            margin-top: 5px;
            font-style: italic;
            letter-spacing: 0.8px;
            position: relative;
            z-index: 2;
        }
        
        .content {
            padding: 40px;
        }
        
        .notice-banner {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 25px;
            margin-bottom: 30px;
            border-radius: 10px;
            text-align: center;
            position: relative;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }
        
        .notice-banner::before {
            content: '🛡️';
            position: absolute;
            top: 50%;
            left: 20px;
            transform: translateY(-50%);
            font-size: 24px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: translateY(-50%) scale(1); }
            50% { transform: translateY(-50%) scale(1.1); }
        }
        
        .notice-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .notice-subtitle {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .main-title {
            font-size: 28px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 25px;
            border-bottom: 3px solid #ff6500;
            padding-bottom: 10px;
            position: relative;
        }
        
        .main-title::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 50px;
            height: 3px;
            background: #ff8500;
        }
        
        .customer-details {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 5px solid #ff6500;
        }
        
        .customer-name {
            font-size: 20px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 8px;
        }
        
        .customer-info {
            font-size: 14px;
            color: #666;
            line-height: 1.4;
        }
        
        .intro-text {
            font-size: 16px;
            margin-bottom: 25px;
            line-height: 1.6;
            color: #444;
        }
        
        .status-box {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
            position: relative;
        }
        
        .status-box::before {
            content: 'ℹ️';
            position: absolute;
            top: 15px;
            left: 15px;
            font-size: 20px;
        }
        
        .status-title {
            font-size: 18px;
            font-weight: bold;
            color: #856404;
            margin-bottom: 15px;
            margin-left: 35px;
        }
        
        .status-list {
            list-style: none;
            margin-left: 35px;
        }
        
        .status-list li {
            padding: 5px 0;
            position: relative;
            padding-left: 30px;
        }
        
        .status-list li::before {
            content: '✅';
            position: absolute;
            left: 0;
            top: 5px;
        }
        
        .next-steps {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border: 2px solid #2196f3;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
        }
        
        .next-steps-title {
            font-size: 20px;
            font-weight: bold;
            color: #1565c0;
            margin-bottom: 15px;
        }
        
        .timeline-info {
            background: #fff;
            border: 2px solid #ff6500;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }
        
        .timeline-highlight {
            font-size: 18px;
            font-weight: bold;
            color: #ff6500;
            margin-bottom: 10px;
        }
        
        .payment-section {
            background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
            border: 2px solid #9c27b0;
            border-radius: 10px;
            padding: 25px;
            margin: 25px 0;
        }
        
        .payment-title {
            font-size: 18px;
            font-weight: bold;
            color: #6a1b9a;
            margin-bottom: 15px;
        }
        
        .contact-section {
            background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
            border: 2px solid #ff6500;
            border-radius: 10px;
            padding: 25px;
            margin: 30px 0;
            text-align: center;
        }
        
        .contact-title {
            font-size: 20px;
            font-weight: bold;
            color: #1a365d;
            margin-bottom: 15px;
        }
        
        .contact-info {
            font-size: 16px;
            line-height: 1.6;
        }
        
        .highlight {
            background: linear-gradient(135deg, #ff6500, #ff8500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: bold;
        }
        
        .footer {
            background: #1a365d;
            color: white;
            padding: 25px 40px;
            text-align: center;
        }
        
        .footer-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .footer-text {
            font-size: 14px;
            opacity: 0.8;
            line-height: 1.5;
        }
        
        @media print {
            body { 
                background: white; 
                padding: 0; 
            }
            .document-container {
                box-shadow: none;
                border: none;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <!-- Header -->
        <div class="header">
            <div class="company-name">The Flash Team</div>
            <div class="tagline">Your Trusted Home Protection Partner</div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Status Banner -->
            <div class="notice-banner">
                <div class="notice-title">🛡️ You Are Still Fully Protected 🛡️</div>
                <div class="notice-subtitle">Your home protection plan remains active and will continue as normal</div>
            </div>
            
            <h1 class="main-title">Important: Your Coverage Continues</h1>
            
            <!-- Customer Details -->
            <div class="customer-details">
                <div class="customer-name">Dear {{customerFirstName}} {{customerLastName}},</div>
                <div class="customer-info">
                    Policy Number: <strong>{{policyNumber}}</strong><br>
                    Address: {{address}}<br>
                    Date: {{currentDate}}
                </div>
            </div>
            
            <div class="intro-text">
                We hope this letter finds you well. We are writing to inform you that despite our recent attempts to contact you, 
                <span class="highlight">your home protection plan remains fully active and in effect</span>.
            </div>
            
            <!-- Status Information -->
            <div class="status-box">
                <div class="status-title">Important Information:</div>
                <ul class="status-list">
                    <li><strong>Your coverage is still fully active</strong></li>
                    <li><strong>No interruption to your protection</strong></li>
                    <li><strong>All terms remain the same</strong></li>
                </ul>
            </div>
            
            <!-- Next Steps -->
            <div class="next-steps">
                <div class="next-steps-title">What Happens Next?</div>
                <div class="timeline-info">
                    <div class="timeline-highlight">Your plan will continue as normal and will be starting within the next 7-14 working days</div>
                    <p>You don't need to take any action - everything will proceed automatically.</p>
                </div>
            </div>
            
            <!-- Payment Information -->
            <div class="payment-section">
                <div class="payment-title">💳 Payment Processing</div>
                <p><strong>Monthly Cost:</strong> £{{monthlyCost}}</p>
                <p>Your payments will continue to be processed by <strong>Warmcare</strong> as previously arranged. No changes to your payment schedule.</p>
            </div>
            
            <!-- Coverage Details -->
            {{#if hasApplianceCover}}
            <div style="background: #e8f5e8; border-left: 4px solid #28a745; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #155724; margin-bottom: 10px;">✅ Appliance Cover Included</h3>
                <p style="color: #155724;">Your appliances are fully protected under this plan.</p>
            </div>
            {{/if}}
            
            {{#if hasBoilerCover}}
            <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #e65100; margin-bottom: 10px;">🔥 Boiler Cover Included</h3>
                <p style="color: #e65100;">Your boiler is protected with full coverage and annual service.</p>
            </div>
            {{/if}}
            
            <!-- Contact Information -->
            <div class="contact-section">
                <div class="contact-title">Need to Contact Us?</div>
                <div class="contact-info">
                    <strong>The Flash Team Customer Service</strong><br>
                    📞 Phone: 0800 123 4567<br>
                    ✉️ Email: hello@theflashteam.co.uk<br>
                    🕒 Hours: Monday - Friday, 9:00 AM - 6:00 PM
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-title">The Flash Team - Home Protection Specialists</div>
            <div class="footer-text">
                Protecting your home and giving you peace of mind since 2020.<br>
                This document was generated on {{currentDate}} for policy {{policyNumber}}.
            </div>
        </div>
    </div>
</body>
</html>`;

    const result = await prisma.documentTemplate.update({
      where: {
        id: 'cml6e85p70005tsey7avbhm90'
      },
      data: {
        htmlContent: professionalTemplate,
        description: 'Professional branded notice for customers who haven\'t been contacted - confirms coverage continues with Flash Team branding',
        updatedAt: new Date()
      }
    });

    console.log('✅ Coverage Continuation Notice updated with professional Flash Team branding!');
    console.log('- Added Flash Team header with gradient branding');
    console.log('- Included professional styling and animations');  
    console.log('- Added status boxes, payment info, and contact details');
    console.log('- Matches the quality and branding of other Flash Team documents');

  } catch (error) {
    console.error('❌ Error updating template:', error);
  } finally {
    await prisma.$disconnect();
  }
}

updateCoverageTemplate();