/**
 * @jest/globals
 */

// Mock Prisma first, before any imports
const mockPrisma = {
  sale: {
    findFirst: jest.fn(),
    create: jest.fn(),
  }
}

// Mock the prisma import
jest.mock('@/lib/prisma', () => ({
  prisma: mockPrisma
}))

// Mock NextAuth
jest.mock('next-auth', () => ({
  getServerSession: jest.fn(() => Promise.resolve({
    user: { id: 'test-user-id', role: 'admin' }
  }))
}))

// Mock auth options
jest.mock('@/lib/auth', () => ({
  authOptions: {}
}))

import { describe, it, expect, beforeEach } from '@jest/globals'
import { NextRequest } from 'next/server'

describe('Import Deduplication', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  const createMockFormData = (csvData: string) => {
    const formData = new FormData()
    
    // Create a buffer from the CSV data
    const buffer = Buffer.from(csvData, 'utf8')
    
    // Create a mock file-like object
    const mockFile = {
      name: 'test.csv',
      type: 'text/csv',
      size: buffer.length,
      arrayBuffer: async () => buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength),
      text: async () => csvData,
      stream: () => new ReadableStream({
        start(controller) {
          controller.enqueue(buffer)
          controller.close()
        }
      })
    }
    
    formData.append('file', mockFile as any)
    formData.append('format', 'csv')
    
    return formData
  }

  it('should detect duplicate by email', async () => {
    // Mock existing customer with same email
    mockPrisma.sale.findFirst.mockResolvedValueOnce({
      id: 'existing-id',
      customerFirstName: 'Jane',
      customerLastName: 'Smith', 
      email: 'john.doe@example.com',
      phoneNumber: '01234567890',
      createdAt: new Date('2024-01-01')
    })

    const csvData = `customerFirstName,customerLastName,phoneNumber,email,accountName,sortCode,accountNumber,directDebitDate,totalPlanCost
John,Doe,01234567890,john.doe@example.com,John Doe,12-34-56,12345678,2026-02-01,29.99`

    const formData = createMockFormData(csvData)
    const request = new NextRequest('http://localhost:3000/api/sales/import', {
      method: 'POST',
      body: formData
    })
    
    // Import the POST handler
    const { POST } = await import('@/app/api/sales/import/route')
    const response = await POST(request)
    const result = await response.json()

    expect(result.success).toBe(true)
    expect(result.imported).toBe(0)
    expect(result.skipped).toBe(1)
    expect(result.duplicates).toHaveLength(1)
    expect(result.duplicates[0].reason).toBe('Email address already exists')
    expect(result.duplicates[0].customer).toBe('John Doe')
  })

  it('should detect duplicate by phone number', async () => {
    // Mock no email match first, then phone match
    mockPrisma.sale.findFirst
      .mockResolvedValueOnce(null) // No email match
      .mockResolvedValueOnce({ // Phone match
        id: 'existing-id',
        customerFirstName: 'Jane',
        customerLastName: 'Smith',
        email: 'jane@example.com',
        phoneNumber: '01234567890',
        createdAt: new Date('2024-01-01')
      })

    const csvData = `customerFirstName,customerLastName,phoneNumber,email,accountName,sortCode,accountNumber,directDebitDate,totalPlanCost
John,Doe,01234567890,john.doe@example.com,John Doe,12-34-56,12345678,2026-02-01,29.99`

    const formData = createMockFormData(csvData)
    const request = new NextRequest('http://localhost:3000/api/sales/import', {
      method: 'POST',
      body: formData
    })
    
    const { POST } = await import('@/app/api/sales/import/route')
    const response = await POST(request)
    const result = await response.json()

    expect(result.success).toBe(true)
    expect(result.imported).toBe(0)
    expect(result.skipped).toBe(1)
    expect(result.duplicates).toHaveLength(1)
    expect(result.duplicates[0].reason).toBe('Phone number already exists')
  })

  it('should import new customer when no duplicates found', async () => {
    // Mock no duplicates found
    mockPrisma.sale.findFirst.mockResolvedValue(null)
    
    // Mock successful creation
    mockPrisma.sale.create.mockResolvedValueOnce({
      id: 'new-id',
      customerFirstName: 'John',
      customerLastName: 'Doe',
      email: 'john.doe@example.com',
      phoneNumber: '01234567890',
      appliances: [],
      createdBy: { id: 'test-user-id' }
    })

    const csvData = `customerFirstName,customerLastName,phoneNumber,email,accountName,sortCode,accountNumber,directDebitDate,totalPlanCost
John,Doe,01234567890,john.doe@example.com,John Doe,12-34-56,12345678,2026-02-01,29.99`

    const formData = createMockFormData(csvData)
    const request = new NextRequest('http://localhost:3000/api/sales/import', {
      method: 'POST',
      body: formData
    })
    
    const { POST } = await import('@/app/api/sales/import/route')
    const response = await POST(request)
    const result = await response.json()

    expect(result.success).toBe(true)
    expect(result.imported).toBe(1)
    expect(result.skipped).toBe(0)
    expect(result.duplicates).toBeUndefined()
    expect(mockPrisma.sale.create).toHaveBeenCalledTimes(1)
  })
})