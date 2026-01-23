import { SalesDataBackup } from './lib/SalesDataBackup';

async function createInitialBackup() {
  const backup = new SalesDataBackup();
  
  console.log('Creating initial backup before any future changes...');
  
  await backup.createBackup(
    'Initial backup after pricing recalculation fixes',
    'System Setup'
  );
}

createInitialBackup().catch(console.error);