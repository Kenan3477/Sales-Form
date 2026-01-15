/** @type {import('next').NextConfig} */
const nextConfig = {
  // Updated for Next.js 16
  serverExternalPackages: ['@prisma/client', 'bcryptjs'],
  
  // Add empty turbopack config to silence the warning
  turbopack: {},

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig