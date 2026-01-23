import { NextApiRequest, NextApiResponse } from 'next';
import { SalesDataBackup } from '../../../../lib/SalesDataBackup';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { reason, createdBy } = req.body;
      
      const backup = new SalesDataBackup();
      const filepath = await backup.createBackup(
        reason || 'Manual backup via API',
        createdBy || 'API User'
      );
      
      res.status(200).json({
        success: true,
        message: 'Backup created successfully',
        filepath,
        timestamp: new Date().toISOString()
      });
      
    } catch (error) {
      console.error('Backup API error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to create backup',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  } else if (req.method === 'GET') {
    try {
      const backup = new SalesDataBackup();
      
      // Return list of backups as JSON
      const fs = require('fs');
      const path = require('path');
      const backupDir = path.join(process.cwd(), 'backups', 'sales-data');
      
      const files = fs.readdirSync(backupDir)
        .filter((file: string) => file.startsWith('sales-summary-') && file.endsWith('.json'))
        .map((file: string) => {
          const filepath = path.join(backupDir, file);
          const stats = fs.statSync(filepath);
          const summaryData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
          
          return {
            filename: file.replace('sales-summary-', 'sales-backup-'),
            summaryFilename: file,
            timestamp: summaryData.timestamp,
            totalSales: summaryData.totalSales,
            totalSystemValue: summaryData.totalSystemValue,
            reason: summaryData.metadata.backupReason,
            createdBy: summaryData.metadata.createdBy,
            size: stats.size,
            date: new Date(summaryData.timestamp).toLocaleString()
          };
        })
        .sort((a: any, b: any) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      
      res.status(200).json({
        success: true,
        backups: files
      });
      
    } catch (error) {
      console.error('Backup list API error:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to list backups',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  } else {
    res.setHeader('Allow', ['POST', 'GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}