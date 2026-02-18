#!/usr/bin/env node

/**
 * Fix Vercel Email Configuration
 * This script helps diagnose and fix email configuration issues in Vercel deployment
 */

const fs = require('fs')
const path = require('path')

console.log('🔧 Vercel Email Configuration Fixer')
console.log('=====================================')

// Check environment files
const envFiles = [
  '.env.local',
  '.env.production', 
  '.env.vercel',
  '.env'
]

console.log('\n📁 Environment Files Status:')
envFiles.forEach(file => {
  const exists = fs.existsSync(file)
  console.log(`${exists ? '✅' : '❌'} ${file}`)
  
  if (exists) {
    const content = fs.readFileSync(file, 'utf8')
    const hasEmailConfig = content.includes('EMAIL_HOST') && content.includes('EMAIL_USER')
    console.log(`   📧 Email config: ${hasEmailConfig ? '✅ Found' : '❌ Missing'}`)
    
    if (content.includes('localhost') || content.includes('127.0.0.1')) {
      console.log('   ⚠️  WARNING: Contains localhost references!')
    }
  }
})

console.log('\n📋 Required Email Environment Variables:')
const requiredVars = [
  'EMAIL_HOST=smtp.gmail.com',
  'EMAIL_PORT=587',
  'EMAIL_USER=Hello@theflashteam.co.uk',
  'EMAIL_PASSWORD=tgul dkdc ncnc qwhc'
]

requiredVars.forEach(variable => {
  console.log(`   ${variable}`)
})

console.log('\n🚀 Vercel Deployment Commands:')
console.log('Set these environment variables in your Vercel dashboard:')
console.log('')
console.log('vercel env add EMAIL_HOST')
console.log('Enter value: smtp.gmail.com')
console.log('')
console.log('vercel env add EMAIL_PORT') 
console.log('Enter value: 587')
console.log('')
console.log('vercel env add EMAIL_USER')
console.log('Enter value: Hello@theflashteam.co.uk')
console.log('')
console.log('vercel env add EMAIL_PASSWORD')
console.log('Enter value: tgul dkdc ncnc qwhc')
console.log('')

console.log('🌐 Or use CLI commands:')
console.log('vercel env add EMAIL_HOST production')
console.log('vercel env add EMAIL_PORT production') 
console.log('vercel env add EMAIL_USER production')
console.log('vercel env add EMAIL_PASSWORD production')

console.log('\n💡 After setting environment variables, redeploy:')
console.log('vercel --prod')

console.log('\n🔍 Debug Information:')
console.log('Current working directory:', process.cwd())
console.log('Node.js version:', process.version)

// Check for common issues
console.log('\n🩺 Common Issues Check:')

// Check if .env.local has localhost references
if (fs.existsSync('.env.local')) {
  const localEnv = fs.readFileSync('.env.local', 'utf8')
  if (localEnv.includes('NEXTAUTH_URL="http://localhost:3000"')) {
    console.log('⚠️  .env.local contains localhost NEXTAUTH_URL - this is OK for development')
    console.log('   Make sure Vercel has NEXTAUTH_URL set to your production domain')
  }
}

// Create a production-ready env template
const prodEnvTemplate = `# Production Environment Variables
# Set these in Vercel Dashboard -> Settings -> Environment Variables

# Database
DATABASE_URL=your_prisma_accelerate_url_here

# NextAuth
NEXTAUTH_URL=https://your-vercel-domain.vercel.app
NEXTAUTH_SECRET=your_nextauth_secret_here

# Email Configuration (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=Hello@theflashteam.co.uk
EMAIL_PASSWORD=tgul dkdc ncnc qwhc

# Optional: SMS Configuration
VOODOO_API_KEY=your_api_key_here
VOODOO_FROM=Flash
`

fs.writeFileSync('.env.vercel.template', prodEnvTemplate)
console.log('✅ Created .env.vercel.template with production configuration')

console.log('\n📱 Next Steps:')
console.log('1. Go to your Vercel dashboard')
console.log('2. Navigate to your project settings')
console.log('3. Add the environment variables listed above')
console.log('4. Redeploy your application')
console.log('5. Test email functionality')

console.log('\n🔗 Vercel Dashboard URL:')
console.log('https://vercel.com/dashboard')