import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'

export async function GET(request: NextRequest) {
  try {
    // Check authentication
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Check if user is admin
    if (session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 })
    }

    // CSV headers - all possible fields for import
    const headers = [
      'customerFirstName',
      'customerLastName', 
      'title',
      'phoneNumber',
      'email',
      'notes',
      'mailingStreet',
      'mailingCity',
      'mailingProvince',
      'mailingPostalCode',
      'accountName',
      'sortCode',
      'accountNumber',
      'directDebitDate',
      'applianceCoverSelected',
      'boilerCoverSelected',
      'boilerPriceSelected',
      'totalPlanCost',
      'appliance1',
      'appliance1Cost',
      'appliance1CoverLimit',
      'appliance2',
      'appliance2Cost',
      'appliance2CoverLimit',
      'appliance3',
      'appliance3Cost',
      'appliance3CoverLimit',
      'appliance4',
      'appliance4Cost',
      'appliance4CoverLimit',
      'appliance5',
      'appliance5Cost',
      'appliance5CoverLimit',
      'appliance6',
      'appliance6Cost',
      'appliance6CoverLimit',
      'appliance7',
      'appliance7Cost',
      'appliance7CoverLimit',
      'appliance8',
      'appliance8Cost',
      'appliance8CoverLimit',
      'appliance9',
      'appliance9Cost',
      'appliance9CoverLimit',
      'appliance10',
      'appliance10Cost',
      'appliance10CoverLimit'
    ]

    // Sample data row
    const sampleData = [
      'John',
      'Doe',
      'Mr',
      '01234567890',
      'john.doe@email.com',
      'Customer requested early installation',
      '123 Main Street',
      'London',
      'London',
      'SW1A 1AA',
      'John Doe',
      '12-34-56',
      '12345678',
      '2026-02-01',
      'true',
      'true', 
      '25.99',
      '45.98',
      'Washing Machine',
      '15.99',
      '500',
      'Dishwasher',
      '4.00',
      '600',
      'Boiler',
      '25.99',
      '700',
      '', // appliance4
      '', // appliance4Cost
      '', // appliance4CoverLimit
      '', // appliance5
      '', // appliance5Cost
      '', // appliance5CoverLimit
      '', // appliance6
      '', // appliance6Cost
      '', // appliance6CoverLimit
      '', // appliance7
      '', // appliance7Cost
      '', // appliance7CoverLimit
      '', // appliance8
      '', // appliance8Cost
      '', // appliance8CoverLimit
      '', // appliance9
      '', // appliance9Cost
      '', // appliance9CoverLimit
      '', // appliance10
      '', // appliance10Cost
      ''  // appliance10CoverLimit
    ]

    // Create CSV content
    const csvContent = [
      headers.join(','),
      sampleData.join(',')
    ].join('\n')

    // Return CSV file
    return new NextResponse(csvContent, {
      status: 200,
      headers: {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="sales_import_template.csv"'
      }
    })

  } catch (error) {
    console.error('Template download error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}