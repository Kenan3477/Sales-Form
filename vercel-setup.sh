#!/bin/bash

echo "🚀 Vercel Database Setup Script"
echo "================================"

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not found"
    echo "Please set your DATABASE_URL environment variable in Vercel"
    exit 1
fi

echo "✅ DATABASE_URL found"

# Generate Prisma client
echo "🔧 Generating Prisma client..."
npx prisma generate

# Push database schema
echo "🗄️ Setting up database schema..."
npx prisma db push --accept-data-loss

# Seed database with default users
echo "🌱 Seeding database..."
npx prisma db seed || echo "⚠️ Seeding failed or already completed"

echo "✅ Database setup complete!"
echo ""
echo "🎉 Your Sales Form Portal is ready!"
echo "Default accounts:"
echo "Admin: admin@salesportal.com / admin123"
echo "Agent: agent@salesportal.com / agent123"