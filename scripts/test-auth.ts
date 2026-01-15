import { prisma } from '../src/lib/prisma';
import { compare } from 'bcryptjs';

async function testAuth() {
  try {
    console.log('🔍 Testing authentication...');

    // Check if admin user exists
    const user = await prisma.user.findUnique({
      where: { email: 'admin@salesportal.com' }
    });

    if (!user) {
      console.log('❌ Admin user not found!');
      return;
    }

    console.log('✅ Admin user found:', {
      id: user.id,
      email: user.email,
      role: user.role,
      hasPassword: !!user.password
    });

    // Test password comparison
    const testPassword = 'admin123';
    const isValid = await compare(testPassword, user.password);
    
    console.log('🔐 Password test result:', isValid ? '✅ VALID' : '❌ INVALID');
    
    if (!isValid) {
      console.log('💡 This might be the issue - password hash mismatch');
    }

  } catch (error) {
    console.error('❌ Error testing auth:', error);
  } finally {
    await prisma.$disconnect();
  }
}

testAuth();