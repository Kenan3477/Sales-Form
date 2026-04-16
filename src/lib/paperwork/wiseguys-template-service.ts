// Self-contained type definitions
type TemplateType = 'welcome-letter' | 'service-agreement' | 'direct-debit-form' | 'coverage-summary' | string;

/**
 * Wiseguys branded template service for professional welcome letters
 */
export class WiseguysTemplateService {
  private static templates = [
    {
      id: 'wiseguys-welcome-letter',
      name: 'Wiseguys Welcome Letter',
      description: 'Professional welcome letter with Wiseguys Bournemouth branding',
      category: 'Customer Communications',
      html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wiseguys Bournemouth - Welcome Letter</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Roboto:wght@300;400;500;700;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.5;
            color: #ffffff;
            background: #3a3a3a;
            font-size: 14px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .document-container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            background: #3a3a3a;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Header Section with Authentic Wiseguys Branding */
        .header {
            background: linear-gradient(135deg, #4a4a4a 0%, #3a3a3a 50%, #2a2a2a 100%);
            color: white;
            padding: 40px 40px 30px 40px;
            position: relative;
            text-align: center;
            border-bottom: 4px solid #7ED321;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            position: relative;
        }
        
        .wiseguys-logo {
            width: 120px;
            height: 120px;
            background: #3a3a3a;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 3px solid #7ED321;
        }
        
        .logo-w {
            font-size: 72px;
            font-weight: 900;
            color: #7ED321;
            font-family: 'Roboto', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .owl-left {
            position: absolute;
            top: -10px;
            left: -15px;
            width: 45px;
            height: 45px;
            background: #8B4513;
            border-radius: 50% 50% 40% 40%;
            border: 2px solid #7ED321;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2;
        }
        
        .owl-left::before {
            content: '🥽';
            font-size: 16px;
            color: #333;
        }
        
        .owl-right {
            position: absolute;
            top: -10px;
            right: -15px;
            width: 45px;
            height: 45px;
            background: #D2691E;
            border-radius: 50% 50% 40% 40%;
            border: 2px solid #7ED321;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2;
        }
        
        .owl-right::before {
            content: '🔧';
            font-size: 16px;
        }
        
        .company-name {
            font-family: 'Roboto', sans-serif;
            font-size: 48px;
            font-weight: 900;
            color: #7ED321;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 8px;
            letter-spacing: -1px;
            text-transform: uppercase;
        }
        
        .company-tagline {
            font-size: 18px;
            font-weight: 400;
            color: #cccccc;
            margin-bottom: 15px;
            font-style: italic;
        }
        
        .company-location {
            font-size: 16px;
            font-weight: 500;
            color: #7ED321;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        /* Main Content Area */
        .main-content {
            flex: 1;
            padding: 40px;
            background: #3a3a3a;
            color: white;
        }
        
        .welcome-banner {
            background: linear-gradient(135deg, #7ED321 0%, #6BB31A 50%, #5A9916 100%);
            border: 3px solid #7ED321;
            border-radius: 20px;
            padding: 35px;
            margin-bottom: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(126, 211, 33, 0.3);
        }
        
        .welcome-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            z-index: 1;
        }
        
        .welcome-banner > * {
            position: relative;
            z-index: 2;
        }
        
        .welcome-title {
            font-family: 'Roboto', sans-serif;
            font-size: 36px;
            font-weight: 900;
            color: #333333;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            text-transform: uppercase;
        }
        
        .welcome-message {
            font-size: 18px;
            font-weight: 500;
            color: #2a2a2a;
            line-height: 1.6;
        }
        
        .customer-greeting {
            font-size: 24px;
            font-weight: 700;
            color: #7ED321;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .customer-greeting .name {
            color: #ffffff;
            font-weight: 900;
        }
        
        /* Services Section */
        .services-section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-family: 'Roboto', sans-serif;
            font-size: 28px;
            font-weight: 900;
            color: #7ED321;
            margin-bottom: 25px;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
            text-transform: uppercase;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: #7ED321;
            border-radius: 2px;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 35px;
        }
        
        .service-card {
            background: linear-gradient(135deg, #4a4a4a 0%, #3a3a3a 100%);
            border: 2px solid #7ED321;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }
        
        .service-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(126, 211, 33, 0.4);
            border-color: #9FE83A;
        }
        
        .service-icon {
            width: 60px;
            height: 60px;
            margin: 0 auto 20px;
            background: #7ED321;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            color: #333333;
            box-shadow: 0 4px 16px rgba(126, 211, 33, 0.4);
        }
        
        .service-title {
            font-family: 'Roboto', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: #7ED321;
            margin-bottom: 12px;
            text-transform: uppercase;
        }
        
        .service-description {
            font-size: 14px;
            color: #cccccc;
            line-height: 1.5;
        }
        
        /* Quote Section */
        .quote-section {
            background: linear-gradient(135deg, #4a4a4a 0%, #3a3a3a 100%);
            border-left: 6px solid #7ED321;
            border-radius: 0 15px 15px 0;
            padding: 35px;
            margin: 40px 0;
            position: relative;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }
        
        .quote-icon {
            position: absolute;
            top: -15px;
            left: 25px;
            width: 50px;
            height: 50px;
            background: #7ED321;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333333;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .quote-text {
            font-size: 18px;
            font-style: italic;
            color: #ffffff;
            line-height: 1.7;
            margin-bottom: 20px;
            padding-left: 40px;
        }
        
        .quote-author {
            text-align: right;
            font-weight: 600;
            color: #7ED321;
            font-size: 16px;
        }
        
        /* Contact Information */
        .contact-info {
            background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
            color: white;
            padding: 35px;
            border-radius: 20px;
            margin: 40px 0;
            border: 2px solid #7ED321;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        
        .contact-title {
            font-family: 'Roboto', sans-serif;
            font-size: 26px;
            font-weight: 900;
            margin-bottom: 25px;
            text-align: center;
            color: #7ED321;
            text-transform: uppercase;
        }
        
        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
        }
        
        .contact-item {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .contact-icon {
            width: 50px;
            height: 50px;
            background: #7ED321;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333333;
            font-size: 20px;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.4);
        }
        
        .contact-details {
            flex: 1;
        }
        
        .contact-label {
            font-size: 12px;
            color: #cccccc;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .contact-value {
            font-size: 18px;
            font-weight: 700;
            color: #7ED321;
        }
        
        /* Customer Details Panel */
        .customer-details {
            background: linear-gradient(135deg, #4a4a4a 0%, #3a3a3a 100%);
            border: 2px solid #7ED321;
            border-radius: 15px;
            padding: 30px;
            margin: 35px 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }
        
        .customer-details h3 {
            font-family: 'Roboto', sans-serif;
            color: #7ED321;
            margin-bottom: 25px;
            text-align: center;
            font-size: 22px;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #5a5a5a;
        }
        
        .detail-row:last-child {
            border-bottom: none;
        }
        
        .detail-label {
            font-weight: 500;
            color: #cccccc;
            text-transform: uppercase;
            font-size: 13px;
        }
        
        .detail-value {
            font-weight: 600;
            color: #7ED321;
        }
        
        /* What's Next Section */
        .whats-next {
            background: linear-gradient(135deg, #7ED321 0%, #6BB31A 50%, #5A9916 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 35px 0;
            box-shadow: 0 8px 32px rgba(126, 211, 33, 0.3);
        }
        
        .whats-next h3 {
            font-family: 'Roboto', sans-serif;
            color: #333333;
            margin-bottom: 20px;
            text-align: center;
            font-size: 22px;
            font-weight: 900;
            text-transform: uppercase;
        }
        
        .whats-next ul {
            list-style: none;
            padding: 0;
        }
        
        .whats-next li {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .step-number {
            background: #333333;
            color: #7ED321;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: bold;
        }
        
        .step-text {
            color: #333333;
            font-weight: 500;
            font-size: 15px;
        }
        
        /* Footer */
        .footer {
            background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
            color: #cccccc;
            padding: 30px 40px;
            text-align: center;
            border-top: 4px solid #7ED321;
            box-shadow: 0 -4px 16px rgba(0,0,0,0.3);
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .footer-text {
            font-size: 14px;
            line-height: 1.6;
            color: #cccccc;
        }
        
        .footer-text strong {
            color: #7ED321;
            font-weight: 700;
        }
        
        .social-links {
            display: flex;
            gap: 15px;
        }
        
        .social-link {
            width: 40px;
            height: 40px;
            background: #3a3a3a;
            border: 2px solid #7ED321;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #7ED321;
            text-decoration: none;
            transition: all 0.3s ease;
            font-size: 18px;
        }
        
        .social-link:hover {
            background: #7ED321;
            color: #333333;
            transform: translateY(-2px);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-content {
                padding: 25px;
            }
            
            .services-grid {
                grid-template-columns: 1fr;
            }
            
            .contact-grid {
                grid-template-columns: 1fr;
            }
            
            .company-name {
                font-size: 36px;
            }
            
            .welcome-title {
                font-size: 28px;
            }
            
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
            
            .wiseguys-logo {
                width: 100px;
                height: 100px;
            }
            
            .logo-w {
                font-size: 60px;
            }
        }
        
        /* Print Styles */
        @media print {
            .document-container {
                box-shadow: none;
                margin: 0;
                max-width: 100%;
                background: white !important;
            }
            
            .header, .main-content {
                background: white !important;
                color: black !important;
            }
            
            .service-card:hover {
                transform: none;
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <!-- Header Section -->
        <div class="header">
            <div class="logo-section">
                <div class="wiseguys-logo">
                    <div class="logo-w">W</div>
                    <div class="owl-left"></div>
                    <div class="owl-right"></div>
                </div>
            </div>
            <h1 class="company-name">Wiseguys</h1>
            <p class="company-tagline">Device Repair Specialists</p>
            <div class="company-location">
                📍 Bournemouth, UK
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Welcome Banner -->
            <div class="welcome-banner">
                <h2 class="welcome-title">Welcome to Wiseguys!</h2>
                <p class="welcome-message">
                    Thank you for choosing Wiseguys Bournemouth for your device repair needs. 
                    We're the wise choice for professional, reliable tech solutions!
                </p>
            </div>

            <!-- Customer Greeting -->
            <div class="customer-greeting">
                Hello <span class="name">{{customerName}}</span>, welcome to the family!
            </div>

            <!-- Services Section -->
            <div class="services-section">
                <h2 class="section-title">Our Expert Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">�</div>
                        <h3 class="service-title">Mobile & Tablet</h3>
                        <p class="service-description">Professional repair services for smartphones and tablets with same-day turnaround</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">💻</div>
                        <h3 class="service-title">PC & Laptop</h3>
                        <p class="service-description">Complete computer repair and maintenance services for all makes and models</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">🎮</div>
                        <h3 class="service-title">Gaming Console</h3>
                        <p class="service-description">Specialist console repair services to get you back gaming quickly</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">�</div>
                        <h3 class="service-title">Collection Service</h3>
                        <p class="service-description">We collect from your home or work with safe & secure handling and delivery back</p>
                    </div>
                </div>
            </div>

            <!-- Quote Section with Real Customer Review -->
            <div class="quote-section">
                <div class="quote-icon">"</div>
                <p class="quote-text">
                    "Wiseguys really are very wise and have been an absolute godsend. They have helped me set up new computers for my kids going to Uni and college and transfer files off old computers. Without them I would have really struggled as I'm so computer illiterate. They never once made me feel stupid and always explained things in simple, non-techie language. Thank you so much - you are all stars ⭐"
                </p>
                <div class="quote-author">- Lindsay Tara, Verified Customer</div>
            </div>

            <!-- Customer Details -->
            <div class="customer-details">
                <h3>Your Account Information</h3>
                <div>
                    <div class="detail-row">
                        <span class="detail-label">Customer:</span>
                        <span class="detail-value">{{customerName}}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">{{email}}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Phone:</span>
                        <span class="detail-value">{{phone}}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Service Date:</span>
                        <span class="detail-value">{{serviceDate}}</span>
                    </div>
                </div>
            </div>

            <!-- What's Next Section -->
            <div class="whats-next">
                <h3>What Happens Next?</h3>
                <ul>
                    <li>
                        <span class="step-number">1</span>
                        <span class="step-text">We'll contact you within 24 hours to arrange collection or drop-off</span>
                    </li>
                    <li>
                        <span class="step-number">2</span>
                        <span class="step-text">Our expert technicians will diagnose and repair your device</span>
                    </li>
                    <li>
                        <span class="step-number">3</span>
                        <span class="step-text">Same-day turnaround with safe delivery back to you</span>
                    </li>
                </ul>
            </div>

            <!-- Contact Information -->
            <div class="contact-info">
                <h3 class="contact-title">Get in Touch</h3>
                <div class="contact-grid">
                    <div class="contact-item">
                        <div class="contact-icon">📞</div>
                        <div class="contact-details">
                            <div class="contact-label">Phone</div>
                            <div class="contact-value">01202 806060</div>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">📧</div>
                        <div class="contact-details">
                            <div class="contact-label">Email</div>
                            <div class="contact-value">hello@wiseguys.co.uk</div>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">🌐</div>
                        <div class="contact-details">
                            <div class="contact-label">Website</div>
                            <div class="contact-value">www.wiseguys.co.uk</div>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">📱</div>
                        <div class="contact-details">
                            <div class="contact-label">Facebook</div>
                            <div class="contact-value">WiseGuys - Bournemouth</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-content">
                <div class="footer-text">
                    <strong>Wiseguys Bournemouth</strong><br>
                    Device Repair Specialists • Same Day Service • Collection & Delivery Available<br>
                    Mobile • Tablet • PC • Laptop • Console Repairs
                </div>
                <div class="social-links">
                    <a href="https://www.facebook.com/wiseguysbournemouth" class="social-link" target="_blank">📘</a>
                    <a href="tel:01202806060" class="social-link">�</a>
                    <a href="mailto:hello@wiseguys.co.uk" class="social-link">�</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>`
    }
  ];

  /**
   * Get a specific template by ID
   */
  static getTemplate(id: string) {
    return this.templates.find(template => template.id === id);
  }

  /**
   * Get all available templates
   */
  static getAllTemplates() {
    return this.templates;
  }

  /**
   * Render a template with provided data
   */
  static renderTemplate(templateId: string, data: Record<string, any>): string {
    const template = this.getTemplate(templateId);
    if (!template) {
      throw new Error(`Template with ID "${templateId}" not found`);
    }

    let renderedHtml = template.html;

    // Simple template variable replacement
    Object.keys(data).forEach(key => {
      const placeholder = new RegExp(`{{${key}}}`, 'g');
      renderedHtml = renderedHtml.replace(placeholder, data[key] || '');
    });

    return renderedHtml;
  }

  /**
   * Generate a document with the provided data
   */
  async generateDocument(templateType: string, data: Record<string, any>): Promise<string> {
    // Map template types to template IDs
    const templateMap: Record<string, string> = {
      'welcome-letter': 'wiseguys-welcome-letter',
      'wiseguys-welcome-letter': 'wiseguys-welcome-letter'
    };

    const templateId = templateMap[templateType] || templateType;
    return WiseguysTemplateService.renderTemplate(templateId, data);
  }

  /**
   * Get default template content for a template type
   */
  getDefaultTemplate(templateType: string): string {
    const template = WiseguysTemplateService.getTemplate('wiseguys-welcome-letter');
    return template ? template.html : '';
  }

  /**
   * Validate template syntax (basic validation)
   */
  validateTemplate(htmlContent: string): { valid: boolean; error?: string } {
    try {
      // Basic HTML structure validation
      if (!htmlContent.includes('<html') || !htmlContent.includes('</html>')) {
        return { valid: false, error: 'Template must be a complete HTML document' };
      }
      
      if (!htmlContent.includes('<head') || !htmlContent.includes('</head>')) {
        return { valid: false, error: 'Template must include a head section' };
      }
      
      if (!htmlContent.includes('<body') || !htmlContent.includes('</body>')) {
        return { valid: false, error: 'Template must include a body section' };
      }

      return { valid: true };
    } catch (error) {
      return { valid: false, error: 'Template parsing error' };
    }
  }
}

export default WiseguysTemplateService;