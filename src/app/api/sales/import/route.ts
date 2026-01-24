import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/prisma'
import Papa from 'papaparse'
import { withSecurity, handleSecureUpload } from '@/lib/apiSecurity'
import { logSecurityEvent, createSecurityContext } from '@/lib/security'

/**
 * Normalize status values from import to match database enum
 */
function normalizeCustomerStatus(status?: string): 'ACTIVE' | 'CANCELLED' | 'CANCELLATION_NOTICE_RECEIVED' | 'FAILED_PAYMENT' | 'PROCESS_DD' {
  if (!status) return 'ACTIVE'
  
  const normalizedStatus = status.toLowerCase().trim()
  console.log(`Normalizing status: "${status}" -> "${normalizedStatus}"`)
  
  // More flexible matching with partial string matching
  if (normalizedStatus.includes('cancel')) {
    if (normalizedStatus.includes('notice') || normalizedStatus.includes('cnr')) {
      console.log(`Matched CANCELLATION_NOTICE_RECEIVED for: ${status}`)
      return 'CANCELLATION_NOTICE_RECEIVED'
    } else {
      console.log(`Matched CANCELLED for: ${status}`)
      return 'CANCELLED'
    }
  }
  
  if (normalizedStatus.includes('fail') && normalizedStatus.includes('payment')) {
    console.log(`Matched FAILED_PAYMENT for: ${status}`)
    return 'FAILED_PAYMENT'
  }
  
  if (normalizedStatus.includes('process') && normalizedStatus.includes('dd')) {
    console.log(`Matched PROCESS_DD for: ${status}`)
    return 'PROCESS_DD'
  }
  
  if (normalizedStatus.includes('active')) {
    console.log(`Matched ACTIVE for: ${status}`)
    return 'ACTIVE'
  }
  
  console.log(`No match found for "${status}", defaulting to ACTIVE`)
  return 'ACTIVE' // Default fallback
}

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
  mailingStreet?: string
  mailingCity?: string
  mailingPostalCode?: string
}): Promise<DuplicateCheckResult> {
  const { customerFirstName, customerLastName, email, phoneNumber, mailingStreet, mailingCity, mailingPostalCode } = customerData

  console.log(`🔍 Checking for duplicate: ${customerFirstName} ${customerLastName}, Phone: ${phoneNumber}, Address: ${mailingStreet}, ${mailingCity}, ${mailingPostalCode}`)

  // Skip duplicate checking if essential fields are missing
  if (!customerFirstName || !customerLastName || !phoneNumber) {
    console.log(`⚠️ Skipping duplicate check due to missing required fields (name or phone)`)
    return {
      isDuplicate: false,
      existingCustomer: undefined,
      duplicateReason: undefined
    }
  }

  // Normalize phone number for comparison (remove spaces, dashes, etc.)
  const normalizedPhone = phoneNumber.replace(/[\s\-\(\)+]/g, '')

  // Check for duplicate based on: same name + same phone + same address
  const duplicateMatch = await prisma.sale.findFirst({
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
        },
        {
          OR: [
            { phoneNumber: phoneNumber },
            { phoneNumber: normalizedPhone },
            { phoneNumber: { contains: normalizedPhone.slice(-10) } } // Last 10 digits for different formats
          ]
        },
        // Address matching (if provided)
        ...(mailingStreet ? [{
          mailingStreet: {
            equals: mailingStreet,
            mode: 'insensitive' as const
          }
        }] : []),
        ...(mailingPostalCode ? [{
          mailingPostalCode: {
            equals: mailingPostalCode,
            mode: 'insensitive' as const
          }
        }] : [])
      ]
    },
    select: {
      id: true,
      customerFirstName: true,
      customerLastName: true,
      email: true,
      phoneNumber: true,
      createdAt: true,
      mailingStreet: true,
      mailingCity: true,
      mailingPostalCode: true
    }
  })

  if (duplicateMatch) {
    console.log(`❌ Duplicate found: ${duplicateMatch.customerFirstName} ${duplicateMatch.customerLastName}, Phone: ${duplicateMatch.phoneNumber}, Address: ${duplicateMatch.mailingStreet}`)
    return {
      isDuplicate: true,
      existingCustomer: duplicateMatch,
      duplicateReason: 'Same name, phone number, and address'
    }
  }

  console.log(`✅ No duplicate found for: ${customerFirstName} ${customerLastName}`)

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
  status?: string

  // Sales agent information
  salesAgentName?: string
  salesAgentId?: string

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
  customerPackage?: string // Store what's covered for reference

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
    const formData = await request.formData()
    const file = formData.get('file') as File
    const format = formData.get('format') as string
    
    console.log('🚀 IMPORT PROCESS STARTED')
    console.log('📁 File:', file?.name)
    console.log('📋 Format:', format)
    
    if (!file) {
      return NextResponse.json({ 
        success: false,
        error: 'No file provided' 
      }, { status: 400 })
    }
    
    // Check file size
    if (file.size > 10 * 1024 * 1024) { // 10MB max
      return NextResponse.json({ 
        success: false,
        error: 'File too large' 
      }, { status: 400 })
    }
    
    // Check file type
    const allowedTypes = ['text/csv', 'application/json']
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json({ 
        success: false,
        error: 'Invalid file type' 
      }, { status: 400 })
    }

    logSecurityEvent('IMPORT_FILE_ACCEPTED', securityContext, {
      fileName: file.name,
      fileSize: file.size,
      format: format,
      userId: user.id
    })

    const fileContent = await file.text()
    let salesData: ImportSaleData[] = []

    // DEBUG: Show raw file content (first 500 characters)
    console.log('🔍 RAW FILE CONTENT (first 500 chars):', fileContent.substring(0, 500))
    console.log('🔍 FILE CONTENT LINES COUNT:', fileContent.split('\n').length)

    // Field mapping from CRM export format to database format
    const fieldMapping: Record<string, string> = {
      'First Name': 'customerFirstName',
      'Last Name': 'customerLastName', 
      'Name': 'fullName', // For simple CSV format - will be split later
      'Full Name': 'fullName', // Alternative full name field
      'Customer Name': 'fullName', // Another alternative
      'Title': 'title',
      'Phone': 'phoneNumber',
      'Phone Number': 'phoneNumber',
      'Plain Phone': 'phoneNumber',
      'Mobile': 'phoneNumber', // Alternative phone field
      'Email': 'email',
      'Email Address': 'email', // Alternative email field
      'Mailing Street': 'mailingStreet',
      'First Line Add': 'mailingStreet',
      'Mailing City': 'mailingCity',
      'Mailing Province': 'mailingProvince',
      'Mailing Postal Code': 'mailingPostalCode',
      'SortCode': 'sortCode',
      'Acc Number': 'accountNumber',
      'First DD Date': 'directDebitDate',
      'Date of Sale': 'saleDate', // Use special field name for sale date
      'Sale Date': 'saleDate',
      'Created Date': 'saleDate',
      'Customer Premium': 'totalPlanCost',
      'Customer Package': 'customerPackage', // Store what's covered for reference
      'DD Amount': 'totalPlanCost',
      'App Bundle Price': 'totalPlanCost', // Map directly to totalPlanCost
      'App Bundle Price (Internal)': 'totalPlanCost', // Alternative name
      'Single App Price': 'totalPlanCost', // Map directly to totalPlanCost
      'Single App Price (Internal)': 'totalPlanCost', // Alternative name
      'Boiler Package Price': 'totalPlanCost', // Map directly to totalPlanCost
      'Boiler Package Price (Internal)': 'boilerPriceSelected',
      'Total Cost': 'totalPlanCost',
      'Monthly Cost': 'totalPlanCost',
      'Premium': 'totalPlanCost',
      'Price': 'totalPlanCost',
      'Cost': 'totalPlanCost',
      'Amount': 'totalPlanCost',
      'Monthly Premium': 'totalPlanCost',
      'Monthly Payment': 'totalPlanCost',
      'Payment Amount': 'totalPlanCost',
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
      'Appliance 6 Type': 'appliance6',
      'Appliance 6 Value': 'appliance6Cost',
      'Appliance 7 Type': 'appliance7',
      'Appliance 7 Value': 'appliance7Cost',
      'Appliance 8 Type': 'appliance8',
      'Appliance 8 Value': 'appliance8Cost',
      'Appliance 9 Type': 'appliance9',
      'Appliance 9 Value': 'appliance9Cost',
      'Appliance 10 Type': 'appliance10',
      'Appliance 10 Value': 'appliance10Cost',
      // ACTUAL CSV FIELD NAMES (based on real CSV structure)
      'salesAgentId': 'salesAgentId',
      'salesAgentName': 'salesAgentName',
      'customerFirstName': 'customerFirstName',
      'customerLastName': 'customerLastName',
      'title': 'title',
      'phoneNumber': 'phoneNumber',
      'mailingStreet': 'mailingStreet',
      'mailingCity': 'mailingCity',
      'mailingPostalCode': 'mailingPostalCode',
      'status': 'status',
      'sortCode': 'sortCode',
      'accountNumber': 'accountNumber',
      'customerPackage': 'customerPackage',
      'directDebitDate': 'directDebitDate',
      'appliance1': 'appliance1',
      'appliance2': 'appliance2',
      'appliance3': 'appliance3',
      'appliance4': 'appliance4',
      'appliance1Cost': 'appliance1Cost',
      'appliance2Cost': 'appliance2Cost',
      'appliance3Cost': 'appliance3Cost',
      'appliance4Cost': 'appliance4Cost',
      'accountName': 'accountName',
      'applianceCoverSelected': 'applianceCoverSelected',
      'appliance1CoverLimit': 'appliance1CoverLimit',
      'appliance2CoverLimit': 'appliance2CoverLimit',
      'appliance3CoverLimit': 'appliance3CoverLimit',
      'appliance4CoverLimit': 'appliance4CoverLimit',
      'Call Notes': 'notes',
      'Description': 'notes',
      'Customers Name': '_ignore', // Calculated field
      'Lead Source': '_ignore',
      'Payment Method': '_ignore',
      'Status': 'status',
      'Brand': '_ignore',
      'Processor': '_ignore',
      'Record Id': '_ignore',
      'Customers Owner.id': 'salesAgentId',
      'Customers Owner': 'salesAgentName',
      'Lead Sales Agent': 'salesAgentName',
      'Sales Agent': 'salesAgentName',
      'Agent': 'salesAgentName',
      'Sold By': 'salesAgentName',
      'Rep': 'salesAgentName',
      'Representative': 'salesAgentName',
      'Advisor': 'salesAgentName',
      'Sales Rep': 'salesAgentName',
      'Date of Birth': '_ignore',
      'Modified By.id': '_ignore',
      'Modified By': '_ignore',
      'Modified Time': '_ignore',
      'Salutation': '_ignore',
      'Last Activity Time': '_ignore',
      'Tag': '_ignore',
      'Unsubscribed Mode': '_ignore',
      'Unsubscribed Time': '_ignore',
      'Change Log Time': '_ignore',
      'Locked': '_ignore',
      'Last Enriched Time': '_ignore',
      'Enrich Status': '_ignore'
    }

    // Function to normalize data from CRM export format to import format
    const normalizeDataRow = (row: any): any => {
      const normalized: any = {}
      
      console.log(`🔧 Normalizing row with keys:`, Object.keys(row))
      console.log(`🔧 Raw row data sample:`, JSON.stringify(row, null, 2).substring(0, 500) + '...')
      
      // Track pricing fields specifically
      const foundPricingFields: string[] = []
      
      for (const [key, value] of Object.entries(row)) {
        const mappedKey = fieldMapping[key as string] || key
        
        console.log(`🗺️ Mapping "${key}" -> "${mappedKey}" (value: "${value}")`)
        
        // Track pricing-related fields
        if (key.toLowerCase().includes('price') || key.toLowerCase().includes('amount') || 
            key.toLowerCase().includes('cost') || key.toLowerCase().includes('premium') ||
            key.toLowerCase().includes('dd')) {
          foundPricingFields.push(`${key}: "${value}"`)
        }
        
        // Skip fields marked to ignore
        if (mappedKey === '_ignore') {
          continue
        }
        
        // Skip empty values
        if (value === '' || value === null || value === undefined) {
          continue
        }
        
        normalized[mappedKey] = value
      }
      
      console.log(`💰 Found pricing fields in this row:`, foundPricingFields)
      
      // Handle fullName field (split into first and last name)
      if (normalized.fullName && !normalized.customerFirstName && !normalized.customerLastName) {
        const nameParts = normalized.fullName.trim().split(/\s+/)
        if (nameParts.length >= 2) {
          normalized.customerFirstName = nameParts[0]
          normalized.customerLastName = nameParts.slice(1).join(' ') // Everything after first name as last name
        } else if (nameParts.length === 1) {
          normalized.customerFirstName = nameParts[0]
          normalized.customerLastName = '' // Set empty last name
        }
        delete normalized.fullName // Remove the fullName field
      }
      
      // Handle special cases for currency fields and pricing
      let totalCost = 0
      let boilerPrice = 0
      
      // Check various price fields in order of priority
      const priceFields = [
        'DD Amount', // High priority - direct pricing field
        'App Bundle Price', // High priority - direct pricing field
        'App Bundle Price (Internal)', 
        'Single App Price',
        'Single App Price (Internal)',
        'Boiler Package Price',
        'Boiler Package Price (Internal)', 
        'Customer Premium', 
        'totalPlanCost',
        'Total Cost',
        'Monthly Cost',
        'Premium',
        'Price',
        'Cost',
        'Amount',
        'Monthly Premium',
        'Monthly Payment',
        'Payment Amount'
      ]
      
      console.log(`🔍 Checking pricing fields for row:`, Object.keys(normalized))
      console.log(`🔍 Available data:`, JSON.stringify(normalized, null, 2))
      
      for (const priceField of priceFields) {
        const mappedField = fieldMapping[priceField] || priceField
        const value = normalized[mappedField] || normalized[priceField]
        
        if (value !== undefined && value !== null && value !== '') {
          console.log(`💰 Found price field "${priceField}" -> "${mappedField}": "${value}" (type: ${typeof value})`)
          
          let parsedPrice = 0
          if (typeof value === 'string') {
            parsedPrice = parseFloat(value.replace(/[£$,\s]/g, '')) || 0
          } else if (typeof value === 'number') {
            parsedPrice = value
          }
          
          if (parsedPrice > 0) {
            console.log(`💰 Parsed price: £${parsedPrice}`)
            if (priceField === 'Boiler Package Price (Internal)') {
              boilerPrice = parsedPrice
              normalized.boilerPriceSelected = parsedPrice
              normalized.boilerCoverSelected = true
              totalCost = parsedPrice // Use boiler price as total cost
              console.log(`🔧 Set boiler price and total cost: £${parsedPrice}`)
              break // Found boiler pricing, use this as total
            } else if (priceField === 'Single App Price (Internal)' || priceField === 'App Bundle Price (Internal)') {
              totalCost = parsedPrice
              normalized.applianceCoverSelected = true // Set appliance cover for app pricing
              console.log(`🔧 Set appliance total cost: £${parsedPrice}`)
              break // Found appliance pricing, use this as total
            } else {
              totalCost = parsedPrice
              console.log(`💷 Set total cost: £${parsedPrice}`)
              break // Stop on first valid total cost found
            }
          } else {
            console.log(`⚠️ Price field "${priceField}" has invalid value: "${value}" -> ${parsedPrice}`)
          }
          // Clean up the original field
          delete normalized[priceField]
          delete normalized[mappedField]
        }
      }
      
      // Set total cost from the highest priority field found
      if (totalCost > 0) {
        normalized.totalPlanCost = totalCost
        console.log(`✅ Final total cost set: £${totalCost}`)
      } else if (boilerPrice > 0) {
        normalized.totalPlanCost = boilerPrice
        console.log(`✅ Using boiler price as total cost: £${boilerPrice}`)
      } else {
        console.log(`⚠️ No pricing found in any price field`)
        
        // Try to calculate total from individual appliance costs
        const applianceCosts = [
          normalized.appliance1Cost,
          normalized.appliance2Cost,
          normalized.appliance3Cost,
          normalized.appliance4Cost
        ]
        
        let calculatedTotal = 0
        const validCosts: number[] = []
        
        for (let i = 0; i < applianceCosts.length; i++) {
          const cost = applianceCosts[i]
          if (cost !== undefined && cost !== null && cost !== '') {
            let parsedCost = 0
            if (typeof cost === 'string') {
              parsedCost = parseFloat(cost.replace(/[£$,\s]/g, '')) || 0
            } else if (typeof cost === 'number') {
              parsedCost = cost
            }
            
            if (parsedCost > 0) {
              validCosts.push(parsedCost)
              calculatedTotal += parsedCost
              console.log(`💰 Appliance ${i + 1} cost: £${parsedCost}`)
            }
          }
        }
        
        if (calculatedTotal > 0) {
          normalized.totalPlanCost = calculatedTotal
          normalized.applianceCoverSelected = true
          console.log(`✅ Calculated total from appliance costs: £${calculatedTotal} (from ${validCosts.length} appliances)`)
        } else {
          console.log(`❌ No valid appliance costs found either`)
        }
      }
      
      // Handle Date of Sale vs Created Date with enhanced parsing
      const dateFields = [
        'saleDate', 'Date of Sale', 'Sale Date', 'Created Date', 'createdAt', '_saleDate',
        'directDebitDate' // Add directDebitDate as potential sale date
      ]
      let foundDate = false
      
      for (const dateField of dateFields) {
        if (normalized[dateField] && !foundDate) {
          console.log(`📅 Processing date field "${dateField}": ${normalized[dateField]}`)
          // Parse the date of sale for when the record was actually created
          const saleDate = new Date(normalized[dateField])
          if (!isNaN(saleDate.getTime())) {
            normalized._saleDate = saleDate // Store for later use
            console.log(`✅ Parsed sale date: ${saleDate.toISOString()}`)
            foundDate = true // Stop after finding first valid date
          } else {
            console.log(`❌ Invalid date format: ${normalized[dateField]}`)
          }
        }
      }
      
      // If no valid sale date found, check raw row data for common date patterns
      if (!foundDate) {
        console.log(`⚠️ No date found in normalized fields, checking raw row data...`)
        console.log(`⚠️ Available raw fields:`, Object.keys(row))
        
        // Check for common date field names in the raw CSV
        const rawDateFields = [
          'Date of Sale', 'Sale Date', 'Created Date', 'Date Created', 'Transaction Date', 'Order Date',
          'directDebitDate' // Add directDebitDate for raw CSV checking too
        ]
        for (const rawDateField of rawDateFields) {
          if (row[rawDateField] && !foundDate) {
            console.log(`📅 Found raw date field "${rawDateField}": ${row[rawDateField]}`)
            const saleDate = new Date(row[rawDateField])
            if (!isNaN(saleDate.getTime())) {
              normalized._saleDate = saleDate
              console.log(`✅ Parsed raw sale date: ${saleDate.toISOString()}`)
              foundDate = true
            }
          }
        }
      }
      
      if (!foundDate) {
        console.log(`⚠️ No valid sale date found, checking if directDebitDate can be used...`)
        
        // Try to use directDebitDate as sale date if no other date is available
        if (normalized.directDebitDate) {
          console.log(`📅 Trying to use directDebitDate as sale date: ${normalized.directDebitDate}`)
          const directDebitDate = new Date(normalized.directDebitDate)
          if (!isNaN(directDebitDate.getTime())) {
            normalized._saleDate = directDebitDate
            console.log(`✅ Using directDebitDate as sale date: ${directDebitDate.toISOString()}`)
            foundDate = true
          } else {
            console.log(`❌ Invalid directDebitDate format: ${normalized.directDebitDate}`)
          }
        }
      }
      
      if (!foundDate) {
        console.log(`⚠️ No valid sale date found anywhere, will use current date as fallback`)
      }
      
      // Clean up date fields to avoid confusion
      dateFields.forEach(field => delete normalized[field])
      
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
      
      // Set coverage based on Customer Package field
      if (normalized.customerPackage) {
        const packageLower = normalized.customerPackage.toLowerCase()
        if (packageLower.includes('boiler')) {
          normalized.boilerCoverSelected = true
        }
        if (packageLower.includes('appliance') || packageLower.includes('app')) {
          normalized.applianceCoverSelected = true
        }
        console.log(`📦 Customer Package: "${normalized.customerPackage}" -> Boiler: ${normalized.boilerCoverSelected}, Appliances: ${normalized.applianceCoverSelected}`)
      }
      
      // Add cover limits for appliances (default to common values if missing)
      for (let i = 1; i <= 10; i++) {
        const applianceField = `appliance${i}`
        const costField = `appliance${i}Cost`
        const coverLimitField = `appliance${i}CoverLimit`
        
        if (normalized[applianceField] && normalized[costField] && !normalized[coverLimitField]) {
          // Set default cover limits based on appliance type
          const applianceType = normalized[applianceField].toLowerCase()
          if (applianceType.includes('washing machine') || applianceType.includes('dishwasher')) {
            normalized[coverLimitField] = 600
          } else if (applianceType.includes('refrigerator') || applianceType.includes('fridge')) {
            normalized[coverLimitField] = 400
          } else if (applianceType.includes('oven') || applianceType.includes('cooker')) {
            normalized[coverLimitField] = 800
          } else {
            normalized[coverLimitField] = 500 // Default
          }
        }
      }
      
      console.log(`✅ Normalized result:`, {
        customerFirstName: normalized.customerFirstName,
        customerLastName: normalized.customerLastName,
        email: normalized.email,
        phoneNumber: normalized.phoneNumber,
        fullName: normalized.fullName
      })
      
      return normalized
    }

    // Parse based on format
    if (format === 'csv') {
      const parseResult = Papa.parse(fileContent, {
        header: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.trim()
      })

      console.log('🔍 CSV PARSING DEBUG:')
      console.log('📋 Raw CSV Headers (first 5 rows):', parseResult.data.slice(0, 5))
      console.log('📋 All CSV Headers found:', parseResult.meta?.fields || 'No headers detected')
      console.log('📋 Total rows parsed:', parseResult.data.length)
      
      // DEBUG: Show actual CSV header line
      const csvLines = fileContent.split('\n')
      console.log('🔍 ACTUAL CSV HEADER LINE:', csvLines[0])
      console.log('🔍 SECOND CSV LINE (first data):', csvLines[1])
      
      // DEBUG: Show specific rows around Row 194
      if (parseResult.data.length > 193) {
        const row194 = parseResult.data[193] as any
        console.log('🔍 ROW 194 RAW DATA:', JSON.stringify(row194, null, 2))
        console.log('🔍 ROW 194 AVAILABLE KEYS:', Object.keys(row194))
      }
      
      if (parseResult.errors && parseResult.errors.length > 0) {
        console.error('🚨 CSV Parsing Errors:', parseResult.errors)
      }

      console.log('🔍 CSV Headers found:', parseResult.meta.fields)
      console.log('🔧 Field mapping available:', Object.keys(fieldMapping))

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
        // Validate required fields (be very lenient for CRM imports)
        const criticalFields = ['customerFirstName', 'customerLastName']
        const contactFields = ['phoneNumber', 'email']
        
        console.log(`Processing row ${i + 1}:`, Object.keys(saleData))
        console.log(`🔄 Raw data for row ${i + 1}:`, {
          customerFirstName: saleData.customerFirstName,
          customerLastName: saleData.customerLastName,
          email: saleData.email,
          phoneNumber: saleData.phoneNumber,
          salesAgentName: saleData.salesAgentName,
          totalPlanCost: saleData.totalPlanCost,
          dateOfSale: (saleData as any)._saleDate || 'Not specified'
        })
        
        // Check for critical fields (name)
        const missingCritical = criticalFields.filter(field => !saleData[field as keyof ImportSaleData] || saleData[field as keyof ImportSaleData] === '')
        if (missingCritical.length > 0) {
          console.log(`Row ${i + 1} missing critical fields:`, missingCritical)
          errors.push({
            row: i + 1,
            error: `Missing critical fields: ${missingCritical.join(', ')}`
          })
          continue
        }
        
        // Check for at least one contact method (phone OR email)
        const hasPhone = saleData.phoneNumber && saleData.phoneNumber !== ''
        const hasEmail = saleData.email && saleData.email !== ''
        
        if (!hasPhone && !hasEmail) {
          console.log(`Row ${i + 1} missing both phone and email`)
          errors.push({
            row: i + 1,
            error: `Missing both phone and email - need at least one contact method`
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
          const rawRow = salesData[i] as any // Get the actual raw CSV row
          
          console.log(`⚠️ Row ${i + 1}: Missing or zero totalPlanCost, attempting to calculate from appliances...`)
          console.log(`⚠️ Row ${i + 1}: Current saleData.totalPlanCost = "${saleData.totalPlanCost}"`)
          console.log(`🔍 Row ${i + 1}: RAW CSV DATA:`, JSON.stringify(rawRow, null, 2))
          console.log(`🔍 Row ${i + 1}: Raw CSV Headers:`, Object.keys(rawRow))
          console.log(`💰 Row ${i + 1}: DD Amount in raw:`, rawRow['DD Amount'])
          console.log(`💰 Row ${i + 1}: App Bundle Price in raw:`, rawRow['App Bundle Price'])
          console.log(`💰 Row ${i + 1}: Customer Premium in raw:`, rawRow['Customer Premium'])
          console.log(`🔍 Row ${i + 1}: All price-related fields in raw:`)
          
          // Show all fields that might contain pricing
          Object.keys(rawRow).forEach(key => {
            if (key.toLowerCase().includes('price') || key.toLowerCase().includes('amount') || 
                key.toLowerCase().includes('cost') || key.toLowerCase().includes('premium') ||
                key.toLowerCase().includes('dd')) {
              console.log(`  💷 "${key}": "${rawRow[key]}"`)
            }
          })
          
          console.log(`⚠️ Row ${i + 1}: Normalized sale data keys:`, Object.keys(saleData))
          
          // Calculate from appliances if available
          let calculatedCost = 0
          for (let j = 1; j <= 10; j++) {
            const costField = saleData[`appliance${j}Cost` as keyof ImportSaleData] as number
            if (costField && !isNaN(costField)) {
              calculatedCost += Number(costField)
              console.log(`  - appliance${j}Cost: £${costField}`)
            }
          }
          
          if (calculatedCost > 0) {
            saleData.totalPlanCost = calculatedCost
            console.log(`✅ Row ${i + 1}: Calculated total cost from appliances: £${calculatedCost}`)
          } else {
            // 🚨 CRITICAL: Never set arbitrary £1.00 - this corrupts pricing data
            console.error(`❌ Row ${i + 1}: No valid pricing found - SKIPPING to prevent data corruption`)
            console.error(`❌ Row ${i + 1}: Actual CSV column headers:`, Object.keys(rawRow))
            errors.push({
              row: i + 1,
              error: `Missing pricing information. Raw CSV headers: ${Object.keys(rawRow).join(', ')}`
            })
            continue // Skip this row instead of corrupting pricing
          }
        }
        
        // 🚨 CRITICAL DATA PROTECTION: Never generate fake customer data
        // Set default contact info if missing - NEVER SIMULATE REAL DATA
        if (!hasPhone) {
          // Use empty string instead of fake phone number
          saleData.phoneNumber = '' // NO fake numbers - customer data integrity is critical
        }
        if (!hasEmail) {
          // 🔒 DATA PROTECTION: NEVER generate placeholder emails
          // Leave email blank - NEVER create @placeholder.com, @example.com, or any fake emails
          saleData.email = '' // Empty string only - preserves data integrity
        }

        // 🛡️ ADDITIONAL DATA VALIDATION: Check for accidentally imported fake data
        if (saleData.email && (
          saleData.email.includes('@placeholder.') ||
          saleData.email.includes('@example.') ||
          saleData.email.includes('@test.') ||
          saleData.email.includes('@fake.') ||
          saleData.email.includes('@demo.')
        )) {
          // Reject any fake emails that might have been imported
          throw new Error(`CRITICAL: Fake email detected: ${saleData.email}. Customer data integrity violation.`)
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
            
            if (applianceField && applianceField !== '') {
              // Parse cost - handle various formats and default to reasonable values
              let cost = 0
              if (costField !== undefined && costField !== null) {
                const parsedCost = typeof costField === 'string' 
                  ? parseFloat((costField as string).replace(/[£$,]/g, '')) 
                  : Number(costField)
                cost = isNaN(parsedCost) ? 0 : parsedCost
              }
              
              // If cost is 0 or missing, set reasonable defaults based on appliance type
              if (cost <= 0) {
                const applianceType = applianceField.toLowerCase()
                if (applianceType.includes('washing machine')) cost = 19.99
                else if (applianceType.includes('fridge') || applianceType.includes('freezer')) cost = 10.00
                else if (applianceType.includes('dishwasher')) cost = 15.00
                else if (applianceType.includes('oven') || applianceType.includes('cooker')) cost = 25.00
                else if (applianceType.includes('hob')) cost = 4.99
                else cost = 15.00 // Default appliance cost
              }
              
              // Parse cover limit
              let coverLimit = coverLimitField
              if (!coverLimit || coverLimit === 0) {
                const applianceType = applianceField.toLowerCase()
                if (applianceType.includes('washing machine') || applianceType.includes('dishwasher')) {
                  coverLimit = 600
                } else if (applianceType.includes('fridge') || applianceType.includes('freezer')) {
                  coverLimit = 400
                } else if (applianceType.includes('oven') || applianceType.includes('cooker')) {
                  coverLimit = 800
                } else {
                  coverLimit = 500 // Default
                }
              }
              
              appliances.push({
                appliance: applianceField,
                otherText: null,
                coverLimit: Number(coverLimit),
                cost: Number(cost)
              })
            }
          }
        }

        // Create sale object with proper date handling
        const saleDate = (saleData as any)._saleDate || new Date() // Use Date of Sale or current date as fallback
        console.log(`📅 Final sale date for ${saleData.customerFirstName} ${saleData.customerLastName}: ${saleDate.toISOString()}`)
        
        // Resolve sales agent ID with enhanced lookup
        let salesAgentId = user.id // Default to importing user
        let resolvedAgentInfo = `${user.email} (importing user)`
        
        if (saleData.salesAgentName && saleData.salesAgentName.trim() !== '') {
          console.log(`🔍 Looking up sales agent: "${saleData.salesAgentName}"`)
          
          // Multiple lookup strategies for sales agent resolution
          const agentSearchTerm = saleData.salesAgentName.trim()
          
          // Strategy 1: Direct email match
          let salesAgent = await prisma.user.findFirst({
            where: {
              email: { equals: agentSearchTerm, mode: 'insensitive' }
            },
            select: { id: true, email: true }
          })
          
          // Strategy 2: Partial email search if direct lookup failed
          if (!salesAgent) {
            // Extract potential email parts from the search term
            const emailPattern = /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/
            const emailMatch = agentSearchTerm.match(emailPattern)
            
            if (emailMatch) {
              salesAgent = await prisma.user.findFirst({
                where: {
                  email: { equals: emailMatch[1], mode: 'insensitive' }
                },
                select: { id: true, email: true }
              })
            } else {
              // Try partial email matching by assuming the search term might be part of an email
              salesAgent = await prisma.user.findFirst({
                where: {
                  email: { contains: agentSearchTerm.toLowerCase().replace(/\s+/g, ''), mode: 'insensitive' }
                },
                select: { id: true, email: true }
              })
            }
          }
          
          // Strategy 3: Look for emails that start with the search term (for names like "John Smith" -> "john.smith@")
          if (!salesAgent) {
            const nameToEmail = agentSearchTerm.toLowerCase().replace(/\s+/g, '.')
            salesAgent = await prisma.user.findFirst({
              where: {
                email: { startsWith: nameToEmail, mode: 'insensitive' }
              },
              select: { id: true, email: true }
            })
          }
          
          if (salesAgent) {
            salesAgentId = salesAgent.id
            resolvedAgentInfo = `${salesAgent.email}`
            console.log(`✅ Found sales agent: ${resolvedAgentInfo}`)
          } else {
            console.log(`⚠️ Sales agent not found: "${agentSearchTerm}", defaulting to importing user`)
            resolvedAgentInfo = `${user.email} (importing user - original: "${agentSearchTerm}")`
          }
        }
        
        console.log(`👤 Using sales agent: ${resolvedAgentInfo}`)
        
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
          status: normalizeCustomerStatus(saleData.status),
          applianceCoverSelected: Boolean(saleData.applianceCoverSelected) || appliances.length > 0,
          boilerCoverSelected: Boolean(saleData.boilerCoverSelected) || Boolean(saleData.boilerPriceSelected),
          boilerPriceSelected: saleData.boilerPriceSelected ? Number(saleData.boilerPriceSelected) : null,
          totalPlanCost: Number(saleData.totalPlanCost),
          createdById: salesAgentId,
          agentName: saleData.salesAgentName || null, // Store original agent name for reference
          createdAt: saleDate, // Set the actual sale date
          appliances: appliances,
          originalRowNumber: i + 2 // Keep for duplicate tracking only, don't save to DB
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
          phoneNumber: saleData.phoneNumber,
          mailingStreet: saleData.mailingStreet || undefined,
          mailingCity: saleData.mailingCity || undefined,
          mailingPostalCode: saleData.mailingPostalCode || undefined
        })

        if (duplicateCheck.isDuplicate) {
          duplicates.push({
            customer: `${saleData.customerFirstName} ${saleData.customerLastName}`,
            email: saleData.email,
            phone: saleData.phoneNumber,
            reason: duplicateCheck.duplicateReason,
            existingCustomer: duplicateCheck.existingCustomer,
            data: {
              postcode: saleData.mailingPostalCode || '',
              address: `${saleData.mailingStreet || ''} ${saleData.mailingCity || ''}`.trim(),
              accountName: saleData.accountName || '',
              directDebitDate: saleData.directDebitDate || '',
              totalCost: saleData.totalPlanCost || 0,
              applianceCover: saleData.applianceCoverSelected || false,
              boilerCover: saleData.boilerCoverSelected || false,
              originalRowNumber: (saleData as any).originalRowNumber || 0
            }
          })
          console.log(`Skipping duplicate customer: ${saleData.customerFirstName} ${saleData.customerLastName} - ${duplicateCheck.duplicateReason}`)
          continue
        }

        // Create sale if not duplicate
        const { originalRowNumber, ...saleDataForDB } = saleData as any
        const sale = await prisma.sale.create({
          data: {
            ...saleDataForDB,
            appliances: {
              create: saleDataForDB.appliances
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
  validateInput: false, // Disable for file uploads - we handle validation internally
  logAccess: true
})