import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

interface DataIntegrityCheck {
  tableName: string
  recordCount: number
  sampleRecords: any[]
  dataIntegrityHash: string
  customerDataFields: string[]
}

interface IntegrityReport {
  timestamp: string
  totalRecords: number
  tables: DataIntegrityCheck[]
  criticalCustomerData: {
    salesCount: number
    uniqueCustomers: number
    emailsWithData: number
    phonesWithData: number
    addressesWithData: number
  }
}

// 🔒 DATA PROTECTION: Generate hash of customer data to detect any modifications
function generateDataHash(data: any[]): string {
  const serialized = JSON.stringify(data.sort((a, b) => a.id?.localeCompare(b.id) || 0))
  let hash = 0
  for (let i = 0; i < serialized.length; i++) {
    const char = serialized.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32-bit integer
  }
  return hash.toString(36)
}

// 🛡️ CUSTOMER DATA PROTECTION: Validate that customer data contains no fake/corrupted information
function validateCustomerDataIntegrity(sales: any[]): { valid: boolean; issues: string[] } {
  const issues: string[] = []

  for (const sale of sales) {
    // Check for fake email domains
    if (sale.email && (
      sale.email.includes('@placeholder.') ||
      sale.email.includes('@example.') ||
      sale.email.includes('@test.') ||
      sale.email.includes('@fake.') ||
      sale.email.includes('@demo.')
    )) {
      issues.push(`CRITICAL: Fake email detected: ${sale.email} for customer ${sale.customerFirstName} ${sale.customerLastName}`)
    }

    // Check for obviously fake names
    if (sale.customerFirstName?.toLowerCase().includes('test') || 
        sale.customerLastName?.toLowerCase().includes('test') ||
        sale.customerFirstName?.toLowerCase().includes('fake') || 
        sale.customerLastName?.toLowerCase().includes('fake')) {
      issues.push(`WARNING: Suspicious customer name: ${sale.customerFirstName} ${sale.customerLastName}`)
    }

    // Check for fake phone numbers
    if (sale.phoneNumber && (
      sale.phoneNumber === '0000000000' ||
      sale.phoneNumber === '00000000000' ||
      sale.phoneNumber === '1111111111' ||
      sale.phoneNumber === '12345678901' ||
      /^(.)\1+$/.test(sale.phoneNumber) // All same digit
    )) {
      issues.push(`WARNING: Fake phone number detected: ${sale.phoneNumber} for customer ${sale.customerFirstName} ${sale.customerLastName}`)
    }
  }

  return {
    valid: issues.length === 0,
    issues
  }
}

