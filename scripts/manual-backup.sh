#!/bin/bash

# 📦 MANUAL DATABASE BACKUP
# =========================
# Quick script to run a manual backup of the Sales Form database
# 🔒 DATA PROTECTION: Read-only operations only

echo "🔄 Running manual database backup..."
echo "===================================="

cd "/Users/zenan/Sales Form"

# Run the backup script
npx ts-node scripts/database-backup.ts

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Manual backup completed successfully!"
    echo "📁 Check the backups/database/ directory for the backup file"
    
    # Show recent backup files
    echo ""
    echo "📋 Recent backup files:"
    ls -lt backups/database/database-backup-*.json | head -5
else
    echo ""
    echo "❌ Manual backup failed!"
    exit 1
fi