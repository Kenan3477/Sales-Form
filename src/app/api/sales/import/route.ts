import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import Papa from 'papaparse'
import { withSecurity, handleSecureUpload } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext } from '@/lib/security'

interface DuplicateCheckResult {
  isDuplicate: boolean
  existingCustomer?: {
    id: string
    customerFirstName: string
    customerLastName: string
    email: string
    phoneNumber: string
    createdAt: Date
  }
  duplicateReason?: string
}

/**
 * Check if a customer already exists in the system
 */
async function checkForDuplicate(customerData: {
  customerFirstName: string
  customerLastName: string
  email: string
  phoneNumber: string
}): Promise<DuplicateCheckResult> {
  const { customerFirstName, customerLastName, email, phoneNumber } = customerData

  // Normalize phone number for comparison (remove spaces, dashes, etc.)
  const normalizedPhone = phoneNumber.replace(/[\s\-\(\)]/g, '')
  
  // Check for exact email match (most reliable)
  const emailMatch = await prisma.sale.findFirst({
    where: {
      email: {
        equals: email,
        mode: 'insensitive'
      }
    },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      phoneNumber: true,
      createdAt: true
    }
  })

  if (emailMatch) {
    return {
      isDuplicate: true,
      existingCustomer: emailMatch,
      duplicateReason: 'Email address already exists'
    }
  }

  // Check for phone number match
  const phoneMatch = await prisma.sale.findFirst({
    where: {
      OR: [
        { phoneNumber: phoneNumber },
        { phoneNumber: normalizedPhone },
        { phoneNumber: { contains: normalizedPhone.slice(-10) } }, // Last 10 digits for UK numbers
      ]
    },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      phoneNumber: true,
      createdAt: true
    }
  })

  if (phoneMatch) {
    return {
      isDuplicate: true,
      existingCustomer: phoneMatch,
      duplicateReason: 'Phone number already exists'
    }
  }

  // Check for name + similar contact info combination
  const nameMatch = await prisma.sale.findFirst({
    where: {
      AND: [
        {
          customerFirstName: {
            equals: customerFirstName,
            mode: 'insensitive'
          }
        },
        {
          customerLastName: {
            equals: customerLastName,
            mode: 'insensitive'
          }
        }
      ]
    },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      phoneNumber: true,
      createdAt: true
    }
  })

  if (nameMatch) {
    // Additional check: if names match and emails/phones are similar
    const emailSimilar = nameMatch.email.toLowerCase().includes(email.split('@')[0].toLowerCase()) ||
                        email.toLowerCase().includes(nameMatch.email.split('@')[0].toLowerCase())
    
    if (emailSimilar) {
      return {
        isDuplicate: true,
        existingCustomer: nameMatch,
        duplicateReason: 'Same name with similar email address'
      }
    }
  }

  return {
    isDuplicate: false
  }
}

interface ImportSaleData {
  // Customer information
  customerFirstName: string
  customerLastName: string
  title?: string
  phoneNumber: string
  email: string
  notes?: string

  // Address information
  mailingStreet?: string
  mailingCity?: string
  mailingProvince?: string
  mailingPostalCode?: string

  // Direct debit information
  accountName: string
  sortCode: string
  accountNumber: string
  directDebitDate: string // Will be converted to Date

  // Coverage selection
  applianceCoverSelected: boolean
  boilerCoverSelected: boolean
  boilerPriceSelected?: number

  // Total cost
  totalPlanCost: number

  // Appliances (can be JSON string or separate fields)
  appliances?: Array<{
    appliance: string
    otherText?: string
    coverLimit: number
    cost: number
  }>

  // Alternative appliance fields (for CSV compatibility)
  appliance1?: string
  appliance1Cost?: number
  appliance1CoverLimit?: number
  appliance2?: string
  appliance2Cost?: number
  appliance2CoverLimit?: number
  appliance3?: string
  appliance3Cost?: number
  appliance3CoverLimit?: number
  appliance4?: string
  appliance4Cost?: number
  appliance4CoverLimit?: number
  appliance5?: string
  appliance5Cost?: number
  appliance5CoverLimit?: number
  appliance6?: string
  appliance6Cost?: number
  appliance6CoverLimit?: number
  appliance7?: string
  appliance7Cost?: number
  appliance7CoverLimit?: number
  appliance8?: string
  appliance8Cost?: number
  appliance8CoverLimit?: number
  appliance9?: string
  appliance9Cost?: number
  appliance9CoverLimit?: number
  appliance10?: string
  appliance10Cost?: number
  appliance10CoverLimit?: number
}

