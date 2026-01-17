import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { compare } from 'bcryptjs'
import { prisma } from '@/lib/prisma'
import { trackFailedLogin, getFailedLoginAttempts, clearFailedLoginAttempts } from '@/lib/rateLimit'
import { isValidEmail, sanitizeInput, logSecurityEvent, createSecurityContext } from '@/lib/security'

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials, req) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        // Validate email format
        if (!isValidEmail(credentials.email)) {
          return null
        }

        // Sanitize inputs
        const email = sanitizeInput(credentials.email).toLowerCase()
        const password = sanitizeInput(credentials.password)

        // Get client IP for rate limiting
        const ip = req?.headers?.['x-forwarded-for'] || req?.headers?.['x-real-ip'] || 'unknown'
        const userAgent = req?.headers?.['user-agent'] || 'unknown'
        
        // Check for too many failed attempts
        const failedAttempts = await getFailedLoginAttempts(email)
        const ipFailedAttempts = await getFailedLoginAttempts(`ip:${ip}`)
        
        if (failedAttempts >= 5 || ipFailedAttempts >= 10) {
          logSecurityEvent('LOGIN_BLOCKED_RATE_LIMIT', {
            ip: ip as string,
            userAgent: userAgent as string,
            timestamp: Date.now(),
            requestId: 'auth-' + Date.now()
          }, { email, failedAttempts, ipFailedAttempts })
          return null
        }

        const user = await prisma.user.findUnique({
          where: { email: email }
        })

        if (!user) {
          // Track failed attempt for both email and IP
          await trackFailedLogin(email)
          await trackFailedLogin(`ip:${ip}`)
          
          logSecurityEvent('LOGIN_FAILED_USER_NOT_FOUND', {
            ip: ip as string,
            userAgent: userAgent as string,
            timestamp: Date.now(),
            requestId: 'auth-' + Date.now()
          }, { email })
          
          return null
        }

        const isValid = await compare(password, user.password)

        if (!isValid) {
          // Track failed attempt for both email and IP
          await trackFailedLogin(email)
          await trackFailedLogin(`ip:${ip}`)
          
          logSecurityEvent('LOGIN_FAILED_INVALID_PASSWORD', {
            ip: ip as string,
            userAgent: userAgent as string,
            timestamp: Date.now(),
            requestId: 'auth-' + Date.now()
          }, { email, userId: user.id })
          
          return null
        }

        // Successful login - clear failed attempts
        await clearFailedLoginAttempts(email)
        await clearFailedLoginAttempts(`ip:${ip}`)
        
        logSecurityEvent('LOGIN_SUCCESS', {
          ip: ip as string,
          userAgent: userAgent as string,
          timestamp: Date.now(),
          requestId: 'auth-' + Date.now()
        }, { email, userId: user.id, role: user.role })

        return {
          id: user.id,
          email: user.email,
          role: user.role,
        }
      }
    })
  ],
  session: {
    strategy: 'jwt',
    maxAge: 4 * 60 * 60, // 4 hours
  },
  jwt: {
    maxAge: 4 * 60 * 60, // 4 hours
  },
  cookies: {
    sessionToken: {
      name: 'next-auth.session-token',
      options: {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        path: '/',
        maxAge: 4 * 60 * 60, // 4 hours
      }
    }
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub!
        session.user.role = token.role as string
      }
      return session
    },
  },
  pages: {
    signIn: '/auth/login',
  },
}