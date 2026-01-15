#!/bin/bash

echo "🚀 Preparing Sales Form Portal for clean repository"
echo "=================================================="

# Create the clean SalesForm directory
SALESFORM_DIR="../SalesForm"
mkdir -p "$SALESFORM_DIR"

echo "📁 Creating directory structure..."

# Copy core application files
cp -r src "$SALESFORM_DIR/"
cp -r prisma "$SALESFORM_DIR/"
cp -r components "$SALESFORM_DIR/" 2>/dev/null || echo "No components directory"

# Copy configuration files
cp package.json "$SALESFORM_DIR/"
cp package-lock.json "$SALESFORM_DIR/"
cp next.config.js "$SALESFORM_DIR/"
cp tailwind.config.js "$SALESFORM_DIR/"
cp postcss.config.js "$SALESFORM_DIR/"
cp tsconfig.json "$SALESFORM_DIR/"
cp .eslintrc.json "$SALESFORM_DIR/"

# Copy environment files
cp .env.example "$SALESFORM_DIR/"
cp .env.vercel "$SALESFORM_DIR/"

# Copy documentation
cp README.md "$SALESFORM_DIR/"
cp VERCEL_DEPLOY.md "$SALESFORM_DIR/"
cp DEPLOYMENT.md "$SALESFORM_DIR/"

# Create clean .gitignore for Next.js
cat > "$SALESFORM_DIR/.gitignore" << EOF
# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Database
database.db
database.db-journal

# IDE
.vscode/
.idea/
EOF

# Create scripts directory if it exists
if [ -d "scripts" ]; then
    cp -r scripts "$SALESFORM_DIR/"
fi

echo "✅ All Sales Form Portal files copied to $SALESFORM_DIR"
echo ""
echo "🎯 Next steps:"
echo "1. cd $SALESFORM_DIR"
echo "2. git init"
echo "3. git add ."
echo "4. git commit -m 'Initial commit: Clean Sales Form Portal'"
echo "5. git remote add origin https://github.com/Kenan3477/SalesForm.git"
echo "6. git push -u origin main"
echo ""
echo "🚀 Then deploy on Vercel!"