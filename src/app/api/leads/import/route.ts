import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { leadImportService } from '@/lib/leads/import'
import { prisma } from '@/lib/prisma'
import * as csv from 'csv-parse/sync'

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const formData = await request.formData()
    const file = formData.get('file') as File
    
    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 })
    }

    if (!file.name.endsWith('.csv')) {
      return NextResponse.json({ error: 'File must be a CSV' }, { status: 400 })
    }

    // Read and parse CSV
    const fileContent = await file.text()
    let csvData: any[]

    try {
      csvData = csv.parse(fileContent, {
        columns: true,
        skip_empty_lines: true,
        trim: true
      })
    } catch (error) {
      return NextResponse.json({ 
        error: 'Invalid CSV format',
        details: error instanceof Error ? error.message : 'Unknown parsing error'
      }, { status: 400 })
    }

    if (csvData.length === 0) {
      return NextResponse.json({ error: 'CSV file is empty' }, { status: 400 })
    }

    if (csvData.length > 5000) {
      return NextResponse.json({ 
        error: 'CSV file too large. Maximum 5000 rows allowed' 
      }, { status: 400 })
    }

    // Import leads
    const result = await leadImportService.importLeads(
      csvData,
      file.name,
      session.user.id
    )

    return NextResponse.json(result)

  } catch (error) {
    console.error('Lead import error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user || session.user.role !== 'ADMIN') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const limit = parseInt(url.searchParams.get('limit') || '20')

    const result = await leadImportService.getImportBatches(page, limit)

    return NextResponse.json(result)

  } catch (error) {
    console.error('Get import batches error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}