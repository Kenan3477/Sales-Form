import { NextRequest, NextResponse } from 'next/server'

interface SecurityHeaders {
  nonce: string
}

export function generateNonce(): string {
  // Use Web Crypto API for Edge Runtime compatibility
  const array = new Uint8Array(16)
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    crypto.getRandomValues(array)
  } else {
    // Fallback for environments without crypto
    for (let i = 0; i < array.length; i++) {
      array[i] = Math.floor(Math.random() * 256)
    }
  }
  return btoa(String.fromCharCode.apply(null, Array.from(array))).replace(/[/+=]/g, '')
}

export function createSecureCSP(nonce: string): string {
  const isDev = process.env.NODE_ENV === 'development'
  const reportOnly = process.env.CSP_REPORT_ONLY === 'true'
  
  // Base CSP configuration
  const cspDirectives = [
    "default-src 'self'",
    `script-src 'self' 'nonce-${nonce}' ${isDev ? "'unsafe-eval'" : ''}`, // unsafe-eval only for dev
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com", // Next.js requires unsafe-inline for styled-jsx
    "img-src 'self' data: https: blob:",
    "font-src 'self' https://fonts.gstatic.com",
    "connect-src 'self' https://api.vercel.com https://*.vercel.app",
    "frame-src 'none'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "block-all-mixed-content"
  ]
  
  // Add upgrade-insecure-requests for HTTPS
  if (!isDev) {
    cspDirectives.push("upgrade-insecure-requests")
  }
  
  // Add report-uri if available
  if (process.env.CSP_REPORT_URL) {
    cspDirectives.push(`report-uri ${process.env.CSP_REPORT_URL}`)
  }
  
  const csp = cspDirectives.join('; ')
  return reportOnly ? `${csp}; report-only` : csp
}

export function addSecurityHeaders(response: NextResponse, securityHeaders?: SecurityHeaders): void {
  const nonce = securityHeaders?.nonce || generateNonce()
  
  // CSP Header
  const cspHeaderName = process.env.CSP_REPORT_ONLY === 'true' 
    ? 'Content-Security-Policy-Report-Only' 
    : 'Content-Security-Policy'
  response.headers.set(cspHeaderName, createSecureCSP(nonce))
  
  // Store nonce for Next.js Script components
  response.headers.set('x-nonce', nonce)
  
  // Additional Security Headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  
  // CORP, COOP, COEP Headers
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin')
  response.headers.set('Cross-Origin-Resource-Policy', 'same-origin')
  
  // Only add COEP if explicitly enabled (can break external resources)
  if (process.env.ENABLE_COEP === 'true') {
    response.headers.set('Cross-Origin-Embedder-Policy', 'require-corp')
  }
  
  // Additional Security Headers
  response.headers.set('X-Permitted-Cross-Domain-Policies', 'none')
  response.headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=(), payment=(), usb=(), bluetooth=()')
  
  // Remove Information Disclosure Headers
  response.headers.delete('X-Powered-By')
  
  // HSTS (if not already set by Vercel)
  if (!response.headers.has('Strict-Transport-Security')) {
    response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload')
  }
}