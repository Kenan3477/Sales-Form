const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

const PROFESSIONAL_WISEGUYS_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wiseguys Remote Support Tech Plan</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.3;
            color: #2d3748;
            background: white;
            font-size: 12px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }
        
        .document-container {
            width: 100%;
            height: 100%;
            background: white;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 30%, #404040 70%, #3a3a3a 100%);
            color: white;
            padding: 8px 20px;
            position: relative;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 100%;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #7ED321 0%, #9AE456 50%, #7ED321 100%);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .wiseguys-icon {
            width: 28px;
            height: 28px;
            background: linear-gradient(45deg, #7ED321, #9AE456);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: #3a3a3a;
            box-shadow: 0 3px 6px rgba(0,0,0,0.4);
            flex-shrink: 0;
            font-weight: bold;
            border: 2px solid white;
        }
        
        .wiseguys-icon::before {
            content: 'W';
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 16px;
            font-weight: 900;
            letter-spacing: -0.5px;
        }
        
        .logo-text {
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
            color: white;
        }
        
        .tagline {
            font-size: 9px;
            opacity: 0.9;
            margin-top: 1px;
            font-style: italic;
        }
        
        .content {
            padding: 12px 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .main-title {
            font-size: 18px;
            font-weight: 700;
            color: #3a3a3a;
            margin-bottom: 14px;
            border-bottom: 2px solid #7ED321;
            padding-bottom: 8px;
            letter-spacing: -0.25px;
        }
        
        .intro-text {
            font-size: 12px;
            margin-bottom: 14px;
            line-height: 1.5;
        }
        
        .activation-banner {
            background: linear-gradient(135deg, #7ED321 0%, #9AE456 100%);
            color: #3a3a3a;
            padding: 12px 18px;
            margin-bottom: 16px;
            border-radius: 4px;
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            box-shadow: 0 2px 6px rgba(126, 211, 33, 0.2);
            letter-spacing: 0.25px;
        }
        
        .three-column {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 12px;
            margin-bottom: 16px;
            flex: 1;
        }
        
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            background: #fafbfc;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: box-shadow 0.2s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .card-header {
            background: linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 100%);
            color: white;
            padding: 14px 10px;
            font-weight: 600;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .card-content {
            padding: 16px 10px;
            background: white;
            font-size: 10px;
            line-height: 1.4;
            flex: 1;
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
            font-size: 8px;
            letter-spacing: 0.5px;
            width: 45%;
        }
        
        .detail-value {
            font-weight: 600;
            color: #3a3a3a;
            text-align: right;
            flex: 1;
            font-size: 10px;
            word-break: break-word;
            overflow-wrap: break-word;
        }
        
        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 6px;
            margin-bottom: 8px;
            font-size: 10px;
            line-height: 1.4;
        }
        
        .checklist-item:last-child {
            margin-bottom: 3px;
        }
        
        .check-icon {
            width: 10px;
            height: 10px;
            background: linear-gradient(135deg, #7ED321, #9AE456);
            border-radius: 50%;
            position: relative;
            flex-shrink: 0;
            margin-top: 1px;
            box-shadow: 0 1px 2px rgba(126, 211, 33, 0.3);
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
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .compact-list {
            list-style: none;
            font-size: 9px;
            line-height: 1.4;
        }
        
        .compact-list li {
            margin-bottom: 5px;
            padding-left: 10px;
            position: relative;
        }
        
        .compact-list li::before {
            content: '•';
            color: #7ED321;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .numbered-steps {
            font-size: 10px;
            counter-reset: step-counter;
        }
        
        .numbered-steps div {
            margin-bottom: 7px;
            padding-left: 14px;
            position: relative;
            line-height: 1.4;
        }
        
        .numbered-steps div::before {
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            background: linear-gradient(135deg, #3a3a3a, #2d2d2d);
            color: white;
            border-radius: 50%;
            width: 12px;
            height: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 7px;
            font-weight: bold;
        }
        
        .footer {
            padding: 8px 20px;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            font-size: 8px;
            color: #64748b;
            text-align: center;
            margin-top: auto;
        }
        
        .contact-info {
            display: flex;
            justify-content: space-around;
            align-items: center;
            gap: 20px;
        }
        
        .contact-item {
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 500;
        }
        
        .contact-highlight {
            color: #7ED321;
            font-weight: 600;
        }
        
        @media print {
            body {
                overflow: visible;
                height: auto;
            }
            
            .document-container {
                min-height: auto;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <div class="header">
            <div class="logo-section">
                <div class="wiseguys-icon"></div>
                <div>
                    <div class="logo-text">WISEGUYS</div>
                    <div class="tagline">Remote Support Tech Plan</div>
                </div>
            </div>
        </div>
        
        <div class="content">
            <h1 class="main-title">REMOTE SUPPORT TECH PLAN ACTIVATION</h1>
            
            <p class="intro-text">
                Welcome to Wiseguys Remote Support! Your comprehensive tech plan provides 24/7 remote assistance, 
                device monitoring, and priority support for all your technology needs.
            </p>
            
            <div class="activation-banner">
                🎉 PLAN ACTIVATED FOR {{customerName}} - Welcome to Premium Support!
            </div>
            
            <div class="three-column">
                <div class="card">
                    <div class="card-header">Customer Information</div>
                    <div class="card-content">
                        <div class="detail-row">
                            <span class="detail-label">Name:</span>
                            <span class="detail-value">{{customerName}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Address:</span>
                            <span class="detail-value">{{customerAddress}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Plan Type:</span>
                            <span class="detail-value">{{planType}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Monthly Cost:</span>
                            <span class="detail-value">£{{monthlyPrice}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Plan ID:</span>
                            <span class="detail-value">{{planId}}</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">Plan Features</div>
                    <div class="card-content">
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>24/7 Remote Desktop Support</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Virus & Malware Protection</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>System Optimization</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Software Installation Help</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Priority Phone Support</span>
                        </div>
                        <div class="checklist-item">
                            <div class="check-icon"></div>
                            <span>Monthly System Health Check</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">Getting Started</div>
                    <div class="card-content">
                        <div class="numbered-steps">
                            <div>Download TeamViewer from our secure portal</div>
                            <div>Install with your unique customer ID: {{customerId}}</div>
                            <div>Test connection with our support team</div>
                            <div>Bookmark our support portal</div>
                            <div>Save our priority support number</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="two-column-bottom">
                <div class="card">
                    <div class="card-header">Support Channels</div>
                    <div class="card-content">
                        <ul class="compact-list">
                            <li><strong>Priority Phone:</strong> 01202 806060 (Ext. 2)</li>
                            <li><strong>Remote Portal:</strong> support.wiseguys.co.uk</li>
                            <li><strong>Email:</strong> techplan@wiseguys.co.uk</li>
                            <li><strong>Live Chat:</strong> Available 9AM-9PM</li>
                            <li><strong>Emergency:</strong> 24/7 Remote Access</li>
                        </ul>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">Plan Benefits</div>
                    <div class="card-content">
                        <ul class="compact-list">
                            <li>Unlimited remote support sessions</li>
                            <li>Free software troubleshooting</li>
                            <li>Proactive system monitoring</li>
                            <li>Priority booking for on-site visits</li>
                            <li>Monthly performance reports</li>
                            <li>Device backup assistance</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="contact-info">
                <div class="contact-item">
                    📱 <span class="contact-highlight">01202 806060</span>
                </div>
                <div class="contact-item">
                    ✉️ <span class="contact-highlight">techplan@wiseguys.co.uk</span>
                </div>
                <div class="contact-item">
                    🌐 <span class="contact-highlight">wiseguys.co.uk/support</span>
                </div>
                <div class="contact-item">
                    📍 <span class="contact-highlight">Bournemouth, UK</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>`;

async function updateProfessionalTemplate() {
    try {
        console.log('🔄 Updating Wiseguys template with professional design...');

        // Check if we have any admin users
        const adminUser = await prisma.user.findFirst({
            where: { role: 'ADMIN' },
        });

        if (!adminUser) {
            console.log('❌ No admin user found. Please create an admin user first.');
            return;
        }

        // Update the existing template or create new one
        const template = await prisma.documentTemplate.upsert({
            where: {
                templateType_version: {
                    templateType: 'wiseguys-tech-plan',
                    version: 1
                }
            },
            update: {
                name: 'Wiseguys Remote Support Tech Plan - Professional',
                htmlContent: PROFESSIONAL_WISEGUYS_TEMPLATE,
                updatedAt: new Date()
            },
            create: {
                templateType: 'wiseguys-tech-plan',
                name: 'Wiseguys Remote Support Tech Plan - Professional',
                description: 'Professional Wiseguys remote support tech plan documentation with modular design',
                htmlContent: PROFESSIONAL_WISEGUYS_TEMPLATE,
                isActive: true,
                version: 1,
                createdById: adminUser.id
            }
        });

        console.log('✅ Professional Wiseguys template updated successfully!');
        console.log('📋 Template Details:');
        console.log(`   - ID: ${template.id}`);
        console.log(`   - Type: ${template.templateType}`);
        console.log(`   - Name: ${template.name}`);
        console.log('');
        console.log('🎨 Design Features:');
        console.log('   ✅ White background (as requested)');
        console.log('   ✅ Professional modular design');
        console.log('   ✅ Wiseguys charcoal + lime green branding');
        console.log('   ✅ Customer info placeholders ({{customerName}}, {{customerAddress}})');
        console.log('   ✅ Plan pricing placeholder ({{monthlyPrice}})');
        console.log('   ✅ Remote support tech plan focus');
        console.log('   ✅ Enterprise-level styling matching Flash Team quality');
        
    } catch (error) {
        console.error('❌ Error updating template:', error);
        throw error;
    } finally {
        await prisma.$disconnect();
    }
}

updateProfessionalTemplate();