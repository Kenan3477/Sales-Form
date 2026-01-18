import { NextRequest, NextResponse } from 'next/server'import { NextRequest, NextResponse } from 'next/server'import { NextRequest, NextResponse } from 'next/server'import { NextRequest, NextResponse } from 'next/server'

import { getServerSession } from 'next-auth'

import { authOptions } from '../../../../../lib/auth'import { getServerSession } from 'next-auth'

import { prisma } from '../../../../../lib/prisma'

import { analyzePhoneNumber } from '../../../../../lib/sms'import { authOptions } from '../../../../../lib/auth'import { getServerSession } from 'next-auth'import { getServerSession } from 'next-auth'



export async function GET(request: NextRequest) {import { prisma } from '../../../../../lib/prisma'

  try {

    const session = await getServerSession(authOptions)import { analyzePhoneNumber } from '../../../../../lib/sms'import { authOptions } from '../../../../../lib/auth'import { authOptions } from '../../../../../lib/auth'

    

    if (!session || session.user.role !== 'ADMIN') {

      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

    }export async function GET(request: NextRequest) {import { prisma } from '../../../../../lib/prisma'import { prisma } from '../../../../../lib/prisma'



    const searchParams = request.nextUrl.searchParams  try {

    const dateFrom = searchParams.get('dateFrom')

    const dateTo = searchParams.get('dateTo')    const session = await getServerSession(authOptions)import { analyzePhoneNumber } from '../../../../../lib/sms'import { normalizeUkNumber, isUkMobile } from '../../../../../lib/sms'

    const agentFilter = searchParams.get('agent')

    const analyzeAll = searchParams.get('analyzeAll') === 'true'    



    let whereClause: any = {}    if (!session || session.user.role !== 'ADMIN') {



    if (!analyzeAll) {      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

      if (dateFrom || dateTo || (!dateFrom && !dateTo)) {

        whereClause.createdAt = {}    }export async function GET(request: NextRequest) {interface PhoneAnalysis {

        

        if (dateFrom) {

          whereClause.createdAt.gte = new Date(dateFrom)

        } else {    const searchParams = request.nextUrl.searchParams  try {  original: string

          const today = new Date()

          today.setHours(0, 0, 0, 0)    const dateFrom = searchParams.get('dateFrom')

          whereClause.createdAt.gte = today

        }    const dateTo = searchParams.get('dateTo')    const session = await getServerSession(authOptions)  normalized: string | null

        

        if (dateTo) {    const agentFilter = searchParams.get('agent')

          whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')

        } else if (!dateFrom) {    const analyzeAll = searchParams.get('analyzeAll') === 'true'      type: 'mobile' | 'landline' | 'invalid' | 'unknown'

          const today = new Date()

          today.setHours(23, 59, 59, 999)

          whereClause.createdAt.lte = today

        }    let whereClause: any = {}    if (!session || session.user.role !== 'ADMIN') {  canSendSMS: boolean

      }

    }



    if (agentFilter) {    // If not analyzing all, apply date filters (default to today)      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })  reason?: string

      whereClause.createdById = agentFilter

    }    if (!analyzeAll) {



    const sales = await prisma.sale.findMany({      if (dateFrom || dateTo || (!dateFrom && !dateTo)) {    }}

      where: whereClause,

      include: {        whereClause.createdAt = {}

        createdBy: {

          select: {        

            email: true,

            id: true        if (dateFrom) {

          }

        },          whereClause.createdAt.gte = new Date(dateFrom)    const searchParams = request.nextUrl.searchParamsexport async function GET(request: NextRequest) {

        smsLogs: {

          orderBy: { createdAt: 'desc' },        } else {

          take: 1

        }          const today = new Date()    const dateFrom = searchParams.get('dateFrom')  try {

      },

      orderBy: { createdAt: 'desc' }          today.setHours(0, 0, 0, 0)

    })

          whereClause.createdAt.gte = today    const dateTo = searchParams.get('dateTo')    const session = await getServerSession(authOptions)

    let totalCustomers = 0

    let validMobiles = 0        }

    let landlines = 0

    let specialNumbers = 0            const agentFilter = searchParams.get('agent')    

    let invalidNumbers = 0

    let customersWithoutNumbers = 0        if (dateTo) {



    const validMobileList: any[] = []          whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')    const analyzeAll = searchParams.get('analyzeAll') === 'true' // New parameter for full analysis    if (!session || session.user.role !== 'ADMIN') {

    const phoneBreakdown: any[] = []

        } else if (!dateFrom) {

    sales.forEach(sale => {

      totalCustomers++          const today = new Date()      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

      

      if (!sale.phoneNumber) {          today.setHours(23, 59, 59, 999)

        customersWithoutNumbers++

        phoneBreakdown.push({          whereClause.createdAt.lte = today    let whereClause: any = {}    }

          saleId: sale.id,

          customerName: `${sale.customerFirstName} ${sale.customerLastName}`,        }

          original: '',

          type: 'missing',      }

          reason: 'No phone number provided'

        })    }

        return

      }    // If not analyzing all, apply date filters (default to today)    const searchParams = request.nextUrl.searchParams

      

      const analysis = analyzePhoneNumber(sale.phoneNumber)    if (agentFilter) {

      

      phoneBreakdown.push({      whereClause.createdById = agentFilter    if (!analyzeAll) {    const dateFrom = searchParams.get('dateFrom')

        saleId: sale.id,

        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,    }

        original: analysis.original,

        normalized: analysis.normalized,      if (dateFrom || dateTo || (!dateFrom && !dateTo)) {    const dateTo = searchParams.get('dateTo')

        type: analysis.type,

        canSendSMS: analysis.canSendSMS,    const sales = await prisma.sale.findMany({

        reason: analysis.reason

      })      where: whereClause,        whereClause.createdAt = {}    const agentFilter = searchParams.get('agent')

      

      switch (analysis.type) {      include: {

        case 'mobile':

          validMobiles++        createdBy: {            const analyzeAll = searchParams.get('analyzeAll') === 'true' // New parameter for full analysis

          if (analysis.canSendSMS) {

            validMobileList.push({          select: {

              saleId: sale.id,

              customerName: `${sale.customerFirstName} ${sale.customerLastName}`,            email: true,        if (dateFrom) {

              phoneNumber: analysis.normalized,

              originalNumber: analysis.original,            id: true

              createdAt: sale.createdAt,

              agentEmail: sale.createdBy.email,          }          whereClause.createdAt.gte = new Date(dateFrom)    let whereClause: any = {}

              smsStatus: sale.smsLogs[0]?.smsStatus || 'NOT_SENT',

              canSend: !sale.smsLogs[0] || sale.smsLogs[0].smsStatus !== 'SENT'        },

            })

          }        smsLogs: {        } else {

          break

        case 'landline':          orderBy: { createdAt: 'desc' },

          landlines++

          break          take: 1          // Default to today    // If not analyzing all, apply date filters (default to today)

        case 'special':

          specialNumbers++        }

          break

        case 'invalid':      },          const today = new Date()    if (!analyzeAll) {

          invalidNumbers++

          break      orderBy: { createdAt: 'desc' }

      }

    })    })          today.setHours(0, 0, 0, 0)      if (dateFrom || dateTo || (!dateFrom && !dateTo)) {



    const salesWithSmsStatus = sales.map(sale => {

      const latestSms = sale.smsLogs[0]

      const analysis = sale.phoneNumber ? analyzePhoneNumber(sale.phoneNumber) : {    // Analyze all phone numbers          whereClause.createdAt.gte = today        whereClause.createdAt = {}

        original: '',

        normalized: null,    const phoneAnalysisMap = new Map<string, any>()

        type: 'invalid' as const,

        canSendSMS: false,    let totalCustomers = 0        }        

        reason: 'No phone number provided'

      }    let validMobiles = 0

      

      return {    let landlines = 0                if (dateFrom) {

        id: sale.id,

        createdAt: sale.createdAt,    let specialNumbers = 0

        customerFirstName: sale.customerFirstName,

        customerLastName: sale.customerLastName,    let invalidNumbers = 0        if (dateTo) {          whereClause.createdAt.gte = new Date(dateFrom)

        phoneNumber: sale.phoneNumber,

        phoneAnalysis: analysis,    let duplicateNumbers = 0

        email: sale.email,

        agentEmail: sale.createdBy.email,    let customersWithoutNumbers = 0          whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')        } else {

        agentName: sale.agentName || sale.createdBy.email,

        totalPlanCost: sale.totalPlanCost,

        smsStatus: latestSms?.smsStatus || 'NOT_SENT',

        smsSentAt: latestSms?.smsSentAt,    const processedNumbers = new Set<string>()        } else if (!dateFrom) {          // Default to today

        smsError: latestSms?.smsError,

        canSendSms: analysis.canSendSMS && (!latestSms || latestSms.smsStatus !== 'SENT')    const validMobileList: any[] = []

      }

    })          // Default to end of today          const today = new Date()



    const agents = await prisma.user.findMany({    sales.forEach(sale => {

      where: {

        role: { in: ['AGENT', 'ADMIN'] }      totalCustomers++          const today = new Date()          today.setHours(0, 0, 0, 0)

      },

      select: {      

        id: true,

        email: true      if (!sale.phoneNumber) {          today.setHours(23, 59, 59, 999)          whereClause.createdAt.gte = today

      },

      orderBy: { email: 'asc' }        customersWithoutNumbers++

    })

        return          whereClause.createdAt.lte = today        }

    return NextResponse.json({

      sales: salesWithSmsStatus,      }

      agents,

      phoneAnalysis: {              }        

        totalCustomers,

        customersWithoutNumbers,      const original = sale.phoneNumber.trim()

        validMobiles,

        landlines,            }        if (dateTo) {

        specialNumbers,

        invalidNumbers,      if (processedNumbers.has(original)) {

        validMobileList,

        phoneBreakdown,        duplicateNumbers++    }          whereClause.createdAt.lte = new Date(dateTo + 'T23:59:59.999Z')

        summary: {

          total: totalCustomers,      } else {

          withNumbers: totalCustomers - customersWithoutNumbers,

          withoutNumbers: customersWithoutNumbers,        processedNumbers.add(original)        } else if (!dateFrom) {

          breakdown: {

            mobiles: validMobiles,      }

            landlines: landlines,

            special: specialNumbers,    // Agent filter          // Default to end of today

            invalid: invalidNumbers

          }      const analysis = analyzePhoneNumber(original)

        }

      }          if (agentFilter) {          const today = new Date()

    })

  } catch (error) {      switch (analysis.type) {

    console.error('SMS analysis error:', error)

    return NextResponse.json(        case 'mobile':      whereClause.createdById = agentFilter          today.setHours(23, 59, 59, 999)

      { error: 'Internal server error' },

      { status: 500 }          validMobiles++

    )

  }          if (analysis.canSendSMS) {    }          whereClause.createdAt.lte = today

}
            validMobileList.push({

              saleId: sale.id,        }

              customerName: `${sale.customerFirstName} ${sale.customerLastName}`,

              phoneNumber: analysis.normalized,    const sales = await prisma.sale.findMany({      }

              originalNumber: original,

              createdAt: sale.createdAt,      where: whereClause,    }

              agentEmail: sale.createdBy.email,

              smsStatus: sale.smsLogs[0]?.smsStatus || 'NOT_SENT',      include: {

              canSend: !sale.smsLogs[0] || sale.smsLogs[0].smsStatus !== 'SENT'

            })        createdBy: {    // Agent filter

          }

          break          select: {    if (agentFilter) {

        case 'landline':

          landlines++            email: true,      whereClause.createdById = agentFilter

          break

        case 'special':            id: true    }

          specialNumbers++

          break          }

        case 'invalid':

          invalidNumbers++        },    const sales = await prisma.sale.findMany({

          break

      }        smsLogs: {      where: whereClause,



      phoneAnalysisMap.set(original, analysis)          orderBy: { createdAt: 'desc' },      include: {

    })

          take: 1 // Get latest SMS log for status        createdBy: {

    const salesWithSmsStatus = sales.map(sale => {

      const latestSms = sale.smsLogs[0]        }          select: {

      const phoneAnalysisData = phoneAnalysisMap.get(sale.phoneNumber?.trim()) || {

        original: sale.phoneNumber || '',      },            email: true,

        normalized: null,

        type: 'invalid',      orderBy: { createdAt: 'desc' }            id: true

        canSendSMS: false,

        reason: 'No phone number provided'    })          }

      }

              },

      return {

        id: sale.id,    // Analyze all phone numbers comprehensively        smsLogs: {

        createdAt: sale.createdAt,

        customerFirstName: sale.customerFirstName,    const phoneAnalysisMap = new Map<string, any>()          orderBy: { createdAt: 'desc' },

        customerLastName: sale.customerLastName,

        phoneNumber: sale.phoneNumber,    let totalCustomers = 0          take: 1 // Get latest SMS log for status

        phoneAnalysis: phoneAnalysisData,

        email: sale.email,    let validMobiles = 0        }

        agentEmail: sale.createdBy.email,

        agentName: sale.agentName || sale.createdBy.email,    let landlines = 0      },

        totalPlanCost: sale.totalPlanCost,

        smsStatus: latestSms?.smsStatus || 'NOT_SENT',    let specialNumbers = 0      orderBy: { createdAt: 'desc' }

        smsSentAt: latestSms?.smsSentAt,

        smsError: latestSms?.smsError,    let invalidNumbers = 0    })

        canSendSms: phoneAnalysisData.canSendSMS && (!latestSms || latestSms.smsStatus !== 'SENT')

      }    let duplicateNumbers = 0

    })

    let customersWithoutNumbers = 0    // Analyze all phone numbers

    const agents = await prisma.user.findMany({

      where: {    const phoneAnalysis: Record<string, PhoneAnalysis> = {}

        role: { in: ['AGENT', 'ADMIN'] }

      },    const processedNumbers = new Set<string>()    let totalNumbers = 0

      select: {

        id: true,    const validMobileList: any[] = []    let validMobiles = 0

        email: true

      },    let landlines = 0

      orderBy: { email: 'asc' }

    })    sales.forEach(sale => {    let invalidNumbers = 0



    return NextResponse.json({      totalCustomers++    let duplicateNumbers = 0

      sales: salesWithSmsStatus,

      agents,      

      phoneAnalysis: {

        totalCustomers,      if (!sale.phoneNumber) {    const processedNumbers = new Set<string>()

        customersWithoutNumbers,

        uniqueNumbers: processedNumbers.size,        customersWithoutNumbers++

        duplicateNumbers,

        validMobiles,        return    sales.forEach(sale => {

        landlines,

        specialNumbers,      }      if (!sale.phoneNumber) return

        invalidNumbers,

        validMobileList,            

        summary: {

          total: totalCustomers,      const original = sale.phoneNumber.trim()      totalNumbers++

          withNumbers: totalCustomers - customersWithoutNumbers,

          withoutNumbers: customersWithoutNumbers,            const original = sale.phoneNumber.trim()

          duplicates: duplicateNumbers,

          breakdown: {      // Track duplicates      

            mobiles: validMobiles,

            landlines: landlines,      if (processedNumbers.has(original)) {      // Skip if we've already processed this exact number

            special: specialNumbers,

            invalid: invalidNumbers        duplicateNumbers++      if (processedNumbers.has(original)) {

          }

        }      } else {        duplicateNumbers++

      }

    })        processedNumbers.add(original)        return

  } catch (error) {

    console.error('SMS analysis error:', error)      }      }

    return NextResponse.json(

      { error: 'Internal server error' },      processedNumbers.add(original)

      { status: 500 }

    )      // Analyze the phone number

  }

}      const analysis = analyzePhoneNumber(original)      const analysis: PhoneAnalysis = {

              original,

      // Count by type        normalized: null,

      switch (analysis.type) {        type: 'invalid',

        case 'mobile':        canSendSMS: false

          validMobiles++      }

          if (analysis.canSendSMS) {

            validMobileList.push({      // Try to normalize the number

              saleId: sale.id,      const normalized = normalizeUkNumber(original)

              customerName: `${sale.customerFirstName} ${sale.customerLastName}`,      

              phoneNumber: analysis.normalized,      if (normalized) {

              originalNumber: original,        analysis.normalized = normalized

              createdAt: sale.createdAt,        

              agentEmail: sale.createdBy.email,        if (isUkMobile(normalized)) {

              smsStatus: sale.smsLogs[0]?.smsStatus || 'NOT_SENT',          analysis.type = 'mobile'

              canSend: !sale.smsLogs[0] || sale.smsLogs[0].smsStatus !== 'SENT'          analysis.canSendSMS = true

            })          validMobiles++

          }        } else {

          break          // Check if it's a UK landline (starts with +44 but not +447)

        case 'landline':          if (normalized.startsWith('+44') && !normalized.startsWith('+447')) {

          landlines++            analysis.type = 'landline'

          break            analysis.reason = 'Landline numbers cannot receive SMS'

        case 'special':            landlines++

          specialNumbers++          } else {

          break            analysis.type = 'unknown'

        case 'invalid':            analysis.reason = 'Unknown number format'

          invalidNumbers++            invalidNumbers++

          break          }

      }        }

      } else {

      // Store analysis        analysis.type = 'invalid'

      phoneAnalysisMap.set(original, analysis)        analysis.reason = 'Could not normalize to valid UK format'

    })        invalidNumbers++

      }

    // Format response with SMS status and phone analysis

    const salesWithSmsStatus = sales.map(sale => {      phoneAnalysis[original] = analysis

      const latestSms = sale.smsLogs[0]    })

      const phoneAnalysisData = phoneAnalysisMap.get(sale.phoneNumber?.trim()) || {

        original: sale.phoneNumber || '',    // Format response with SMS status and phone analysis

        normalized: null,    const salesWithSmsStatus = sales.map(sale => {

        type: 'invalid',      const latestSms = sale.smsLogs[0]

        canSendSMS: false,      const phoneAnalysisData = phoneAnalysis[sale.phoneNumber?.trim()] || {

        reason: 'No phone number provided'        original: sale.phoneNumber || '',

      }        normalized: null,

              type: 'invalid',

      return {        canSendSMS: false,

        id: sale.id,        reason: 'No phone number provided'

        createdAt: sale.createdAt,      }

        customerFirstName: sale.customerFirstName,      

        customerLastName: sale.customerLastName,      return {

        phoneNumber: sale.phoneNumber,        id: sale.id,

        phoneAnalysis: phoneAnalysisData,        createdAt: sale.createdAt,

        email: sale.email,        customerFirstName: sale.customerFirstName,

        agentEmail: sale.createdBy.email,        customerLastName: sale.customerLastName,

        agentName: sale.agentName || sale.createdBy.email,        phoneNumber: sale.phoneNumber,

        totalPlanCost: sale.totalPlanCost,        phoneAnalysis: phoneAnalysisData,

        smsStatus: latestSms?.smsStatus || 'NOT_SENT',        email: sale.email,

        smsSentAt: latestSms?.smsSentAt,        agentEmail: sale.createdBy.email,

        smsError: latestSms?.smsError,        agentName: sale.agentName || sale.createdBy.email,

        canSendSms: phoneAnalysisData.canSendSMS && (!latestSms || latestSms.smsStatus !== 'SENT')        totalPlanCost: sale.totalPlanCost,

      }        smsStatus: latestSms?.smsStatus || 'NOT_SENT',

    })        smsSentAt: latestSms?.smsSentAt,

        smsError: latestSms?.smsError,

    // Get unique agents for filter dropdown        canSendSms: phoneAnalysisData.canSendSMS && (!latestSms || latestSms.smsStatus !== 'SENT')

    const agents = await prisma.user.findMany({      }

      where: {    })

        role: { in: ['AGENT', 'ADMIN'] }

      },    // Get valid mobile numbers for SMS

      select: {    const validMobileNumbers = salesWithSmsStatus

        id: true,      .filter(sale => sale.phoneAnalysis.canSendSMS)

        email: true      .map(sale => ({

      },        saleId: sale.id,

      orderBy: { email: 'asc' }        customerName: `${sale.customerFirstName} ${sale.customerLastName}`,

    })        phoneNumber: sale.phoneAnalysis.normalized,

        originalNumber: sale.phoneNumber,

    return NextResponse.json({        smsStatus: sale.smsStatus,

      sales: salesWithSmsStatus,        canSend: sale.canSendSms

      agents,      }))

      phoneAnalysis: {

        totalCustomers,    // Get unique agents for filter dropdown

        customersWithoutNumbers,    const agents = await prisma.user.findMany({

        uniqueNumbers: processedNumbers.size,      where: {

        duplicateNumbers,        role: { in: ['AGENT', 'ADMIN'] }

        validMobiles,      },

        landlines,      select: {

        specialNumbers,        id: true,

        invalidNumbers,        email: true

        validMobileList,      },

        summary: {      orderBy: { email: 'asc' }

          total: totalCustomers,    })

          withNumbers: totalCustomers - customersWithoutNumbers,

          withoutNumbers: customersWithoutNumbers,    return NextResponse.json({

          duplicates: duplicateNumbers,      sales: salesWithSmsStatus,

          breakdown: {      agents,

            mobiles: validMobiles,      phoneAnalysis: {

            landlines: landlines,        totalNumbers,

            special: specialNumbers,        uniqueNumbers: Object.keys(phoneAnalysis).length,

            invalid: invalidNumbers        duplicateNumbers,

          }        validMobiles,

        }        landlines,

      }        invalidNumbers,

    })        validMobileNumbers,

  } catch (error) {        breakdown: phoneAnalysis

    console.error('SMS analysis error:', error)      }

    return NextResponse.json(    })

      { error: 'Internal server error' },  } catch (error) {

      { status: 500 }    console.error('SMS analysis error:', error)

    )    return NextResponse.json(

  }      { error: 'Internal server error' },

}      { status: 500 }
    )
  }
}
      orderBy: { email: 'asc' }
    })

    return NextResponse.json({
      sales: salesWithSmsStatus,
      agents
    })

  } catch (error) {
    console.error('Error fetching sales for SMS:', error)
    return NextResponse.json(
      { error: 'Failed to fetch sales data' },
      { status: 500 }
    )
  }
}