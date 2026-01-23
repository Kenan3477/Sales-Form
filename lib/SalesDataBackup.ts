import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';

const prisma = new PrismaClient();

interface BackupData {
  timestamp: string;
  version: string;
  totalSales: number;
  totalSystemValue: number;
  sales: any[];
  appliances: any[];
  metadata: {
    backupReason: string;
    createdBy: string;
    systemStats: {
      averagePerCustomer: number;
      customersWithBoilers: number;
      totalAppliances: number;
    };
  };
}

export class SalesDataBackup {
  private backupDir: string;

  constructor() {
    this.backupDir = path.join(process.cwd(), 'backups', 'sales-data');
    this.ensureBackupDirectory();
  }

  private ensureBackupDirectory() {
    if (!fs.existsSync(this.backupDir)) {
      fs.mkdirSync(this.backupDir, { recursive: true });
      console.log(`Created backup directory: ${this.backupDir}`);
    }
  }

  async createBackup(reason: string = 'Manual backup', createdBy: string = 'System'): Promise<string> {
    try {
      console.log(`\n=== CREATING SALES DATA BACKUP ===`);
      console.log(`Reason: ${reason}`);
      console.log(`Created by: ${createdBy}\n`);

      // Get all sales data with relationships
      const sales = await prisma.sale.findMany({
        include: {
          appliances: true
        }
      });

      // Get all appliances data separately for reference
      const allAppliances = await prisma.appliance.findMany();

      // Calculate system stats
      let totalSystemValue = 0;
      let customersWithBoilers = 0;
      
      sales.forEach(sale => {
        totalSystemValue += sale.totalPlanCost;
        if (sale.boilerCoverSelected) {
          customersWithBoilers++;
        }
      });

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const backupData: BackupData = {
        timestamp: new Date().toISOString(),
        version: '1.0',
        totalSales: sales.length,
        totalSystemValue,
        sales: sales.map(sale => ({
          ...sale,
          createdAt: sale.createdAt.toISOString(),
          updatedAt: sale.updatedAt.toISOString(),
          directDebitDate: sale.directDebitDate.toISOString(),
          documentsGeneratedAt: sale.documentsGeneratedAt?.toISOString() || null,
          appliances: sale.appliances
        })),
        appliances: allAppliances,
        metadata: {
          backupReason: reason,
          createdBy,
          systemStats: {
            averagePerCustomer: totalSystemValue / sales.length,
            customersWithBoilers,
            totalAppliances: allAppliances.length
          }
        }
      };

      const filename = `sales-backup-${timestamp}.json`;
      const filepath = path.join(this.backupDir, filename);

      fs.writeFileSync(filepath, JSON.stringify(backupData, null, 2));

      // Also create a compressed summary
      const summaryFilename = `sales-summary-${timestamp}.json`;
      const summaryData = {
        timestamp: backupData.timestamp,
        totalSales: backupData.totalSales,
        totalSystemValue: backupData.totalSystemValue,
        metadata: backupData.metadata,
        topCustomers: sales
          .sort((a, b) => b.totalPlanCost - a.totalPlanCost)
          .slice(0, 10)
          .map(sale => ({
            name: `${sale.customerFirstName} ${sale.customerLastName}`,
            total: sale.totalPlanCost,
            applianceCount: sale.appliances.length
          }))
      };
      
      const summaryFilepath = path.join(this.backupDir, summaryFilename);
      fs.writeFileSync(summaryFilepath, JSON.stringify(summaryData, null, 2));

      console.log(`✅ Backup created successfully:`);
      console.log(`   Full backup: ${filename}`);
      console.log(`   Summary: ${summaryFilename}`);
      console.log(`   Location: ${this.backupDir}`);
      console.log(`   Size: ${this.formatFileSize(fs.statSync(filepath).size)}`);
      console.log(`\n=== BACKUP STATS ===`);
      console.log(`Total sales backed up: ${sales.length}`);
      console.log(`Total appliances: ${allAppliances.length}`);
      console.log(`System value: £${totalSystemValue.toFixed(2)}`);
      console.log(`Average per customer: £${(totalSystemValue / sales.length).toFixed(2)}`);

      return filepath;
    } catch (error) {
      console.error('Error creating backup:', error);
      throw error;
    }
  }

