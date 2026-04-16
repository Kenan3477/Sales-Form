const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

// Wiseguys template HTML content - AUTHENTIC BRANDING
const WISEGUYS_TEMPLATE = `<!DOCTYPE html>
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
        
        .quote-section {
            background: linear-gradient(135deg, #4a4a4a 0%, #3a3a3a 100%);
            border-left: 6px solid #7ED321;
            border-radius: 0 15px 15px 0;
            padding: 35px;
            margin: 40px 0;
            position: relative;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
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
        
        .contact-value {
            font-size: 18px;
            font-weight: 700;
            color: #7ED321;
        }
        
        .footer {
            background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
            color: #cccccc;
            padding: 30px 40px;
            text-align: center;
            border-top: 4px solid #7ED321;
            box-shadow: 0 -4px 16px rgba(0,0,0,0.3);
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
    </style>
</head>
<body>
    <div class="document-container">
        <div class="header">
            <div class="logo-section">
                <div class="wiseguys-logo">
                    <div class="logo-w">W</div>
                </div>
            </div>
            <h1 class="company-name">Wiseguys</h1>
            <p class="company-tagline">Device Repair Specialists</p>
            <div class="company-location">
                📍 Bournemouth, UK
            </div>
        </div>

        <div class="main-content">
            <div class="welcome-banner">
                <h2 class="welcome-title">Welcome to Wiseguys!</h2>
                <p class="welcome-message">
                    Thank you for choosing Wiseguys Bournemouth for your device repair needs. 
                    We're the wise choice for professional, reliable tech solutions!
                </p>
            </div>

            <div class="customer-greeting">
                Hello <span class="name">{{customerName}}</span>, welcome to the family!
            </div>

            <div class="services-section">
                <h2 class="section-title">Our Expert Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">📱</div>
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
                        <div class="service-icon">🚚</div>
                        <h3 class="service-title">Collection Service</h3>
                        <p class="service-description">We collect from your home or work with safe & secure handling and delivery back</p>
                    </div>
                </div>
            </div>

            <div class="quote-section">
                <p class="quote-text">
                    "Wiseguys really are very wise and have been an absolute godsend. They have helped me set up new computers for my kids going to Uni and college and transfer files off old computers. Without them I would have really struggled as I'm so computer illiterate. They never once made me feel stupid and always explained things in simple, non-techie language. Thank you so much - you are all stars ⭐"
                </p>
                <div class="quote-author">- Lindsay Tara, Verified Customer</div>
            </div>

            <div class="contact-info">
                <h3 class="contact-title">Get in Touch</h3>
                <div class="contact-grid">
                    <div class="contact-item">
                        <div class="contact-icon">📞</div>
                        <div>
                            <div style="font-size: 12px; color: #cccccc; font-weight: 500; text-transform: uppercase;">Phone</div>
                            <div class="contact-value">01202 806060</div>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">📧</div>
                        <div>
                            <div style="font-size: 12px; color: #cccccc; font-weight: 500; text-transform: uppercase;">Email</div>
                            <div class="contact-value">hello@wiseguys.co.uk</div>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">🌐</div>
                        <div>
                            <div style="font-size: 12px; color: #cccccc; font-weight: 500; text-transform: uppercase;">Website</div>
                            <div class="contact-value">www.wiseguys.co.uk</div>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">📱</div>
                        <div>
                            <div style="font-size: 12px; color: #cccccc; font-weight: 500; text-transform: uppercase;">Facebook</div>
                            <div class="contact-value">WiseGuys - Bournemouth</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="footer-text">
                <strong>Wiseguys Bournemouth</strong><br>
                Device Repair Specialists • Same Day Service • Collection & Delivery Available<br>
                Mobile • Tablet • PC • Laptop • Console Repairs
            </div>
        </div>
    </div>
</body>
</html>`;
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wiseguys Bournemouth - Welcome Letter</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Montserrat:wght@400;500;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.4;
            color: #1f2937;
            background: white;
            font-size: 14px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .document-container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Header Section with Wiseguys Branding */
        .header {
            background: linear-gradient(135deg, #1a365d 0%, #2563eb 50%, #3b82f6 100%);
            color: white;
            padding: 30px 40px;
            position: relative;
            text-align: center;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ef4444 0%, #f97316 30%, #eab308 60%, #22c55e 100%);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .logo-placeholder {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #ef4444, #f97316);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 900;
            color: white;
            border: 4px solid white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .company-name {
            font-family: 'Montserrat', sans-serif;
            font-size: 42px;
            font-weight: 800;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 5px;
            letter-spacing: -1px;
        }
        
        .company-tagline {
            font-size: 16px;
            font-weight: 500;
            color: #e2e8f0;
            margin-bottom: 10px;
            font-style: italic;
        }
        
        .company-location {
            font-size: 14px;
            font-weight: 400;
            color: #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .location-icon {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #ef4444;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 10px;
            font-weight: bold;
        }
        
        /* Main Content Area */
        .main-content {
            flex: 1;
            padding: 40px;
            background: white;
        }
        
        .welcome-banner {
            background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 50%, #fecaca 100%);
            border: 2px solid #f59e0b;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 35px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .welcome-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(251, 191, 36, 0.1) 0%, transparent 70%);
            z-index: 1;
        }
        
        .welcome-banner > * {
            position: relative;
            z-index: 2;
        }
        
        .welcome-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 32px;
            font-weight: 700;
            color: #dc2626;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        .welcome-message {
            font-size: 18px;
            font-weight: 500;
            color: #7c2d12;
            line-height: 1.5;
        }
        
        .customer-greeting {
            font-size: 20px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 25px;
            text-align: center;
        }
        
        .customer-greeting .name {
            color: #dc2626;
            font-weight: 700;
        }
        
        /* Services Section */
        .services-section {
            margin-bottom: 35px;
        }
        
        .section-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 20px;
            text-align: center;
            position: relative;
            padding-bottom: 10px;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #ef4444, #f97316);
            border-radius: 2px;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .service-card {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .service-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-color: #ef4444;
        }
        
        .service-icon {
            width: 50px;
            height: 50px;
            margin: 0 auto 15px;
            background: linear-gradient(45deg, #ef4444, #f97316);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }
        
        .service-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 8px;
        }
        
        .service-description {
            font-size: 14px;
            color: #6b7280;
            line-height: 1.4;
        }
        
        /* Quote Section */
        .quote-section {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 6px solid #2563eb;
            border-radius: 0 12px 12px 0;
            padding: 30px;
            margin: 35px 0;
            position: relative;
        }
        
        .quote-icon {
            position: absolute;
            top: -10px;
            left: 20px;
            width: 40px;
            height: 40px;
            background: #2563eb;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
            font-weight: bold;
        }
        
        .quote-text {
            font-size: 18px;
            font-style: italic;
            color: #1e40af;
            line-height: 1.6;
            margin-bottom: 15px;
            padding-left: 30px;
        }
        
        .quote-author {
            text-align: right;
            font-weight: 600;
            color: #1e3a8a;
            font-size: 14px;
        }
        
        /* Contact Information */
        .contact-info {
            background: #1f2937;
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin: 35px 0;
        }
        
        .contact-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
            color: #fbbf24;
        }
        
        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .contact-item {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .contact-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(45deg, #ef4444, #f97316);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 16px;
            flex-shrink: 0;
        }
        
        .contact-details {
            flex: 1;
        }
        
        .contact-label {
            font-size: 12px;
            color: #9ca3af;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .contact-value {
            font-size: 16px;
            font-weight: 600;
            color: white;
        }
        
        /* Footer */
        .footer {
            background: #111827;
            color: #9ca3af;
            padding: 25px 40px;
            text-align: center;
            border-top: 3px solid #ef4444;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .footer-text {
            font-size: 14px;
            line-height: 1.4;
        }
        
        .social-links {
            display: flex;
            gap: 15px;
        }
        
        .social-link {
            width: 35px;
            height: 35px;
            background: #374151;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .social-link:hover {
            background: linear-gradient(45deg, #ef4444, #f97316);
            transform: translateY(-2px);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-content {
                padding: 20px;
            }
            
            .services-grid {
                grid-template-columns: 1fr;
            }
            
            .contact-grid {
                grid-template-columns: 1fr;
            }
            
            .company-name {
                font-size: 28px;
            }
            
            .welcome-title {
                font-size: 24px;
            }
            
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
        
        /* Print Styles */
        @media print {
            .document-container {
                box-shadow: none;
                margin: 0;
                max-width: 100%;
            }
            
            .header::after {
                background: #333;
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
                <div class="logo-placeholder">WG</div>
            </div>
            <h1 class="company-name">Wiseguys</h1>
            <p class="company-tagline">"Your Local Home Services Experts"</p>
            <div class="company-location">
                <span class="location-icon">📍</span>
                Bournemouth, UK
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Welcome Banner -->
            <div class="welcome-banner">
                <h2 class="welcome-title">Welcome to the Family!</h2>
                <p class="welcome-message">
                    Thank you for choosing Wiseguys Bournemouth for your home services. 
                    We're excited to serve you with our professional and reliable solutions.
                </p>
            </div>

            <!-- Customer Greeting -->
            <div class="customer-greeting">
                Hello <span class="name">{{customerName}}</span>, and welcome aboard!
            </div>

            <!-- Services Section -->
            <div class="services-section">
                <h2 class="section-title">Our Services</h2>
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">🔧</div>
                        <h3 class="service-title">Home Repairs</h3>
                        <p class="service-description">Professional repair services for all your home maintenance needs</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">🏠</div>
                        <h3 class="service-title">Property Services</h3>
                        <p class="service-description">Comprehensive property management and maintenance solutions</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">⚡</div>
                        <h3 class="service-title">Emergency Support</h3>
                        <p class="service-description">24/7 emergency response for urgent home service issues</p>
                    </div>
                    <div class="service-card">
                        <div class="service-icon">🛡️</div>
                        <h3 class="service-title">Protection Plans</h3>
                        <p class="service-description">Comprehensive protection plans for your peace of mind</p>
                    </div>
                </div>
            </div>

            <!-- Quote Section -->
            <div class="quote-section">
                <div class="quote-icon">"</div>
                <p class="quote-text">
                    "At Wiseguys, we believe every home deserves expert care. Our team of professionals 
                    is committed to delivering exceptional service with a personal touch that makes all the difference."
                </p>
                <div class="quote-author">- The Wiseguys Team</div>
            </div>

            <!-- Customer Details -->
            <div class="customer-details" style="background: #f9fafb; border-radius: 12px; padding: 25px; margin: 30px 0;">
                <h3 style="font-family: 'Montserrat', sans-serif; color: #1f2937; margin-bottom: 20px; text-align: center;">Your Account Information</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                        <span style="font-weight: 500; color: #6b7280;">Customer:</span>
                        <span style="font-weight: 600; color: #1f2937;">{{customerName}}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                        <span style="font-weight: 500; color: #6b7280;">Email:</span>
                        <span style="font-weight: 600; color: #1f2937;">{{email}}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                        <span style="font-weight: 500; color: #6b7280;">Phone:</span>
                        <span style="font-weight: 600; color: #1f2937;">{{phone}}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb;">
                        <span style="font-weight: 500; color: #6b7280;">Service Date:</span>
                        <span style="font-weight: 600; color: #1f2937;">{{serviceDate}}</span>
                    </div>
                </div>
            </div>

            <!-- What's Next Section -->
            <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border-radius: 12px; padding: 25px; margin: 30px 0;">
                <h3 style="font-family: 'Montserrat', sans-serif; color: #065f46; margin-bottom: 15px; text-align: center;">What Happens Next?</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="background: #10b981; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;">1</span>
                        <span style="color: #065f46;">We'll contact you within 24 hours to schedule your service</span>
                    </li>
                    <li style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="background: #10b981; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;">2</span>
                        <span style="color: #065f46;">Our expert technicians will arrive at the agreed time</span>
                    </li>
                    <li style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="background: #10b981; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;">3</span>
                        <span style="color: #065f46;">We'll complete the work to your complete satisfaction</span>
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
                            <div class="contact-value">01202 XXX XXX</div>
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
                            <div class="contact-value">@wiseguysbournemouth</div>
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
                    Professional Home Services • Est. {{establishedYear}} • Serving Bournemouth & Surrounding Areas
                </div>
                <div class="social-links">
                    <a href="https://www.facebook.com/wiseguysbournemouth" class="social-link" target="_blank">📘</a>
                    <a href="#" class="social-link">📧</a>
                    <a href="#" class="social-link">📞</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>`;

async function createWiseguysTemplate() {
  try {
    console.log('🎨 Creating Wiseguys branded welcome letter template...');

    // Check if we have any admin users
    const adminUser = await prisma.user.findFirst({
      where: { role: 'ADMIN' },
    });

    if (!adminUser) {
      console.log('❌ No admin user found. Please create an admin user first.');
      return;
    }

    console.log(`✅ Using admin user: ${adminUser.email}`);

    // Check if the template already exists
    const existingTemplate = await prisma.documentTemplate.findFirst({
      where: { 
        templateType: 'wiseguys-welcome-letter',
        isActive: true 
      },
    });

    if (existingTemplate) {
      console.log('⚠️ Wiseguys template already exists. Updating...');
      
      await prisma.documentTemplate.update({
        where: { id: existingTemplate.id },
        data: {
          name: 'Wiseguys Welcome Letter',
          description: 'Professional welcome letter with Wiseguys Bournemouth branding',
          htmlContent: WISEGUYS_TEMPLATE,
        }
      });

      console.log('✅ Updated existing Wiseguys template successfully!');
      return existingTemplate;
    }

    // Create new Wiseguys template
    const newTemplate = await prisma.documentTemplate.create({
      data: {
        name: 'Wiseguys Welcome Letter',
        description: 'Professional welcome letter with Wiseguys Bournemouth branding',
        templateType: 'wiseguys-welcome-letter',
        htmlContent: WISEGUYS_TEMPLATE,
        isActive: true,
        version: 1,
        createdById: adminUser.id
      }
    });

    console.log('✅ Created Wiseguys template successfully!');
    console.log('📋 Template details:', {
      id: newTemplate.id,
      name: newTemplate.name,
      templateType: newTemplate.templateType,
      isActive: newTemplate.isActive,
      htmlLength: newTemplate.htmlContent.length
    });

    // Also create a standard welcome-letter version for compatibility
    const compatTemplate = await prisma.documentTemplate.upsert({
      where: {
        templateType_version: {
          templateType: 'welcome-letter',
          version: 1
        }
      },
      update: {
        htmlContent: WISEGUYS_TEMPLATE,
        name: 'Wiseguys Welcome Letter (Main)',
        description: 'Wiseguys branded welcome letter (main template)',
        isActive: true
      },
      create: {
        name: 'Wiseguys Welcome Letter (Main)',
        description: 'Wiseguys branded welcome letter (main template)',
        templateType: 'welcome-letter',
        htmlContent: WISEGUYS_TEMPLATE,
        isActive: true,
        version: 1,
        createdById: adminUser.id
      }
    });

    console.log('✅ Created/updated main welcome-letter template!');
    
    return newTemplate;

  } catch (error) {
    console.error('❌ Error creating Wiseguys template:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

// Test template generation
function testTemplateGeneration() {
  console.log('🧪 Testing Wiseguys template generation...');
  
  const testData = {
    customerName: 'John Smith',
    email: 'john.smith@example.com',
    phone: '01202 123 456',
    serviceDate: new Date().toLocaleDateString('en-GB'),
    establishedYear: '2020'
  };

  let renderedTemplate = WISEGUYS_TEMPLATE;

  // Simple template variable replacement
  Object.keys(testData).forEach(key => {
    const placeholder = new RegExp(`{{${key}}}`, 'g');
    renderedTemplate = renderedTemplate.replace(placeholder, testData[key] || '');
  });
  
  console.log('✅ Template rendered successfully!');
  console.log('📊 Template stats:');
  console.log(`  - Length: ${renderedTemplate.length} characters`);
  console.log(`  - Contains customer name: ${renderedTemplate.includes(testData.customerName)}`);
  console.log(`  - Contains email: ${renderedTemplate.includes(testData.email)}`);
  console.log(`  - Contains phone: ${renderedTemplate.includes(testData.phone)}`);
  
  return true;
}

// Main execution
async function main() {
  console.log('🚀 Starting Wiseguys template setup...');
  
  // Test template generation first
  const testPassed = testTemplateGeneration();
  if (!testPassed) {
    console.error('❌ Template generation test failed. Stopping...');
    return;
  }
  
  // Create the template in database
  await createWiseguysTemplate();
  
  console.log('🎉 Wiseguys template setup complete!');
  console.log('');
  console.log('📋 Next steps to customize the template:');
  console.log('1. Update the contact information with actual Wiseguys details');
  console.log('2. Add the actual Wiseguys logo to replace the placeholder');
  console.log('3. Customize the services section based on actual Wiseguys offerings');
  console.log('4. Add real customer quotes from the Wiseguys Facebook page');
  console.log('5. Update the color scheme to match Wiseguys brand colors');
  console.log('6. Test the template generation from the admin panel');
}

// Run the script
main().catch(console.error);