import { NextRequest, NextResponse } from 'next/server'import { NextRequest, NextResponse } from 'next/server'

import { secureDebugEndpoint } from '@/lib/debugSecurity'import { secureDebugEndpoint } from '@/lib/debugSecurity'



export async function GET(request: NextRequest) {export async function GET(request: NextRequest) {

  return await secureDebugEndpoint(request, async () => {  return await secureDebugEndpoint(request, async () => {

    // This endpoint is now secured and only accessible by super admins in development    // This endpoint is now secured and only accessible by super admins in development

    return NextResponse.json({    return NextResponse.json({

      message: 'Debug endpoint access is restricted',      message: 'Debug endpoint access is restricted',

      note: 'This endpoint requires SUPER_ADMIN privileges and is disabled in production',      note: 'This endpoint requires SUPER_ADMIN privileges and is disabled in production',

      timestamp: new Date().toISOString()      timestamp: new Date().toISOString()

    })    })

  })  })

}}
        },
        allCookieNames: cookies.map(c => c.name)
      },
      request_info: {
        url: request.url,
        method: request.method,
        userAgent: headers['user-agent'],
        origin: headers['origin'],
        referer: headers['referer']
      },
      environment: {
        nodeEnv: process.env.NODE_ENV,
        nextAuthUrl: process.env.NEXTAUTH_URL,
        hasNextAuthSecret: !!process.env.NEXTAUTH_SECRET,
        nextAuthSecretLength: process.env.NEXTAUTH_SECRET?.length
      }
    })
  } catch (error) {
    return NextResponse.json({
      error: 'Session check failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}