export async function performDataIntegrityCheck(): Promise<IntegrityReport> {
  console.log('🔍 PERFORMING DATA INTEGRITY CHECK')
  console.log('=================================')
  console.log('🔒 Validating customer data has not been corrupted or modified')
  
  try {
    // Fetch all data for integrity checking
    const [users, sales, appliances] = await Promise.all([
      prisma.user.findMany(),
      prisma.sale.findMany({ 
        include: { appliances: true },
        orderBy: { createdAt: 'asc' }
      }),
      prisma.appliance.findMany()
    ])

    const integrityChecks: DataIntegrityCheck[] = []

    // Check Sales Data (most critical for customer data)
    const salesHash = generateDataHash(sales.map(sale => ({
      id: sale.id,
      customerFirstName: sale.customerFirstName,
      customerLastName: sale.customerLastName,
      email: sale.email,
      phoneNumber: sale.phoneNumber,
      mailingStreet: sale.mailingStreet,
      mailingCity: sale.mailingCity,
      mailingPostalCode: sale.mailingPostalCode
    })))

    integrityChecks.push({
      tableName: 'sales',
      recordCount: sales.length,
      sampleRecords: sales.slice(0, 3).map(sale => ({
        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
        email: sale.email,
        phone: sale.phoneNumber,
        createdAt: sale.createdAt
      })),
      dataIntegrityHash: salesHash,
      customerDataFields: ['customerFirstName', 'customerLastName', 'email', 'phoneNumber', 'mailingStreet', 'mailingCity', 'mailingPostalCode']
    })

    // Check Users Data
    const usersHash = generateDataHash(users.map(user => ({
      id: user.id,
      email: user.email,
      role: user.role
    })))

    integrityChecks.push({
      tableName: 'users',
      recordCount: users.length,
      sampleRecords: users.slice(0, 3).map(user => ({
        email: user.email,
        role: user.role,
        createdAt: user.createdAt
      })),
      dataIntegrityHash: usersHash,
      customerDataFields: ['email']
    })

    // Check Appliances Data
    const appliancesHash = generateDataHash(appliances)

    integrityChecks.push({
      tableName: 'appliances',
      recordCount: appliances.length,
      sampleRecords: appliances.slice(0, 3),
      dataIntegrityHash: appliancesHash,
      customerDataFields: ['appliance', 'otherText']
    })

    // 🔒 CRITICAL: Validate customer data integrity
    const customerValidation = validateCustomerDataIntegrity(sales)
    
    if (!customerValidation.valid) {
      console.error('🚨 CUSTOMER DATA INTEGRITY VIOLATIONS DETECTED:')
      customerValidation.issues.forEach(issue => {
        console.error(`  ❌ ${issue}`)
      })
      throw new Error(`Customer data integrity violations: ${customerValidation.issues.length} issues found`)
    }

    // Calculate critical customer data metrics
    const uniqueCustomers = new Set(sales.map(sale => `${sale.customerFirstName}-${sale.customerLastName}-${sale.phoneNumber}`)).size
    const emailsWithData = sales.filter(sale => sale.email && sale.email.trim() !== '').length
    const phonesWithData = sales.filter(sale => sale.phoneNumber && sale.phoneNumber.trim() !== '').length
    const addressesWithData = sales.filter(sale => sale.mailingStreet && sale.mailingStreet.trim() !== '').length

    const report: IntegrityReport = {
      timestamp: new Date().toISOString(),
      totalRecords: users.length + sales.length + appliances.length,
      tables: integrityChecks,
      criticalCustomerData: {
        salesCount: sales.length,
        uniqueCustomers,
        emailsWithData,
        phonesWithData,
        addressesWithData
      }
    }

    console.log('✅ DATA INTEGRITY CHECK COMPLETE')
    console.log('================================')
    console.log(`📊 Total records validated: ${report.totalRecords}`)
    console.log(`👥 Sales records: ${report.criticalCustomerData.salesCount}`)
    console.log(`🆔 Unique customers: ${report.criticalCustomerData.uniqueCustomers}`)
    console.log(`📧 Customers with emails: ${report.criticalCustomerData.emailsWithData}`)
    console.log(`📞 Customers with phones: ${report.criticalCustomerData.phonesWithData}`)
    console.log(`🏠 Customers with addresses: ${report.criticalCustomerData.addressesWithData}`)
    console.log('🔒 No customer data corruption detected')

    return report

  } catch (error) {
    console.error('❌ Data integrity check failed:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

export async function compareDataIntegrity(beforeHash: string, afterHash: string, operation: string): Promise<boolean> {
  if (beforeHash === afterHash) {
    console.log(`✅ ${operation}: Customer data integrity preserved - no changes detected`)
    return true
  } else {
    console.error(`🚨 ${operation}: CUSTOMER DATA INTEGRITY VIOLATION - data has been modified!`)
    console.error(`  Before hash: ${beforeHash}`)
    console.error(`  After hash:  ${afterHash}`)
    throw new Error(`Customer data integrity violation during ${operation}`)
  }
}

// Run integrity check if called directly
if (process.env.NODE_ENV !== 'test') {
  performDataIntegrityCheck()
    .then((report) => {
      console.log(`✅ Data integrity check completed successfully`)
      console.log(`📄 Full report available with ${report.tables.length} tables validated`)
      process.exit(0)
    })
    .catch((error) => {
      console.error('❌ Data integrity check failed:', error)
      process.exit(1)
    })
}