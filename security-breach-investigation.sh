#!/bin/bash

echo "🔍 SECURITY BREACH INVESTIGATION - SALES FORM PORTAL"
echo "===================================================="
echo "Timestamp: $(date)"
echo ""

echo "🚨 1. CHECKING FOR SIGNS OF UNAUTHORIZED ACCESS"
echo "----------------------------------------------"

echo "📊 Analyzing authentication logs and patterns..."

# Check for suspicious authentication patterns in the codebase
echo "🔍 Checking for hardcoded credentials or backdoors:"
grep -r -i "password.*=" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" | head -10
grep -r -i "admin.*password" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" | head -5
grep -r -i "backdoor\|bypass\|skip.*auth" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" | head -5

echo ""
echo "🔍 Checking for suspicious API endpoints or debug routes:"
find src/app/api -name "*.ts" -exec grep -l "debug\|test\|admin.*bypass\|no.*auth" {} \; | head -10

echo ""
echo "🔍 Checking for unauthorized admin creation or privilege escalation:"
grep -r "role.*=.*ADMIN\|role.*=.*admin" src/ --include="*.ts" --include="*.tsx" | head -10
grep -r "createUser.*admin\|admin.*true" src/ --include="*.ts" --include="*.tsx" | head -5

echo ""
echo "🚨 2. CHECKING FOR BRUTE FORCE ATTACK INDICATORS"
echo "-----------------------------------------------"

echo "🔍 Checking rate limiting implementation:"
grep -r "rate.*limit\|brute.*force\|attempt.*count" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🔍 Checking for login attempt tracking:"
grep -r "failed.*login\|login.*attempt\|auth.*fail" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🔍 Checking authentication middleware for vulnerabilities:"
find src/ -name "middleware*" -o -name "*auth*" | xargs grep -l "NextAuth\|session\|token" | head -5

echo ""
echo "🚨 3. CHECKING DATA INTEGRITY AND UNAUTHORIZED MODIFICATIONS"
echo "----------------------------------------------------------"

echo "🔍 Checking for suspicious database operations:"
grep -r "delete.*where\|drop.*table\|truncate" src/ --include="*.ts" --include="*.tsx" | head -10
grep -r "UPDATE.*users\|DELETE.*users" src/ --include="*.ts" --include="*.tsx" | head -5

echo ""
echo "🔍 Checking for mass data export attempts:"
grep -r "export.*all\|download.*all\|bulk.*download" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🔍 Checking for unauthorized data access patterns:"
grep -r "findMany()\|findFirst()" src/ --include="*.ts" --include="*.tsx" | wc -l
echo "Total Prisma queries without filters found above"

echo ""
echo "🚨 4. CHECKING FOR MALICIOUS CODE INJECTION"
echo "------------------------------------------"

echo "🔍 Checking for eval() or dangerous functions:"
grep -r "eval\|Function\|setTimeout.*string" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" | head -10

echo ""
echo "🔍 Checking for script injection patterns:"
grep -r "<script\|javascript:\|onclick.*=" src/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" | head -10

echo ""
echo "🔍 Checking for suspicious imports or requires:"
grep -r "require.*http\|import.*child_process\|exec\|spawn" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🚨 5. CHECKING ENVIRONMENT AND CONFIGURATION SECURITY"
echo "----------------------------------------------------"

echo "🔍 Checking for exposed environment variables:"
if [ -f ".env" ]; then
    echo "✅ .env file exists - checking for suspicious entries:"
    grep -v "^#" .env | grep -v "^$" | sed 's/=.*/=***REDACTED***/' | head -10
else
    echo "⚠️  No .env file found"
fi

echo ""
echo "🔍 Checking for suspicious configuration changes:"
find . -name "*.config.*" -exec grep -l "disable.*security\|allow.*all\|cors.*\*" {} \; | head -5

echo ""
echo "🔍 Checking for unauthorized file modifications (recent git history):"
if [ -d ".git" ]; then
    echo "Recent commits (last 10):"
    git log --oneline -10 --pretty=format:"%h %s [%an]"
    echo ""
    echo ""
    echo "Files changed in last 5 commits:"
    git diff --name-only HEAD~5..HEAD | head -20
else
    echo "⚠️  No git repository found"
fi

echo ""
echo "🚨 6. CHECKING FOR DATA EXFILTRATION ATTEMPTS"
echo "--------------------------------------------"

