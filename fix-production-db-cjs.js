const { PrismaClient } = require('@prisma/client')
const bcryptjs = require('bcryptjs')

// Direct database fix script
async function fixProductionDatabase() {
  const prisma = new PrismaClient({
    datasources: {
      db: {
        url: process.env.DATABASE_URL
      }
    }
  })

  try {
    console.log('🔍 Checking production database...')

    // Check existing users
    const existingUsers = await prisma.user.findMany({
      select: { email: true, role: true, createdAt: true }
    })

    console.log('📋 Existing users:', existingUsers)

    // Create admin if missing
    const adminExists = existingUsers.find(u => u.email === 'admin@salesportal.com')
    if (!adminExists) {
      console.log('🔧 Creating admin user...')
      const adminPassword = await bcryptjs.hash('admin123', 12)
      await prisma.user.create({
        data: {
          email: 'admin@salesportal.com',
          password: adminPassword,
          role: 'ADMIN',
        }
      })
      console.log('✅ Admin user created: admin@salesportal.com / admin123')
    } else {
      console.log('✅ Admin user already exists')
    }

    // Create agent if missing
    const agentExists = existingUsers.find(u => u.email === 'agent@salesportal.com')
    if (!agentExists) {
      console.log('🔧 Creating agent user...')
      const agentPassword = await bcryptjs.hash('agent123', 12)
      await prisma.user.create({
        data: {
          email: 'agent@salesportal.com', 
          password: agentPassword,
          role: 'AGENT',
        }
      })
      console.log('✅ Agent user created: agent@salesportal.com / agent123')
    } else {
      console.log('✅ Agent user already exists')
    }

    // Final user count
    const finalUsers = await prisma.user.findMany({
      select: { email: true, role: true }
    })

    console.log('🎉 Database fix completed!')
    console.log('📊 Total users:', finalUsers.length)
    console.log('👥 Users:')
    finalUsers.forEach(user => {
      console.log(`   - ${user.email} (${user.role})`)
    })

    return { success: true, users: finalUsers }

  } catch (error) {
    console.error('❌ Database fix failed:', error)
    throw error
  } finally {
    await prisma.$disconnect()
  }
}

// Run the fix
if (require.main === module) {
  fixProductionDatabase()
    .then(() => {
      console.log('🚀 Database is ready for authentication!')
      process.exit(0)
    })
    .catch((error) => {
      console.error('💥 Fix failed:', error)
      process.exit(1)
    })
}

module.exports = { fixProductionDatabase }