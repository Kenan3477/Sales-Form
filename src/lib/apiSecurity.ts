import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { checkLoginRateLimit, checkApiRateLimit } from '@/lib/rateLimit'
import { 
  createSecurityContext, 
  logSecurityEvent, 
  sanitizeInput,
  validateSessionToken,
  detectSQLInjection,
  detectXSS
} from '@/lib/security'

export interface SecureApiOptions {
  requireAuth?: boolean
  requireAdmin?: boolean
  rateLimit?: {
    requests: number
    windowMs: number
  }
  validateInput?: boolean
  logAccess?: boolean
}

export function withSecurity(
  handler: (req: NextRequest, context?: any) => Promise<NextResponse>,
  options: SecureApiOptions = {}
) {
  return async function secureHandler(req: NextRequest, context?: any): Promise<NextResponse> {
    const {
      requireAuth = false,
      requireAdmin = false,
      rateLimit,
      validateInput = true,
      logAccess = true
    } = options

    const securityContext = createSecurityContext(req)

    try {
      // Log API access if enabled
      if (logAccess) {
        logSecurityEvent('API_ACCESS', securityContext, {
          endpoint: req.nextUrl.pathname,
          method: req.method
        })
      }

      // Rate limiting
      if (rateLimit) {
        const rateLimitResult = await checkApiRateLimit(securityContext.ip)
        if (rateLimitResult.blocked) {
          logSecurityEvent('API_RATE_LIMIT_EXCEEDED', securityContext)
          return NextResponse.json(
            { error: 'Rate limit exceeded' },
            { status: 429 }
          )
        }
      }

      // Authentication check
      if (requireAuth || requireAdmin) {
        const session = await getServerSession(authOptions)
        
        if (!session?.user) {
          logSecurityEvent('UNAUTHORIZED_API_ACCESS', securityContext)
          return NextResponse.json(
            { error: 'Unauthorized' },
            { status: 401 }
          )
        }

        if (requireAdmin && session.user.role !== 'ADMIN') {
          logSecurityEvent('UNAUTHORIZED_ADMIN_ACCESS', securityContext, {
            userId: session.user.id,
            userRole: session.user.role
          })
          return NextResponse.json(
            { error: 'Admin access required' },
            { status: 403 }
          )
        }

        // Add user context
        context = { ...context, user: session.user }
      }

      // Input validation
      if (validateInput && req.method !== 'GET') {
        try {
          const body = await req.text()
          
          if (body) {
            // Check for SQL injection and XSS
            if (detectSQLInjection(body) || detectXSS(body)) {
              logSecurityEvent('MALICIOUS_INPUT_DETECTED', securityContext, {
                inputType: 'body',
                sample: body.substring(0, 100)
              })
              return NextResponse.json(
                { error: 'Invalid input detected' },
                { status: 400 }
              )
            }

            // Create new request with validated body
            req = new NextRequest(req.url, {
              method: req.method,
              headers: req.headers,
              body: body
            })
          }
        } catch (error) {
          console.error('Input validation error:', error)
        }
      }

      // Call the original handler
      const response = await handler(req, context)

      // Add security headers to response
      response.headers.set('X-Content-Type-Options', 'nosniff')
      response.headers.set('X-Frame-Options', 'DENY')
      response.headers.set('X-XSS-Protection', '1; mode=block')

      return response

    } catch (error) {
      logSecurityEvent('API_ERROR', securityContext, {
        error: error instanceof Error ? error.message : 'Unknown error'
      })
      
      console.error('Security middleware error:', error)
      return NextResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      )
    }
  }
}

export async function validateApiKey(apiKey: string): Promise<boolean> {
  // In a production environment, you'd validate against a database
  // For now, we'll just check if it matches an environment variable
  const validApiKey = process.env.API_KEY
  
  if (!validApiKey) {
    return false
  }
  
  return apiKey === validApiKey
}

export function createApiResponse(data: any, status: number = 200): NextResponse {
  const response = NextResponse.json(data, { status })
  
  // Add security headers
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Cache-Control', 'no-store, max-age=0')
  
  return response
}

export async function handleSecureUpload(
  req: NextRequest,
  maxSizeBytes: number = 10 * 1024 * 1024, // 10MB default
  allowedTypes: string[] = ['text/csv', 'application/json'],
  skipContentScan: boolean = false // Skip malicious content detection for data files
): Promise<{ file: File; isValid: boolean; error?: string }> {
  try {
    const formData = await req.formData()
    const file = formData.get('file') as File
    
    if (!file) {
      return { file: file, isValid: false, error: 'No file provided' }
    }
    
    // Check file size
    if (file.size > maxSizeBytes) {
      return { file, isValid: false, error: 'File too large' }
    }
    
    // Check file type
    if (!allowedTypes.includes(file.type)) {
      return { file, isValid: false, error: 'Invalid file type' }
    }
    
    // Only check file content for malicious patterns if not skipped
    // Skip for data files like CSV which may contain legitimate SQL-like content
    if (!skipContentScan) {
      const content = await file.text()
      if (detectSQLInjection(content) || detectXSS(content)) {
        return { file, isValid: false, error: 'Malicious content detected' }
      }
    }
    
    return { file, isValid: true }
    
  } catch (error) {
    return { 
      file: null as any, 
      isValid: false, 
      error: 'Upload processing failed' 
    }
  }
}