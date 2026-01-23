#!/usr/bin/env node
import { SalesDataBackup } from '../lib/SalesDataBackup';

async function main() {
  const backup = new SalesDataBackup();
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'create':
        const reason = args[1] || 'Manual backup via CLI';
        const createdBy = args[2] || 'CLI User';
        await backup.createBackup(reason, createdBy);
        break;

      case 'list':
        await backup.listBackups();
        break;

      case 'restore':
        const filename = args[1];
        const dryRun = args[2] !== '--confirm';
        
        if (!filename) {
          console.error('Usage: npm run backup:restore <filename> [--confirm]');
          console.error('Use --confirm to actually perform the restoration (default is dry run)');
          process.exit(1);
        }
        
        await backup.restoreFromBackup(filename, dryRun);
        break;

      case 'cleanup':
        const days = parseInt(args[1]) || 30;
        await backup.cleanup(days);
        break;

      default:
        console.log('Sales Data Backup System');
        console.log('Usage:');
        console.log('  npm run backup:create [reason] [createdBy]  - Create a new backup');
        console.log('  npm run backup:list                         - List all available backups');
        console.log('  npm run backup:restore <file> [--confirm]   - Restore from backup (dry run by default)');
        console.log('  npm run backup:cleanup [days]               - Delete backups older than X days (default 30)');
        console.log('');
        console.log('Examples:');
        console.log('  npm run backup:create "Before pricing changes" "John Doe"');
        console.log('  npm run backup:restore sales-backup-2026-01-23T13-45-30-123Z.json');
        console.log('  npm run backup:restore sales-backup-2026-01-23T13-45-30-123Z.json --confirm');
        console.log('  npm run backup:cleanup 7');
        break;
    }
  } catch (error) {
    console.error('Backup operation failed:', error);
    process.exit(1);
  }
}

main();