  async listBackups(): Promise<void> {
    try {
      const files = fs.readdirSync(this.backupDir)
        .filter(file => file.startsWith('sales-backup-') && file.endsWith('.json'))
        .sort()
        .reverse();

      console.log(`\n=== AVAILABLE BACKUPS ===`);
      console.log(`Backup directory: ${this.backupDir}\n`);

      if (files.length === 0) {
        console.log('No backups found.');
        return;
      }

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const filepath = path.join(this.backupDir, file);
        const stats = fs.statSync(filepath);
        
        try {
          const backupData = JSON.parse(fs.readFileSync(filepath, 'utf8')) as BackupData;
          console.log(`${i + 1}. ${file}`);
          console.log(`   Date: ${new Date(backupData.timestamp).toLocaleString()}`);
          console.log(`   Reason: ${backupData.metadata.backupReason}`);
          console.log(`   Sales: ${backupData.totalSales}`);
          console.log(`   System Value: £${backupData.totalSystemValue.toFixed(2)}`);
          console.log(`   Size: ${this.formatFileSize(stats.size)}`);
          console.log(`   Created by: ${backupData.metadata.createdBy}\n`);
        } catch (error) {
          console.log(`${i + 1}. ${file} (corrupted backup)`);
          console.log(`   Size: ${this.formatFileSize(stats.size)}\n`);
        }
      }
    } catch (error) {
      console.error('Error listing backups:', error);
    }
  }

  async restoreFromBackup(backupFilename: string, dryRun: boolean = true): Promise<void> {
    try {
      const filepath = path.join(this.backupDir, backupFilename);
      
      if (!fs.existsSync(filepath)) {
        throw new Error(`Backup file not found: ${backupFilename}`);
      }

      const backupData = JSON.parse(fs.readFileSync(filepath, 'utf8')) as BackupData;

      console.log(`\n=== ${dryRun ? 'DRY RUN - ' : ''}RESTORING FROM BACKUP ===`);
      console.log(`Backup file: ${backupFilename}`);
      console.log(`Backup date: ${new Date(backupData.timestamp).toLocaleString()}`);
      console.log(`Backup reason: ${backupData.metadata.backupReason}`);
      console.log(`Sales to restore: ${backupData.sales.length}`);
      console.log(`System value: £${backupData.totalSystemValue.toFixed(2)}\n`);

      if (dryRun) {
        console.log('🔍 DRY RUN MODE - No changes will be made');
        console.log('This would restore:');
        console.log(`- Delete all current sales (${(await prisma.sale.count())} records)`);
        console.log(`- Delete all current appliances (${(await prisma.appliance.count())} records)`);
        console.log(`- Restore ${backupData.sales.length} sales`);
        console.log(`- Restore ${backupData.appliances.length} appliances`);
        console.log('\nTo perform actual restoration, run with dryRun=false');
        return;
      }

      // Create a backup before restoration
      await this.createBackup(`Before restoration of ${backupFilename}`, 'Auto-backup');

      // Clear existing data
      console.log('🗑️  Clearing existing appliances...');
      await prisma.appliance.deleteMany();
      
      console.log('🗑️  Clearing existing sales...');
      await prisma.sale.deleteMany();

      // Restore sales data
      console.log('📥 Restoring sales data...');
      for (const sale of backupData.sales) {
        const { appliances, ...saleData } = sale;
        
        // Convert date strings back to Date objects
        const restoreData = {
          ...saleData,
          createdAt: new Date(saleData.createdAt),
          updatedAt: new Date(saleData.updatedAt),
          directDebitDate: new Date(saleData.directDebitDate),
          documentsGeneratedAt: saleData.documentsGeneratedAt ? new Date(saleData.documentsGeneratedAt) : null
        };

        const restoredSale = await prisma.sale.create({
          data: restoreData
        });

        // Restore appliances for this sale
        for (const appliance of appliances) {
          await prisma.appliance.create({
            data: {
              ...appliance,
              saleId: restoredSale.id
            }
          });
        }
      }

      console.log('✅ Restoration completed successfully!');
      console.log(`Restored ${backupData.sales.length} sales`);
      console.log(`Restored ${backupData.appliances.length} appliances`);

    } catch (error) {
      console.error('Error restoring backup:', error);
      throw error;
    }
  }

  private formatFileSize(bytes: number): string {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  }

  async cleanup(keepDays: number = 30): Promise<void> {
    try {
      const files = fs.readdirSync(this.backupDir)
        .filter(file => file.startsWith('sales-backup-') && file.endsWith('.json'));

      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - keepDays);

      let deletedCount = 0;

      for (const file of files) {
        const filepath = path.join(this.backupDir, file);
        const stats = fs.statSync(filepath);
        
        if (stats.mtime < cutoffDate) {
          fs.unlinkSync(filepath);
          
          // Also delete corresponding summary file
          const summaryFile = file.replace('sales-backup-', 'sales-summary-');
          const summaryPath = path.join(this.backupDir, summaryFile);
          if (fs.existsSync(summaryPath)) {
            fs.unlinkSync(summaryPath);
          }
          
          deletedCount++;
          console.log(`Deleted old backup: ${file}`);
        }
      }

      console.log(`\n✅ Cleanup completed: ${deletedCount} old backups deleted (older than ${keepDays} days)`);
    } catch (error) {
      console.error('Error during cleanup:', error);
    }
  }
}

// Export for use in other files
export default SalesDataBackup;