echo "🔍 Checking for suspicious external connections:"
grep -r "fetch.*http\|axios.*http\|webhook\|external.*api" src/ --include="*.ts" --include="*.tsx" | grep -v "localhost\|vercel\|googleapis\|postcodes.io" | head -10

echo ""
echo "🔍 Checking for unauthorized file uploads or downloads:"
grep -r "upload.*file\|download.*file\|writeFile\|createWriteStream" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🚨 7. CHECKING DATABASE SCHEMA AND SEED INTEGRITY"
echo "------------------------------------------------"

echo "🔍 Checking Prisma schema for unauthorized changes:"
if [ -f "prisma/schema.prisma" ]; then
    echo "Database models found:"
    grep "^model\|^enum" prisma/schema.prisma | head -15
    echo ""
    echo "Checking for suspicious database configurations:"
    grep -i "@@ignore\|@@map.*admin\|password.*String" prisma/schema.prisma | head -5
else
    echo "⚠️  No Prisma schema found"
fi

echo ""
echo "🔍 Checking seed file for unauthorized admin accounts:"
if [ -f "prisma/seed.ts" ]; then
    echo "Seed file contents (user creation):"
    grep -A5 -B5 "email.*admin\|role.*ADMIN" prisma/seed.ts | head -15
else
    echo "⚠️  No seed file found"
fi

echo ""
echo "🚨 8. CHECKING FOR SECURITY BYPASS MECHANISMS"
echo "--------------------------------------------"

echo "🔍 Checking for authentication bypass patterns:"
grep -r "skip.*auth\|bypass.*auth\|no.*session\|auth.*false" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🔍 Checking for CORS misconfigurations:"
grep -r "Access-Control-Allow-Origin.*\*\|cors.*origin.*\*" src/ --include="*.ts" --include="*.tsx" | head -5

echo ""
echo "🔍 Checking for CSP bypass attempts:"
grep -r "unsafe-inline\|unsafe-eval\|disable.*csp" src/ --include="*.ts" --include="*.tsx" | head -10

echo ""
echo "🚨 9. CHECKING FOR SUSPICIOUS PACKAGE MODIFICATIONS"
echo "--------------------------------------------------"

echo "🔍 Checking package.json for unauthorized dependencies:"
if [ -f "package.json" ]; then
    echo "Recently added or suspicious packages (checking for crypto, network, file system access):"
    grep -E "crypto|bitcoin|mining|backdoor|exec|shell|fs-extra|child_process" package.json | head -10
    
    echo ""
    echo "Total dependencies:"
    grep -c '".*":' package.json || echo "Could not count dependencies"
else
    echo "⚠️  No package.json found"
fi

echo ""
echo "🚨 10. FINAL SECURITY ASSESSMENT"
echo "==============================="

echo ""
echo "🔍 Checking for immediate security indicators:"

# Count potential security risks
HARDCODED_CREDS=$(grep -r -i "password.*=" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l)
DANGEROUS_FUNCTIONS=$(grep -r "eval\|exec\|spawn" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l)
EXTERNAL_CONNECTIONS=$(grep -r "fetch.*http\|axios.*http" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v "localhost\|vercel\|googleapis" | wc -l)
AUTH_BYPASSES=$(grep -r "skip.*auth\|bypass.*auth" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l)

echo "📊 SECURITY METRICS:"
echo "  - Hardcoded credentials found: $HARDCODED_CREDS"
echo "  - Dangerous functions found: $DANGEROUS_FUNCTIONS"
echo "  - External connections found: $EXTERNAL_CONNECTIONS"
echo "  - Auth bypass patterns found: $AUTH_BYPASSES"

echo ""
if [ "$HARDCODED_CREDS" -eq 0 ] && [ "$DANGEROUS_FUNCTIONS" -eq 0 ] && [ "$EXTERNAL_CONNECTIONS" -lt 5 ] && [ "$AUTH_BYPASSES" -eq 0 ]; then
    echo "✅ SECURITY STATUS: NO BREACH INDICATORS DETECTED"
    echo "✅ SYSTEM APPEARS SECURE AND INTACT"
else
    echo "⚠️  SECURITY STATUS: POTENTIAL CONCERNS DETECTED"
    echo "⚠️  RECOMMEND IMMEDIATE REVIEW OF FLAGGED ITEMS"
fi

echo ""
echo "🔒 BREACH INVESTIGATION COMPLETE"
echo "==============================="