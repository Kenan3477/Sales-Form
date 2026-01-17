import CryptoJS from 'crypto-js'
import { NextRequest, NextResponse } from 'next/server'

// Security configuration
const ENCRYPTION_KEY = process.env.ENCRYPTION_SECRET || 'fallback-key-change-in-production'
const MAX_REQUEST_SIZE = 10 * 1024 * 1024 // 10MB

// Default origins with flexible production support
const getDefaultOrigins = () => {
  const origins = ['http://localhost:3000']
  
  // Add Vercel deployment URLs if in production
  if (process.env.NODE_ENV === 'production') {
    // Add common Vercel patterns
    if (process.env.VERCEL_URL) {
      origins.push(`https://${process.env.VERCEL_URL}`)
    }
    // Add the NEXTAUTH_URL if it's a Vercel deployment
    if (process.env.NEXTAUTH_URL) {
      origins.push(process.env.NEXTAUTH_URL)
    }
  }
  
  return origins
}

const ALLOWED_ORIGINS = process.env.ALLOWED_ORIGINS?.split(',') || getDefaultOrigins()

export interface SecurityContext {
  ip: string
  userAgent: string
  timestamp: number
  requestId: string
}

export function getClientIP(request: NextRequest): string {
  // Check for IP in various headers (Vercel, Cloudflare, etc.)
  const forwarded = request.headers.get('x-forwarded-for')
  const realIP = request.headers.get('x-real-ip')
  const cfConnectingIP = request.headers.get('cf-connecting-ip')
  
  if (forwarded) {
    // x-forwarded-for can contain multiple IPs, take the first one
    return forwarded.split(',')[0].trim()
  }
  
  if (realIP) {
    return realIP
  }
  
  if (cfConnectingIP) {
    return cfConnectingIP
  }
  
  // Fallback - for Vercel, this should be handled by headers above
  return 'unknown'
}

export function createSecurityContext(request: NextRequest): SecurityContext {
  return {
    ip: getClientIP(request),
    userAgent: request.headers.get('user-agent') || 'unknown',
    timestamp: Date.now(),
    requestId: generateRequestId()
  }
}

export function generateRequestId(): string {
  return CryptoJS.lib.WordArray.random(16).toString()
}

export function encryptSensitiveData(data: string): string {
  try {
    return CryptoJS.AES.encrypt(data, ENCRYPTION_KEY).toString()
  } catch (error) {
    console.error('Encryption failed:', error)
    throw new Error('Failed to encrypt sensitive data')
  }
}

export function decryptSensitiveData(encryptedData: string): string {
  try {
    const bytes = CryptoJS.AES.decrypt(encryptedData, ENCRYPTION_KEY)
    return bytes.toString(CryptoJS.enc.Utf8)
  } catch (error) {
    console.error('Decryption failed:', error)
    throw new Error('Failed to decrypt sensitive data')
  }
}

export function hashData(data: string): string {
  return CryptoJS.SHA256(data).toString()
}

export function validateRequestSize(request: NextRequest): boolean {
  const contentLength = request.headers.get('content-length')
  if (contentLength && parseInt(contentLength) > MAX_REQUEST_SIZE) {
    return false
  }
  return true
}

export function validateOrigin(request: NextRequest): boolean {
  const origin = request.headers.get('origin')
  if (!origin) {
    // Allow requests without origin (direct API calls, etc.)
    return true
  }
  
  // Debug logging for production issues
  if (process.env.NODE_ENV === 'production') {
    console.log('Origin validation:', {
      receivedOrigin: origin,
      allowedOrigins: ALLOWED_ORIGINS,
      isValid: ALLOWED_ORIGINS.includes(origin)
    })
  }
  
  return ALLOWED_ORIGINS.includes(origin)
}

export function isValidEmail(email: string): boolean {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return emailRegex.test(email)
}

export function sanitizeInput(input: string): string {
  // Remove potential XSS characters
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=/gi, '')
    .trim()
}

export function addSecurityHeaders(response: NextResponse): NextResponse {
  // Content Security Policy - Allow postcodes.io for postcode lookup
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self' https://api.postcodes.io; frame-ancestors 'none';"
  )
  
  // Security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
  response.headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')
  
  return response
}

export function logSecurityEvent(event: string, context: SecurityContext, details?: any): void {
  const logEntry = {
    timestamp: new Date().toISOString(),
    event,
    ip: context.ip,
    userAgent: context.userAgent,
    requestId: context.requestId,
    details: details || {}
  }
  
  // Log to console (in production, you'd want to send to a logging service)
  console.log('[SECURITY EVENT]', JSON.stringify(logEntry))
  
  // For critical security events, you might want to alert administrators
  if (event.includes('ATTACK') || event.includes('BREACH')) {
    console.error('[CRITICAL SECURITY EVENT]', JSON.stringify(logEntry))
  }
}

export function detectSQLInjection(input: string): boolean {
  const sqlInjectionPatterns = [
    /(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)/i,
    /(\b(or|and)\b\s+\d+\s*=\s*\d+)/i,
    /(\'|\"|`).*(\=|\<|\>).*(\;|\/\*|\*\/|--)/i,
    /(\b(union|select)\b.*\bfrom\b)/i,
    /(\/\*.*\*\/|--.*$|\;)/i
  ]
  
  return sqlInjectionPatterns.some(pattern => pattern.test(input))
}

export function detectXSS(input: string): boolean {
  const xssPatterns = [
    /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
    /<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi,
    /javascript:/gi,
    /on\w+\s*=/gi,
    /<img\b.*\bonerror\s*=/gi,
    /<svg\b.*\bonload\s*=/gi
  ]
  
  return xssPatterns.some(pattern => pattern.test(input))
}

export function isBot(userAgent: string): boolean {
  const botPatterns = [
    /bot/i,
    /crawl/i,
    /spider/i,
    /scrape/i,
    /curl/i,
    /wget/i,
    /python/i,
    /php/i,
    /ruby/i,
    /go-http/i,
    /java/i
  ]
  
  return botPatterns.some(pattern => pattern.test(userAgent))
}

export function validateSessionToken(token: string): boolean {
  try {
    // Basic token validation - in production you'd verify JWT signature
    const parts = token.split('.')
    return parts.length === 3 && parts.every(part => part.length > 0)
  } catch {
    return false
  }
}