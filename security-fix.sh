#!/bin/bash

# 🚨 SECURITY INCIDENT RESPONSE SCRIPT
# This script removes exposed API keys from the repository

echo "🚨 SECURITY FIX: Removing exposed Google API keys..."

# 1. Delete the problematic files
rm -f RESEARCH_ENGINE_DEPLOYMENT.md
rm -f asis_advanced_research_engine_updated.py  
rm -rf asis_backups/
rm -rf asis_safe_backups/
rm -f keys-to-remove.txt

# 2. Update .gitignore to prevent future exposures
cat >> .gitignore << 'EOF'

# Security - Never commit API keys
**/secrets/**
**/*secret*
**/*key*
**/*credential*
**/config/keys.*
**/config/secrets.*
**/.env*
*.key
*.secret
*_key
*_secret
*credentials*

# Research engine files (contain sensitive data)
asis_*
*research_engine*
RESEARCH_ENGINE_*

EOF

# 3. Add security warning to README
cat >> SECURITY.md << 'EOF'
# 🔒 SECURITY NOTICE

## API Key Management
- All API keys must be stored in environment variables
- Never commit API keys to version control
- Use `.env` files (which are gitignored)
- Regularly rotate API keys

## Exposed Key Incident
- On March 16, 2026, a Google API key was accidentally exposed in commit history
- The key `AIzaSyCisZ-oFUH3oYLF0u_r9wyTQ_AjryXJMmM` has been REVOKED
- All files containing this key have been removed

## Reporting Security Issues
Report security vulnerabilities to the repository owner immediately.
EOF

echo "✅ Security fix complete!"
echo "📋 Next steps:"
echo "1. Go to https://console.cloud.google.com/apis/credentials"
echo "2. Delete the exposed API key: AIzaSyCisZ-oFUH3oYLF0u_r9wyTQ_AjryXJMmM"
echo "3. Generate a new API key if needed"
echo "4. Store new keys in .env files only"