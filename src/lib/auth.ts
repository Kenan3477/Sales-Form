import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { compare } from 'bcryptjs'
import { prisma } from '@/lib/prisma'
import { checkLoginRateLimit } from '@/lib/rateLimit'
import { logSecurityEvent, sanitizeErrorMessage } from '@/lib/securityHeaders'
import { isValidEmail, sanitizeInput } from '@/lib/security'

export const authOptions: NextAuthOptions = {
  debug: process.env.DEBUG_AUTH === 'true' || process.env.NODE_ENV === 'development',
  secret: process.env.NEXTAUTH_SECRET,
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

        // Get client IP for security logging
        const ip = req?.headers?.['x-forwarded-for'] || req?.headers?.['x-real-ip'] || 'unknown'
        const userAgent = req?.headers?.['user-agent'] || 'unknown'

        try {
          const user = await prisma.user.findUnique({
            where: { email: email }
          })

          if (!user) {
            // Don't reveal that user doesn't exist
            console.warn(`Login attempt for non-existent user: ${email} from IP: ${ip}`)
            return null
          }

          const isValid = await compare(password, user.password)

          if (!isValid) {
            console.warn(`Invalid password attempt for user: ${email} from IP: ${ip}`)
            return null
          }

          // Successful login
          console.log(`Successful login for user: ${email} from IP: ${ip}`)

          return {
            id: user.id,
            email: user.email,
            role: user.role,
          }
        } catch (error) {
          console.error('Auth error:', error)
          return null
        }
      }
    })
  ],
  session: {
    strategy: 'jwt',
    maxAge: 4 * 60 * 60, // 4 hours
  },
  jwt: {
    secret: process.env.NEXTAUTH_SECRET,
    maxAge: 4 * 60 * 60, // 4 hours
  },
  cookies: {
    sessionToken: {
      name: process.env.NODE_ENV === 'production' ? '__Secure-next-auth.session-token' : 'next-auth.session-token',
      options: {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        path: '/',
        maxAge: 4 * 60 * 60, // 4 hours
        domain: undefined, // Let NextAuth handle domain automatically
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