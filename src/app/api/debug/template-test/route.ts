import { NextRequest, NextResponse } from 'next/server';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';

export async function GET(request: NextRequest) {
  try {
    const enhancedTemplateService = new EnhancedTemplateService();
    
    // Test data matching the format
    const testData = {
      customerName: 'Giuseppe Raccio',
      email: 'Racciofamily@hotmail.com',
      phone: '7836517717',
      address: '34 Lomond Cresent, , , KA15 2EA',
      coverageStartDate: '18/01/2026',
      policyNumber: 'TFT3182',
      totalCost: '671.76',
      monthlyCost: '55.98',
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
      boilerCost: '£24.99',
      currentDate: '18th January 2026',
      agreement: {
        coverage: {
          hasBoilerCover: true,
          boilerPriceFormatted: '£24.99/month'
        }
      },
      metadata: {
        agentName: 'Test Agent'
      }
    };

    console.log('🧪 Testing template generation with data:', testData);
    
    // Generate the document
    const result = await enhancedTemplateService.generateDocument('welcome-letter', testData);
    
    console.log('✅ Generated document length:', result.length);
    console.log('📄 First 500 characters:', result.substring(0, 500));
    
    // Return as HTML so we can see how it renders
    return new Response(result, {
      headers: {
        'Content-Type': 'text/html',
      },
    });

  } catch (error) {
    console.error('❌ Template test error:', error);
    return NextResponse.json(
      { error: 'Template test failed', details: error },
      { status: 500 }
    );
  }
}