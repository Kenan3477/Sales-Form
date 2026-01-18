import { NextRequest, NextResponse } from 'next/server';
import { EnhancedTemplateService } from '@/lib/paperwork/enhanced-template-service';

export async function GET(request: NextRequest) {
  try {
    const enhancedTemplateService = new EnhancedTemplateService();
    
    // Get available templates
    const templates = enhancedTemplateService.getAvailableTemplates();
    console.log('📄 Available templates:', templates.map(t => ({ id: t.id, name: t.name })));
    
    // Test data for document generation
    const testData = {
      customerName: 'John Doe',
      email: 'john.doe@example.com',
      phone: '01234567890',
      address: '123 Test Street, Test City, TC, T3ST 1NG',
      coverageStartDate: new Date().toLocaleDateString('en-GB'),
      policyNumber: 'TFT1234',
      totalCost: '360.00',
      monthlyCost: '30.00',
      hasApplianceCover: true,
      hasBoilerCover: true,
      appliances: [
        {
          name: 'Washing Machine',
          coverLimit: '£500.00',
          monthlyCost: '£15.00'
        }
      ],
      boilerCost: '£15.00',
      currentDate: new Date().toLocaleDateString('en-GB'),
      agreement: {
        coverage: {
          hasBoilerCover: true,
          boilerPriceFormatted: '£15.00/month'
        }
      },
      metadata: {
        agentName: 'Test Agent'
      }
    };
    
    // Try to generate a document
    console.log('📄 Attempting to generate welcome-letter document...');
    const documentContent = await enhancedTemplateService.generateDocument('welcome-letter', testData);
    
    const result = {
      success: true,
      availableTemplates: templates.map(t => ({ id: t.id, name: t.name })),
      testDataUsed: {
        customerName: testData.customerName,
        email: testData.email,
        totalCost: testData.totalCost,
        hasAppliances: testData.appliances.length > 0
      },
      documentGenerated: {
        success: !!documentContent,
        contentLength: documentContent?.length || 0,
        hasContent: documentContent && documentContent.length > 100
      }
    };
    
    console.log('📄 Test result:', result);
    
    return NextResponse.json(result);
    
  } catch (error) {
    console.error('❌ Debug test error:', error);
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    }, { status: 500 });
  }
}