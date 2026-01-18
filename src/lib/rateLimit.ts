import { Redis } from '@upstash/redis'
import { Ratelimit } from '@upstash/ratelimit'

// Initialize Redis for rate limiting (use Upstash Redis for Vercel)
let redis: Redis | undefined
let ratelimit: Ratelimit | undefined

// Only initialize Redis if we have credentials
if (process.env.UPSTASH_REDIS_REST_URL && process.env.UPSTASH_REDIS_REST_TOKEN) {
  redis = new Redis({
    url: process.env.UPSTASH_REDIS_REST_URL,
    token: process.env.UPSTASH_REDIS_REST_TOKEN,
  })

  // Rate limiting configurations
  ratelimit = new Ratelimit({
    redis: redis,
    limiter: Ratelimit.slidingWindow(10, '1 h'), // 10 requests per hour for login attempts
    analytics: true,
  })
}

// In-memory fallback for development (not recommended for production)
const memoryStore = new Map<string, { count: number; resetTime: number }>()

// Clear cache for development
if (process.env.NODE_ENV === 'development') {
  memoryStore.clear()
}

export interface RateLimitResult {
  success: boolean
  remaining: number
  reset: number
  blocked: boolean
}

export async function checkRateLimit(identifier: string, limit = 10, window = 3600000): Promise<RateLimitResult> {
  try {
    if (ratelimit) {
      // Use Redis-based rate limiting
      const { success, remaining, reset } = await ratelimit.limit(identifier)
      return {
        success,
        remaining,
        reset: reset,
        blocked: !success
      }
    } else {
      // Fallback to memory-based rate limiting (development only)
      console.warn('Redis not configured, using memory-based rate limiting (not suitable for production)')
      
      const now = Date.now()
      const key = identifier
      const stored = memoryStore.get(key)
      
      if (!stored || now > stored.resetTime) {
        // Reset window
        memoryStore.set(key, { count: 1, resetTime: now + window })
        return {
          success: true,
          remaining: limit - 1,
          reset: now + window,
          blocked: false
        }
      } else if (stored.count >= limit) {
        // Rate limit exceeded
        return {
          success: false,
          remaining: 0,
          reset: stored.resetTime,
          blocked: true
        }
      } else {
        // Increment counter
        stored.count++
        memoryStore.set(key, stored)
        return {
          success: true,
          remaining: limit - stored.count,
          reset: stored.resetTime,
          blocked: false
        }
      }
    }
  } catch (error) {
    console.error('Rate limiting error:', error)
    // On error, allow the request (fail open)
    return {
      success: true,
      remaining: limit - 1,
      reset: Date.now() + window,
      blocked: false
    }
  }
}

export async function checkLoginRateLimit(ip: string): Promise<RateLimitResult> {
  return checkRateLimit(`login:${ip}`, 50, 3600000) // 50 attempts per hour per IP (increased for dev)
}

export async function checkApiRateLimit(ip: string): Promise<RateLimitResult> {
  return checkRateLimit(`api:${ip}`, 1000, 3600000) // 1000 API calls per hour per IP (increased for dev)
}

export async function checkSMSRateLimit(userId: string): Promise<RateLimitResult> {
  return checkRateLimit(`sms:${userId}`, 50, 86400000) // 50 SMS per day per user
}

// Track failed login attempts with exponential backoff
export async function trackFailedLogin(identifier: string): Promise<void> {
  try {
    if (redis) {
      const key = `failed_login:${identifier}`
      const attempts = await redis.incr(key)
      
      // Set expiration - exponential backoff
      const expiration = Math.min(300 * Math.pow(2, attempts - 1), 86400) // Max 24 hours
      await redis.expire(key, expiration)
    } else {
      // Memory fallback
      const key = `failed_login:${identifier}`
      const stored = memoryStore.get(key) || { count: 0, resetTime: Date.now() }
      stored.count++
      
      const expiration = Math.min(300 * Math.pow(2, stored.count - 1), 86400) * 1000
      stored.resetTime = Date.now() + expiration
      memoryStore.set(key, stored)
    }
  } catch (error) {
    console.error('Failed to track failed login:', error)
  }
}

export async function getFailedLoginAttempts(identifier: string): Promise<number> {
  try {
    if (redis) {
      const key = `failed_login:${identifier}`
      const attempts = await redis.get(key)
      return typeof attempts === 'number' ? attempts : 0
    } else {
      // Memory fallback
      const key = `failed_login:${identifier}`
      const stored = memoryStore.get(key)
      if (stored && Date.now() < stored.resetTime) {
        return stored.count
      }
      return 0
    }
  } catch (error) {
    console.error('Failed to get failed login attempts:', error)
    return 0
  }
}

export async function clearFailedLoginAttempts(identifier: string): Promise<void> {
  try {
    if (redis) {
      const key = `failed_login:${identifier}`
      await redis.del(key)
    } else {
      const key = `failed_login:${identifier}`
      memoryStore.delete(key)
    }
  } catch (error) {
    console.error('Failed to clear failed login attempts:', error)
  }
}