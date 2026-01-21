import { Redis } from '@upstash/redis'
import { Ratelimit } from '@upstash/ratelimit'

// Rate limiting configurations
interface RateLimitConfig {
  requests: number
  window: string
  blockDuration?: string
}

const RATE_LIMIT_CONFIGS = {
  login: { requests: 5, window: '15 m', blockDuration: '15 m' },
  signup: { requests: 3, window: '1 h', blockDuration: '1 h' },
  passwordReset: { requests: 3, window: '1 h', blockDuration: '1 h' },
  api: { requests: 100, window: '1 h' },
  adminActions: { requests: 10, window: '1 h', blockDuration: '1 h' }
} as const

// Parse time window strings into milliseconds
function parseTimeWindow(window: string): number {
  const match = window.match(/(\d+)\s*(m|h|d)/)
  if (!match) return 3600000
  
  const value = parseInt(match[1])
  const unit = match[2]
  
  switch (unit) {
    case 'm': return value * 60 * 1000
    case 'h': return value * 60 * 60 * 1000
    case 'd': return value * 24 * 60 * 60 * 1000
    default: return 3600000
  }
}

// Initialize Redis for production rate limiting
let redis: Redis | undefined
let rateLimiters: Record<string, Ratelimit> = {}

if (process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN) {
  redis = new Redis({
    url: process.env.UPSTASH_REDIS_REST_URL,
    token: process.env.UPSTASH_REDIS_REST_TOKEN,
  })

  Object.keys(RATE_LIMIT_CONFIGS).forEach((key) => {
    const config = RATE_LIMIT_CONFIGS[key as keyof typeof RATE_LIMIT_CONFIGS]
    rateLimiters[key] = new Ratelimit({
      redis: redis!,
      limiter: Ratelimit.slidingWindow(config.requests, config.window as any),
      analytics: true,
      prefix: `ratelimit_${key}`,
    })
  })
}

// Memory store fallback for development
const memoryStore = new Map<string, { count: number; resetTime: number; blockedUntil?: number }>()

if (process.env.NODE_ENV === 'development') {
  setInterval(() => {
    const now = Date.now()
    for (const [key, value] of Array.from(memoryStore.entries())) {
      if (value.resetTime < now && (!value.blockedUntil || value.blockedUntil < now)) {
        memoryStore.delete(key)
      }
    }
  }, 60000)
}

export interface RateLimitResult {
  success: boolean
  remaining: number
  reset: number
  blocked: boolean
}

export type RateLimitType = keyof typeof RATE_LIMIT_CONFIGS

export async function checkRateLimit(
  identifier: string, 
  type: RateLimitType = 'api'
): Promise<RateLimitResult> {
  try {
    const rateLimiter = rateLimiters[type]
    
    if (rateLimiter) {
      const { success, remaining, reset } = await rateLimiter.limit(identifier)
      return { success, remaining, reset, blocked: !success }
    } else {
      console.warn('Redis not configured, using memory-based rate limiting')
      
      const config = RATE_LIMIT_CONFIGS[type]
      const windowMs = parseTimeWindow(config.window)
      const limit = config.requests
      
      const now = Date.now()
      const key = `${type}:${identifier}`
      const stored = memoryStore.get(key)
      
      if (stored?.blockedUntil && now < stored.blockedUntil) {
        return { success: false, remaining: 0, reset: stored.blockedUntil, blocked: true }
      }
      
      if (!stored || now > stored.resetTime) {
        memoryStore.set(key, { count: 1, resetTime: now + windowMs })
        return { success: true, remaining: limit - 1, reset: now + windowMs, blocked: false }
      } else if (stored.count >= limit) {
        const blockDuration = (config as any).blockDuration ? parseTimeWindow((config as any).blockDuration) : 0
        if (blockDuration > 0) {
          stored.blockedUntil = now + blockDuration
        }
        return { success: false, remaining: 0, reset: stored.resetTime, blocked: true }
      } else {
        stored.count++
        memoryStore.set(key, stored)
        return { success: true, remaining: limit - stored.count, reset: stored.resetTime, blocked: false }
      }
    }
  } catch (error) {
    console.error('Rate limit check failed:', error)
    return { success: true, remaining: 999, reset: Date.now() + 3600000, blocked: false }
  }
}

export async function checkLoginRateLimit(ip: string): Promise<RateLimitResult> {
  return checkRateLimit(ip, 'login')
}

export async function checkApiRateLimit(ip: string): Promise<RateLimitResult> {
  return checkRateLimit(ip, 'api')
}

export async function checkSMSRateLimit(userId: string): Promise<RateLimitResult> {
  return checkRateLimit(userId, 'adminActions')
}

export async function checkPasswordResetRateLimit(ip: string): Promise<RateLimitResult> {
  return checkRateLimit(ip, 'passwordReset')
}

export async function checkSignupRateLimit(ip: string): Promise<RateLimitResult> {
  return checkRateLimit(ip, 'signup')
}