async function handleImport(request: NextRequest, context: any) {
  const securityContext = createSecurityContext(request)
  
  try {
    // Check authentication (already handled by withSecurity)
    const { user } = context
    
    logSecurityEvent('IMPORT_ATTEMPT', securityContext, { 
      userId: user.id,
      userRole: user.role 
    })

    // Secure file upload handling
    const uploadResult = await handleSecureUpload(
      request, 
      10 * 1024 * 1024, // 10MB max
      ['text/csv', 'application/json'],
      true // Skip content scanning for data files
    )
    
    if (!uploadResult.isValid) {
      logSecurityEvent('IMPORT_INVALID_FILE', securityContext, { 
        error: uploadResult.error,
        userId: user.id
      })
      return NextResponse.json({ 
        success: false,
        error: uploadResult.error 
      }, { status: 400 })
    }

    const file = uploadResult.file
    const formData = await request.formData()
    const format = formData.get('format') as string

    logSecurityEvent('IMPORT_FILE_ACCEPTED', securityContext, {
      fileName: file.name,
      fileSize: file.size,
      format: format,
      userId: user.id
    })

    const fileContent = await file.text()
    let salesData: ImportSaleData[] = []

    // Field mapping from CRM export format to database format
    const fieldMapping: Record<string, string> = {
      'First Name': 'customerFirstName',
      'Last Name': 'customerLastName', 
      'Title': 'title',
      'Phone': 'phoneNumber',
      'Email': 'email',
      'Mailing Street': 'mailingStreet',
      'Mailing City': 'mailingCity',
      'Mailing Province': 'mailingProvince',
      'Mailing Postal Code': 'mailingPostalCode',
      'SortCode': 'sortCode',
      'Acc Number': 'accountNumber',
      'First DD Date': 'directDebitDate',
      'Customer Premium': 'totalPlanCost',
      'DD Amount': 'totalPlanCost',
      'Appliance 1 Type': 'appliance1',
      'Appliance 1 Value': 'appliance1Cost',
      'Appliance 2 Type': 'appliance2',
      'Appliance 2 Value': 'appliance2Cost',
      'Appliance 3 Type': 'appliance3',
      'Appliance 3 Value': 'appliance3Cost',
      'Appliance 4 Type': 'appliance4',
      'Appliance 4 Value': 'appliance4Cost',
      'Appliance 5 Type': 'appliance5',
      'Appliance 5 Value': 'appliance5Cost',
      'Call Notes': 'notes'
    }

    // Function to normalize data from CRM export format to import format
    const normalizeDataRow = (row: any): any => {
      const normalized: any = {}
      
      for (const [key, value] of Object.entries(row)) {
        const mappedKey = fieldMapping[key as string] || key
        normalized[mappedKey] = value
      }
      
      // Handle special cases
      if (normalized['Customer Premium']) {
        // Remove currency symbol and convert to number
        const premium = normalized['Customer Premium']
        if (typeof premium === 'string') {
          normalized.totalPlanCost = parseFloat(premium.replace(/[£$,]/g, '')) || 0
        }
        delete normalized['Customer Premium']
      }
      
      if (normalized['DD Amount']) {
        const ddAmount = normalized['DD Amount']
        if (typeof ddAmount === 'string') {
          normalized.totalPlanCost = parseFloat(ddAmount.replace(/[£$,]/g, '')) || 0
        }
        delete normalized['DD Amount']
      }
      
      // Set account name from customer name if missing
      if (!normalized.accountName && normalized.customerFirstName && normalized.customerLastName) {
        normalized.accountName = `${normalized.customerFirstName} ${normalized.customerLastName}`
      }
      
      // Default values for required fields that might be missing
      if (!normalized.applianceCoverSelected && (normalized.appliance1 || normalized.appliance2)) {
        normalized.applianceCoverSelected = true
      }
      
      if (!normalized.boilerCoverSelected && normalized.boilerPriceSelected) {
        normalized.boilerCoverSelected = true
      }
      
      return normalized
    }

    // Parse based on format
    if (format === 'csv') {
      const parseResult = Papa.parse(fileContent, {
        header: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.trim()
      })

      if (parseResult.errors.length > 0) {
        logSecurityEvent('IMPORT_CSV_ERROR', securityContext, { 
          errors: parseResult.errors,
          userId: user.id
        })
        return NextResponse.json({ 
          error: 'CSV parsing error', 
          details: parseResult.errors 
        }, { status: 400 })
      }

      // Normalize the data from CRM export format
      salesData = parseResult.data.map(normalizeDataRow) as ImportSaleData[]
    } else if (format === 'json') {
      try {
        const jsonData = JSON.parse(fileContent)
        salesData = Array.isArray(jsonData) ? jsonData : [jsonData]
        console.log('Parsed JSON data:', salesData.length, 'items')
        console.log('First item keys:', Object.keys(salesData[0] || {}))
      } catch (error) {
        logSecurityEvent('IMPORT_JSON_ERROR', securityContext, { 
          error: error instanceof Error ? error.message : 'Unknown error',
          userId: user.id
        })
        return NextResponse.json({ 
          success: false,
          error: 'Invalid JSON format',
          imported: 0,
          total: 0
        }, { status: 400 })
      }
    } else {
      return NextResponse.json({ 
        error: 'Unsupported format. Use csv or json' 
      }, { status: 400 })
    }

    // Process and validate each sale
    const processedSales = []
    const errors = []

    for (let i = 0; i < salesData.length; i++) {
      const saleData = salesData[i]
      
      try {
        // Validate required fields (be more flexible for CRM imports)
        const requiredFields = ['customerFirstName', 'customerLastName', 'phoneNumber', 'email']
        const optionalFields = ['accountName', 'sortCode', 'accountNumber', 'directDebitDate', 'totalPlanCost']
        
        console.log(`Processing row ${i + 1}:`, Object.keys(saleData))
        
        const missingFields = requiredFields.filter(field => !saleData[field as keyof ImportSaleData] || saleData[field as keyof ImportSaleData] === '')
        if (missingFields.length > 0) {
          console.log(`Row ${i + 1} missing critical fields:`, missingFields)
          errors.push({
            row: i + 1,
            error: `Missing required fields: ${missingFields.join(', ')}`
          })
          continue
        }

        // Set default values for missing optional fields
        if (!saleData.accountName) {
          saleData.accountName = `${saleData.customerFirstName} ${saleData.customerLastName}`
        }
        if (!saleData.sortCode) {
          saleData.sortCode = '00-00-00'
        }
        if (!saleData.accountNumber) {
          saleData.accountNumber = '00000000'
        }
        if (!saleData.directDebitDate) {
          saleData.directDebitDate = new Date().toISOString().split('T')[0] // Today's date
        }
        if (!saleData.totalPlanCost || saleData.totalPlanCost === 0) {
          // Calculate from appliances if available
          let calculatedCost = 0
          for (let j = 1; j <= 10; j++) {
            const costField = saleData[`appliance${j}Cost` as keyof ImportSaleData] as number
            if (costField) {
              calculatedCost += Number(costField)
            }
          }
          saleData.totalPlanCost = calculatedCost || 1 // Minimum 1 for validation
        }

        // Process appliances
        const appliances = []
        
        if (saleData.appliances && Array.isArray(saleData.appliances)) {
          // Use appliances array if provided
          appliances.push(...saleData.appliances)
        } else {
          // Check individual appliance fields (for CSV compatibility)
          for (let j = 1; j <= 10; j++) {
            const applianceField = saleData[`appliance${j}` as keyof ImportSaleData] as string
            const costField = saleData[`appliance${j}Cost` as keyof ImportSaleData] as number
            const coverLimitField = saleData[`appliance${j}CoverLimit` as keyof ImportSaleData] as number
            
            if (applianceField && costField && coverLimitField) {
              appliances.push({
                appliance: applianceField,
                otherText: null,
                coverLimit: Number(coverLimitField),
                cost: Number(costField)
              })
            }
          }
        }

        // Create sale object
        const processedSale = {
          customerFirstName: saleData.customerFirstName,
          customerLastName: saleData.customerLastName,
          title: saleData.title || null,
          phoneNumber: saleData.phoneNumber,
          email: saleData.email,
          notes: saleData.notes || null,
          mailingStreet: saleData.mailingStreet || null,
          mailingCity: saleData.mailingCity || null,
          mailingProvince: saleData.mailingProvince || null,
          mailingPostalCode: saleData.mailingPostalCode || null,
          accountName: saleData.accountName,
          sortCode: saleData.sortCode,
          accountNumber: saleData.accountNumber,
          directDebitDate: new Date(saleData.directDebitDate),
          applianceCoverSelected: Boolean(saleData.applianceCoverSelected) || appliances.length > 0,
          boilerCoverSelected: Boolean(saleData.boilerCoverSelected) || Boolean(saleData.boilerPriceSelected),
          boilerPriceSelected: saleData.boilerPriceSelected ? Number(saleData.boilerPriceSelected) : null,
          totalPlanCost: Number(saleData.totalPlanCost),
          createdById: user.id,
          appliances: appliances
        }

        processedSales.push(processedSale)
      } catch (error) {
        errors.push({
          row: i + 1,
          error: `Processing error: ${error instanceof Error ? error.message : 'Unknown error'}`
        })
      }
    }

    if (errors.length > 0 && processedSales.length === 0) {
      return NextResponse.json({ 
        success: false,
        error: 'No valid sales data found', 
        errors,
        imported: 0,
        total: salesData.length
      }, { status: 400 })
    }

    // Save to database with duplicate checking
    const results = []
    const duplicates = []
    
    for (const saleData of processedSales) {
      try {
        // Check for duplicates before creating
        const duplicateCheck = await checkForDuplicate({
          customerFirstName: saleData.customerFirstName,
          customerLastName: saleData.customerLastName,
          email: saleData.email,
          phoneNumber: saleData.phoneNumber
        })

        if (duplicateCheck.isDuplicate) {
          duplicates.push({
            customer: `${saleData.customerFirstName} ${saleData.customerLastName}`,
            email: saleData.email,
            phone: saleData.phoneNumber,
            reason: duplicateCheck.duplicateReason,
            existingCustomer: duplicateCheck.existingCustomer
          })
          console.log(`Skipping duplicate customer: ${saleData.customerFirstName} ${saleData.customerLastName} - ${duplicateCheck.duplicateReason}`)
          continue
        }

        // Create sale if not duplicate
        const sale = await prisma.sale.create({
          data: {
            ...saleData,
            appliances: {
              create: saleData.appliances
            }
          },
          include: {
            appliances: true,
            createdBy: true
          }
        })
        results.push(sale)
      } catch (error) {
        errors.push({
          sale: `${saleData.customerFirstName} ${saleData.customerLastName}`,
          error: `Database error: ${error instanceof Error ? error.message : 'Unknown error'}`
        })
      }
    }

    logSecurityEvent('IMPORT_SUCCESS', securityContext, {
      imported: results.length,
      total: salesData.length,
      duplicatesSkipped: duplicates.length,
      userId: user.id
    })

    return NextResponse.json({
      success: true,
      imported: results.length,
      total: salesData.length,
      skipped: duplicates.length,
      duplicates: duplicates.length > 0 ? duplicates : undefined,
      errors: errors.length > 0 ? errors : undefined,
      data: results,
      summary: {
        totalProcessed: salesData.length,
        imported: results.length,
        duplicatesSkipped: duplicates.length,
        errors: errors.length
      }
    })

  } catch (error) {
    logSecurityEvent('IMPORT_ERROR', securityContext, {
      error: error instanceof Error ? error.message : 'Unknown error',
      userId: context?.user?.id
    })
    console.error('Import error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// Secure API endpoint with authentication and rate limiting
export const POST = withSecurity(handleImport, {
  requireAuth: true,
  requireAdmin: true,
  rateLimit: {
    requests: 10,
    windowMs: 60 * 60 * 1000 // 10 imports per hour
  },
  validateInput: true,
  logAccess: true
})