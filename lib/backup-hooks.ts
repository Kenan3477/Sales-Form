import { SalesDataBackup } from '../lib/SalesDataBackup';

/**
 * Auto-backup hook for protecting sales data before operations
 * Call this before any major data modifications
 */
export async function createAutoBackup(
  operation: string,
  user: string = 'System'
): Promise<string> {
  const backup = new SalesDataBackup();
  
  try {
    const filepath = await backup.createBackup(
      `Auto-backup before: ${operation}`,
      user
    );
    
    console.log(`🛡️  Auto-backup created for operation: ${operation}`);
    return filepath;
  } catch (error) {
    console.error('⚠️  Auto-backup failed:', error);
    throw new Error(`Failed to create backup before ${operation}: ${error}`);
  }
}

/**
 * Scheduled backup function - can be called from cron or scheduled tasks
 */
export async function createScheduledBackup(): Promise<void> {
  const backup = new SalesDataBackup();
  
  try {
    await backup.createBackup(
      'Scheduled automatic backup',
      'Scheduled Task'
    );
    
    // Cleanup old backups (keep 30 days)
    await backup.cleanup(30);
    
    console.log('✅ Scheduled backup completed successfully');
  } catch (error) {
    console.error('❌ Scheduled backup failed:', error);
    throw error;
  }
}