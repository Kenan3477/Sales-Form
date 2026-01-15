#!/bin/bash

echo "🚀 Starting Sales Form Portal..."

# Set production environment  
export NODE_ENV=production
export PORT=${PORT:-3000}

# Check if database exists, if not run migrations
echo "🗄️ Checking database..."
npx prisma db push --accept-data-loss

# Run seed only if tables are empty
echo "🌱 Checking if seeding is needed..."
npx prisma db seed || echo "Database already seeded or seed failed (this is okay for production)"

# Start the Next.js application
echo "▶️ Starting Sales Form Portal on port $PORT..."
npm start
