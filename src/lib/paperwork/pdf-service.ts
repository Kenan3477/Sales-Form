import puppeteer, { Browser, Page } from 'puppeteer';
import * as fs from 'fs/promises';
import * as path from 'path';
import { PDFGenerationOptions, DEFAULT_PDF_OPTIONS, DocumentGenerationError } from './types';

/**
 * PDF generation service using Puppeteer
 */
export class PDFService {
  private static browser: Browser | null = null;
  private static isInitializing = false;

  /**
   * Initialize browser instance (singleton)
   */
  private static async getBrowser(): Promise<Browser> {
    if (this.browser) {
      return this.browser;
    }

    if (this.isInitializing) {
      // Wait for initialization to complete
      while (this.isInitializing) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      if (this.browser) {
        return this.browser;
      }
    }

    this.isInitializing = true;

    try {
      this.browser = await puppeteer.launch({
        headless: true,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--no-first-run',
          '--no-zygote',
          '--disable-gpu',
        ],
        timeout: 30000,
      });

      // Handle browser disconnect
      this.browser.on('disconnected', () => {
        this.browser = null;
      });

      return this.browser;
    } catch (error) {
      this.browser = null;
      throw new Error(`Failed to launch browser: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      this.isInitializing = false;
    }
  }

  /**
   * Generate PDF from HTML content
   */
  static async generatePDF(
    htmlContent: string,
    outputPath: string,
    options: Partial<PDFGenerationOptions> = {}
  ): Promise<{ filePath: string; fileSize: number }> {
    const fullOptions = { ...DEFAULT_PDF_OPTIONS, ...options };
    let page: Page | null = null;

    try {
      // Ensure output directory exists
      await this.ensureDirectoryExists(path.dirname(outputPath));

      const browser = await this.getBrowser();
      page = await browser.newPage();

      // Set content and wait for network to be idle
      await page.setContent(htmlContent, {
        waitUntil: 'networkidle0',
        timeout: fullOptions.timeout,
      });

      // Generate PDF
      const pdfBuffer = await page.pdf({
        path: outputPath,
        format: fullOptions.format,
        margin: fullOptions.margin,
        displayHeaderFooter: fullOptions.displayHeaderFooter,
        headerTemplate: fullOptions.headerTemplate || '',
        footerTemplate: fullOptions.footerTemplate || '',
        printBackground: fullOptions.printBackground,
        timeout: fullOptions.timeout,
      });

      // Get file size
      const stats = await fs.stat(outputPath);
      const fileSize = stats.size;

      return {
        filePath: outputPath,
        fileSize,
      };

    } catch (error) {
      const pdfError: DocumentGenerationError = {
        code: 'PDF_GENERATION_FAILED',
        message: `PDF generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        details: error,
      };
      throw pdfError;
    } finally {
      if (page) {
        await page.close().catch(() => {}); // Ignore close errors
      }
    }
  }

  /**
   * Generate PDF buffer (in-memory) from HTML content
   */
  static async generatePDFBuffer(
    htmlContent: string,
    options: Partial<PDFGenerationOptions> = {}
  ): Promise<Buffer> {
    const fullOptions = { ...DEFAULT_PDF_OPTIONS, ...options };
    let page: Page | null = null;

    try {
      const browser = await this.getBrowser();
      page = await browser.newPage();

      // Set content and wait for network to be idle
      await page.setContent(htmlContent, {
        waitUntil: 'networkidle0',
        timeout: fullOptions.timeout,
      });

      // Generate PDF buffer
      const pdfBuffer = await page.pdf({
        format: fullOptions.format,
        margin: fullOptions.margin,
        displayHeaderFooter: fullOptions.displayHeaderFooter,
        headerTemplate: fullOptions.headerTemplate || '',
        footerTemplate: fullOptions.footerTemplate || '',
        printBackground: fullOptions.printBackground,
        timeout: fullOptions.timeout,
      });

      return Buffer.from(pdfBuffer);

    } catch (error) {
      const pdfError: DocumentGenerationError = {
        code: 'PDF_GENERATION_FAILED',
        message: `PDF buffer generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        details: error,
      };
      throw pdfError;
    } finally {
      if (page) {
        await page.close().catch(() => {}); // Ignore close errors
      }
    }
  }

  /**
   * Validate HTML content for PDF generation
   */
  static async validateHTML(htmlContent: string): Promise<{ valid: boolean; error?: string }> {
    let page: Page | null = null;

    try {
      const browser = await this.getBrowser();
      page = await browser.newPage();

      // Try to load the HTML
      await page.setContent(htmlContent, {
        waitUntil: 'domcontentloaded',
        timeout: 10000,
      });

      // Check for any console errors
      const errors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') {
          errors.push(msg.text());
        }
      });

      // Wait a bit for any async errors
      await new Promise(resolve => setTimeout(resolve, 1000));

      if (errors.length > 0) {
        return {
          valid: false,
          error: `HTML validation errors: ${errors.join(', ')}`
        };
      }

      return { valid: true };

    } catch (error) {
      return {
        valid: false,
        error: `HTML validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      };
    } finally {
      if (page) {
        await page.close().catch(() => {});
      }
    }
  }

  /**
   * Get PDF storage directory
   */
  static getStorageDirectory(): string {
    // Use environment variable or default to storage/pdfs in project root
    const storageDir = process.env.PDF_STORAGE_PATH || path.join(process.cwd(), 'storage', 'pdfs');
    return storageDir;
  }

  /**
   * Generate unique filename for PDF
   */
  static generateFilename(saleId: string, templateType: string, extension: string = 'pdf'): string {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `${templateType}_${saleId}_${timestamp}.${extension}`;
    return filename;
  }

  /**
   * Get full file path for generated document
   */
  static getFilePath(filename: string): string {
    return path.join(this.getStorageDirectory(), filename);
  }

  /**
   * Ensure directory exists, create if it doesn't
   */
  private static async ensureDirectoryExists(dirPath: string): Promise<void> {
    try {
      await fs.access(dirPath);
    } catch (error) {
      // Directory doesn't exist, create it
      await fs.mkdir(dirPath, { recursive: true });
    }
  }

  /**
   * Clean up old PDF files (older than specified days)
   */
  static async cleanupOldFiles(retentionDays: number = 30): Promise<{ deletedCount: number; freedSpace: number }> {
    const storageDir = this.getStorageDirectory();
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retentionDays);

    let deletedCount = 0;
    let freedSpace = 0;

    try {
      const files = await fs.readdir(storageDir);
      
      for (const file of files) {
        if (!file.endsWith('.pdf')) continue;
        
        const filePath = path.join(storageDir, file);
        const stats = await fs.stat(filePath);
        
        if (stats.mtime < cutoffDate) {
          freedSpace += stats.size;
          await fs.unlink(filePath);
          deletedCount++;
        }
      }

      return { deletedCount, freedSpace };
    } catch (error) {
      console.error('Error during PDF cleanup:', error);
      return { deletedCount: 0, freedSpace: 0 };
    }
  }

  /**
   * Close browser instance (cleanup)
   */
  static async closeBrowser(): Promise<void> {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }

  /**
   * Check if PDF service is available
   */
  static async healthCheck(): Promise<{ healthy: boolean; error?: string }> {
    try {
      const browser = await this.getBrowser();
      const page = await browser.newPage();
      
      // Try to generate a simple PDF
      await page.setContent('<html><body><h1>Health Check</h1></body></html>');
      const buffer = await page.pdf({ format: 'A4' });
      await page.close();

      return { 
        healthy: buffer.length > 0 
      };
    } catch (error) {
      return {
        healthy: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
}

// Handle process exit to clean up browser
process.on('exit', () => {
  PDFService.closeBrowser();
});

process.on('SIGINT', () => {
  PDFService.closeBrowser();
  process.exit(0);
});

process.on('SIGTERM', () => {
  PDFService.closeBrowser();
  process.exit(0);
});