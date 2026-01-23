#!/bin/bash

# 📦 AUTOMATED DATABASE BACKUP SCHEDULER
# =====================================
# This script sets up automated daily backups of the Sales Form database
# 🔒 DATA PROTECTION: Read-only operations only - never modifies customer data

echo "🔧 SETTING UP AUTOMATED DATABASE BACKUPS"
echo "========================================="

# Configuration
BACKUP_TIME="02:00"  # 2:00 AM daily
PROJECT_DIR="/Users/zenan/Sales Form"
LOG_FILE="$PROJECT_DIR/backups/backup.log"

# Ensure backup directories exist
mkdir -p "$PROJECT_DIR/backups/database"
mkdir -p "$PROJECT_DIR/backups/logs"

# Create backup log file if it doesn't exist
touch "$LOG_FILE"

echo "📁 Backup directory: $PROJECT_DIR/backups/database"
echo "📋 Log file: $LOG_FILE"
echo "⏰ Scheduled time: $BACKUP_TIME daily"

# Check if Node.js and required dependencies are available
echo ""
echo "🔍 Checking system requirements..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed or not in PATH"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed or not in PATH" 
    exit 1
fi
echo "✅ npm found: $(npm --version)"

# Check if the backup script exists
BACKUP_SCRIPT="$PROJECT_DIR/scripts/database-backup.ts"
if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo "❌ Backup script not found: $BACKUP_SCRIPT"
    exit 1
fi
echo "✅ Backup script found: $BACKUP_SCRIPT"

# Create the cron job command
CRON_COMMAND="cd '$PROJECT_DIR' && /usr/local/bin/node -r ts-node/register scripts/database-backup.ts >> '$LOG_FILE' 2>&1"

# Check current crontab
echo ""
echo "🔍 Checking existing cron jobs..."
if crontab -l 2>/dev/null | grep -q "database-backup"; then
    echo "⚠️  Database backup cron job already exists"
    echo "📋 Current backup jobs:"
    crontab -l 2>/dev/null | grep "database-backup"
    
    read -p "❓ Replace existing backup job? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "🚫 Backup scheduling cancelled"
        exit 0
    fi
    
    # Remove existing backup jobs
    crontab -l 2>/dev/null | grep -v "database-backup" | crontab -
    echo "🗑️  Removed existing backup jobs"
fi

# Add new cron job (2:00 AM daily)
(crontab -l 2>/dev/null; echo "0 2 * * * $CRON_COMMAND") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Automated backup successfully scheduled!"
    echo ""
    echo "📅 BACKUP SCHEDULE CONFIGURED:"
    echo "  - Time: $BACKUP_TIME daily"
    echo "  - Location: $PROJECT_DIR/backups/database/"
    echo "  - Logs: $LOG_FILE"
    echo ""
    echo "🔒 Data Protection: Backups are read-only and never modify customer data"
    echo ""
    echo "📋 Current cron jobs:"
    crontab -l | grep "database-backup"
else
    echo "❌ Failed to schedule backup"
    exit 1
fi

# Test backup script
echo ""
echo "🧪 Testing backup script..."
cd "$PROJECT_DIR"
if command -v npx &> /dev/null; then
    echo "🔄 Running test backup..."
    npx ts-node scripts/database-backup.ts
    
    if [ $? -eq 0 ]; then
        echo "✅ Test backup successful!"
        echo ""
        echo "🎉 AUTOMATED BACKUP SYSTEM IS NOW ACTIVE"
        echo "========================================"
        echo "✅ Daily backups will run at $BACKUP_TIME"
        echo "✅ All sales and customer data will be preserved"
        echo "✅ Backups are stored in: $PROJECT_DIR/backups/database/"
        echo "✅ Logs are written to: $LOG_FILE"
        echo ""
        echo "🔒 Your client's data is now automatically protected every 24 hours"
    else
        echo "❌ Test backup failed - check the log for details"
        exit 1
    fi
else
    echo "⚠️  npx not found - backup script may need manual testing"
fi