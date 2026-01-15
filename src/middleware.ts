import { withAuth } from 'next-auth/middleware'

export default withAuth(
  function middleware(req) {
    // Additional middleware logic can be added here
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        // Allow access to public pages
        if (req.nextUrl.pathname === '/' || req.nextUrl.pathname.startsWith('/auth/')) {
          return true
        }
        
        // Require authentication for all other pages
        if (!token) {
          return false
        }

        // Admin-only routes
        if (req.nextUrl.pathname.startsWith('/admin/')) {
          return token.role === 'ADMIN'
        }

        // Dashboard and agent routes
        return true
      },
    },
  }
)

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}