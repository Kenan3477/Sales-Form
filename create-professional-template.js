const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function createProfessionalTemplate() {
  try {
    console.log('Creating truly professional Coverage Continuation Notice...')
    
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
            font-family: 'Arial', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: #ffffff;
            font-size: 14px;
        }
        
        .document-container {
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            min-height: 297mm;
            position: relative;
        }
        
        .letterhead {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #3182ce 100%);
            padding: 40px;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .letterhead::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(50%, -50%);
        }
        
        .company-header {
            position: relative;
            z-index: 2;
        }
        
        .company-name {
            font-size: 36px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }
        
        .company-tagline {
            font-size: 16px;
            opacity: 0.9;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        .document-header {
            padding: 40px;
            border-bottom: 3px solid #e2e8f0;
        }
        
        .document-title {
            font-size: 24px;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .document-subtitle {
            font-size: 16px;
            color: #4a5568;
            font-weight: 400;
        }
        
        .content {
            padding: 40px;
        }
        
        .notice-alert {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
        }
        
        .alert-icon {
            font-size: 48px;
            margin-bottom: 15px;
            display: block;
        }
        
        .alert-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .alert-text {
            font-size: 16px;
            font-weight: 400;
            opacity: 0.95;
        }
        
        .customer-info-section {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .customer-greeting {
            font-size: 18px;
            font-weight: 600;
            color: #1a365d;
            margin-bottom: 20px;
        }
        
        .policy-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .detail-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }
        
        .detail-label {
            font-size: 12px;
            font-weight: 600;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-size: 14px;
            font-weight: 600;
            color: #1a365d;
        }
        
        .main-content {
            margin: 30px 0;
        }
        
        .content-paragraph {
            font-size: 15px;
            line-height: 1.8;
            color: #4a5568;
            margin-bottom: 25px;
            text-align: justify;
        }
        
        .status-confirmation {
            background: #fff5f5;
            border-left: 6px solid #e53e3e;
            padding: 25px;
            margin: 30px 0;
            border-radius: 0 8px 8px 0;
        }
        
        .status-title {
            font-size: 18px;
            font-weight: 700;
            color: #c53030;
            margin-bottom: 15px;
            text-transform: uppercase;
        }
        
        .status-grid {
            display: grid;
            gap: 15px;
        }
        
        .status-item {
            display: flex;
            align-items: center;
            font-size: 15px;
            color: #2d3748;
        }
        
        .status-item::before {
            content: '✓';
            background: #48bb78;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-weight: bold;
            font-size: 12px;
        }
        
        .timeline-section {
            background: #ebf8ff;
            border: 2px solid #3182ce;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .timeline-title {
            font-size: 20px;
            font-weight: 700;
            color: #2c5282;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        
        .timeline-title::before {
            content: '📅';
            margin-right: 10px;
            font-size: 24px;
        }
        
        .timeline-content {
            background: white;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid #bee3f8;
        }
        
        .timeline-highlight {
            font-size: 16px;
            font-weight: 600;
            color: #2c5282;
            margin-bottom: 10px;
        }
        
        .timeline-text {
            font-size: 14px;
            color: #4a5568;
            line-height: 1.6;
        }
        
        .payment-section {
            background: #f0fff4;
            border: 2px solid #48bb78;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .payment-title {
            font-size: 18px;
            font-weight: 700;
            color: #22543d;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        
        .payment-title::before {
            content: '💳';
            margin-right: 10px;
            font-size: 20px;
        }
        
        .payment-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .payment-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #c6f6d5;
        }
        
        .coverage-summary {
            background: #fffaf0;
            border: 2px solid #ed8936;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .coverage-title {
            font-size: 18px;
            font-weight: 700;
            color: #c05621;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        
        .coverage-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .coverage-item {
            background: white;
            padding: 20px;
            border-radius: 6px;
            border: 1px solid #fbd38d;
            text-align: center;
        }
        
        .coverage-icon {
            font-size: 36px;
            margin-bottom: 10px;
            display: block;
        }
        
        .coverage-name {
            font-size: 16px;
            font-weight: 600;
            color: #c05621;
            margin-bottom: 5px;
        }
        
        .coverage-status {
            font-size: 14px;
            color: #48bb78;
            font-weight: 600;
        }
        
        .contact-section {
            background: #1a365d;
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin: 40px 0;
            text-align: center;
        }
        
        .contact-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .contact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }
        
        .contact-item {
            text-align: center;
        }
        
        .contact-icon {
            font-size: 32px;
            margin-bottom: 10px;
            display: block;
        }
        
        .contact-label {
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .contact-value {
            font-size: 16px;
            font-weight: 600;
        }
        
        .footer {
            background: #2d3748;
            color: #a0aec0;
            padding: 30px 40px;
            text-align: center;
            margin-top: 50px;
        }
        
        .footer-content {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .footer-title {
            font-size: 18px;
            font-weight: 600;
            color: white;
            margin-bottom: 15px;
        }
        
        .footer-text {
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .document-ref {
            font-size: 11px;
            opacity: 0.7;
            font-family: 'Courier New', monospace;
        }
        
        @media print {
            body { 
                background: white;
                font-size: 12px;
            }
            .document-container {
                max-width: none;
                box-shadow: none;
                margin: 0;
                padding: 0;
            }
            .letterhead {
                background: #1a365d !important;
                -webkit-print-color-adjust: exact;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <!-- Professional Letterhead -->
        <div class="letterhead">
            <div class="company-header">
                <div class="company-name">THE FLASH TEAM</div>
                <div class="company-tagline">Professional Home Protection Services</div>
            </div>
        </div>
        
        <!-- Document Header -->
        <div class="document-header">
            <div class="document-title">Coverage Continuation Notice</div>
            <div class="document-subtitle">Important Information Regarding Your Home Protection Plan</div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <!-- Status Alert -->
            <div class="notice-alert">
                <span class="alert-icon">🛡️</span>
                <div class="alert-title">Your Protection Remains Active</div>
                <div class="alert-text">Your home protection plan continues without interruption</div>
            </div>
            
            <!-- Customer Information -->
            <div class="customer-info-section">
                <div class="customer-greeting">Dear {{customerFirstName}} {{customerLastName}},</div>
                
                <div class="policy-details">
                    <div class="detail-item">
                        <div class="detail-label">Policy Number</div>
                        <div class="detail-value">{{policyNumber}}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Issue Date</div>
                        <div class="detail-value">{{currentDate}}</div>
                    </div>
                </div>
                
                <div class="detail-item">
                    <div class="detail-label">Property Address</div>
                    <div class="detail-value">{{address}}</div>
                </div>
            </div>
            
            <!-- Main Message -->
            <div class="main-content">
                <p class="content-paragraph">
                    We are writing to provide you with important information regarding your home protection plan. 
                    Despite our recent attempts to establish contact, we want to assure you that <strong>your coverage 
                    remains fully active and effective</strong>.
                </p>
                
                <p class="content-paragraph">
                    Your home protection plan has been carefully designed to provide comprehensive coverage for your 
                    property, and we are committed to maintaining this protection without interruption. No action 
                    is required on your part at this time.
                </p>
            </div>
            
            <!-- Status Confirmation -->
            <div class="status-confirmation">
                <div class="status-title">Coverage Status Confirmation</div>
                <div class="status-grid">
                    <div class="status-item">Your protection plan remains fully active and operational</div>
                    <div class="status-item">All coverage terms and conditions continue as originally agreed</div>
                    <div class="status-item">No interruption to your home protection services</div>
                    <div class="status-item">All emergency response procedures remain in effect</div>
                </div>
            </div>
            
            <!-- Timeline Information -->
            <div class="timeline-section">
                <div class="timeline-title">Implementation Timeline</div>
                <div class="timeline-content">
                    <div class="timeline-highlight">Service Commencement: 7-14 Working Days</div>
                    <div class="timeline-text">
                        Your home protection services will commence within the next 7-14 working days. 
                        All systems and processes will be automatically activated without requiring any 
                        intervention from you.
                    </div>
                </div>
            </div>
            
            <!-- Payment Information -->
            <div class="payment-section">
                <div class="payment-title">Payment Processing</div>
                <div class="payment-details">
                    <div class="payment-item">
                        <div class="detail-label">Monthly Premium</div>
                        <div class="detail-value">£{{monthlyCost}}</div>
                    </div>
                    <div class="payment-item">
                        <div class="detail-label">Payment Processor</div>
                        <div class="detail-value">Warmcare Ltd</div>
                    </div>
                </div>
                <div class="timeline-text">
                    Your monthly premiums will continue to be processed by Warmcare Ltd as previously 
                    arranged. No changes to your existing payment schedule or method are required.
                </div>
            </div>
            
            <!-- Coverage Summary -->
            <div class="coverage-summary">
                <div class="coverage-title">Your Protection Portfolio</div>
                <div class="coverage-grid">
                    <div class="coverage-item">
                        <span class="coverage-icon">🏠</span>
                        <div class="coverage-name">Appliance Protection</div>
                        <div class="coverage-status">✓ Active</div>
                    </div>
                    <div class="coverage-item">
                        <span class="coverage-icon">🔥</span>
                        <div class="coverage-name">Boiler Coverage</div>
                        <div class="coverage-status">✓ Active</div>
                    </div>
                </div>
            </div>
            
            <!-- Contact Information -->
            <div class="contact-section">
                <div class="contact-title">Customer Service</div>
                <div class="contact-grid">
                    <div class="contact-item">
                        <span class="contact-icon">📞</span>
                        <div class="contact-label">Telephone</div>
                        <div class="contact-value">0800 123 4567</div>
                    </div>
                    <div class="contact-item">
                        <span class="contact-icon">✉️</span>
                        <div class="contact-label">Email</div>
                        <div class="contact-value">hello@theflashteam.co.uk</div>
                    </div>
                    <div class="contact-item">
                        <span class="contact-icon">🕒</span>
                        <div class="contact-label">Hours</div>
                        <div class="contact-value">Monday - Friday<br>9:00 AM - 6:00 PM</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Professional Footer -->
        <div class="footer">
            <div class="footer-content">
                <div class="footer-title">The Flash Team Ltd</div>
                <div class="footer-text">
                    Professional Home Protection Services | Established 2020<br>
                    Registered in England and Wales | Company No. 12345678
                </div>
                <div class="document-ref">
                    Document Reference: CC-{{policyNumber}}-{{currentDate}} | Generated: {{currentDate}}
                </div>
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
        htmlContent: professionalTemplate,
        description: 'Professional corporate-grade coverage continuation notice with Flash Team branding',
        updatedAt: new Date()
      }
    });

    console.log('✅ Created truly professional Coverage Continuation Notice!');
    console.log('- Corporate letterhead with professional branding');
    console.log('- Structured layout with proper typography');  
    console.log('- Professional color scheme and spacing');
    console.log('- Corporate-grade content and messaging');
    console.log('- Matches the quality of official business documents');

  } catch (error) {
    console.error('❌ Error updating template:', error);
  } finally {
    await prisma.$disconnect();
  }
}

createProfessionalTemplate();