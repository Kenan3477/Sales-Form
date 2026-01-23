import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function resetDownloadCounts() {
  console.log('🔄 Starting to reset all document download counts...');
  
  try {
    // Get current count of documents with downloads
    const documentsWithDownloads = await prisma.generatedDocument.count({
      where: {
        downloadCount: {
          gt: 0
        }
      }
    });

    console.log(`📊 Found ${documentsWithDownloads} documents with download counts > 0`);

    if (documentsWithDownloads === 0) {
      console.log('✅ All documents already have download count of 0');
      return;
    }

    // Reset all download counts to 0
    const result = await prisma.generatedDocument.updateMany({
      where: {
        downloadCount: {
          gt: 0
        }
      },
      data: {
        downloadCount: 0
      }
    });

    console.log(`✅ Successfully reset download counts for ${result.count} documents`);
    
    // Verify the reset
    const remainingDownloads = await prisma.generatedDocument.count({
      where: {
        downloadCount: {
          gt: 0
        }
      }
    });

    if (remainingDownloads === 0) {
      console.log('🎉 All document download counts have been successfully reset to 0');
    } else {
      console.log(`⚠️  Warning: ${remainingDownloads} documents still have download counts > 0`);
    }

  } catch (error) {
    console.error('❌ Error resetting download counts:', error);
    throw error;
  } finally {
    await prisma.$disconnect();
  }
}

// Run the reset
resetDownloadCounts()
  .catch((error) => {
    console.error('Script failed:', error);
    process.exit(1);
  });