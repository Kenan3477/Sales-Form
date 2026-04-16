// Self-contained type definitions
type TemplateType = 'welcome-letter' | 'service-agreement' | 'direct-debit-form' | 'coverage-summary' | string;

/**
 * Professional Wiseguys template service for remote support tech plans
 */
export class WiseguysProfessionalTemplateService {
  private static templates = [
    {
      id: 'wiseguys-tech-plan',
      name: 'Wiseguys Remote Support Tech Plan',
      description: 'Professional Wiseguys remote support tech plan documentation with modular design',
      category: 'Customer Communications',
      html: `<!DOCTYPE html>
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
            background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
            font-size: 12px;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(126, 211, 33, 0.02) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(126, 211, 33, 0.02) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }
        
        .document-container {
            width: 100%;
            height: 100%;
            background: transparent;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            position: relative;
            z-index: 2;
        }
        
        .header {
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 30%, #333333 70%, #2c2c2c 100%);
            color: white;
            padding: 16px 20px;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            width: 100%;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.02);
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #7ED321 0%, #a3ff3d 25%, #7ED321 50%, #a3ff3d 75%, #7ED321 100%);
            box-shadow: 0 2px 8px rgba(126, 211, 33, 0.4);
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
            z-index: 2;
        }
        
        .wiseguys-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(45deg, #7ED321 0%, #a3ff3d 50%, #7ED321 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1a1a1a;
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.3), inset 0 1px 0 rgba(255,255,255,0.2);
            flex-shrink: 0;
            font-weight: 900;
            border: 2px solid rgba(255,255,255,0.9);
            position: relative;
            overflow: hidden;
        }
        
        .wiseguys-icon::before {
            content: 'W';
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 20px;
            font-weight: 900;
            letter-spacing: -1px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            position: relative;
            z-index: 2;
        }
        
        .wiseguys-icon::after {
            content: '';
            position: absolute;
            top: -2px;
            right: -2px;
            width: 12px;
            height: 12px;
            background: #ff6b35;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .logo-text {
            font-size: 24px;
            font-weight: 900;
            letter-spacing: 2px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            line-height: 1;
        }
        
        .tagline {
            font-size: 10px;
            color: #7ED321;
            margin-top: 2px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .content {
            padding: 20px 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: linear-gradient(to bottom, #ffffff 0%, #fafbfc 100%);
        }
        
        .main-title {
            font-size: 22px;
            font-weight: 900;
            color: #2c2c2c;
            margin-bottom: 18px;
            border-bottom: 3px solid #7ED321;
            padding-bottom: 12px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            position: relative;
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .main-title::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #7ED321 0%, #a3ff3d 50%, #7ED321 100%);
            box-shadow: 0 2px 6px rgba(126, 211, 33, 0.3);
        }
        
        .intro-text {
            font-size: 13px;
            margin-bottom: 18px;
            line-height: 1.6;
            color: #4a5568;
            font-weight: 500;
        }
        
        .activation-banner {
            background: linear-gradient(135deg, #7ED321 0%, #a3ff3d 50%, #7ED321 100%);
            color: #1a1a1a;
            padding: 16px 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 14px;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.25), inset 0 1px 0 rgba(255,255,255,0.2);
            letter-spacing: 0.5px;
            border: 1px solid rgba(255,255,255,0.3);
            text-transform: uppercase;
        }
        
        .three-column {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 16px;
            margin-bottom: 20px;
            flex: 1;
        }
        
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            background: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.03);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
            position: relative;
        }
        
        .card:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.05);
            transform: translateY(-2px);
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #7ED321, #a3ff3d, #7ED321);
        }
        
        .card-header {
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
            color: white;
            padding: 16px 12px;
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            border-bottom: 1px solid rgba(126, 211, 33, 0.3);
        }
        
        .card-header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, #7ED321, #a3ff3d, #7ED321);
        }
        
        .card-content {
            padding: 18px 12px;
            background: white;
            font-size: 10px;
            line-height: 1.5;
            flex: 1;
            position: relative;
        }
        
        .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 6px 0;
            border-bottom: 1px solid #f1f5f9;
            transition: background-color 0.2s ease;
        }
        
        .detail-row:hover {
            background-color: #f8fafc;
            margin: 0 -6px;
            padding-left: 6px;
            padding-right: 6px;
            border-radius: 4px;
        }
        
        .detail-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        
        .detail-label {
            font-weight: 700;
            color: #4a5568;
            text-transform: uppercase;
            font-size: 8px;
            letter-spacing: 0.75px;
            width: 50%;
            line-height: 1.4;
        }
        
        .detail-value {
            font-weight: 700;
            color: #2c2c2c;
            text-align: right;
            flex: 1;
            font-size: 10px;
            word-break: break-word;
            overflow-wrap: break-word;
            line-height: 1.4;
        }
        
        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 10px;
            font-size: 10px;
            line-height: 1.5;
            padding: 2px 0;
            transition: background-color 0.2s ease;
        }
        
        .checklist-item:hover {
            background-color: #f8fafc;
            margin: 0 -8px;
            padding-left: 8px;
            padding-right: 8px;
            border-radius: 4px;
        }
        
        .checklist-item:last-child {
            margin-bottom: 0;
        }
        
        .check-icon {
            width: 12px;
            height: 12px;
            background: linear-gradient(135deg, #7ED321, #a3ff3d);
            border-radius: 50%;
            position: relative;
            flex-shrink: 0;
            margin-top: 1px;
            box-shadow: 0 2px 4px rgba(126, 211, 33, 0.3);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .check-icon::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #1a1a1a;
            font-size: 8px;
            font-weight: 900;
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
            padding: 12px 20px;
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
            border-top: 1px solid #e2e8f0;
            font-size: 9px;
            color: #cbd5e0;
            text-align: center;
            margin-top: auto;
            position: relative;
        }
        
        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #7ED321 0%, #a3ff3d 50%, #7ED321 100%);
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
            gap: 6px;
            font-weight: 600;
            color: #e2e8f0;
        }
        
        .contact-highlight {
            color: #7ED321;
            font-weight: 700;
            text-shadow: 0 1px 2px rgba(126, 211, 33, 0.3);
        }
        
        .device-repair-section {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(126, 211, 33, 0.2);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
        }
        
        .device-repair-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #7ED321 0%, #a3ff3d 25%, #7ED321 50%, #a3ff3d 75%, #7ED321 100%);
            box-shadow: 0 2px 8px rgba(126, 211, 33, 0.4);
        }
        
        .device-repair-main-header {
            font-size: 26px;
            font-weight: 900;
            color: white;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            line-height: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .device-repair-green-text {
            color: #7ED321;
            font-weight: 900;
            text-shadow: 0 0 10px rgba(126, 211, 33, 0.5);
        }
        
        .device-repair-subheader {
            font-size: 20px;
            color: white;
            margin-bottom: 20px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        }
        
        .repair-content-wrapper {
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .repair-van-circle {
            width: 130px;
            height: 130px;
            background: linear-gradient(45deg, #7ED321 0%, #a3ff3d 50%, #7ED321 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            border: 4px solid white;
            box-shadow: 0 6px 20px rgba(0,0,0,0.4), inset 0 2px 4px rgba(255,255,255,0.2);
            position: relative;
            overflow: hidden;
        }
        
        .repair-van-circle::before {
            content: '';
            position: absolute;
            top: -2px;
            right: -2px;
            width: 20px;
            height: 20px;
            background: #ff6b35;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .repair-van-text {
            font-size: 11px;
            color: #1a1a1a;
            font-weight: 900;
            text-align: center;
            line-height: 1;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
        }
        
        .repair-features-bubble {
            background: linear-gradient(135deg, #7ED321 0%, #a3ff3d 100%);
            color: #1a1a1a;
            padding: 20px 24px;
            border-radius: 24px;
            position: relative;
            flex: 1;
            margin-left: -12px;
            box-shadow: 0 6px 20px rgba(126, 211, 33, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .repair-features-bubble::before {
            content: '';
            position: absolute;
            left: -12px;
            top: 50%;
            transform: translateY(-50%);
            width: 0;
            height: 0;
            border-top: 18px solid transparent;
            border-bottom: 18px solid transparent;
            border-right: 18px solid #7ED321;
            filter: drop-shadow(-2px 0 4px rgba(0,0,0,0.2));
        }
        
        .repair-feature-list {
            list-style: none;
            margin: 0;
            padding: 0;
        }
        
        .repair-feature-item {
            font-size: 15px;
            font-weight: 800;
            margin-bottom: 6px;
            color: #1a1a1a;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            line-height: 1.2;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.2);
        }
        
        .repair-feature-item:last-child {
            margin-bottom: 0;
        }
        
        .device-types-large {
            font-size: 22px;
            font-weight: 900;
            text-align: center;
            margin: 24px 0;
            color: white;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            line-height: 1.2;
        }
        
        .contact-section {
            background: linear-gradient(135deg, #7ED321 0%, #a3ff3d 100%);
            color: #1a1a1a;
            padding: 20px 24px;
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0 6px 20px rgba(126, 211, 33, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        .contact-item {
            text-align: center;
        }
        
        .contact-main-text {
            font-size: 18px;
            font-weight: 900;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
        }
        
        .contact-sub-text {
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            color: #2c2c2c;
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
                    <div class="card-header">Device Repair Service</div>
                    <div class="card-content">
                        <div class="device-repair-section">
                            <div class="device-repair-main-header">
                                NEED A DEVICE <span class="device-repair-green-text">REPAIRED</span>
                            </div>
                            <div class="device-repair-subheader">
                                BUT CAN'T GET TO US?
                            </div>
                            
                            <div class="repair-content-wrapper">
                                <div class="repair-van-circle">
                                    <div class="repair-van-text">
                                        WISEGUYS<br>
                                        VAN<br>
                                        SERVICE
                                    </div>
                                </div>
                                
                                <div class="repair-features-bubble">
                                    <ul class="repair-feature-list">
                                        <li class="repair-feature-item">WE COLLECT FROM YOUR HOME OR WORK</li>
                                        <li class="repair-feature-item">Same day turn around</li>
                                        <li class="repair-feature-item">Includes delivery back</li>
                                        <li class="repair-feature-item">Safe & Secure handling</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <div class="device-types-large">
                                MOBILE • TABLET • PC • LAPTOP • CONSOLE
                            </div>
                            
                            <div class="contact-section">
                                <div class="contact-grid">
                                    <div class="contact-item">
                                        <div class="contact-main-text">CALL 08081232820</div>
                                        <div class="contact-sub-text">TO BOOK YOUR COLLECTION TODAY</div>
                                    </div>
                                    <div class="contact-item">
                                        <div class="contact-main-text">EMAIL US</div>
                                        <div class="contact-sub-text">hello@wiseguys.co.uk</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="two-column-bottom">
                <div class="card">
                    <div class="card-header">Support Channels</div>
                    <div class="card-content">
                        <ul class="compact-list">
                            <li><strong>Priority Phone:</strong> 08081232820</li>
                            <li><strong>Remote Portal:</strong> support.wiseguys.co.uk</li>
                            <li><strong>Email:</strong> hello@wiseguys.co.uk</li>
                            <li><strong>Live Chat:</strong> Available 9AM-5PM</li>
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
</html>`
    }
  ];

  static getTemplates() {
    return this.templates;
  }

  static getTemplate(id: string) {
    return this.templates.find(template => template.id === id);
  }

  static async renderTemplate(templateId: string, data: Record<string, any>) {
    const template = this.getTemplate(templateId);
    if (!template) {
      throw new Error(`Template not found: ${templateId}`);
    }

    let html = template.html;
    
    // Replace handlebars-style variables
    Object.keys(data).forEach(key => {
      const regex = new RegExp(`{{${key}}}`, 'g');
      html = html.replace(regex, data[key] || '');
    });

    return html;
  }
}