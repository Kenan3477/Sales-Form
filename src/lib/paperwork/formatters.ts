/**
 * Utility functions for formatting data in paperwork generation
 * Ensures no null/undefined values appear in generated documents
 */

/**
 * Safely format an address from sale data, removing null/undefined values
 */
export function formatAddress(sale: {
  mailingStreet?: string | null
  mailingCity?: string | null
  mailingProvince?: string | null
  mailingPostalCode?: string | null
}): string {
  const parts = [
    sale.mailingStreet,
    sale.mailingCity,
    sale.mailingProvince,
    sale.mailingPostalCode
  ].filter(part => part && part.trim() !== ''); // Remove null, undefined, and empty strings

  return parts.join(', ') || 'Address not provided';
}

/**
 * Safely format a price, returning empty string for null/undefined
 */
export function formatPrice(price: number | null | undefined, prefix = '£'): string {
  if (price === null || price === undefined || isNaN(price)) {
    return '';
  }
  return `${prefix}${price.toFixed(2)}`;
}

/**
 * Safely format a monthly price with suffix
 */
export function formatMonthlyPrice(price: number | null | undefined): string {
  if (price === null || price === undefined || isNaN(price)) {
    return '';
  }
  return `£${price.toFixed(2)}/month`;
}

/**
 * Safely get a string value, returning empty string for null/undefined
 */
export function safeString(value: any): string {
  if (value === null || value === undefined) {
    return '';
  }
  return String(value);
}

/**
 * Safely format customer name
 */
export function formatCustomerName(firstName?: string | null, lastName?: string | null): string {
  const parts = [firstName, lastName].filter(part => part && part.trim() !== '');
  return parts.join(' ') || 'Customer';
}