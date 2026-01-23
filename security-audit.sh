#!/bin/bash

echo "🔒 SECURITY AUDIT - SALES FORM PORTAL"
echo "===================================="
echo "Timestamp: $(date)"
echo ""

# Check for common security vulnerabilities
echo "🔍 1. CHECKING FOR EXPOSED SECRETS AND KEYS"
echo "--------------------------------------------"

# Check for hardcoded secrets in code
echo "Scanning for potential exposed secrets:"
grep -r -i "password\|secret\|key\|token" src/ --include="*.ts" --include="*.tsx" --include="*.js" | grep -v "placeholder\|example\|type" | head -10

echo ""
echo "Checking environment files:"
if [ -f ".env" ]; then
    echo "⚠️  .env file exists - checking if properly gitignored"
    if git check-ignore .env > /dev/null 2>&1; then
        echo "✅ .env is properly gitignored"
    else
        echo "❌ .env is NOT gitignored - SECURITY RISK!"
    fi
else
    echo "✅ No .env file in root directory"
fi

echo ""
echo "🔍 2. CHECKING AUTHENTICATION AND AUTHORIZATION"
echo "----------------------------------------------"

# Check auth implementation
echo "Checking authentication middleware:"
if [ -f "src/lib/auth.ts" ]; then
    echo "✅ Auth configuration found"
    grep -n "secret\|jwt\|session" src/lib/auth.ts | head -5
else
    echo "❌ No auth configuration found"
fi

echo ""
echo "Checking protected routes:"
find src/app -name "*.tsx" -exec grep -l "getServerSession\|session" {} \; | wc -l | xargs -I {} echo "Found {} files with session checks"

echo ""
echo "🔍 3. CHECKING FOR SQL INJECTION VULNERABILITIES"
echo "-----------------------------------------------"

# Check for potential SQL injection
echo "Checking for raw SQL queries:"
grep -r "sql\|query\|execute" src/ --include="*.ts" --include="*.tsx" | grep -v "prisma\|@prisma" | head -5

echo ""
echo "Checking Prisma usage (should be safe from SQL injection):"
grep -r "prisma\." src/ --include="*.ts" | wc -l | xargs -I {} echo "Found {} Prisma queries"

echo ""
echo "🔍 4. CHECKING FOR XSS VULNERABILITIES"
echo "-------------------------------------"

# Check for potential XSS
echo "Checking for dangerouslySetInnerHTML usage:"
grep -r "dangerouslySetInnerHTML" src/ --include="*.tsx" || echo "✅ No dangerouslySetInnerHTML found"

echo ""
echo "Checking for user input handling:"
grep -r "innerHTML\|eval\|Function" src/ --include="*.ts" --include="*.tsx" || echo "✅ No dangerous HTML manipulation found"

echo ""
echo "🔍 5. CHECKING FILE UPLOAD SECURITY"
echo "-----------------------------------"

# Check file upload handling
echo "Checking file upload endpoints:"
find src/app/api -name "*.ts" -exec grep -l "multipart\|upload\|file" {} \; || echo "No file upload endpoints found"

echo ""
echo "🔍 6. CHECKING CORS AND SECURITY HEADERS"
echo "---------------------------------------"

# Check CORS configuration
echo "Checking for CORS configuration:"
grep -r "cors\|Access-Control" src/ --include="*.ts" || echo "No CORS configuration found"

echo ""
echo "Checking for security headers:"
grep -r "helmet\|csp\|x-frame-options" src/ --include="*.ts" || echo "No security headers middleware found"

echo ""
echo "🔍 7. CHECKING API RATE LIMITING"
echo "-------------------------------"

# Check for rate limiting
echo "Checking for rate limiting:"
find . -name "*.ts" -exec grep -l "rateLimit\|rate-limit" {} \; || echo "No rate limiting found"

echo ""
echo "🔍 8. CHECKING FOR EXPOSED DEBUG INFO"
echo "------------------------------------"

# Check for debug info
echo "Checking for console.log in production code:"
grep -r "console\." src/ --include="*.ts" --include="*.tsx" | wc -l | xargs -I {} echo "Found {} console statements"

echo ""
echo "Checking for exposed error details:"
grep -r "stack\|trace" src/ --include="*.ts" | head -5

echo ""
echo "🔍 9. CHECKING DEPENDENCIES FOR VULNERABILITIES"
echo "----------------------------------------------"

# Check package vulnerabilities
echo "Running npm audit:"
npm audit --audit-level=moderate

echo ""
echo "🔍 10. CHECKING ACCESS CONTROLS"
echo "------------------------------"

# Check role-based access
echo "Checking role-based access controls:"
grep -r "role.*ADMIN\|role.*AGENT" src/ --include="*.ts" --include="*.tsx" | wc -l | xargs -I {} echo "Found {} role checks"

echo ""
echo "Checking middleware protection:"
grep -r "middleware\|unauthorized\|forbidden" src/ --include="*.ts" | wc -l | xargs -I {} echo "Found {} authorization checks"

echo ""
echo "✅ SECURITY AUDIT COMPLETE"
echo "========================="